# 开发指南 - Development Guide

## 项目概述

独立书源系统是一个专为legado阅读软件开发的免费书源聚合工具，旨在替代需要付费登录的第三方书源服务。

## 开发环境设置

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器
- Git 版本控制

### 安装开发环境

1. **克隆项目**
```bash
git clone https://github.com/your-username/independent-book-source.git
cd independent-book-source
```

2. **创建虚拟环境**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**
```bash
# 安装基础依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -e .[dev]
```

4. **配置开发工具**
```bash
# 安装pre-commit钩子
pre-commit install

# 配置IDE（推荐VSCode）
code .
```

## 项目结构

```
independent-book-source/
├── src/                    # 源代码
│   ├── core/              # 核心模块
│   │   ├── engine.py      # 书源引擎
│   │   ├── network.py     # 网络管理
│   │   ├── rules.py       # 规则引擎
│   │   └── cache.py       # 缓存管理
│   ├── sources/           # 书源实现
│   │   ├── manager.py     # 书源管理器
│   │   ├── fanqie/        # 番茄小说
│   │   ├── qimao/         # 七猫小说
│   │   └── ...
│   ├── utils/             # 工具模块
│   └── main.py            # 主程序
├── config/                # 配置文件
├── tests/                 # 测试用例
├── docs/                  # 文档
└── output/                # 输出目录
```

## 添加新书源

### 1. 创建书源目录

```bash
mkdir src/sources/your_source
cd src/sources/your_source
```

### 2. 创建配置文件

创建 `config.json`：

```json
{
  "bookSourceName": "你的书源名称",
  "bookSourceUrl": "https://example.com",
  "bookSourceType": 0,
  "bookSourceGroup": "分组名称",
  "bookSourceComment": "书源描述",
  "enabled": true,
  
  "searchUrl": "/search?q={{key}}",
  
  "ruleSearch": {
    "bookList": ".book-list .book-item",
    "name": ".title@text",
    "author": ".author@text",
    "bookUrl": ".title@href",
    "coverUrl": ".cover@src",
    "intro": ".intro@text"
  },
  
  "ruleBookInfo": {
    "name": ".book-title@text",
    "author": ".book-author@text",
    "intro": ".book-intro@text",
    "tocUrl": ".toc-link@href"
  },
  
  "ruleToc": {
    "chapterList": ".chapter-list .chapter",
    "chapterName": ".chapter-title@text",
    "chapterUrl": ".chapter-title@href"
  },
  
  "ruleContent": {
    "content": ".chapter-content@text",
    "title": ".chapter-title@text"
  }
}
```

### 3. 实现书源类

创建 `source.py`：

```python
from typing import List
from ...core.engine import BaseSource, BookInfo, ChapterInfo, ContentInfo

class YourSource(BaseSource):
    """你的书源实现"""
    
    def __init__(self, config):
        super().__init__(config)
        self.base_url = "https://example.com"
    
    async def search(self, keyword: str, page: int = 1) -> List[BookInfo]:
        """搜索书籍"""
        # 实现搜索逻辑
        pass
    
    async def get_book_info(self, book_url: str) -> BookInfo:
        """获取书籍详情"""
        # 实现书籍详情获取逻辑
        pass
    
    async def get_toc(self, toc_url: str) -> List[ChapterInfo]:
        """获取目录"""
        # 实现目录获取逻辑
        pass
    
    async def get_content(self, chapter_url: str) -> ContentInfo:
        """获取正文内容"""
        # 实现正文获取逻辑
        pass
```

### 4. 创建初始化文件

创建 `__init__.py`：

```python
from .source import YourSource

__all__ = ["YourSource"]
```

### 5. 编写测试

在 `tests/` 目录下创建测试文件：

```python
import pytest
from src.sources.your_source.source import YourSource

class TestYourSource:
    def setup_method(self):
        self.config = {...}  # 测试配置
        self.source = YourSource(self.config)
    
    @pytest.mark.asyncio
    async def test_search(self):
        results = await self.source.search("测试")
        assert len(results) > 0
```

## 规则语法说明

### CSS选择器

