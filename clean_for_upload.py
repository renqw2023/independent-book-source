#!/usr/bin/env python3
"""
上传前清理脚本 - Clean for Upload Script

清理不需要上传到GitHub的文件和目录
"""

import os
import shutil
import sys
from pathlib import Path


def get_project_size(path="."):
    """计算项目大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except (OSError, FileNotFoundError):
                pass
    return total_size


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def clean_reference_dirs():
    """清理参考目录和文件"""
    reference_items = [
        "legado-master",
        "shuyuan-shuyuan",
        "参考资料",
        "reference",
        "legado-master.zip",
        "shuyuan-shuyuan.zip",
        "shuyuan01",
        "需求.txt"
    ]
    
    cleaned_dirs = []
    saved_size = 0
    
    for item_name in reference_items:
        if os.path.exists(item_name):
            try:
                if os.path.isdir(item_name):
                    # 计算目录大小
                    item_size = get_project_size(item_name)
                    # 删除目录
                    shutil.rmtree(item_name)
                    print(f"✅ 已删除目录: {item_name} ({format_size(item_size)})")
                else:
                    # 计算文件大小
                    item_size = os.path.getsize(item_name)
                    # 删除文件
                    os.remove(item_name)
                    print(f"✅ 已删除文件: {item_name} ({format_size(item_size)})")

                cleaned_dirs.append(item_name)
                saved_size += item_size

            except Exception as e:
                print(f"❌ 删除失败 {item_name}: {e}")
    
    return cleaned_dirs, saved_size


def clean_cache_dirs():
    """清理缓存目录"""
    cache_dirs = [
        "data/cache",
        "data/logs",
        "data/debug",
        "data/temp",
        "__pycache__",
        ".pytest_cache"
    ]
    
    cleaned_dirs = []
    saved_size = 0
    
    for dir_name in cache_dirs:
        if os.path.exists(dir_name):
            try:
                # 计算目录大小
                dir_size = get_project_size(dir_name)
                
                # 删除目录
                shutil.rmtree(dir_name)
                
                cleaned_dirs.append(dir_name)
                saved_size += dir_size
                print(f"✅ 已清理缓存: {dir_name} ({format_size(dir_size)})")
                
            except Exception as e:
                print(f"❌ 清理失败 {dir_name}: {e}")
    
    return cleaned_dirs, saved_size


def clean_temp_files():
    """清理临时文件"""
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.bak",
        "*.swp",
        "*.swo",
        "*~",
        ".DS_Store",
        "Thumbs.db"
    ]
    
    import glob
    
    cleaned_files = []
    saved_size = 0
    
    for pattern in temp_patterns:
        for file_path in glob.glob(pattern, recursive=True):
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                
                cleaned_files.append(file_path)
                saved_size += file_size
                print(f"✅ 已删除临时文件: {file_path}")
                
            except Exception as e:
                print(f"❌ 删除失败 {file_path}: {e}")
    
    return cleaned_files, saved_size


def show_final_structure():
    """显示最终的项目结构"""
    print("\n📁 最终项目结构:")
    print("=" * 50)
    
    important_items = [
        "src/",
        "config/",
        "tests/",
        "docs/",
        ".github/",
        "README.md",
        "requirements.txt",
        "setup.py",
        "LICENSE",
        ".gitignore"
    ]
    
    for item in important_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                print(f"📂 {item}")
            else:
                print(f"📄 {item}")
        else:
            print(f"❌ {item} (缺失)")


def main():
    """主函数"""
    print("🧹 上传前清理脚本")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists("src/main.py"):
        print("❌ 请在项目根目录（包含src文件夹的目录）中运行此脚本")
        return
    
    # 计算清理前的项目大小
    original_size = get_project_size()
    print(f"📊 清理前项目大小: {format_size(original_size)}")
    
    total_saved = 0
    
    # 清理参考目录
    print(f"\n📁 清理参考目录...")
    ref_dirs, ref_size = clean_reference_dirs()
    total_saved += ref_size
    
    if ref_dirs:
        print(f"✅ 已清理 {len(ref_dirs)} 个参考目录")
    else:
        print("ℹ️  没有发现参考目录")
    
    # 清理缓存目录
    print(f"\n🗂️ 清理缓存目录...")
    cache_dirs, cache_size = clean_cache_dirs()
    total_saved += cache_size
    
    if cache_dirs:
        print(f"✅ 已清理 {len(cache_dirs)} 个缓存目录")
    else:
        print("ℹ️  没有发现缓存目录")
    
    # 清理临时文件
    print(f"\n🗑️ 清理临时文件...")
    temp_files, temp_size = clean_temp_files()
    total_saved += temp_size
    
    if temp_files:
        print(f"✅ 已清理 {len(temp_files)} 个临时文件")
    else:
        print("ℹ️  没有发现临时文件")
    
    # 计算清理后的项目大小
    final_size = get_project_size()
    
    # 显示清理结果
    print(f"\n📊 清理结果:")
    print(f"   清理前大小: {format_size(original_size)}")
    print(f"   清理后大小: {format_size(final_size)}")
    print(f"   节省空间: {format_size(total_saved)}")
    print(f"   压缩比例: {(total_saved/original_size*100):.1f}%")
    
    # 显示最终结构
    show_final_structure()
    
    print(f"\n🎉 清理完成！项目已准备好上传到GitHub")
    print(f"💡 接下来运行: python setup_github.py")


if __name__ == "__main__":
    main()
