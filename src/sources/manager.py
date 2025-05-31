"""
书源管理器 - Source Manager

负责管理和协调所有书源：
- 书源注册和发现
- 书源配置管理
- 书源状态监控
"""

import os
import json
import logging
import importlib
from typing import Dict, List, Optional, Any, Type
from pathlib import Path

from ..core.engine import BaseSource, BookSourceEngine


class SourceManager:
    """书源管理器"""
    
    def __init__(self, engine: BookSourceEngine):
        self.engine = engine
        self.sources: Dict[str, BaseSource] = {}
        self.source_configs: Dict[str, Dict[str, Any]] = {}
        self.source_classes: Dict[str, Type[BaseSource]] = {}
        
        self.logger = logging.getLogger("source_manager")
        
        # 自动发现和注册书源
        self._discover_sources()
    
    def _discover_sources(self):
        """自动发现书源"""
        sources_dir = Path(__file__).parent
        
        # 遍历书源目录
        for item in sources_dir.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                source_name = item.name
                try:
                    self._load_source_module(source_name)
                except Exception as e:
                    self.logger.error(f"加载书源模块 {source_name} 失败: {e}")
    
    def _load_source_module(self, source_name: str):
        """加载书源模块"""
        try:
            # 动态导入书源模块
            module_path = f"src.sources.{source_name}.source"
            module = importlib.import_module(module_path)
            
            # 查找书源类
            source_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseSource) and 
                    attr != BaseSource):
                    source_class = attr
                    break
            
            if source_class:
                self.source_classes[source_name] = source_class
                self.logger.info(f"发现书源: {source_name}")
                
                # 加载配置
                self._load_source_config(source_name)
            else:
                self.logger.warning(f"书源模块 {source_name} 中未找到有效的书源类")
                
        except ImportError as e:
            self.logger.warning(f"书源模块 {source_name} 导入失败: {e}")
        except Exception as e:
            self.logger.error(f"加载书源模块 {source_name} 时发生错误: {e}")
    
    def _load_source_config(self, source_name: str):
        """加载书源配置"""
        config_path = Path(__file__).parent / source_name / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.source_configs[source_name] = config
                self.logger.info(f"加载书源配置: {source_name}")
            except Exception as e:
                self.logger.error(f"加载书源配置 {source_name} 失败: {e}")
        else:
            self.logger.warning(f"书源配置文件不存在: {config_path}")
    
    def register_source(self, source_name: str, enabled: bool = True) -> bool:
        """注册书源"""
        if source_name not in self.source_classes:
            self.logger.error(f"未找到书源类: {source_name}")
            return False
        
        if source_name not in self.source_configs:
            self.logger.error(f"未找到书源配置: {source_name}")
            return False
        
        try:
            # 创建书源实例
            source_class = self.source_classes[source_name]
            config = self.source_configs[source_name].copy()
            config["enabled"] = enabled
            
            source_instance = source_class(config)
            
            # 验证书源
            if self.engine.validate_source(source_instance):
                self.sources[source_name] = source_instance
                self.engine.register_source(source_name, source_instance)
                self.logger.info(f"注册书源成功: {source_name}")
                return True
            else:
                self.logger.error(f"书源验证失败: {source_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"注册书源 {source_name} 失败: {e}")
            return False
    
    def unregister_source(self, source_name: str) -> bool:
        """注销书源"""
        if source_name in self.sources:
            del self.sources[source_name]
            self.logger.info(f"注销书源: {source_name}")
            return True
        return False
    
    def get_source(self, source_name: str) -> Optional[BaseSource]:
        """获取书源实例"""
        return self.sources.get(source_name)
    
    def list_available_sources(self) -> List[str]:
        """列出可用的书源"""
        return list(self.source_classes.keys())
    
    def list_registered_sources(self) -> List[str]:
        """列出已注册的书源"""
        return list(self.sources.keys())
    
    def get_source_info(self, source_name: str) -> Optional[Dict[str, Any]]:
        """获取书源信息"""
        if source_name in self.source_configs:
            config = self.source_configs[source_name]
            return {
                "name": config.get("bookSourceName", source_name),
                "url": config.get("bookSourceUrl", ""),
                "type": config.get("bookSourceType", 0),
                "enabled": source_name in self.sources,
                "description": config.get("bookSourceComment", ""),
                "group": config.get("bookSourceGroup", ""),
                "version": config.get("version", "1.0.0"),
                "author": config.get("author", ""),
                "update_time": config.get("lastUpdateTime", 0)
            }
        return None
    
    def register_all_sources(self, enabled_only: bool = True) -> Dict[str, bool]:
        """注册所有书源"""
        results = {}
        
        for source_name in self.source_classes:
            # 检查是否在配置中启用
            config = self.source_configs.get(source_name, {})
            is_enabled = config.get("enabled", True)
            
            if enabled_only and not is_enabled:
                results[source_name] = False
                continue
            
            results[source_name] = self.register_source(source_name, is_enabled)
        
        return results
    
    def test_source(self, source_name: str, test_keyword: str = "测试") -> Dict[str, Any]:
        """测试书源"""
        if source_name not in self.sources:
            return {
                "success": False,
                "error": "书源未注册"
            }
        
        source = self.sources[source_name]
        
        try:
            import asyncio
            
            async def run_test():
                # 测试搜索功能
                search_results = await source.search(test_keyword, 1)
                
                if not search_results:
                    return {
                        "success": False,
                        "error": "搜索无结果"
                    }
                
                # 测试书籍详情
                first_book = search_results[0]
                book_info = await source.get_book_info(first_book.book_url)
                
                if not book_info.name:
                    return {
                        "success": False,
                        "error": "获取书籍详情失败"
                    }
                
                # 测试目录
                if book_info.toc_url:
                    toc = await source.get_toc(book_info.toc_url)
                    
                    if not toc:
                        return {
                            "success": False,
                            "error": "获取目录失败"
                        }
                    
                    # 测试正文
                    first_chapter = toc[0]
                    content = await source.get_content(first_chapter.url)
                    
                    if not content.content:
                        return {
                            "success": False,
                            "error": "获取正文失败"
                        }
                
                return {
                    "success": True,
                    "search_count": len(search_results),
                    "book_name": book_info.name,
                    "chapter_count": len(toc) if book_info.toc_url else 0,
                    "content_length": len(content.content) if book_info.toc_url else 0
                }
            
            # 运行异步测试
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(run_test())
                return result
            finally:
                loop.close()
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_source_stats(self) -> Dict[str, Any]:
        """获取书源统计信息"""
        total_available = len(self.source_classes)
        total_registered = len(self.sources)
        
        # 按类型统计
        type_stats = {}
        for source_name, source in self.sources.items():
            source_type = source.type
            type_stats[source_type] = type_stats.get(source_type, 0) + 1
        
        # 按分组统计
        group_stats = {}
        for source_name, source in self.sources.items():
            group = source.config.get("bookSourceGroup", "默认")
            group_stats[group] = group_stats.get(group, 0) + 1
        
        return {
            "total_available": total_available,
            "total_registered": total_registered,
            "registration_rate": total_registered / max(total_available, 1) * 100,
            "type_distribution": type_stats,
            "group_distribution": group_stats,
            "source_list": [
                {
                    "name": name,
                    "enabled": source.enabled,
                    "type": source.type,
                    "group": source.config.get("bookSourceGroup", "默认")
                }
                for name, source in self.sources.items()
            ]
        }
    
    def update_source_config(self, source_name: str, config_updates: Dict[str, Any]) -> bool:
        """更新书源配置"""
        if source_name not in self.source_configs:
            return False
        
        try:
            # 更新配置
            self.source_configs[source_name].update(config_updates)
            
            # 保存配置文件
            config_path = Path(__file__).parent / source_name / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.source_configs[source_name], f, ensure_ascii=False, indent=2)
            
            # 如果书源已注册，重新注册
            if source_name in self.sources:
                self.unregister_source(source_name)
                self.register_source(source_name)
            
            self.logger.info(f"更新书源配置: {source_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新书源配置 {source_name} 失败: {e}")
            return False
