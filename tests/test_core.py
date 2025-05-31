"""
核心模块测试 - Core Module Tests

测试书源系统的核心功能：
- 引擎测试
- 网络管理器测试
- 规则引擎测试
- 缓存管理器测试
"""

import pytest
import asyncio
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.engine import BookSourceEngine, BaseSource, BookInfo, ChapterInfo, ContentInfo
from src.core.network import NetworkManager
from src.core.rules import RuleEngine
from src.core.cache import CacheManager


class TestBookSourceEngine:
    """书源引擎测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
        
        # 创建测试配置
        test_config = {
            "network": {"timeout": 10},
            "cache": {"enabled": False},
            "rules": {"js_timeout": 1000},
            "logging": {"level": "ERROR"}
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.engine = BookSourceEngine(self.config_path)
    
    def teardown_method(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_engine_initialization(self):
        """测试引擎初始化"""
        assert self.engine is not None
        assert self.engine.config is not None
        assert isinstance(self.engine.sources, dict)
    
    def test_register_source(self):
        """测试书源注册"""
        # 创建模拟书源
        mock_source = Mock(spec=BaseSource)
        mock_source.name = "test_source"
        mock_source.enabled = True
        mock_source.config = {"bookSourceName": "测试书源", "bookSourceUrl": "https://test.com"}
        
        # 注册书源
        self.engine.register_source("test_source", mock_source)
        
        # 验证注册成功
        assert "test_source" in self.engine.sources
        assert self.engine.get_source("test_source") == mock_source
    
    def test_list_sources(self):
        """测试列出书源"""
        # 注册测试书源
        mock_source = Mock(spec=BaseSource)
        mock_source.name = "test_source"
        self.engine.register_source("test_source", mock_source)
        
        # 获取书源列表
        sources = self.engine.list_sources()
        
        assert "test_source" in sources
    
    @pytest.mark.asyncio
    async def test_search_all(self):
        """测试全局搜索"""
        # 创建模拟书源
        mock_source = Mock(spec=BaseSource)
        mock_source.enabled = True
        mock_source.search = AsyncMock(return_value=[
            BookInfo(name="测试书籍", author="测试作者", book_url="https://test.com/book/1")
        ])
        
        self.engine.register_source("test_source", mock_source)
        
        # 执行搜索
        results = await self.engine.search_all("测试")
        
        assert "test_source" in results
        assert len(results["test_source"]) == 1
        assert results["test_source"][0].name == "测试书籍"
    
    def test_generate_legado_sources(self):
        """测试生成legado格式书源"""
        # 创建模拟书源
        mock_source = Mock(spec=BaseSource)
        mock_source.enabled = True
        mock_source.to_legado_format.return_value = {
            "bookSourceName": "测试书源",
            "bookSourceUrl": "https://test.com"
        }
        
        self.engine.register_source("test_source", mock_source)
        
        # 生成书源文件
        output_path = os.path.join(self.temp_dir, "test_sources.json")
        result_path = self.engine.generate_legado_sources(output_path)
        
        assert result_path == output_path
        assert os.path.exists(output_path)
        
        # 验证文件内容
        with open(output_path, 'r', encoding='utf-8') as f:
            sources_data = json.load(f)
        
        assert len(sources_data) == 1
        assert sources_data[0]["bookSourceName"] == "测试书源"


class TestNetworkManager:
    """网络管理器测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.network = NetworkManager({
            "timeout": 5,
            "retry_times": 1
        })
    
    @pytest.mark.asyncio
    async def test_create_session(self):
        """测试创建会话"""
        await self.network.create_session()
        assert self.network.session is not None
        await self.network.close_session()
    
    @pytest.mark.asyncio
    async def test_get_request(self):
        """测试GET请求"""
        with patch('aiohttp.ClientSession.request') as mock_request:
            # 模拟响应
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.__aenter__.return_value = mock_response
            mock_request.return_value = mock_response
            
            async with self.network:
                response = await self.network.get("https://httpbin.org/get")
                assert response.status == 200
    
    def test_generate_signature(self):
        """测试签名生成"""
        params = {"key1": "value1", "key2": "value2"}
        signature = self.network._generate_signature(params)
        assert isinstance(signature, str)
        assert len(signature) > 0
    
    def test_get_stats(self):
        """测试获取统计信息"""
        stats = self.network.get_stats()
        assert "total_requests" in stats
        assert "successful_requests" in stats
        assert "failed_requests" in stats
        assert "success_rate" in stats


