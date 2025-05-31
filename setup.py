"""
独立书源系统安装脚本 - Setup Script
Independent Book Source System Setup
"""

from setuptools import setup, find_packages
import os
import sys
from pathlib import Path

# 读取README文件
def read_readme():
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "独立书源系统 - 大灰狼融合书源独立版"

# 读取requirements.txt
def read_requirements():
    requirements_path = Path(__file__).parent / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 过滤注释和空行
        requirements = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                # 处理平台特定依赖
                if "sys_platform" in line:
                    requirements.append(line)
                else:
                    requirements.append(line)
        
        return requirements
    return []

# 版本信息
VERSION = "1.0.0"
AUTHOR = "大灰狼开发团队"
EMAIL = "contact@example.com"
DESCRIPTION = "独立书源系统 - 专为legado阅读软件开发的免费书源聚合工具"
URL = "https://github.com/your-username/independent-book-source"

# 分类信息
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Internet :: WWW/HTTP :: Browsers",
    "Topic :: Multimedia :: Graphics :: Viewers",
    "Topic :: Text Processing :: Markup :: HTML",
    "Topic :: Utilities",
]

# 关键词
KEYWORDS = [
    "book-source",
    "legado",
    "novel",
    "ebook",
    "reader",
    "crawler",
    "parser",
    "chinese-novel",
    "fanqie",
    "qimao",
    "independent"
]

# 项目URLs
PROJECT_URLS = {
    "Bug Reports": f"{URL}/issues",
    "Source": URL,
    "Documentation": f"{URL}/wiki",
    "Changelog": f"{URL}/releases",
}

# 入口点
ENTRY_POINTS = {
    "console_scripts": [
        "book-source=src.main:main",
        "independent-book-source=src.main:main",
    ],
}

# 包数据
PACKAGE_DATA = {
    "src": [
        "sources/*/config.json",
        "sources/*/*.py",
    ],
    "config": ["*.json"],
    "docs": ["*.md"],
}

# 数据文件
DATA_FILES = [
    ("config", ["config/settings.json"]),
    ("docs", ["README.md", "LICENSE"]),
]

# 额外的安装要求
EXTRAS_REQUIRE = {
    "dev": [
        "pytest>=7.1.0",
        "pytest-asyncio>=0.19.0",
        "black>=22.6.0",
        "flake8>=5.0.0",
        "mypy>=0.971",
        "coverage>=6.4.0",
    ],
    "web": [
        "fastapi>=0.79.0",
        "uvicorn>=0.18.0",
        "starlette>=0.19.0",
    ],
    "performance": [
        "orjson>=3.7.0",
        "cchardet>=2.1.7",
        "uvloop>=0.16.0; sys_platform != 'win32'",
    ],
    "image": [
        "pillow>=9.2.0",
        "opencv-python>=4.6.0",
    ],
    "analysis": [
        "pandas>=1.4.0",
        "numpy>=1.23.0",
        "matplotlib>=3.5.0",
    ],
}

# 所有额外依赖
EXTRAS_REQUIRE["all"] = [
    dep for deps in EXTRAS_REQUIRE.values() for dep in deps
]

setup(
    name="independent-book-source",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=URL,
    project_urls=PROJECT_URLS,
    
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    data_files=DATA_FILES,
    include_package_data=True,
    
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require=EXTRAS_REQUIRE,
    
    entry_points=ENTRY_POINTS,
    
    classifiers=CLASSIFIERS,
    keywords=" ".join(KEYWORDS),
    
    license="MIT",
    platforms=["any"],
    
    zip_safe=False,
    
    # 元数据
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python",
        },
    },
)

# 安装后的设置
def post_install():
    """安装后的设置工作"""
    print("🎉 独立书源系统安装完成！")
    print("\n📚 快速开始:")
    print("  1. 生成所有书源: book-source --generate-all")
    print("  2. 测试书源: book-source --test fanqie")
    print("  3. 查看帮助: book-source --help")
    print("\n📁 输出文件:")
    print("  - legado书源: output/legado_sources.json")
    print("  - 单独书源: output/individual/")
    print("\n🔗 更多信息:")
    print(f"  - 项目主页: {URL}")
    print(f"  - 问题反馈: {URL}/issues")
    print(f"  - 使用文档: {URL}/wiki")
    print("\n⭐ 如果觉得有用，请给个Star支持一下！")

if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 执行安装
    setup()
    
    # 安装后设置
    if "install" in sys.argv:
        post_install()
