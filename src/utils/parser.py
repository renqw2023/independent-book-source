"""
解析工具 - Parser Utils

提供各种内容解析功能：
- HTML解析
- JSON解析
- URL处理
- 文本处理
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse, parse_qs, unquote
from bs4 import BeautifulSoup, Tag
import html


class Parser:
    """解析工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger("parser")
    
    @staticmethod
    def parse_html(content: str, parser: str = "html.parser") -> BeautifulSoup:
        """解析HTML内容"""
        return BeautifulSoup(content, parser)
    
    @staticmethod
    def parse_json(content: str) -> Dict[str, Any]:
        """解析JSON内容"""
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logging.getLogger("parser").error(f"JSON解析失败: {e}")
            return {}
    
    @staticmethod
    def extract_text(element: Union[Tag, str], strip: bool = True) -> str:
        """提取文本内容"""
        if isinstance(element, str):
            text = element
        elif hasattr(element, 'get_text'):
            text = element.get_text()
        else:
            text = str(element)
        
        if strip:
            text = text.strip()
        
        # 清理HTML实体
        text = html.unescape(text)
        
        # 清理多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @staticmethod
    def extract_links(soup: BeautifulSoup, base_url: str = "") -> List[str]:
        """提取所有链接"""
        links = []
        for link in soup.find_all(['a', 'link'], href=True):
            href = link['href']
            if base_url and not href.startswith('http'):
                href = urljoin(base_url, href)
            links.append(href)
        return links
    
    @staticmethod
    def extract_images(soup: BeautifulSoup, base_url: str = "") -> List[str]:
        """提取所有图片链接"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            if base_url and not src.startswith('http'):
                src = urljoin(base_url, src)
            images.append(src)
        return images
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 清理HTML实体
        text = html.unescape(text)
        
        # 清理特殊字符
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # 移除首尾空白
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """提取文本中的数字"""
        return re.findall(r'\d+(?:\.\d+)?', text)
    
    @staticmethod
    def extract_chinese(text: str) -> str:
        """提取中文字符"""
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_chars = chinese_pattern.findall(text)
        return ''.join(chinese_chars)
    
    @staticmethod
    def parse_url_params(url: str) -> Dict[str, str]:
        """解析URL参数"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # 将列表值转换为单个值
        result = {}
        for key, value_list in params.items():
            result[key] = value_list[0] if value_list else ""
        
        return result
    
    @staticmethod
    def build_url(base_url: str, path: str = "", params: Dict[str, Any] = None) -> str:
        """构建URL"""
        url = urljoin(base_url, path)
        
        if params:
            param_str = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
            if param_str:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}{param_str}"
        
        return url
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """提取域名"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """验证URL是否有效"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def decode_url(url: str) -> str:
        """URL解码"""
        return unquote(url)
    
    @staticmethod
    def extract_json_from_script(content: str, var_name: str = None) -> Dict[str, Any]:
        """从script标签中提取JSON数据"""
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script')
        
        for script in scripts:
            script_content = script.string
            if not script_content:
                continue
            
            # 如果指定了变量名，查找特定变量
            if var_name:
                pattern = rf'{var_name}\s*=\s*(\{{.*?\}});?'
                match = re.search(pattern, script_content, re.DOTALL)
                if match:
                    try:
                        return json.loads(match.group(1))
                    except json.JSONDecodeError:
                        continue
            else:
                # 查找所有JSON对象
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                matches = re.findall(json_pattern, script_content)
                for match in matches:
                    try:
                        return json.loads(match)
                    except json.JSONDecodeError:
                        continue
        
        return {}
    
    @staticmethod
    def extract_between(text: str, start: str, end: str) -> str:
        """提取两个字符串之间的内容"""
        start_index = text.find(start)
        if start_index == -1:
            return ""
        
        start_index += len(start)
        end_index = text.find(end, start_index)
        if end_index == -1:
            return ""
        
        return text[start_index:end_index]
    
    @staticmethod
    def split_chapters(content: str, pattern: str = None) -> List[str]:
        """分割章节内容"""
        if not pattern:
            # 默认章节分割模式
            pattern = r'第[一二三四五六七八九十百千万\d]+[章节回]'
        
        chapters = re.split(pattern, content)
        
        # 清理空章节
        chapters = [chapter.strip() for chapter in chapters if chapter.strip()]
        
        return chapters
    
    @staticmethod
    def normalize_title(title: str) -> str:
        """标准化标题"""
        if not title:
            return ""
        
        # 移除常见的前缀和后缀
        title = re.sub(r'^(第\d+[章节回][:：\s]*)', '', title)
        title = re.sub(r'[\(\（].*?[\)\）]$', '', title)
        
        # 清理空白字符
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    @staticmethod
    def extract_chapter_number(title: str) -> Optional[int]:
        """提取章节号"""
        # 匹配数字章节号
        match = re.search(r'第(\d+)[章节回]', title)
        if match:
            return int(match.group(1))
        
        # 匹配中文数字章节号
        chinese_numbers = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '百': 100, '千': 1000, '万': 10000
        }
        
        match = re.search(r'第([一二三四五六七八九十百千万]+)[章节回]', title)
        if match:
            chinese_num = match.group(1)
            # 简单的中文数字转换（可以扩展）
            if chinese_num in chinese_numbers:
                return chinese_numbers[chinese_num]
        
        return None
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    @staticmethod
    def parse_time_string(time_str: str) -> Optional[str]:
        """解析时间字符串"""
        if not time_str:
            return None
        
        # 常见时间格式的正则表达式
        patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # YYYY年MM月DD日
            r'(\d{1,2})-(\d{1,2})',  # MM-DD
            r'(\d{1,2})月(\d{1,2})日',  # MM月DD日
        ]
        
        for pattern in patterns:
            match = re.search(pattern, time_str)
            if match:
                return match.group(0)
        
        return time_str