class TestRuleEngine:
    """规则引擎测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.rules = RuleEngine()
    
    def test_parse_text_rule(self):
        """测试文本规则解析"""
        content = "<div>测试内容</div>"
        result = self.rules.parse_rule("text", content)
        assert "测试内容" in result
    
    def test_parse_css_rule(self):
        """测试CSS选择器规则"""
        content = '<div class="title">测试标题</div>'
        result = self.rules.parse_rule(".title@text", content)
        assert result == "测试标题"
    
    def test_parse_regex_rule(self):
        """测试正则表达式规则"""
        content = "书名：《测试小说》"
        result = self.rules.parse_rule("##书名：《(.+?)》", content)
        assert result == "测试小说"
    
    def test_parse_json_rule(self):
        """测试JSON路径规则"""
        content = '{"data": {"name": "测试书籍"}}'
        result = self.rules.parse_rule("$.data.name", content)
        assert result == "测试书籍"
    
    def test_parse_js_rule(self):
        """测试JavaScript规则"""
        content = "测试内容"
        result = self.rules.parse_rule("<js>result + '_processed'</js>", content)
        assert result == "测试内容_processed"
    
    def test_validate_rule(self):
        """测试规则验证"""
        assert self.rules.validate_rule(".title@text") == True
        assert self.rules.validate_rule("##pattern") == True
        assert self.rules.validate_rule("$.data.name") == True
        assert self.rules.validate_rule("<js>result</js>") == True
        assert self.rules.validate_rule("") == False
    
    def test_parse_multiple_rules(self):
        """测试多规则解析"""
        content = '<div class="book"><span class="title">测试书籍</span><span class="author">测试作者</span></div>'
        rules = {
            "name": ".title@text",
            "author": ".author@text"
        }
        
        results = self.rules.parse_multiple_rules(rules, content)
        
        assert results["name"] == "测试书籍"
        assert results["author"] == "测试作者"


class TestCacheManager:
    """缓存管理器测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = CacheManager({
            "enabled": True,
            "expire_time": 60,
            "max_size": 10,
            "cache_dir": self.temp_dir,
            "file_cache": False,  # 禁用文件缓存以简化测试
            "db_cache": False     # 禁用数据库缓存以简化测试
        })
    
    def teardown_method(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_set_and_get(self):
        """测试设置和获取缓存"""
        key = "test_key"
        value = "test_value"
        
        # 设置缓存
        result = self.cache.set(key, value)
        assert result == True
        
        # 获取缓存
        cached_value = self.cache.get(key)
        assert cached_value == value
    
    def test_get_nonexistent(self):
        """测试获取不存在的缓存"""
        result = self.cache.get("nonexistent_key", "default")
        assert result == "default"
    
    def test_delete(self):
        """测试删除缓存"""
        key = "test_key"
        value = "test_value"
        
        # 设置缓存
        self.cache.set(key, value)
        assert self.cache.get(key) == value
        
        # 删除缓存
        self.cache.delete(key)
        assert self.cache.get(key) is None
    
    def test_clear_all(self):
        """测试清空所有缓存"""
        # 设置多个缓存项
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        # 清空所有缓存
        self.cache.clear_all()
        
        # 验证缓存已清空
        assert self.cache.get("key1") is None
        assert self.cache.get("key2") is None
    
    def test_get_stats(self):
        """测试获取缓存统计"""
        stats = self.cache.get_stats()
        
        assert "enabled" in stats
        assert "memory_cache_count" in stats
        assert "max_size" in stats
        assert "expire_time" in stats


class TestBaseSource:
    """基础书源测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.config = {
            "bookSourceName": "测试书源",
            "bookSourceUrl": "https://test.com",
            "bookSourceType": 0,
            "enabled": True
        }
    
    def test_to_legado_format(self):
        """测试转换为legado格式"""
        # 创建具体的书源实现用于测试
        class TestSource(BaseSource):
            async def search(self, keyword, page=1):
                return []
            
            async def get_book_info(self, book_url):
                return BookInfo()
            
            async def get_toc(self, toc_url):
                return []
            
            async def get_content(self, chapter_url):
                return ContentInfo()
        
        source = TestSource(self.config)
        legado_format = source.to_legado_format()
        
        assert legado_format["bookSourceName"] == "测试书源"
        assert legado_format["bookSourceUrl"] == "https://test.com"
        assert legado_format["bookSourceType"] == 0
        assert legado_format["enabled"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
