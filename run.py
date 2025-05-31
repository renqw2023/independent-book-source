#!/usr/bin/env python3
"""
独立书源系统启动脚本 - Startup Script
Independent Book Source System Launcher

快速启动和测试书源系统的便捷脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"   当前版本: {sys.version}")
        return False
    
    print(f"✅ Python版本检查通过: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """检查依赖包"""
    required_packages = [
        "aiohttp",
        "beautifulsoup4", 
        "lxml",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n📦 需要安装以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        
        install = input("\n是否现在安装依赖包? (y/n): ").lower().strip()
        if install in ['y', 'yes', '是']:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "-r", "requirements.txt"
                ])
                print("✅ 依赖包安装完成")
                return True
            except subprocess.CalledProcessError:
                print("❌ 依赖包安装失败")
                return False
        else:
            return False
    
    return True


def create_directories():
    """创建必要的目录"""
    directories = [
        "data/cache",
        "data/logs", 
        "output/individual",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {directory}")


def show_menu():
    """显示主菜单"""
    print("\n" + "="*60)
    print("🍅 独立书源系统 - 大灰狼融合书源独立版")
    print("="*60)
    print("1. 生成所有书源")
    print("2. 生成指定书源")
    print("3. 测试书源")
    print("4. 列出可用书源")
    print("5. 查看统计信息")
    print("6. 运行测试用例")
    print("7. 清理缓存")
    print("8. 查看帮助")
    print("0. 退出")
    print("="*60)


def run_command(cmd_args):
    """运行命令"""
    try:
        cmd = [sys.executable, "src/main.py"] + cmd_args
        print(f"🚀 执行命令: {' '.join(cmd)}")
        print("-" * 60)
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("-" * 60)
        if result.returncode == 0:
            print("✅ 命令执行成功")
        else:
            print(f"❌ 命令执行失败 (退出码: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 命令执行异常: {e}")
        return False


def generate_all_sources():
    """生成所有书源"""
    print("\n📚 开始生成所有书源...")
    return run_command(["--generate-all"])


def generate_specific_sources():
    """生成指定书源"""
    print("\n可用的书源:")
    print("- fanqie (番茄小说)")
    print("- qimao (七猫小说)")
    print("- dejian (得间小说)")
    print("- tadu (塔读小说)")
    print("- qq (QQ阅读)")
    print("- xiaomi (小米阅读)")
    print("- panda (熊猫看书)")
    print("- qidian (起点中文网)")
    print("- ximalaya (喜马拉雅)")
    
    sources = input("\n请输入要生成的书源名称 (用空格分隔): ").strip().split()
    
    if not sources:
        print("❌ 未输入书源名称")
        return False
    
    print(f"\n📚 开始生成指定书源: {', '.join(sources)}")
    return run_command(["--generate"] + sources)


def test_source():
    """测试书源"""
    source_name = input("\n请输入要测试的书源名称: ").strip()
    if not source_name:
        print("❌ 未输入书源名称")
        return False
    
    keyword = input("请输入测试关键词 (默认: 测试): ").strip() or "测试"
    
    print(f"\n🧪 开始测试书源: {source_name}")
    return run_command(["--test", source_name, "--keyword", keyword])


def list_sources():
    """列出可用书源"""
    print("\n📋 列出所有可用书源...")
    return run_command(["--list"])


def show_stats():
    """显示统计信息"""
    print("\n📊 显示统计信息...")
    return run_command(["--stats"])


def run_tests():
    """运行测试用例"""
    print("\n🧪 运行测试用例...")
    try:
        cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
        print(f"🚀 执行命令: {' '.join(cmd)}")
        print("-" * 60)
        
        result = subprocess.run(cmd)
        
        print("-" * 60)
        if result.returncode == 0:
            print("✅ 所有测试通过")
        else:
            print(f"❌ 测试失败 (退出码: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 测试执行异常: {e}")
        return False


def clear_cache():
    """清理缓存"""
    print("\n🧹 清理缓存...")
    
    cache_dirs = ["data/cache", "data/logs"]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir, exist_ok=True)
                print(f"✅ 已清理: {cache_dir}")
            except Exception as e:
                print(f"❌ 清理失败 {cache_dir}: {e}")
        else:
            print(f"📁 目录不存在: {cache_dir}")
    
    print("✅ 缓存清理完成")


def show_help():
    """显示帮助信息"""
    print("\n📖 帮助信息")
    print("-" * 60)
    print("独立书源系统是一个专为legado阅读软件开发的免费书源聚合工具。")
    print("\n主要功能:")
    print("• 支持多个主流小说网站")
    print("• 生成legado兼容的书源文件")
    print("• 完全免费，无需登录")
    print("• 独立部署，数据本地存储")
    print("\n使用流程:")
    print("1. 首次使用建议先生成所有书源")
    print("2. 将生成的书源文件导入legado阅读软件")
    print("3. 定期更新书源以获得最佳体验")
    print("\n输出文件:")
    print("• output/legado_sources.json - 合并的书源文件")
    print("• output/individual/ - 单独的书源文件")
    print("\n更多信息:")
    print("• 项目主页: https://github.com/your-username/independent-book-source")
    print("• 使用文档: docs/DEVELOPMENT.md")
    print("• 问题反馈: https://github.com/your-username/independent-book-source/issues")


def main():
    """主函数"""
    print("🚀 启动独立书源系统...")
    
    # 检查环境
    if not check_python_version():
        return
    
    # 创建目录
    create_directories()
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请手动安装依赖包后重试")
        return
    
    # 主循环
    while True:
        try:
            show_menu()
            choice = input("\n请选择操作 (0-8): ").strip()
            
            if choice == "0":
                print("\n👋 感谢使用独立书源系统！")
                break
            elif choice == "1":
                generate_all_sources()
            elif choice == "2":
                generate_specific_sources()
            elif choice == "3":
                test_source()
            elif choice == "4":
                list_sources()
            elif choice == "5":
                show_stats()
            elif choice == "6":
                run_tests()
            elif choice == "7":
                clear_cache()
            elif choice == "8":
                show_help()
            else:
                print("❌ 无效的选择，请输入0-8之间的数字")
            
            input("\n按回车键继续...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作被用户中断")
            break
        except Exception as e:
            print(f"\n❌ 程序异常: {e}")
            input("按回车键继续...")


if __name__ == "__main__":
    main()
