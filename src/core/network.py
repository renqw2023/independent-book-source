"""
网络请求管理器 - Network Manager

负责处理所有HTTP请求，包括：
- 请求重试机制
- 反爬虫策略
- 代理支持
- 请求头管理
- 响应处理
"""

import asyncio
import aiohttp
import logging
import random
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse
import json


class NetworkManager:
    """网络请求管理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.timeout = self.config.get("timeout", 30)
        self.retry_times = self.config.get("retry_times", 3)
        self.proxy = self.config.get("proxy")
        
        # 用户代理池
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        
        # 会话管理
        self.session = None
        self.cookies = {}
        
        # 请求统计
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        
        self.logger = logging.getLogger("network")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.create_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close_session()
    
    async def create_session(self):
        """创建HTTP会话"""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self._get_default_headers()
        )
        
        self.logger.info("HTTP会话创建成功")
    
    async def close_session(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.logger.info("HTTP会话已关闭")
    
    def _get_default_headers(self) -> Dict[str, str]:
        """获取默认请求头"""
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def _get_random_user_agent(self) -> str:
        """获取随机用户代理"""
        return random.choice(self.user_agents)
    
    async def get(self, url: str, headers: Dict[str, str] = None, 
                  params: Dict[str, Any] = None, **kwargs) -> aiohttp.ClientResponse:
        """GET请求"""
        return await self._request("GET", url, headers=headers, params=params, **kwargs)
    
    async def post(self, url: str, data: Any = None, json_data: Dict[str, Any] = None,
                   headers: Dict[str, str] = None, **kwargs) -> aiohttp.ClientResponse:
        """POST请求"""
        return await self._request("POST", url, data=data, json=json_data, headers=headers, **kwargs)
    
    async def _request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        """通用请求方法"""
        if not self.session:
            await self.create_session()
        
        # 合并请求头
        headers = kwargs.pop("headers", {})
        merged_headers = self._get_default_headers()
        merged_headers.update(headers)
        merged_headers["User-Agent"] = self._get_random_user_agent()
        
        # 添加Referer
        if "Referer" not in merged_headers:
            parsed_url = urlparse(url)
            merged_headers["Referer"] = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        
        kwargs["headers"] = merged_headers
        
        # 代理设置
        if self.proxy:
            kwargs["proxy"] = self.proxy
        
        # 请求重试
        last_exception = None
        for attempt in range(self.retry_times + 1):
            try:
                self.request_count += 1
                
                # 添加随机延迟，避免请求过于频繁
                if attempt > 0:
                    delay = random.uniform(1, 3) * attempt
                    await asyncio.sleep(delay)
                    self.logger.info(f"第 {attempt + 1} 次重试请求: {url}")
                
                async with self.session.request(method, url, **kwargs) as response:
                    # 检查响应状态
                    if response.status == 200:
                        self.success_count += 1
                        return response
                    elif response.status in [403, 429]:
                        # 被限制访问，增加延迟
                        self.logger.warning(f"请求被限制 (状态码: {response.status}): {url}")
                        if attempt < self.retry_times:
                            await asyncio.sleep(random.uniform(5, 10))
                            continue
                    elif response.status >= 500:
                        # 服务器错误，重试
                        self.logger.warning(f"服务器错误 (状态码: {response.status}): {url}")
                        if attempt < self.retry_times:
                            continue
                    
                    # 其他状态码也返回响应，让调用者处理
                    return response
                    
            except asyncio.TimeoutError:
                last_exception = f"请求超时: {url}"
                self.logger.warning(last_exception)
            except aiohttp.ClientError as e:
                last_exception = f"网络错误: {e}"
                self.logger.warning(last_exception)
            except Exception as e:
                last_exception = f"未知错误: {e}"
                self.logger.error(last_exception)
        
        # 所有重试都失败
        self.error_count += 1
        raise Exception(f"请求失败，已重试 {self.retry_times} 次: {last_exception}")
    
    async def get_text(self, url: str, encoding: str = "utf-8", **kwargs) -> str:
        """获取文本内容"""
        response = await self.get(url, **kwargs)
        try:
            content = await response.read()
            # 尝试检测编码
            if encoding == "auto":
                encoding = self._detect_encoding(content, response.headers)
            return content.decode(encoding, errors="ignore")
        finally:
            response.close()
    
    async def get_json(self, url: str, **kwargs) -> Dict[str, Any]:
        """获取JSON内容"""
        response = await self.get(url, **kwargs)
        try:
            return await response.json()
        finally:
            response.close()
    
    async def post_json(self, url: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """POST JSON数据并获取JSON响应"""
        response = await self.post(url, json_data=data, **kwargs)
        try:
            return await response.json()
        finally:
            response.close()
    
    def _detect_encoding(self, content: bytes, headers: Dict[str, str]) -> str:
        """检测内容编码"""
        # 从Content-Type头中获取编码
        content_type = headers.get("Content-Type", "")
        if "charset=" in content_type:
            charset = content_type.split("charset=")[1].split(";")[0].strip()
            return charset
        
        # 尝试从内容中检测编码
        try:
            import chardet
            result = chardet.detect(content)
            if result["confidence"] > 0.7:
                return result["encoding"]
        except ImportError:
            pass
        
        # 默认使用UTF-8
        return "utf-8"
    
    def set_cookies(self, cookies: Dict[str, str]):
        """设置Cookie"""
        self.cookies.update(cookies)
        if self.session:
            for name, value in cookies.items():
                self.session.cookie_jar.update_cookies({name: value})
    
    def get_stats(self) -> Dict[str, int]:
        """获取请求统计信息"""
        return {
            "total_requests": self.request_count,
            "successful_requests": self.success_count,
            "failed_requests": self.error_count,
            "success_rate": self.success_count / max(self.request_count, 1) * 100
        }
    
    async def test_connection(self, url: str) -> bool:
        """测试连接"""
        try:
            response = await self.get(url)
            response.close()
            return response.status == 200
        except Exception as e:
            self.logger.error(f"连接测试失败: {e}")
            return False
