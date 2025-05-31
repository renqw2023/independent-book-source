# 独立书源系统 - 融合书源独立版

## 项目简介

本项目是一个完全独立的书源解析系统，专为legado阅读软件开发。旨在替代需要付费登录的第三方书源服务，提供免费、稳定、高效的多平台小说资源聚合服务。

## 支持平台

### 🌟 精品书源（已完成）
- ⭐ **起点中文网** - 网络文学领军平台，需Cookie验证
- 📚 **阅友小说** - 稳定的免费小说源
- 📖 **就爱文学** - 丰富的小说资源库
- 🐒 **猴子阅读** - API接口稳定，解密支持
- 🏠 **书香之家** - 多备用域名保障
- 🌸 **晋江文学城** - 原创耽美、百合小说平台
- ☁️ **坚果云** - 支持云端书籍存储

### 🆓 免费平台
- 🍅 **番茄小说** - 免费热门网络小说
- 🐱 **七猫小说** - 海量免费小说资源
- 📖 **得间小说** - 精品小说推荐
- 🏗️ **塔读小说** - 多元化阅读体验

### 🔥 热门平台
- 💬 **QQ阅读** - 腾讯官方阅读平台
- 📱 **小米阅读** - 小米生态阅读应用
- 🐼 **熊猫看书** - 优质小说聚合
- 🎧 **喜马拉雅** - 有声读物资源

## 核心特性

- ✅ **完全免费** - 无需付费，无需登录
- ✅ **独立部署** - 数据存储在本地，不依赖第三方服务器
- ✅ **高度兼容** - 完全兼容legado阅读软件书源格式
- ✅ **智能解析** - 支持多种解析规则，自动适配网站变化
- ✅ **反爬虫优化** - 内置多种反爬虫策略，确保稳定访问
- ✅ **实时更新** - 支持书源规则动态更新
- ✅ **多格式支持** - 支持文本、音频、图片等多种内容格式

## 技术架构

### 核心模块
- **书源管理器** - 统一管理多平台书源配置
- **网络请求引擎** - 高效的HTTP请求处理，支持代理和反爬虫
- **内容解析引擎** - 支持CSS选择器、XPath、正则表达式等多种解析方式
- **规则引擎** - 动态规则配置，支持JavaScript脚本扩展
- **缓存系统** - 智能缓存机制，提升访问速度
- **更新机制** - 自动检测和更新书源规则

### 开发语言与框架
- **后端**: Python 3.8+
- **解析库**: BeautifulSoup4, lxml, PyQuery
- **网络库**: requests, aiohttp
- **脚本引擎**: PyV8, js2py
- **数据存储**: SQLite, JSON
- **Web框架**: FastAPI (可选)

## 项目结构

```
independent-book-source/
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── __init__.py
│   │   ├── engine.py      # 解析引擎
│   │   ├── network.py     # 网络请求模块
│   │   ├── rules.py       # 规则引擎
│   │   └── cache.py       # 缓存系统
│   ├── sources/           # 书源实现
│   │   ├── __init__.py
│   │   ├── fanqie/        # 番茄小说
│   │   ├── qimao/         # 七猫小说
│   │   ├── dejian/        # 得间小说
│   │   ├── tadu/          # 塔读小说
│   │   ├── qq/            # QQ阅读
│   │   ├── xiaomi/        # 小米阅读
│   │   ├── panda/         # 熊猫看书
│   │   ├── qidian/        # 起点中文网
│   │   └── ximalaya/      # 喜马拉雅
│   ├── utils/             # 工具模块
│   │   ├── __init__.py
│   │   ├── parser.py      # 解析工具
│   │   ├── crypto.py      # 加密解密
│   │   └── validator.py   # 数据验证
│   └── main.py            # 主程序入口
├── config/                # 配置文件
│   ├── settings.json      # 全局配置
│   └── sources.json       # 书源配置
├── data/                  # 数据存储
│   ├── cache/             # 缓存文件
│   └── logs/              # 日志文件
├── output/                # 输出目录
│   ├── legado_sources.json # legado格式书源
│   └── individual/        # 单独书源文件
├── tests/                 # 测试用例
│   ├── test_core.py
│   └── test_sources.py
├── docs/                  # 文档
│   ├── API.md             # API文档
│   ├── DEVELOPMENT.md     # 开发指南
│   └── RULES.md           # 规则说明
├── requirements.txt       # Python依赖
├── setup.py              # 安装脚本
└── README.md             # 项目说明
```

## 快速开始

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. **下载项目**
```bash
# 如果有git
git clone https://github.com/renqw2023/independent-book-source.git
cd independent-book-source

# 或者直接下载ZIP文件并解压
```