```
.class-name@text          # 获取文本内容
.class-name@attr(href)     # 获取属性值
#id-name@html             # 获取HTML内容
tag.class@src             # 获取src属性
```

### XPath表达式

```
//div[@class='title']/text()    # 获取文本
//a/@href                       # 获取链接
//img/@src                      # 获取图片地址
```

### 正则表达式

```
##pattern                       # 匹配模式
##pattern##replacement          # 替换模式
```

### JSON路径

```
$.data.books[*].name            # 获取所有书名
$.result.chapters[0].url        # 获取第一章链接
```

### JavaScript脚本

```html
<js>
// 可以使用result变量（当前内容）
// 可以使用baseUrl变量（基础URL）
result = result.replace(/\n/g, '\n\n');
return result;
</js>
```

## 调试技巧

### 1. 启用调试模式

在 `config/settings.json` 中设置：

```json
{
  "debug": {
    "enable_debug": true,
    "save_requests": true,
    "save_responses": true,
    "verbose_logging": true
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### 2. 使用测试命令

```bash
# 测试特定书源
python src/main.py --test your_source --keyword "测试关键词"

# 生成单个书源
python src/main.py --generate your_source

# 查看详细日志
python src/main.py --test your_source --log-level DEBUG
```

### 3. 检查网络请求

调试模式下，请求和响应会保存在 `data/debug/` 目录中。

### 4. 验证规则

可以使用在线工具验证规则：
- CSS选择器：浏览器开发者工具
- XPath：浏览器控制台 `$x("xpath")`
- 正则表达式：regex101.com
- JSON路径：jsonpath.com

## 代码规范

### 1. 代码格式化

使用 black 进行代码格式化：

```bash
black src/ tests/
```

### 2. 代码检查

使用 flake8 进行代码检查：

```bash
flake8 src/ tests/
```

### 3. 类型检查

使用 mypy 进行类型检查：

```bash
mypy src/
```

### 4. 测试覆盖率

```bash
pytest --cov=src tests/
```

## 性能优化

### 1. 网络请求优化

- 使用连接池
- 设置合理的超时时间
- 实现请求重试机制
- 添加请求间隔避免被封

### 2. 缓存策略

- 缓存搜索结果
- 缓存书籍详情
- 缓存目录信息
- 设置合理的过期时间

### 3. 并发控制

- 限制并发请求数量
- 使用信号量控制并发
- 避免过于频繁的请求

## 错误处理

### 1. 网络错误

```python
try:
    response = await self.network.get(url)
except Exception as e:
    self.logger.error(f"网络请求失败: {e}")
    return []
```

### 2. 解析错误

```python
try:
    data = self.rules.parse_rule(rule, content)
except Exception as e:
    self.logger.error(f"规则解析失败: {e}")
    return ""
```

### 3. 数据验证

```python
from ...utils.validator import Validator

if not Validator.is_valid_url(book_url):
    self.logger.warning(f"无效的URL: {book_url}")
    return BookInfo()
```

## 贡献指南

### 1. 提交代码

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

### 2. 提交规范

使用约定式提交格式：

```
feat: 添加新书源支持
fix: 修复搜索结果解析错误
docs: 更新开发文档
test: 添加单元测试
refactor: 重构网络请求模块
```

### 3. 代码审查

- 确保所有测试通过
- 遵循代码规范
- 添加必要的文档
- 考虑向后兼容性

## 常见问题

### Q: 如何处理反爬虫？

A: 
- 设置合理的请求头
- 添加随机延迟
- 使用代理池
- 模拟真实浏览器行为

### Q: 如何处理动态内容？

A: 
- 分析网站的API接口
- 使用JavaScript规则
- 考虑使用无头浏览器

### Q: 如何提高解析准确性？

A: 
- 使用多个备选规则
- 添加数据验证
- 处理异常情况
- 定期测试和更新

## 联系方式

- 项目主页：https://github.com/your-username/independent-book-source
- 问题反馈：https://github.com/your-username/independent-book-source/issues
- 讨论交流：[Telegram群组](https://t.me/your-group)
