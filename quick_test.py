#!/usr/bin/env python3
"""
快速测试脚本 - Quick Test Script

用于快速验证系统基本功能的测试脚本
"""

import sys
import json
import asyncio
import logging
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置简单的日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from src.core.engine import BookSourceEngine, BaseSource, BookInfo
        from src.core.network import NetworkManager
        from src.core.rules import RuleEngine
        from src.core.cache import CacheManager
        from src.utils.parser import Parser
        from src.utils.validator import Validator
        from src.utils.crypto import Crypto
        print("✅ 核心模块导入成功")
    except Exception as e:
        print(f"❌ 核心模块导入失败: {e}")
        return False
    
    try:
        from src.sources.manager import SourceManager
        print("✅ 书源管理器导入成功")
    except Exception as e:
        print(f"❌ 书源管理器导入失败: {e}")
        return False
    
    return True


def test_config():
    """测试配置文件"""
    print("\n📋 测试配置文件...")
    
    config_path = "config/settings.json"
    if not Path(config_path).exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_sections = ["network", "cache", "rules", "output", "logging"]
        for section in required_sections:
            if section not in config:
                print(f"❌ 配置文件缺少节: {section}")
                return False
        
        print("✅ 配置文件格式正确")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件解析失败: {e}")
        return False


def test_engine():
    """测试书源引擎"""
    print("\n⚙️ 测试书源引擎...")
    
    try:
        from src.core.engine import BookSourceEngine
        
        # 创建引擎实例
        engine = BookSourceEngine("config/settings.json")
        
        # 测试基本功能
        sources = engine.list_sources()
        print(f"✅ 引擎初始化成功，当前书源数: {len(sources)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 引擎测试失败: {e}")
        return False


def test_network():
    """测试网络管理器"""
    print("\n🌐 测试网络管理器...")
    
    try:
        from src.core.network import NetworkManager
        
        # 创建网络管理器
        network = NetworkManager()
        
        # 测试基本功能
        stats = network.get_stats()
        print(f"✅ 网络管理器初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 网络管理器测试失败: {e}")
        return False


def test_rules():
    """测试规则引擎"""
    print("\n📝 测试规则引擎...")
    
    try:
        from src.core.rules import RuleEngine
        
        # 创建规则引擎
        rules = RuleEngine()
        
        # 测试基本规则解析
        test_html = '<div class="title">测试标题</div>'
        result = rules.parse_rule(".title@text", test_html)
        
        if result == "测试标题":
            print("✅ 规则引擎测试成功")
            return True
        else:
            print(f"❌ 规则解析结果不正确: {result}")
            return False
        
    except Exception as e:
        print(f"❌ 规则引擎测试失败: {e}")
        return False


def test_cache():
    """测试缓存管理器"""
    print("\n💾 测试缓存管理器...")
    
    try:
        from src.core.cache import CacheManager
        
        # 创建缓存管理器
        cache = CacheManager({
            "enabled": True,
            "file_cache": False,
            "db_cache": False
        })
        
        # 测试缓存操作
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        
        if value == "test_value":
            print("✅ 缓存管理器测试成功")
            return True
        else:
            print(f"❌ 缓存值不正确: {value}")
            return False
        
    except Exception as e:
        print(f"❌ 缓存管理器测试失败: {e}")
        return False


def test_utils():
    """测试工具模块"""
    print("\n🔧 测试工具模块...")
    
    try:
        from src.utils.parser import Parser
        from src.utils.validator import Validator
        from src.utils.crypto import Crypto
        
        # 测试解析器
        html = '<div>测试内容</div>'
        soup = Parser.parse_html(html)
        text = Parser.extract_text(soup)
        
        if "测试内容" in text:
            print("✅ 解析器测试成功")
        else:
            print(f"❌ 解析器测试失败: {text}")
            return False
        
        # 测试验证器
        if Validator.is_valid_url("https://example.com"):
            print("✅ 验证器测试成功")
        else:
            print("❌ 验证器测试失败")
            return False
        
        # 测试加密工具
        encoded = Crypto.base64_encode("测试")
        decoded = Crypto.base64_decode(encoded)
        
        if decoded == "测试":
            print("✅ 加密工具测试成功")
        else:
            print(f"❌ 加密工具测试失败: {decoded}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 工具模块测试失败: {e}")
        return False


