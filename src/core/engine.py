"""
书源解析引擎 - Book Source Engine

核心解析引擎，负责统一管理和调度各个书源的解析工作。
支持多种解析规则和动态规则配置。
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from .network import NetworkManager
from .rules import RuleEngine
from .cache import CacheManager


@dataclass
class BookInfo:
    """书籍信息数据类"""
    name: str = ""
    author: str = ""
    intro: str = ""
    kind: str = ""
    last_chapter: str = ""
    update_time: str = ""
    book_url: str = ""
    cover_url: str = ""
    word_count: str = ""
    toc_url: str = ""


@dataclass
class ChapterInfo:
    """章节信息数据类"""
    name: str = ""
    url: str = ""
    is_vip: bool = False
    is_pay: bool = False
    update_time: str = ""


@dataclass
class ContentInfo:
    """正文内容数据类"""
    title: str = ""
    content: str = ""
    next_url: str = ""


class BaseSource(ABC):
    """书源基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("bookSourceName", "")
        self.url = config.get("bookSourceUrl", "")
        self.type = config.get("bookSourceType", 0)
        self.enabled = config.get("enabled", True)
        
        # 初始化管理器
        self.network = NetworkManager()
        self.rules = RuleEngine()
        self.cache = CacheManager()
        
        # 设置日志
        self.logger = logging.getLogger(f"source.{self.name}")
    
    @abstractmethod
    async def search(self, keyword: str, page: int = 1) -> List[BookInfo]:
        """搜索书籍"""
        pass
    
    @abstractmethod
    async def get_book_info(self, book_url: str) -> BookInfo:
        """获取书籍详情"""
        pass
    
    @abstractmethod
    async def get_toc(self, toc_url: str) -> List[ChapterInfo]:
        """获取目录"""
        pass
    
    @abstractmethod
    async def get_content(self, chapter_url: str) -> ContentInfo:
        """获取正文内容"""
        pass
    
    def to_legado_format(self) -> Dict[str, Any]:
        """转换为legado格式"""
        return {
            "bookSourceName": self.name,
            "bookSourceUrl": self.url,
            "bookSourceType": self.type,
            "enabled": self.enabled,
            "bookSourceGroup": self.config.get("bookSourceGroup", ""),
            "bookSourceComment": self.config.get("bookSourceComment", ""),
            "lastUpdateTime": self.config.get("lastUpdateTime", 0),
            "searchUrl": self.config.get("searchUrl", ""),
            "exploreUrl": self.config.get("exploreUrl", ""),
            "ruleSearch": self.config.get("ruleSearch", {}),
            "ruleBookInfo": self.config.get("ruleBookInfo", {}),
            "ruleToc": self.config.get("ruleToc", {}),
            "ruleContent": self.config.get("ruleContent", {}),
            "ruleExplore": self.config.get("ruleExplore", {}),
            "header": self.config.get("header", ""),
            "loginUrl": self.config.get("loginUrl", ""),
            "loginUi": self.config.get("loginUi", ""),
            "loginCheckJs": self.config.get("loginCheckJs", ""),
            "coverDecodeJs": self.config.get("coverDecodeJs", ""),
            "variableComment": self.config.get("variableComment", ""),
            "respondTime": self.config.get("respondTime", 180000),
            "weight": self.config.get("weight", 0),
            "customOrder": self.config.get("customOrder", 0),
            "enabledExplore": self.config.get("enabledExplore", True),
            "enabledCookieJar": self.config.get("enabledCookieJar", False),
            "concurrentRate": self.config.get("concurrentRate", ""),
            "bookUrlPattern": self.config.get("bookUrlPattern", "")
        }


class BookSourceEngine:
    """书源解析引擎主类"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.sources: Dict[str, BaseSource] = {}
        
        # 初始化日志
        self._setup_logging()
        self.logger = logging.getLogger("engine")
        
        # 初始化管理器
        self.network = NetworkManager(self.config.get("network", {}))
        self.rules = RuleEngine(self.config.get("rules", {}))
        self.cache = CacheManager(self.config.get("cache", {}))
        
        self.logger.info("书源解析引擎初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"配置文件 {self.config_path} 不存在，使用默认配置")
            return self._get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"配置文件格式错误: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "network": {
                "timeout": 30,
                "retry_times": 3,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "proxy": None
            },
            "cache": {
                "enabled": True,
                "expire_time": 3600,
                "max_size": 1000
            },
            "rules": {
                "js_timeout": 5000,
                "max_depth": 10
            },
            "output": {
                "format": "legado",
                "merge_sources": True,
                "output_dir": "output"
            },
            "logging": {
                "level": "INFO",
                "file": "data/logs/engine.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
    
    def _setup_logging(self):
        """设置日志"""
        log_config = self.config.get("logging", {})
        level = getattr(logging, log_config.get("level", "INFO"))
        
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 文件处理器
        file_handler = logging.FileHandler(
            log_config.get("file", "data/logs/engine.log"),
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # 配置根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
    
    def register_source(self, name: str, source: BaseSource):
        """注册书源"""
        self.sources[name] = source
        self.logger.info(f"注册书源: {name}")
    
    def get_source(self, name: str) -> Optional[BaseSource]:
        """获取书源"""
        return self.sources.get(name)
    
    def list_sources(self) -> List[str]:
        """列出所有书源"""
        return list(self.sources.keys())
    
    async def search_all(self, keyword: str, page: int = 1) -> Dict[str, List[BookInfo]]:
        """在所有书源中搜索"""
        results = {}
        for name, source in self.sources.items():
            if source.enabled:
                try:
                    results[name] = await source.search(keyword, page)
                    self.logger.info(f"书源 {name} 搜索完成，找到 {len(results[name])} 个结果")
                except Exception as e:
                    self.logger.error(f"书源 {name} 搜索失败: {e}")
                    results[name] = []
        return results
    
    def generate_legado_sources(self, output_path: str = "output/legado_sources.json"):
        """生成legado格式的书源文件"""
        sources_data = []
        for name, source in self.sources.items():
            if source.enabled:
                sources_data.append(source.to_legado_format())
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sources_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"已生成 {len(sources_data)} 个书源到 {output_path}")
        return output_path
    
    def validate_source(self, source: BaseSource) -> bool:
        """验证书源配置"""
        required_fields = ["bookSourceName", "bookSourceUrl"]
        for field in required_fields:
            if not source.config.get(field):
                self.logger.error(f"书源 {source.name} 缺少必需字段: {field}")
                return False
        return True
