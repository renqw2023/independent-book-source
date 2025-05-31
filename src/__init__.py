"""
独立书源系统 - 大灰狼融合书源独立版
Independent Book Source System

一个完全独立的书源解析系统，专为legado阅读软件开发。
提供免费、稳定、高效的多平台小说资源聚合服务。

Author: 大灰狼开发团队
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "大灰狼开发团队"
__license__ = "MIT"

from .core import BookSourceEngine, NetworkManager, RuleEngine, CacheManager
from .sources import SourceManager
from .utils import Parser, Validator, Crypto

__all__ = [
    "BookSourceEngine",
    "NetworkManager", 
    "RuleEngine",
    "CacheManager",
    "SourceManager",
    "Parser",
    "Validator",
    "Crypto"
]