async def test_fanqie_source():
    """测试番茄小说书源"""
    print("\n🍅 测试番茄小说书源...")
    
    try:
        from src.sources.fanqie.source import FanqieSource
        
        # 加载配置
        config_path = "src/sources/fanqie/config.json"
        if not Path(config_path).exists():
            print(f"❌ 番茄小说配置文件不存在: {config_path}")
            return False
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 创建书源实例
        source = FanqieSource(config)
        
        # 测试基本属性
        if source.name and source.url:
            print("✅ 番茄小说书源初始化成功")
            print(f"   书源名称: {source.name}")
            print(f"   书源地址: {source.url}")
        else:
            print("❌ 番茄小说书源属性不完整")
            return False
        
        # 测试legado格式转换
        legado_format = source.to_legado_format()
        if legado_format.get("bookSourceName"):
            print("✅ legado格式转换成功")
        else:
            print("❌ legado格式转换失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 番茄小说书源测试失败: {e}")
        return False


def test_source_manager():
    """测试书源管理器"""
    print("\n📚 测试书源管理器...")
    
    try:
        from src.core.engine import BookSourceEngine
        from src.sources.manager import SourceManager
        
        # 创建引擎和管理器
        engine = BookSourceEngine("config/settings.json")
        manager = SourceManager(engine)
        
        # 测试基本功能
        available = manager.list_available_sources()
        print(f"✅ 书源管理器初始化成功，发现 {len(available)} 个可用书源")
        
        if available:
            print(f"   可用书源: {', '.join(available)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 书源管理器测试失败: {e}")
        return False


def test_output_generation():
    """测试输出生成"""
    print("\n📄 测试输出生成...")
    
    try:
        from src.core.engine import BookSourceEngine
        from src.sources.manager import SourceManager
        
        # 创建引擎和管理器
        engine = BookSourceEngine("config/settings.json")
        manager = SourceManager(engine)
        
        # 尝试注册一个书源
        available = manager.list_available_sources()
        if available:
            source_name = available[0]
            success = manager.register_source(source_name)
            
            if success:
                print(f"✅ 成功注册书源: {source_name}")
                
                # 生成输出文件
                output_path = "output/test_sources.json"
                Path("output").mkdir(exist_ok=True)
                
                generated_path = engine.generate_legado_sources(output_path)
                
                if Path(generated_path).exists():
                    print(f"✅ 输出文件生成成功: {generated_path}")
                    
                    # 验证文件内容
                    with open(generated_path, 'r', encoding='utf-8') as f:
                        sources_data = json.load(f)
                    
                    if sources_data and len(sources_data) > 0:
                        print(f"✅ 输出文件内容正确，包含 {len(sources_data)} 个书源")
                        return True
                    else:
                        print("❌ 输出文件内容为空")
                        return False
                else:
                    print("❌ 输出文件生成失败")
                    return False
            else:
                print(f"❌ 书源注册失败: {source_name}")
                return False
        else:
            print("⚠️  没有可用的书源进行测试")
            return True
        
    except Exception as e:
        print(f"❌ 输出生成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始快速测试...")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置文件", test_config),
        ("书源引擎", test_engine),
        ("网络管理器", test_network),
        ("规则引擎", test_rules),
        ("缓存管理器", test_cache),
        ("工具模块", test_utils),
        ("书源管理器", test_source_manager),
        ("输出生成", test_output_generation),
    ]
    
    async_tests = [
        ("番茄小说书源", test_fanqie_source),
    ]
    
    passed = 0
    total = len(tests) + len(async_tests)
    
    # 运行同步测试
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {name} 测试失败")
        except Exception as e:
            print(f"❌ {name} 测试异常: {e}")
    
    # 运行异步测试
    async def run_async_tests():
        nonlocal passed
        for name, test_func in async_tests:
            try:
                if await test_func():
                    passed += 1
                else:
                    print(f"❌ {name} 测试失败")
            except Exception as e:
                print(f"❌ {name} 测试异常: {e}")
    
    asyncio.run(run_async_tests())
    
    # 显示结果
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        print("\n📝 下一步:")
        print("1. 运行 python run.py 启动完整系统")
        print("2. 或运行 python src/main.py --generate-all 生成所有书源")
    else:
        print("⚠️  部分测试失败，请检查错误信息并修复问题。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
