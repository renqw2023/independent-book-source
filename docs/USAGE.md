# 使用指南

## 📚 书源导入方法

### 方法一：直接链接导入（推荐）

1. 打开legado阅读APP
2. 点击右下角"我的"
3. 选择"书源管理"
4. 点击右上角"+"号
5. 选择"网络导入"
6. 粘贴以下链接之一：

#### 🌟 精品书源合集（推荐）
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/premium_sources.json
```
**包含内容：**
- 起点中文网（需Cookie验证）
- 阅友小说（免费稳定）
- 就爱文学（资源丰富）
- 猴子阅读（API稳定）
- 书香之家（多备用域名）

#### 🌸 晋江文学城书源
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/jjwxc_sources.json
```
**包含内容：**
- 晋江文学城（原创小说平台）
- 坚果云（云端书籍存储）
- 支持登录、收藏、VIP购买

#### 🍅 番茄小说合集
```
https://raw.githubusercontent.com/renqw2023/independent-book-source/main/docs/sources/fanqie_collection.json
```
**包含内容：**
- 番茄小说官方API
- 多种解析规则
- 完全免费阅读

### 方法二：本地文件导入

1. 下载对应的JSON文件到手机
2. 在legado中选择"本地导入"
3. 选择下载的文件

## 🔧 书源配置说明

### 起点中文网配置

**重要提示：** 起点中文网需要Cookie验证才能正常搜索

**配置步骤：**
1. 导入起点书源后
2. 使用legado内置浏览器访问 `https://www.qidian.com`
3. 随便浏览一下网页（无需登录）
4. 返回书源，此时搜索功能已可正常使用

**验证方法：**
- 搜索"斗罗大陆"或其他热门小说
- 如果能正常显示结果，说明配置成功

### 晋江文学城配置

**登录说明：** 晋江文学城支持登录功能，登录后可使用更多功能

**配置步骤：**
1. 导入晋江书源
2. 在legado中访问 `https://m.jjwxc.net/`
3. 登录你的晋江账号
4. 返回书源即可使用收藏、VIP购买等功能

**特殊功能：**
- 我的收藏：显示你的收藏书籍
- 今日限免：显示限免书籍
- 自动购买：支持VIP章节自动购买
- 评论显示：可在正文显示读者评论

### 猴子阅读配置

**特点：** 使用API接口，稳定性好，支持内容解密

**无需特殊配置**，导入即可使用

### 书香之家配置

**特点：** 多个备用域名，保障访问稳定性

**备用域名：**
- https://s.pjxhmy.com
- https://s.klzdp.com
- https://s.mocaiys.com
- https://s.fjwhcbsh.com
- https://s.hngxt.cn

## 📖 使用技巧

### 搜索技巧

1. **精确搜索**：使用完整书名搜索
2. **作者搜索**：在晋江等支持作者搜索的书源中使用
3. **关键词搜索**：使用书籍关键词或标签

### 晋江文学城特殊搜索

- 在关键词前加 `##` 可使用手机版搜索（更准确）
- 例如：`##完整书名`

### 书源变量设置

#### 晋江文学城变量
在书籍详情页可设置以下变量：

**书籍变量（单本书）：**
- `去章节序号` - 去除章节前面的序号
- `目录简介` - 在目录显示章节简介
- `开启购买` - 开启自动购买下五章
- `关闭购买` - 关闭自动购买
- `评论5` - 在正文显示5条评论（数字可调整）

**书源变量（全局）：**
- `去章节序号` - 全局去除章节序号
- `目录简介` - 全局显示章节简介
- `评论5` - 全局显示评论

## ⚠️ 注意事项

### 网络问题
1. **访问失败**：可能是网络问题，稍后重试
2. **加载缓慢**：某些书源服务器在海外，访问可能较慢
3. **域名失效**：如遇域名失效，可尝试备用域名

### 版权问题
1. **支持正版**：建议支持正版阅读
2. **学习用途**：本项目仅供学习交流使用
3. **商业使用**：请勿用于商业用途

### 功能限制
1. **VIP章节**：部分书源的VIP章节需要登录或付费
2. **更新频率**：免费书源的更新可能不如官方及时
3. **稳定性**：免费书源可能存在不稳定情况

## 🔄 更新说明

### 自动更新
- 书源会定期更新规则
- 建议定期重新导入最新版本

### 手动更新
1. 删除旧书源
2. 重新导入新链接
3. 重新配置相关设置

## 🆘 常见问题

### Q: 搜索不到书籍怎么办？
A: 
1. 检查网络连接
2. 尝试不同的搜索关键词
3. 检查书源是否需要特殊配置（如Cookie）
4. 尝试其他书源

### Q: 章节加载失败怎么办？
A:
1. 刷新重试
2. 检查网络连接
3. 尝试切换到其他书源
4. 检查是否为VIP章节

### Q: 起点中文网搜索失败？
A:
1. 使用legado内置浏览器访问起点网站
2. 随便浏览一下获取Cookie
3. 返回重新搜索

### Q: 晋江文学城无法使用收藏功能？
A:
1. 需要先登录晋江账号
2. 在legado内置浏览器中登录
3. 登录后即可使用收藏等功能

## 📞 技术支持

如遇问题，请：
1. 查看本使用指南
2. 在GitHub Issues中搜索相关问题
3. 提交新的Issue描述问题
4. 提供详细的错误信息和操作步骤
