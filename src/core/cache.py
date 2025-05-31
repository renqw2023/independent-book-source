"""
缓存管理器 - Cache Manager

负责管理系统缓存：
- 内存缓存
- 文件缓存
- 数据库缓存
- 缓存过期管理
"""

import os
import json
import time
import hashlib
import logging
import sqlite3
import threading
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CacheItem:
    """缓存项"""
    key: str
    value: Any
    expire_time: float
    create_time: float
    access_count: int = 0
    last_access: float = 0


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)
        self.expire_time = self.config.get("expire_time", 3600)  # 默认1小时
        self.max_size = self.config.get("max_size", 1000)
        self.cache_dir = self.config.get("cache_dir", "data/cache")
        
        # 内存缓存
        self.memory_cache: Dict[str, CacheItem] = {}
        self.cache_lock = threading.RLock()
        
        # 文件缓存
        self.file_cache_enabled = self.config.get("file_cache", True)
        if self.file_cache_enabled:
            Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
        # 数据库缓存
        self.db_cache_enabled = self.config.get("db_cache", True)
        self.db_path = os.path.join(self.cache_dir, "cache.db")
        if self.db_cache_enabled:
            self._init_db()
        
        # 清理任务
        self.cleanup_interval = self.config.get("cleanup_interval", 300)  # 5分钟
        self._start_cleanup_task()
        
        self.logger = logging.getLogger("cache")
        self.logger.info("缓存管理器初始化完成")
    
    def _init_db(self):
        """初始化数据库"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        expire_time REAL,
                        create_time REAL,
                        access_count INTEGER DEFAULT 0,
                        last_access REAL
                    )
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_expire_time ON cache(expire_time)")
                conn.commit()
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
            self.db_cache_enabled = False
    
    def _start_cleanup_task(self):
        """启动清理任务"""
        def cleanup_worker():
            while True:
                try:
                    time.sleep(self.cleanup_interval)
                    self.cleanup_expired()
                except Exception as e:
                    self.logger.error(f"清理任务异常: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def _generate_key(self, key: str) -> str:
        """生成缓存键"""
        if isinstance(key, str):
            return hashlib.md5(key.encode('utf-8')).hexdigest()
        return str(key)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存"""
        if not self.enabled:
            return default
        
        cache_key = self._generate_key(key)
        current_time = time.time()
        
        # 先从内存缓存获取
        with self.cache_lock:
            if cache_key in self.memory_cache:
                item = self.memory_cache[cache_key]
                if item.expire_time > current_time:
                    item.access_count += 1
                    item.last_access = current_time
                    return item.value
                else:
                    # 过期，删除
                    del self.memory_cache[cache_key]
        
        # 从数据库缓存获取
        if self.db_cache_enabled:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT value, expire_time, access_count FROM cache WHERE key = ?",
                        (cache_key,)
                    )
                    row = cursor.fetchone()
                    
                    if row:
                        value_str, expire_time, access_count = row
                        if expire_time > current_time:
                            # 更新访问统计
                            conn.execute(
                                "UPDATE cache SET access_count = ?, last_access = ? WHERE key = ?",
                                (access_count + 1, current_time, cache_key)
                            )
                            conn.commit()
                            
                            # 反序列化值
                            try:
                                value = json.loads(value_str)
                                # 加入内存缓存
                                self._set_memory_cache(cache_key, value, expire_time)
                                return value
                            except json.JSONDecodeError:
                                return value_str
                        else:
                            # 过期，删除
                            conn.execute("DELETE FROM cache WHERE key = ?", (cache_key,))
                            conn.commit()
            except Exception as e:
                self.logger.error(f"数据库缓存读取失败: {e}")
        
        # 从文件缓存获取
        if self.file_cache_enabled:
            file_path = os.path.join(self.cache_dir, f"{cache_key}.json")
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    if cache_data.get("expire_time", 0) > current_time:
                        value = cache_data.get("value")
                        # 加入内存缓存
                        self._set_memory_cache(cache_key, value, cache_data["expire_time"])
                        return value
                    else:
                        # 过期，删除文件
                        os.remove(file_path)
                except Exception as e:
                    self.logger.error(f"文件缓存读取失败: {e}")
        
        return default
    
    def set(self, key: str, value: Any, expire_time: Optional[float] = None) -> bool:
        """设置缓存"""
        if not self.enabled:
            return False
        
        cache_key = self._generate_key(key)
        current_time = time.time()
        
        if expire_time is None:
            expire_time = current_time + self.expire_time
        elif expire_time > 0:
            expire_time = current_time + expire_time
        else:
            expire_time = current_time + self.expire_time
        
        # 设置内存缓存
        self._set_memory_cache(cache_key, value, expire_time)
        
        # 设置数据库缓存
        if self.db_cache_enabled:
            try:
                value_str = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        "INSERT OR REPLACE INTO cache (key, value, expire_time, create_time, access_count, last_access) VALUES (?, ?, ?, ?, ?, ?)",
                        (cache_key, value_str, expire_time, current_time, 0, current_time)
                    )
                    conn.commit()
            except Exception as e:
                self.logger.error(f"数据库缓存写入失败: {e}")
        
        # 设置文件缓存
        if self.file_cache_enabled:
            try:
                file_path = os.path.join(self.cache_dir, f"{cache_key}.json")
                cache_data = {
                    "key": key,
                    "value": value,
                    "expire_time": expire_time,
                    "create_time": current_time
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                self.logger.error(f"文件缓存写入失败: {e}")
        
        return True
    
    def _set_memory_cache(self, cache_key: str, value: Any, expire_time: float):
        """设置内存缓存"""
        with self.cache_lock:
            # 检查缓存大小限制
            if len(self.memory_cache) >= self.max_size:
                self._evict_memory_cache()
            
            current_time = time.time()
            self.memory_cache[cache_key] = CacheItem(
                key=cache_key,
                value=value,
                expire_time=expire_time,
                create_time=current_time,
                access_count=0,
                last_access=current_time
            )
    
    def _evict_memory_cache(self):
        """内存缓存淘汰策略（LRU）"""
        if not self.memory_cache:
            return
        
        # 找到最少使用的缓存项
        lru_key = min(
            self.memory_cache.keys(),
            key=lambda k: (self.memory_cache[k].access_count, self.memory_cache[k].last_access)
        )
        del self.memory_cache[lru_key]
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        cache_key = self._generate_key(key)
        
        # 删除内存缓存
        with self.cache_lock:
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]
        
        # 删除数据库缓存
        if self.db_cache_enabled:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("DELETE FROM cache WHERE key = ?", (cache_key,))
                    conn.commit()
            except Exception as e:
                self.logger.error(f"数据库缓存删除失败: {e}")
        
        # 删除文件缓存
        if self.file_cache_enabled:
            file_path = os.path.join(self.cache_dir, f"{cache_key}.json")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    self.logger.error(f"文件缓存删除失败: {e}")
        
        return True
    
    def cleanup_expired(self):
        """清理过期缓存"""
        current_time = time.time()
        
        # 清理内存缓存
        with self.cache_lock:
            expired_keys = [
                key for key, item in self.memory_cache.items()
                if item.expire_time <= current_time
            ]
            for key in expired_keys:
                del self.memory_cache[key]
        
        # 清理数据库缓存
        if self.db_cache_enabled:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("DELETE FROM cache WHERE expire_time <= ?", (current_time,))
                    conn.commit()
            except Exception as e:
                self.logger.error(f"数据库缓存清理失败: {e}")
        
        # 清理文件缓存
        if self.file_cache_enabled:
            try:
                for file_name in os.listdir(self.cache_dir):
                    if file_name.endswith('.json'):
                        file_path = os.path.join(self.cache_dir, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                cache_data = json.load(f)
                            
                            if cache_data.get("expire_time", 0) <= current_time:
                                os.remove(file_path)
                        except Exception:
                            # 文件损坏，直接删除
                            os.remove(file_path)
            except Exception as e:
                self.logger.error(f"文件缓存清理失败: {e}")
        
        self.logger.info(f"缓存清理完成，清理了 {len(expired_keys)} 个过期项")
    
    def clear_all(self):
        """清空所有缓存"""
        # 清空内存缓存
        with self.cache_lock:
            self.memory_cache.clear()
        
        # 清空数据库缓存
        if self.db_cache_enabled:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("DELETE FROM cache")
                    conn.commit()
            except Exception as e:
                self.logger.error(f"数据库缓存清空失败: {e}")
        
        # 清空文件缓存
        if self.file_cache_enabled:
            try:
                for file_name in os.listdir(self.cache_dir):
                    if file_name.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, file_name))
            except Exception as e:
                self.logger.error(f"文件缓存清空失败: {e}")
        
        self.logger.info("所有缓存已清空")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        memory_count = len(self.memory_cache)
        
        db_count = 0
        if self.db_cache_enabled:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute("SELECT COUNT(*) FROM cache")
                    db_count = cursor.fetchone()[0]
            except Exception:
                pass
        
        file_count = 0
        if self.file_cache_enabled:
            try:
                file_count = len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
            except Exception:
                pass
        
        return {
            "enabled": self.enabled,
            "memory_cache_count": memory_count,
            "db_cache_count": db_count,
            "file_cache_count": file_count,
            "max_size": self.max_size,
            "expire_time": self.expire_time
        }
