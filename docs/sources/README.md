# 书源索引

本项目提供多种类型的书源，满足不同用户的阅读需求。

## 📚 书源分类

### 🆓 免费书源
- **番茄小说** - 字节跳动旗下免费小说平台
- **笔趣阁** - 经典免费小说网站
- **起点中文** - 知名网络文学平台

### 🔥 热门平台
- **七猫小说** - 热门免费阅读平台
- **得间小说** - 优质小说资源
- **塔读文学** - 丰富的小说库

### 📖 专业平台
- **QQ阅读** - 腾讯旗下阅读平台
- **小米阅读** - 小米生态阅读应用
- **熊猫看书** - 专业阅读软件

### 🌟 精品书源
- **XIU2精品书源** - 经过测试的优质书源合集
- **关耳女频书源** - 专注女性向小说的精品书源
- **晋江文学城** - 知名原创文学网站

## 📋 书源列表

### 主要书源文件
- [`fanqie_novel.json`](./fanqie_novel.json) - 🍅 **番茄小说专版**（推荐）- 基于真实API的稳定书源
- [`comprehensive_sources.json`](./comprehensive_sources.json) - 综合书源合集（包含番茄小说+其他平台）
- [`premium_sources.json`](./premium_sources.json) - 精品书源合集（5个优质书源）
- [`jjwxc_sources.json`](./jjwxc_sources.json) - 晋江文学城书源（2个专业书源）
- [`legado_sources.json`](./legado_sources.json) - 基础阅读APP兼容书源
- [`simple_fanqie.json`](./simple_fanqie.json) - 简化版番茄书源（测试用）

### 🔥 热门书源合集
- **破冰书源** - 128个优质书源（已整合到comprehensive_sources.json）
- **shidahuilang书源** - 110个优质书源（已整合到comprehensive_sources.json）
- **酷安@三舞313书源** - 1554个书源超大合集（已整合到comprehensive_sources.json）
- **XIU2精品书源** - 31个精选书源（已整合到premium_sources.json）
- **关耳女频书源** - 86个女性向书源（已整合到premium_sources.json）

### 精品书源详情

#### 🍅 番茄小说专版（强烈推荐）
**基于真实API接口的稳定书源，完全免费无限制**

**✨ 核心特色：**
- ✅ **完全免费** - 所有小说均可免费阅读，无VIP限制
- ✅ **API稳定** - 基于番茄小说真实API接口，稳定性极高
- ✅ **实时更新** - 支持最新章节实时获取，更新及时
- ✅ **分类丰富** - 支持9大分类：玄幻、武侠、都市、科幻、历史、游戏、女频等
- ✅ **搜索强大** - 支持书名、作者等多维度搜索
- ✅ **无广告** - 纯净阅读体验，无任何广告干扰

**📱 导入地址：**
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/fanqie_novel.json
```

**🔧 技术优势：**
- 使用JSONPath解析，兼容性强
- 支持JavaScript脚本处理，功能强大
- 自动处理字数显示和状态识别
- 完整的错误处理和重试机制

#### 🏆 XIU2精品书源
包含经过严格测试的优质书源：
- **起点中文** - 正版小说平台，需要Cookie验证
- **阅友小说** - 稳定的免费小说源
- **就爱文学** - 丰富的小说资源
- **猴子阅读** - API接口稳定
- **书香之家** - 多备用域名保障

#### 🌸 晋江文学城书源
专业的原创文学平台：
- **坚果云** - 支持云端书籍存储
- **晋江文学** - 原创耽美、百合小说平台
- 支持登录、收藏、评论等功能
- 完整的VIP章节购买支持

## 🚀 使用方法

### 方法一：直接导入
1. 复制书源链接
2. 在阅读APP中选择"网络导入"
3. 粘贴链接并导入

### 方法二：本地导入
1. 下载对应的JSON文件
2. 在阅读APP中选择"本地导入"
3. 选择下载的文件

### 方法三：GitHub链接导入
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/premium_sources.json
```

## 📊 书源状态

| 书源名称 | 状态 | 更新时间 | 说明 |
|---------|------|----------|------|
| 🍅番茄小说 | ✅ 正常 | 2025-01-31 | **推荐** - 完全免费，API稳定 |
| 起点中文 | ✅ 正常 | 2024-01-01 | 需Cookie验证 |
| 阅友小说 | ✅ 正常 | 2024-01-01 | 完全免费 |
| 就爱文学 | ✅ 正常 | 2024-01-01 | 资源丰富 |
| 猴子阅读 | ✅ 正常 | 2024-01-01 | API稳定 |
| 书香之家 | ✅ 正常 | 2024-01-01 | 多备用域名 |
| 晋江文学 | ✅ 正常 | 2024-01-01 | 需登录 |
| 笔趣阁 | ✅ 正常 | 2024-01-01 | 经典稳定 |

## ⚠️ 使用说明

1. **免责声明**：本项目仅供学习交流使用，请支持正版阅读
2. **更新频率**：书源会定期更新，建议关注项目动态
3. **问题反馈**：如遇问题请在Issues中反馈
4. **登录说明**：部分书源需要登录才能使用完整功能
5. **Cookie设置**：某些书源需要先访问网站获取Cookie

## 🔗 相关链接

- [项目主页](../../README.md)
- [使用指南](../USAGE.md)
- [精品书源报告](../PREMIUM_SOURCES.md)
- [开发指南](../DEVELOPMENT.md)

## 📥 快速导入链接

### 🍅 番茄小说专版（强烈推荐）
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/fanqie_novel.json
```

### 📚 综合书源合集（包含番茄小说）
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/comprehensive_sources.json
```

### 🏆 精品书源合集
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/premium_sources.json
```

### 🏷 晋江文学城
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/jjwxc_sources.json
```

### 📖 基础书源
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/legado_sources.json
```
