"""
数据验证工具 - Validator Utils

提供各种数据验证功能：
- URL验证
- 书源配置验证
- 数据格式验证
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse


class Validator:
    """数据验证工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger("validator")
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """验证URL是否有效"""
        if not url or not isinstance(url, str):
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """验证域名是否有效"""
        if not domain or not isinstance(domain, str):
            return False
        
        # 域名正则表达式
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        
        return bool(domain_pattern.match(domain))
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """验证邮箱地址是否有效"""
        if not email or not isinstance(email, str):
            return False
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        return bool(email_pattern.match(email))
    
    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """验证JSON字符串是否有效"""
        if not json_str or not isinstance(json_str, str):
            return False
        
        try:
            json.loads(json_str)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    @staticmethod
    def validate_book_source_config(config: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证书源配置"""
        errors = {
            "required_fields": [],
            "invalid_fields": [],
            "warnings": []
        }
        
        # 必需字段检查
        required_fields = [
            "bookSourceName",
            "bookSourceUrl"
        ]
        
        for field in required_fields:
            if field not in config or not config[field]:
                errors["required_fields"].append(f"缺少必需字段: {field}")
        
        # 字段格式验证
        if "bookSourceUrl" in config:
            if not Validator.is_valid_url(config["bookSourceUrl"]):
                errors["invalid_fields"].append("bookSourceUrl格式无效")
        
        if "bookSourceType" in config:
            if not isinstance(config["bookSourceType"], int) or config["bookSourceType"] not in [0, 1, 2, 3]:
                errors["invalid_fields"].append("bookSourceType必须是0-3之间的整数")
        
        if "searchUrl" in config and config["searchUrl"]:
            if not ("{{key}}" in config["searchUrl"] or "{{keyword}}" in config["searchUrl"]):
                errors["warnings"].append("searchUrl中建议包含{{key}}或{{keyword}}占位符")
        
        # 规则验证
        rule_sections = ["ruleSearch", "ruleBookInfo", "ruleToc", "ruleContent", "ruleExplore"]
        for section in rule_sections:
            if section in config and isinstance(config[section], dict):
                rule_errors = Validator._validate_rules(config[section], section)
                errors["invalid_fields"].extend(rule_errors)
        
        return errors
    
    @staticmethod
    def _validate_rules(rules: Dict[str, str], section_name: str) -> List[str]:
        """验证规则配置"""
        errors = []
        
        # 基本规则字段检查
        if section_name == "ruleSearch":
            recommended_fields = ["bookList", "name", "author", "bookUrl"]
        elif section_name == "ruleBookInfo":
            recommended_fields = ["name", "author", "intro", "tocUrl"]
        elif section_name == "ruleToc":
            recommended_fields = ["chapterList", "chapterName", "chapterUrl"]
        elif section_name == "ruleContent":
            recommended_fields = ["content"]
        else:
            recommended_fields = []
        
        # 检查推荐字段
        for field in recommended_fields:
            if field not in rules or not rules[field]:
                errors.append(f"{section_name}.{field}字段为空或缺失")
        
        # 验证规则语法
        for field, rule in rules.items():
            if rule and isinstance(rule, str):
                if not Validator._is_valid_rule_syntax(rule):
                    errors.append(f"{section_name}.{field}规则语法可能有误: {rule}")
        
        return errors
    
    @staticmethod
    def _is_valid_rule_syntax(rule: str) -> bool:
        """验证规则语法"""
        if not rule:
            return False
        
        # JavaScript规则
        if rule.startswith("<js>") and rule.endswith("</js>"):
            return True
        
        # JSON路径规则
        if rule.startswith("$."):
            return True
        
        # CSS选择器规则
        if any(selector in rule for selector in ["@css:", "class.", "tag.", "#", "."]):
            return True
        
        # XPath规则
        if rule.startswith("//") or rule.startswith("./"):
            return True
        
        # 正则表达式规则
        if "##" in rule:
            parts = rule.split("##")
            if len(parts) >= 2:
                try:
                    re.compile(parts[1])
                    return True
                except re.error:
                    return False
        
        # 文本规则（总是有效）
        return True
    
    @staticmethod
    def validate_search_result(result: Dict[str, Any]) -> bool:
        """验证搜索结果格式"""
        required_fields = ["name", "author", "bookUrl"]
        
        for field in required_fields:
            if field not in result or not result[field]:
                return False
        
        # URL格式验证
        if not Validator.is_valid_url(result["bookUrl"]):
            return False
        
        return True
    
    @staticmethod
    def validate_book_info(book_info: Dict[str, Any]) -> bool:
        """验证书籍信息格式"""
        required_fields = ["name", "author"]
        
        for field in required_fields:
            if field not in book_info or not book_info[field]:
                return False
        
        return True
    
    @staticmethod
    def validate_chapter_info(chapter_info: Dict[str, Any]) -> bool:
        """验证章节信息格式"""
        required_fields = ["name", "url"]
        
        for field in required_fields:
            if field not in chapter_info or not chapter_info[field]:
                return False
        
        # URL格式验证
        if not Validator.is_valid_url(chapter_info["url"]):
            return False
        
        return True
    
    @staticmethod
    def validate_content_info(content_info: Dict[str, Any]) -> bool:
        """验证正文内容格式"""
        if "content" not in content_info or not content_info["content"]:
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """清理文件名，移除非法字符"""
        if not filename:
            return "untitled"
        
        # 移除或替换非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        filename = re.sub(illegal_chars, '_', filename)
        
        # 移除首尾空白和点号
        filename = filename.strip('. ')
        
        # 限制长度
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename or "untitled"
    
    @staticmethod
    def validate_config_file(config_path: str) -> Dict[str, List[str]]:
        """验证配置文件"""
        errors = {
            "file_errors": [],
            "format_errors": [],
            "content_errors": []
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            errors["file_errors"].append(f"配置文件不存在: {config_path}")
            return errors
        except Exception as e:
            errors["file_errors"].append(f"读取配置文件失败: {e}")
            return errors
        
        # JSON格式验证
        try:
            config = json.loads(content)
        except json.JSONDecodeError as e:
            errors["format_errors"].append(f"JSON格式错误: {e}")
            return errors
        
        # 内容验证
        if not isinstance(config, dict):
            errors["content_errors"].append("配置文件根节点必须是对象")
            return errors
        
        # 验证各个配置节
        sections = ["network", "cache", "rules", "output", "logging"]
        for section in sections:
            if section in config:
                section_errors = Validator._validate_config_section(config[section], section)
                errors["content_errors"].extend(section_errors)
        
        return errors
    
    @staticmethod
    def _validate_config_section(section_config: Any, section_name: str) -> List[str]:
        """验证配置节"""
        errors = []
        
        if not isinstance(section_config, dict):
            errors.append(f"{section_name}配置必须是对象")
            return errors
        
        if section_name == "network":
            if "timeout" in section_config:
                if not isinstance(section_config["timeout"], (int, float)) or section_config["timeout"] <= 0:
                    errors.append("network.timeout必须是正数")
            
            if "retry_times" in section_config:
                if not isinstance(section_config["retry_times"], int) or section_config["retry_times"] < 0:
                    errors.append("network.retry_times必须是非负整数")
        
        elif section_name == "cache":
            if "expire_time" in section_config:
                if not isinstance(section_config["expire_time"], (int, float)) or section_config["expire_time"] <= 0:
                    errors.append("cache.expire_time必须是正数")
            
            if "max_size" in section_config:
                if not isinstance(section_config["max_size"], int) or section_config["max_size"] <= 0:
                    errors.append("cache.max_size必须是正整数")
        
        return errors
    
    @staticmethod
    def is_safe_content(content: str) -> bool:
        """检查内容是否安全（不包含恶意代码）"""
        if not content:
            return True
        
        # 检查潜在的恶意模式
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'document\.write',
            r'innerHTML\s*=',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return False
        
        return True