2. **安装依赖**
```bash
# 安装基础依赖
pip install aiohttp beautifulsoup4 lxml requests jsonpath-ng

# 或安装完整依赖（可选）
pip install -r requirements.txt
```

3. **快速测试**
```bash
# 运行快速测试验证系统
python quick_test.py
```

4. **生成书源**
```bash
# 方式1：使用交互式界面
python run.py

# 方式2：直接生成所有书源
python src/main.py --generate-all

# 方式3：生成指定书源
python src/main.py --generate fanqie
```

5. **导入legado**
生成的书源文件位于 `output/legado_sources.json`，可直接导入legado阅读软件。

## 📤 GitHub部署（推荐）

### 一键部署到GitHub

1. **Fork或上传项目到GitHub**
2. **启用GitHub Actions和Pages**
3. **获得在线书源链接**

部署后您将获得：
- 🌐 **在线网站**：`https://renqw2023.github.io/independent-book-source/`
- 📚 **书源链接**：`https://renqw2023.github.io/independent-book-source/sources/legado_sources.json`
- 🔄 **自动更新**：每天自动更新书源文件

### legado导入方式

#### 🔥 综合书源合集（最全面，推荐）
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/comprehensive_sources.json
```
**包含超过1800个书源：**
- 破冰书源（128个优质书源）
- shidahuilang书源（110个优质书源）
- 酷安@三舞313书源（1554个书源超大合集）

#### 🌟 精品书源合集（精选推荐）
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/premium_sources.json
```

#### 🌸 晋江文学城书源
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/jjwxc_sources.json
```

#### 🍅 番茄小说合集
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/fanqie_collection.json
```

#### 📚 基础书源
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/legado_sources.json
```

#### 方式2：订阅导入（自动更新）
```
https://renqw2023.github.io/independent-book-source/sources/subscription.json
```

详细部署教程请参考：[GitHub部署指南](docs/DEPLOYMENT.md)

## 项目状态

### ✅ 已完成功能
- ✅ 核心框架搭建完成
- ✅ 书源引擎和管理系统
- ✅ 网络请求和缓存管理
- ✅ 规则解析引擎（支持CSS、XPath、正则、JSON路径）
- ✅ 番茄小说书源实现
- ✅ legado格式书源生成
- ✅ 完整的测试套件
- ✅ 交互式启动界面
- ✅ 详细的开发文档
- ✅ **精品书源合集** - 包含起点中文、阅友小说等优质书源
- ✅ **晋江文学城书源** - 支持登录、收藏、VIP章节购买
- ✅ **多平台书源** - 猴子阅读、书香之家等API书源
- ✅ **云端存储支持** - 坚果云等云端书籍管理
- ✅ **综合书源合集** - 整合超过1800个优质书源
- ✅ **破冰书源** - 128个经过验证的稳定书源
- ✅ **shidahuilang书源** - 110个API接口稳定的书源
- ✅ **酷安@三舞313书源** - 1554个社区维护的书源合集
- ✅ **XIU2精品书源** - 31个精选高质量书源
- ✅ **关耳女频书源** - 86个女性向小说专用书源

### 🚧 开发中功能
- 🚧 七猫小说书源
- 🚧 得间小说书源
- 🚧 塔读小说书源
- 🚧 QQ阅读书源
- 🚧 小米阅读书源
- 🚧 熊猫看书书源
- 🚧 喜马拉雅有声书源

### 📋 计划功能
- 📋 Web管理界面
- 📋 自动更新机制
- 📋 书源测试和监控
- 📋 更多网站支持

## 使用说明

### 生成书源
```bash
# 生成所有书源
python src/main.py --generate-all

# 生成特定书源
python src/main.py --generate fanqie qimao

# 测试书源
python src/main.py --test fanqie
```

### 配置说明
主要配置文件位于 `config/settings.json`：
```json
{
  "network": {
    "timeout": 30,
    "retry_times": 3,
    "user_agent": "Mozilla/5.0...",
    "proxy": null
  },
  "cache": {
    "enabled": true,
    "expire_time": 3600
  },
  "output": {
    "format": "legado",
    "merge_sources": true
  }
}
```

## 开发指南

### 添加新书源

1. 在 `src/sources/` 下创建新目录
2. 实现书源类，继承 `BaseSource`
3. 配置解析规则
4. 添加测试用例

详细开发指南请参考 [DEVELOPMENT.md](docs/DEVELOPMENT.md)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 免责声明

本项目仅供学习交流使用，请勿用于商业用途。使用本项目所产生的任何法律责任由使用者自行承担。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目主页: https://github.com/renqw2023/independent-book-source
- 问题反馈: https://github.com/renqw2023/independent-book-source/issues
- 讨论交流: [Telegram群组](https://t.me/your-group)

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
