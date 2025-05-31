"""
规则引擎 - Rule Engine

负责处理各种解析规则：
- CSS选择器
- XPath表达式
- 正则表达式
- JavaScript脚本
- JSON路径
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse

# JavaScript功能可用性检查（延迟导入）
JS_AVAILABLE = None  # 延迟检查


class RuleEngine:
    """规则引擎"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.js_timeout = self.config.get("js_timeout", 5000)
        self.max_depth = self.config.get("max_depth", 10)

        # JavaScript执行环境（延迟初始化）
        self.js_context = None
        self.js_enabled = False
        self._js_checked = False

        self.logger = logging.getLogger("rules")

    def _check_js_availability(self):
        """检查JavaScript功能可用性"""
        if self._js_checked:
            return self.js_enabled

        self._js_checked = True
        try:
            import js2py
            self.js_context = js2py.EvalJs()
            self._init_js_context()
            self.js_enabled = True
            self.logger.info("JavaScript引擎初始化成功")
        except ImportError:
            self.logger.warning("js2py未安装，JavaScript功能已禁用")
            self.js_enabled = False
        except Exception as e:
            self.logger.warning(f"JavaScript引擎初始化失败: {e}")
            self.js_enabled = False

        return self.js_enabled

    def _init_js_context(self):
        """初始化JavaScript执行环境"""
        # 添加常用的JavaScript函数
        self.js_context.execute("""
            function java_put(key, value) {
                if (typeof window.java_vars === 'undefined') {
                    window.java_vars = {};
                }
                window.java_vars[key] = value;
                return value;
            }
            
            function java_get(key) {
                if (typeof window.java_vars === 'undefined') {
                    return null;
                }
                return window.java_vars[key] || null;
            }
            
            function java_base64Encode(str) {
                return btoa(unescape(encodeURIComponent(str)));
            }
            
            function java_base64Decode(str) {
                return decodeURIComponent(escape(atob(str)));
            }
            
            function java_md5(str) {
                // 简单的MD5实现，实际项目中应该使用更完整的实现
                return str;
            }
            
            function java_toast(message) {
                console.log('Toast: ' + message);
            }
            
            function java_log(message) {
                console.log('Log: ' + message);
            }
            
            // 模拟Java对象
            var java = {
                put: java_put,
                get: java_get,
                base64Encode: java_base64Encode,
                base64Decode: java_base64Decode,
                md5: java_md5,
                toast: java_toast,
                log: java_log
            };
        """)
    
    def parse_rule(self, rule: str, content: str, base_url: str = "") -> Union[str, List[str]]:
        """解析规则"""
        if not rule or not content:
            return ""
        
        try:
            # JavaScript规则
            if rule.startswith("<js>") and rule.endswith("</js>"):
                return self._parse_js_rule(rule[4:-5], content, base_url)
            
            # JSON路径规则
            if rule.startswith("$."):
                return self._parse_json_rule(rule, content)
            
            # CSS选择器规则
            if any(selector in rule for selector in ["@css:", "class.", "tag.", "#", "."]):
                return self._parse_css_rule(rule, content, base_url)
            
            # XPath规则
            if rule.startswith("//") or rule.startswith("./"):
                return self._parse_xpath_rule(rule, content, base_url)
            
            # 正则表达式规则
            if "##" in rule:
                return self._parse_regex_rule(rule, content)
            
            # 直接文本规则
            return self._parse_text_rule(rule, content)
            
        except Exception as e:
            self.logger.error(f"规则解析失败: {rule}, 错误: {e}")
            return ""
    
    def _parse_js_rule(self, js_code: str, content: str, base_url: str = "") -> Union[str, List[str]]:
        """解析JavaScript规则"""
        if not self._check_js_availability():
            self.logger.warning("JavaScript功能不可用，返回原始内容")
            return content

        try:
            # 设置上下文变量
            self.js_context.result = content
            self.js_context.baseUrl = base_url
            self.js_context.src = content

            # 执行JavaScript代码
            result = self.js_context.eval(js_code)

            # 处理返回结果
            if isinstance(result, (list, tuple)):
                return [str(item) for item in result]
            else:
                return str(result) if result is not None else ""

        except Exception as e:
            self.logger.error(f"JavaScript执行失败: {e}")
            return content
    
    def _parse_json_rule(self, rule: str, content: str) -> Union[str, List[str]]:
        """解析JSON路径规则"""
        try:
            import jsonpath_ng

            # 解析JSON内容
            if isinstance(content, str):
                data = json.loads(content)
            else:
                data = content

            # 执行JSONPath查询
            jsonpath_expr = jsonpath_ng.parse(rule)
            matches = jsonpath_expr.find(data)

            if not matches:
                return ""

            # 返回结果
            if len(matches) == 1:
                return str(matches[0].value)
            else:
                return [str(match.value) for match in matches]

        except ImportError:
            self.logger.error("jsonpath_ng未安装，无法解析JSON路径规则")
            return ""
        except Exception as e:
            self.logger.error(f"JSON路径解析失败: {e}")
            return ""
    
    def _parse_css_rule(self, rule: str, content: str, base_url: str = "") -> Union[str, List[str]]:
        """解析CSS选择器规则"""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(content, 'html.parser')

            # 解析规则
            parts = rule.split("@")
            selector = parts[0]

            # 处理特殊选择器格式
            if selector.startswith("@css:"):
                selector = selector[5:]
            elif selector.startswith("class."):
                selector = "." + selector[6:]
            elif selector.startswith("tag."):
                selector = selector[4:]

            # 查找元素
            elements = soup.select(selector)

            if not elements:
                return ""

            # 提取属性或文本
            if len(parts) > 1:
                attr = parts[1]
                if attr == "text":
                    results = [elem.get_text(strip=True) for elem in elements]
                elif attr == "html":
                    results = [str(elem) for elem in elements]
                elif attr.startswith("attr(") and attr.endswith(")"):
                    attr_name = attr[5:-1]
                    results = [elem.get(attr_name, "") for elem in elements]
                else:
                    results = [elem.get(attr, "") for elem in elements]
            else:
                results = [elem.get_text(strip=True) for elem in elements]

            # 处理URL
            if base_url and any(attr in rule for attr in ["href", "src", "url"]):
                results = [urljoin(base_url, url) if url and not url.startswith("http") else url for url in results]

            return results[0] if len(results) == 1 else results

        except ImportError:
            self.logger.error("beautifulsoup4未安装，无法解析CSS选择器")
            return ""
        except Exception as e:
            self.logger.error(f"CSS选择器解析失败: {e}")
            return ""
    
    def _parse_xpath_rule(self, rule: str, content: str, base_url: str = "") -> Union[str, List[str]]:
        """解析XPath规则"""
        try:
            from lxml import etree, html

            # 解析HTML
            tree = html.fromstring(content)

            # 执行XPath查询
            results = tree.xpath(rule)

            if not results:
                return ""

            # 处理结果
            processed_results = []
            for result in results:
                if isinstance(result, str):
                    processed_results.append(result)
                elif hasattr(result, 'text'):
                    processed_results.append(result.text or "")
                else:
                    processed_results.append(str(result))

            return processed_results[0] if len(processed_results) == 1 else processed_results

        except ImportError:
            self.logger.error("lxml未安装，无法解析XPath规则")
            return ""
        except Exception as e:
            self.logger.error(f"XPath解析失败: {e}")
            return ""
    
    def _parse_regex_rule(self, rule: str, content: str) -> Union[str, List[str]]:
        """解析正则表达式规则"""
        try:
            # 分割规则
            parts = rule.split("##")
            if len(parts) < 2:
                return ""
            
            pattern = parts[1]
            replacement = parts[2] if len(parts) > 2 else ""
            
            # 执行正则匹配
            if replacement:
                # 替换模式
                result = re.sub(pattern, replacement, content)
                return result
            else:
                # 匹配模式
                matches = re.findall(pattern, content)
                if not matches:
                    return ""
                
                if len(matches) == 1:
                    return matches[0] if isinstance(matches[0], str) else matches[0][0]
                else:
                    return [match if isinstance(match, str) else match[0] for match in matches]
                    
        except Exception as e:
            self.logger.error(f"正则表达式解析失败: {e}")
            return ""
    
    def _parse_text_rule(self, rule: str, content: str) -> str:
        """解析文本规则"""
        # 简单的文本处理
        if rule == "text":
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                return soup.get_text(strip=True)
            except ImportError:
                # 如果没有BeautifulSoup，使用简单的正则表达式去除HTML标签
                import re
                clean_text = re.sub(r'<[^>]+>', '', content)
                return clean_text.strip()

        return rule
    
    def parse_multiple_rules(self, rules: Dict[str, str], content: str, base_url: str = "") -> Dict[str, Any]:
        """解析多个规则"""
        results = {}
        for key, rule in rules.items():
            if rule:
                results[key] = self.parse_rule(rule, content, base_url)
        return results
    
    def validate_rule(self, rule: str) -> bool:
        """验证规则格式"""
        if not rule:
            return False
        
        try:
            # 基本格式检查
            if rule.startswith("<js>") and rule.endswith("</js>"):
                return True
            elif rule.startswith("$."):
                return True
            elif any(selector in rule for selector in ["@css:", "class.", "tag.", "#", "."]):
                return True
            elif rule.startswith("//") or rule.startswith("./"):
                return True
            elif "##" in rule:
                return True
            else:
                return True  # 文本规则总是有效的
                
        except Exception:
            return False
