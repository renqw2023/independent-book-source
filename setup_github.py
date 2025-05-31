#!/usr/bin/env python3
"""
GitHub设置脚本 - GitHub Setup Script

帮助用户快速配置GitHub相关设置
"""

import os
import re
import sys
from pathlib import Path


def get_github_username():
    """获取GitHub用户名"""
    print("🔧 GitHub设置向导")
    print("=" * 50)
    
    username = input("请输入您的GitHub用户名: ").strip()
    
    if not username:
        print("❌ 用户名不能为空")
        return None
    
    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', username):
        print("❌ 用户名格式不正确")
        return None
    
    return username


def update_files(username):
    """更新文件中的用户名占位符"""
    files_to_update = [
        ".github/workflows/pages.yml",
        "README.md",
        "docs/DEPLOYMENT.md"
    ]
    
    replacements = {
        "your-username": username,
        "YOUR_USERNAME": username
    }
    
    updated_files = []
    
    for file_path in files_to_update:
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(file_path)
                print(f"✅ 已更新: {file_path}")
            else:
                print(f"ℹ️  无需更新: {file_path}")
                
        except Exception as e:
            print(f"❌ 更新失败 {file_path}: {e}")
    
    return updated_files


def generate_git_commands(username):
    """生成Git命令"""
    commands = f"""
📋 Git命令（复制并在命令行中执行）:

# 1. 初始化Git仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交代码
git commit -m "🎉 初始提交：独立书源系统 - 大灰狼融合书源独立版"

# 4. 添加远程仓库
git remote add origin https://github.com/{username}/independent-book-source.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main

📝 注意事项:
1. 请先在GitHub上创建名为 'independent-book-source' 的公开仓库
2. 不要勾选 "Add a README file"（我们已经有了）
3. 执行命令前请确保已安装Git

🔗 创建仓库链接:
https://github.com/new?name=independent-book-source&description=独立书源系统+-+大灰狼融合书源独立版&visibility=public
"""
    return commands


def generate_urls(username):
    """生成最终的访问链接"""
    urls = f"""
🎉 部署完成后，您将获得以下链接:

🌐 项目网站:
https://{username}.github.io/independent-book-source/

📚 legado导入链接（全部书源）:
https://{username}.github.io/independent-book-source/sources/legado_sources.json

🔄 legado订阅链接（自动更新）:
https://{username}.github.io/independent-book-source/sources/subscription.json

🍅 番茄小说单独链接:
https://{username}.github.io/independent-book-source/sources/individual/fanqie.json

📖 GitHub仓库:
https://github.com/{username}/independent-book-source

📋 使用方法:
1. 复制上面的书源链接
2. 打开legado阅读软件
3. 进入"书源管理" → "网络导入"
4. 粘贴链接并导入
"""
    return urls


def check_reference_dirs():
    """检查并提示参考目录"""
    reference_dirs = ["legado-master", "shuyuan-shuyuan"]
    found_dirs = []

    for dir_name in reference_dirs:
        if os.path.exists(dir_name):
            found_dirs.append(dir_name)

    if found_dirs:
        print(f"📁 发现参考目录: {', '.join(found_dirs)}")
        print("ℹ️  这些目录已在.gitignore中排除，不会上传到GitHub")
        print("💡 如果您想删除这些目录以节省空间，可以安全删除")

        choice = input("\n是否要删除这些参考目录？(y/n): ").lower().strip()
        if choice in ['y', 'yes', '是']:
            import shutil
            for dir_name in found_dirs:
                try:
                    shutil.rmtree(dir_name)
                    print(f"✅ 已删除: {dir_name}")
                except Exception as e:
                    print(f"❌ 删除失败 {dir_name}: {e}")
        else:
            print("✅ 保留参考目录（不会上传到GitHub）")

    return found_dirs


def main():
    """主函数"""
    print("🚀 独立书源系统 - GitHub部署设置")
    print("=" * 60)

    # 检查是否在正确的目录
    if not os.path.exists("src/main.py"):
        print("❌ 请在项目根目录（包含src文件夹的目录）中运行此脚本")
        return

    # 检查参考目录
    check_reference_dirs()
    
    # 获取用户名
    username = get_github_username()
    if not username:
        return
    
    print(f"\n✅ GitHub用户名: {username}")
    
    # 更新文件
    print(f"\n📝 更新配置文件...")
    updated_files = update_files(username)
    
    if updated_files:
        print(f"\n✅ 已更新 {len(updated_files)} 个文件")
    
    # 生成Git命令
    print(generate_git_commands(username))
    
    # 生成访问链接
    print(generate_urls(username))
    
    # 保存信息到文件
    info_file = "GITHUB_INFO.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"GitHub用户名: {username}\n")
        f.write(f"仓库地址: https://github.com/{username}/independent-book-source\n")
        f.write(f"网站地址: https://{username}.github.io/independent-book-source/\n")
        f.write(f"书源链接: https://{username}.github.io/independent-book-source/sources/legado_sources.json\n")
        f.write(f"订阅链接: https://{username}.github.io/independent-book-source/sources/subscription.json\n")
    
    print(f"\n💾 信息已保存到: {info_file}")
    print("\n🎯 下一步:")
    print("1. 在GitHub上创建仓库")
    print("2. 执行上面的Git命令")
    print("3. 等待GitHub Actions自动部署")
    print("4. 使用生成的链接导入legado")


if __name__ == "__main__":
    main()
