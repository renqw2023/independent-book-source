"""
书源模块测试 - Sources Module Tests

测试各个书源的具体实现：
- 番茄小说书源测试
- 书源管理器测试
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

from src.core.engine import BookSourceEngine, BookInfo, ChapterInfo, ContentInfo
from src.sources.manager import SourceManager
from src.sources.fanqie.source import FanqieSource


class TestFanqieSource:
    """番茄小说书源测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.config = {
            "bookSourceName": "🍅番茄小说",
            "bookSourceUrl": "https://fanqienovel.com",
            "bookSourceType": 0,
            "enabled": True,
            "searchUrl": "/api/author/search/search_book/v1/",
            "ruleSearch": {
                "bookList": "$.data.search_book_data[*]",
                "name": "$.book_name",
                "author": "$.author",
                "bookUrl": "$.book_id",
                "coverUrl": "$.thumb_url"
            }
        }
        self.source = FanqieSource(self.config)
    
    def test_source_initialization(self):
        """测试书源初始化"""
        assert self.source.name == "🍅番茄小说"
        assert self.source.url == "https://fanqienovel.com"
        assert self.source.base_url == "https://fanqienovel.com"
        assert self.source.aid == "1967"
    
    def test_generate_signature(self):
        """测试签名生成"""
        params = {"query": "测试", "aid": "1967"}
        signature = self.source._generate_signature(params)
        
        assert isinstance(signature, str)
        assert len(signature) == 32  # MD5哈希长度
    
    def test_generate_mstoken(self):
        """测试msToken生成"""
        token = self.source._generate_mstoken()
        
        assert isinstance(token, str)
        assert len(token) == 32
    
    def test_build_api_url(self):
        """测试API URL构建"""
        endpoint = "/api/test"
        params = {"query": "测试"}
        
        url = self.source._build_api_url(endpoint, params)
        
        assert url.startswith("https://fanqienovel.com/api/test")
        assert "query=测试" in url
        assert "aid=1967" in url
        assert "_signature=" in url
        assert "msToken=" in url
    
    @pytest.mark.asyncio
    async def test_search(self):
        """测试搜索功能"""
        # 模拟API响应
        mock_response = {
            "data": {
                "search_book_data": [
                    {
                        "book_id": "123456",
                        "book_name": "测试小说",
                        "author": "测试作者",
                        "abstract": "这是一本测试小说",
                        "category": "都市",
                        "thumb_url": "https://example.com/cover.jpg",
                        "word_count": 100000,
                        "last_chapter_title": "第一章"
                    }
                ]
            }
        }
        
        with patch.object(self.source.network, 'get_text', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = json.dumps(mock_response)
            
            results = await self.source.search("测试")
            
            assert len(results) == 1
            book = results[0]
            assert book.name == "测试小说"
            assert book.author == "测试作者"
            assert book.intro == "这是一本测试小说"
            assert book.book_url == "https://fanqienovel.com/page/123456"
    
    @pytest.mark.asyncio
    async def test_search_empty_response(self):
        """测试搜索空响应"""
        with patch.object(self.source.network, 'get_text', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = ""
            
            results = await self.source.search("测试")
            assert results == []
    
    @pytest.mark.asyncio
    async def test_get_book_info(self):
        """测试获取书籍详情"""
        # 模拟API响应
        mock_response = {
            "data": {
                "book_id": "123456",
                "book_name": "测试小说",
                "author": "测试作者",
                "abstract": "这是一本测试小说的详细介绍",
                "category": "都市",
                "thumb_url": "https://example.com/cover.jpg",
                "word_count": 100000,
                "last_chapter_info": {
                    "chapter_title": "最新章节"
                }
            }
        }
        
        with patch.object(self.source.network, 'get_text', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = json.dumps(mock_response)
            
            book_info = await self.source.get_book_info("https://fanqienovel.com/page/123456")
            
            assert book_info.name == "测试小说"
            assert book_info.author == "测试作者"
            assert book_info.intro == "这是一本测试小说的详细介绍"
            assert book_info.last_chapter == "最新章节"
            assert book_info.toc_url is not None
    
    @pytest.mark.asyncio
    async def test_get_toc(self):
        """测试获取目录"""
        # 设置当前书籍ID
        self.source.current_book_id = "123456"
        
        # 模拟API响应
        mock_response = {
            "data": {
                "chapter_data": [
                    {
                        "chapter_id": "1001",
                        "chapter_title": "第一章 开始"
                    },
                    {
                        "chapter_id": "1002", 
                        "chapter_title": "第二章 发展"
                    }
                ]
            }
        }
        
        with patch.object(self.source.network, 'get_text', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = json.dumps(mock_response)
            
            chapters = await self.source.get_toc("mock_toc_url")
            
            assert len(chapters) == 2
            assert chapters[0].name == "第一章 开始"
            assert chapters[1].name == "第二章 发展"
            assert chapters[0].is_vip == False
            assert chapters[0].is_pay == False
    
    @pytest.mark.asyncio
    async def test_get_content(self):
        """测试获取正文内容"""
        # 模拟API响应
        mock_response = {
            "data": {
                "chapter_title": "第一章 开始",
                "content": "这是第一章的内容。\n这是第二段。"
            }
        }
        
        with patch.object(self.source.network, 'get_text', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = json.dumps(mock_response)
            
            content = await self.source.get_content("mock_chapter_url")
            
            assert content.title == "第一章 开始"
            assert "这是第一章的内容。" in content.content
            assert "\n\n" in content.content  # 验证格式化
    
    def test_to_legado_format(self):
        """测试转换为legado格式"""
        legado_format = self.source.to_legado_format()
        
        assert legado_format["bookSourceName"] == "🍅番茄小说"
        assert legado_format["bookSourceUrl"] == "https://fanqienovel.com"
        assert legado_format["bookSourceType"] == 0
        assert legado_format["enabled"] == True


class TestSourceManager:
    """书源管理器测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建临时配置文件
        config_path = os.path.join(self.temp_dir, "test_config.json")
        test_config = {
            "network": {"timeout": 10},
            "cache": {"enabled": False},
            "logging": {"level": "ERROR"}
        }
        
        with open(config_path, 'w') as f:
            json.dump(test_config, f)
        
        self.engine = BookSourceEngine(config_path)
        self.manager = SourceManager(self.engine)
    
    def teardown_method(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_manager_initialization(self):
        """测试管理器初始化"""
        assert self.manager.engine == self.engine
        assert isinstance(self.manager.sources, dict)
        assert isinstance(self.manager.source_configs, dict)
        assert isinstance(self.manager.source_classes, dict)
    
    def test_register_source(self):
        """测试注册书源"""
        # 模拟书源类和配置
        mock_source_class = Mock()
        mock_source_instance = Mock()
        mock_source_instance.enabled = True
        mock_source_instance.config = {"bookSourceName": "测试", "bookSourceUrl": "https://test.com"}
        mock_source_class.return_value = mock_source_instance
        
        self.manager.source_classes["test_source"] = mock_source_class
        self.manager.source_configs["test_source"] = {
            "bookSourceName": "测试书源",
            "bookSourceUrl": "https://test.com",
            "enabled": True
        }
        
        # 模拟引擎验证
        with patch.object(self.engine, 'validate_source', return_value=True):
            result = self.manager.register_source("test_source")
            
            assert result == True
            assert "test_source" in self.manager.sources
    
    def test_list_available_sources(self):
        """测试列出可用书源"""
        # 添加模拟书源类
        self.manager.source_classes["test_source1"] = Mock()
        self.manager.source_classes["test_source2"] = Mock()
        
        available = self.manager.list_available_sources()
        
        assert "test_source1" in available
        assert "test_source2" in available
    
    def test_list_registered_sources(self):
        """测试列出已注册书源"""
        # 添加模拟已注册书源
        self.manager.sources["registered_source"] = Mock()
        
        registered = self.manager.list_registered_sources()
        
        assert "registered_source" in registered
    
    def test_get_source_info(self):
        """测试获取书源信息"""
        # 添加模拟配置
        self.manager.source_configs["test_source"] = {
            "bookSourceName": "测试书源",
            "bookSourceUrl": "https://test.com",
            "bookSourceType": 0,
            "bookSourceComment": "测试描述",
            "bookSourceGroup": "测试分组",
            "version": "1.0.0",
            "author": "测试作者"
        }
        
        info = self.manager.get_source_info("test_source")
        
        assert info is not None
        assert info["name"] == "测试书源"
        assert info["url"] == "https://test.com"
        assert info["description"] == "测试描述"
        assert info["group"] == "测试分组"
    
    def test_get_source_stats(self):
        """测试获取书源统计"""
        # 添加模拟数据
        self.manager.source_classes["available1"] = Mock()
        self.manager.source_classes["available2"] = Mock()
        
        mock_source = Mock()
        mock_source.enabled = True
        mock_source.type = 0
        mock_source.config = {"bookSourceGroup": "测试分组"}
        self.manager.sources["registered1"] = mock_source
        
        stats = self.manager.get_source_stats()
        
        assert stats["total_available"] == 2
        assert stats["total_registered"] == 1
        assert stats["registration_rate"] == 50.0
        assert 0 in stats["type_distribution"]
        assert "测试分组" in stats["group_distribution"]


class TestSourceIntegration:
    """书源集成测试"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """测试完整工作流程"""
        # 创建临时配置
        temp_dir = tempfile.mkdtemp()
        config_path = os.path.join(temp_dir, "test_config.json")
        
        test_config = {
            "network": {"timeout": 10, "retry_times": 1},
            "cache": {"enabled": False},
            "logging": {"level": "ERROR"}
        }
        
        with open(config_path, 'w') as f:
            json.dump(test_config, f)
        
        try:
            # 初始化引擎和管理器
            engine = BookSourceEngine(config_path)
            manager = SourceManager(engine)
            
            # 创建模拟书源
            config = {
                "bookSourceName": "测试书源",
                "bookSourceUrl": "https://test.com",
                "bookSourceType": 0,
                "enabled": True
            }
            
            class MockSource(FanqieSource):
                async def search(self, keyword, page=1):
                    return [BookInfo(
                        name="测试书籍",
                        author="测试作者",
                        book_url="https://test.com/book/1"
                    )]
                
                async def get_book_info(self, book_url):
                    return BookInfo(
                        name="测试书籍",
                        author="测试作者",
                        book_url=book_url,
                        toc_url="https://test.com/toc/1"
                    )
                
                async def get_toc(self, toc_url):
                    return [ChapterInfo(
                        name="第一章",
                        url="https://test.com/chapter/1"
                    )]
                
                async def get_content(self, chapter_url):
                    return ContentInfo(
                        title="第一章",
                        content="这是测试内容"
                    )
            
            # 注册书源
            source = MockSource(config)
            engine.register_source("mock_source", source)
            
            # 测试搜索
            search_results = await engine.search_all("测试")
            assert "mock_source" in search_results
            assert len(search_results["mock_source"]) == 1
            
            # 测试书籍详情
            book_url = search_results["mock_source"][0].book_url
            book_info = await source.get_book_info(book_url)
            assert book_info.name == "测试书籍"
            
            # 测试目录
            toc = await source.get_toc(book_info.toc_url)
            assert len(toc) == 1
            assert toc[0].name == "第一章"
            
            # 测试正文
            content = await source.get_content(toc[0].url)
            assert content.title == "第一章"
            assert content.content == "这是测试内容"
            
            # 测试生成legado格式
            output_path = os.path.join(temp_dir, "test_output.json")
            generated_path = engine.generate_legado_sources(output_path)
            
            assert os.path.exists(generated_path)
            
            with open(generated_path, 'r', encoding='utf-8') as f:
                sources_data = json.load(f)
            
            assert len(sources_data) == 1
            assert sources_data[0]["bookSourceName"] == "测试书源"
            
        finally:
            # 清理临时文件
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
