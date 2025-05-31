"""
独立书源系统主程序 - Main Program

提供命令行接口和主要功能入口：
- 生成书源文件
- 测试书源功能
- 管理书源配置
"""

import os
import sys
import json
import argparse
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.engine import BookSourceEngine
from src.sources.manager import SourceManager


class BookSourceApp:
    """书源应用主类"""
    
    def __init__(self):
        self.engine = BookSourceEngine()
        self.source_manager = SourceManager(self.engine)
        self.logger = logging.getLogger("app")
    
    def generate_all_sources(self, output_dir: str = "output") -> str:
        """生成所有书源"""
        self.logger.info("开始生成所有书源...")
        
        # 注册所有可用的书源
        results = self.source_manager.register_all_sources()
        
        # 统计注册结果
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        self.logger.info(f"书源注册完成: {success_count}/{total_count}")
        
        # 生成legado格式书源文件
        output_path = os.path.join(output_dir, "legado_sources.json")
        os.makedirs(output_dir, exist_ok=True)
        
        generated_path = self.engine.generate_legado_sources(output_path)
        
        # 生成单独的书源文件
        individual_dir = os.path.join(output_dir, "individual")
        os.makedirs(individual_dir, exist_ok=True)
        
        for source_name, source in self.engine.sources.items():
            individual_path = os.path.join(individual_dir, f"{source_name}.json")
            with open(individual_path, 'w', encoding='utf-8') as f:
                json.dump([source.to_legado_format()], f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"书源文件生成完成: {generated_path}")
        return generated_path
    
    def generate_specific_sources(self, source_names: List[str], output_dir: str = "output") -> str:
        """生成指定的书源"""
        self.logger.info(f"开始生成指定书源: {', '.join(source_names)}")
        
        # 注册指定的书源
        success_sources = []
        for source_name in source_names:
            if self.source_manager.register_source(source_name):
                success_sources.append(source_name)
            else:
                self.logger.error(f"注册书源失败: {source_name}")
        
        if not success_sources:
            self.logger.error("没有成功注册的书源")
            return ""
        
        # 生成书源文件
        output_path = os.path.join(output_dir, f"legado_sources_{'_'.join(success_sources)}.json")
        os.makedirs(output_dir, exist_ok=True)
        
        generated_path = self.engine.generate_legado_sources(output_path)
        
        self.logger.info(f"指定书源文件生成完成: {generated_path}")
        return generated_path
    
    async def test_source(self, source_name: str, keyword: str = "测试") -> Dict[str, Any]:
        """测试书源"""
        self.logger.info(f"开始测试书源: {source_name}")
        
        # 注册书源
        if not self.source_manager.register_source(source_name):
            return {
                "success": False,
                "error": f"注册书源失败: {source_name}"
            }
        
        # 执行测试
        result = self.source_manager.test_source(source_name, keyword)
        
        if result["success"]:
            self.logger.info(f"书源测试成功: {source_name}")
        else:
            self.logger.error(f"书源测试失败: {source_name}, 错误: {result.get('error', '未知错误')}")
        
        return result
    
    def list_sources(self) -> Dict[str, Any]:
        """列出所有书源"""
        available_sources = self.source_manager.list_available_sources()
        
        source_info = {}
        for source_name in available_sources:
            info = self.source_manager.get_source_info(source_name)
            if info:
                source_info[source_name] = info
        
        return {
            "total_count": len(available_sources),
            "sources": source_info
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.source_manager.get_source_stats()


def setup_logging(level: str = "INFO"):
    """设置日志"""
    log_level = getattr(logging, level.upper())
    
    # 创建日志目录
    log_dir = Path("data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="独立书源系统 - 大灰狼融合书源独立版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s --generate-all                    # 生成所有书源
  %(prog)s --generate fanqie qimao          # 生成指定书源
  %(prog)s --test fanqie                    # 测试番茄小说书源
  %(prog)s --list                           # 列出所有可用书源
  %(prog)s --stats                          # 显示统计信息
        """
    )
    
    parser.add_argument(
        "--generate-all",
        action="store_true",
        help="生成所有书源"
    )
    
    parser.add_argument(
        "--generate",
        nargs="+",
        metavar="SOURCE",
        help="生成指定的书源"
    )
    
    parser.add_argument(
        "--test",
        metavar="SOURCE",
        help="测试指定的书源"
    )
    
    parser.add_argument(
        "--keyword",
        default="测试",
        help="测试搜索的关键词 (默认: 测试)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用的书源"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="显示统计信息"
    )
    
    parser.add_argument(
        "--output",
        default="output",
        help="输出目录 (默认: output)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="日志级别 (默认: INFO)"
    )

    parser.add_argument(
        "--subscription",
        action="store_true",
        help="生成订阅文件"
    )

    parser.add_argument(
        "--base-url",
        default="https://your-username.github.io/independent-book-source/sources",
        help="订阅文件的基础URL"
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.log_level)
    
    # 创建应用实例
    app = BookSourceApp()
    
    try:
        if args.generate_all:
            # 生成所有书源
            output_path = app.generate_all_sources(args.output)
            print(f"✅ 所有书源已生成: {output_path}")
            
        elif args.generate:
            # 生成指定书源
            output_path = app.generate_specific_sources(args.generate, args.output)
            if output_path:
                print(f"✅ 指定书源已生成: {output_path}")
            else:
                print("❌ 书源生成失败")
                sys.exit(1)
                
        elif args.test:
            # 测试书源
            async def run_test():
                result = await app.test_source(args.test, args.keyword)
                if result["success"]:
                    print(f"✅ 书源测试成功: {args.test}")
                    print(f"   搜索结果数: {result.get('search_count', 0)}")
                    print(f"   书籍名称: {result.get('book_name', 'N/A')}")
                    print(f"   章节数量: {result.get('chapter_count', 0)}")
                    print(f"   正文长度: {result.get('content_length', 0)}")
                else:
                    print(f"❌ 书源测试失败: {args.test}")
                    print(f"   错误信息: {result.get('error', '未知错误')}")
                    sys.exit(1)
            
            asyncio.run(run_test())

        elif args.subscription:
            # 生成订阅文件
            from src.subscription import SubscriptionManager

            manager = SubscriptionManager(args.base_url)
            manager.generate_all_subscription_files(args.output)
            print(f"✅ 订阅文件已生成: {args.output}")
            print(f"🔗 订阅链接: {args.base_url}/subscription.json")

        elif args.list:
            # 列出书源
            sources_info = app.list_sources()
            print(f"📚 可用书源总数: {sources_info['total_count']}")
            print("\n书源列表:")
            for name, info in sources_info["sources"].items():
                status = "✅" if info["enabled"] else "❌"
                print(f"  {status} {info['name']} ({name})")
                print(f"     作者: {info['author']}")
                print(f"     分组: {info['group']}")
                print(f"     描述: {info['description'][:50]}...")
                print()
                
        elif args.stats:
            # 显示统计信息
            stats = app.get_stats()
            print("📊 书源统计信息:")
            print(f"   可用书源: {stats['total_available']}")
            print(f"   已注册书源: {stats['total_registered']}")
            print(f"   注册率: {stats['registration_rate']:.1f}%")
            print(f"\n类型分布:")
            for source_type, count in stats['type_distribution'].items():
                type_name = {0: "文本", 1: "音频", 2: "图片", 3: "文件"}.get(source_type, "未知")
                print(f"   {type_name}: {count}")
            print(f"\n分组分布:")
            for group, count in stats['group_distribution'].items():
                print(f"   {group}: {count}")
                
        else:
            # 显示帮助信息
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        logging.getLogger("app").exception("程序执行异常")
        sys.exit(1)


if __name__ == "__main__":
    main()
