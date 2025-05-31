# GitHub部署指南 - Deployment Guide

## 📤 上传到GitHub并实现链接导入

### 1. 创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com
   - 登录您的账户

2. **创建新仓库**
   - 点击右上角的 "+" 按钮
   - 选择 "New repository"
   - 仓库名称：`independent-book-source`
   - 描述：`独立书源系统 - 大灰狼融合书源独立版`
   - 设置为 Public（公开）
   - 勾选 "Add a README file"
   - 点击 "Create repository"

### 2. 上传项目代码

#### 方式1：使用Git命令行

```bash
# 在项目目录中初始化Git
cd d:\shuyuan
git init

# 添加远程仓库（替换为您的用户名）
git remote add origin https://github.com/renqw2023/independent-book-source.git

# 添加所有文件
git add .

# 提交代码
git commit -m "🎉 初始提交：独立书源系统"

# 推送到GitHub
git push -u origin main
```

#### 方式2：使用GitHub Desktop

1. 下载并安装 GitHub Desktop
2. 登录您的GitHub账户
3. 选择 "Add an Existing Repository from your Hard Drive"
4. 选择项目目录 `d:\shuyuan`
5. 发布到GitHub

#### 方式3：直接上传文件

1. 在GitHub仓库页面点击 "uploading an existing file"
2. 将项目文件拖拽到页面中
3. 填写提交信息
4. 点击 "Commit changes"

### 3. 配置GitHub Actions

上传代码后，GitHub Actions会自动运行：

1. **自动生成书源文件**
   - 每次代码更新时自动运行
   - 每天凌晨2点自动更新
   - 生成的文件会自动提交到仓库

2. **部署GitHub Pages**
   - 自动创建网站页面
   - 提供友好的导入界面

### 4. 启用GitHub Pages

1. 进入仓库设置页面
2. 滚动到 "Pages" 部分
3. Source 选择 "GitHub Actions"
4. 保存设置

等待几分钟后，您的网站将在以下地址可用：
```
https://renqw2023.github.io/independent-book-source/
```

### 5. 获取书源链接

部署完成后，您将获得以下链接：

#### 📚 全部书源（推荐）
```
https://renqw2023.github.io/independent-book-source/sources/legado_sources.json
```

#### 🍅 单独书源
```
https://renqw2023.github.io/independent-book-source/sources/individual/fanqie.json
```

#### 📋 订阅链接
```
https://renqw2023.github.io/independent-book-source/sources/subscription.json
```

### 6. 在legado中导入

#### 方式1：直接链接导入
1. 打开legado阅读软件
2. 进入 "我的" → "书源管理"
3. 点击右上角 "+" → "网络导入"
4. 粘贴书源链接
5. 点击确定导入

#### 方式2：订阅导入
1. 在legado中进入 "我的" → "订阅"
2. 点击 "+" 添加订阅
3. 粘贴订阅链接
4. 设置自动更新

### 7. 自定义配置

#### 修改GitHub Actions配置

编辑 `.github/workflows/generate-sources.yml`：

```yaml
# 修改自动运行时间
schedule:
  - cron: '0 2 * * *'  # 每天凌晨2点

# 修改Python版本
python-version: '3.9'
```

#### 修改网站配置

编辑 `.github/workflows/pages.yml` 中的网站内容。

#### 修改订阅链接

在 `src/subscription.py` 中修改 `base_url`：

```python
# 替换为您的实际GitHub Pages地址
base_url = "https://renqw2023.github.io/independent-book-source/sources"
```

### 8. 高级功能

#### 自定义域名

1. 在仓库根目录创建 `CNAME` 文件
2. 写入您的域名，如：`booksource.yourdomain.com`
3. 在域名DNS设置中添加CNAME记录指向 `renqw2023.github.io`

#### CDN加速

使用jsDelivr CDN加速访问：
```
https://cdn.jsdelivr.net/gh/renqw2023/independent-book-source@main/output/legado_sources.json
```

#### 多分支部署

- `main` 分支：稳定版本
- `dev` 分支：开发版本
- `beta` 分支：测试版本

### 9. 维护和更新

#### 添加新书源

1. 在 `src/sources/` 下添加新书源
2. 提交代码到GitHub
3. GitHub Actions自动生成新的书源文件

#### 监控运行状态

1. 查看 Actions 页面了解运行状态
2. 查看 Issues 了解用户反馈
3. 定期检查书源可用性

#### 版本发布

GitHub Actions会自动创建Release：
- 包含生成的书源文件
- 自动标记版本号
- 提供下载链接

### 10. 故障排除

#### Actions运行失败

1. 检查 Actions 页面的错误日志
2. 常见问题：
   - 依赖包安装失败
   - 网络请求超时
   - 权限问题

#### 书源导入失败

1. 检查链接是否正确
2. 确认GitHub Pages已启用
3. 验证JSON格式是否正确

#### 网站无法访问

1. 确认GitHub Pages设置正确
2. 等待DNS传播（可能需要几分钟）
3. 检查CNAME文件配置

### 11. 最佳实践

1. **定期更新**：保持书源规则最新
2. **监控可用性**：定期测试书源功能
3. **用户反馈**：及时处理Issues和PR
4. **文档维护**：保持README和文档更新
5. **安全考虑**：不要在代码中包含敏感信息

### 12. 示例链接

假设您的GitHub用户名是 `bookworm`，那么：

- 仓库地址：`https://github.com/bookworm/independent-book-source`
- 网站地址：`https://bookworm.github.io/independent-book-source/`
- 书源链接：`https://bookworm.github.io/independent-book-source/sources/legado_sources.json`
- 订阅链接：`https://bookworm.github.io/independent-book-source/sources/subscription.json`

---

🎉 **恭喜！** 现在您的书源系统已经部署到GitHub，用户可以通过链接直接导入到legado中使用了！
