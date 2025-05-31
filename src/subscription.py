#!/usr/bin/env python3
"""
书源订阅功能 - Book Source Subscription

生成可供legado直接订阅的书源链接和订阅文件
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.engine import BookSourceEngine
from src.sources.manager import SourceManager


class SubscriptionManager:
    """订阅管理器"""
    
    def __init__(self, base_url: str = ""):
        self.base_url = base_url.rstrip('/')
        self.engine = BookSourceEngine()
        self.source_manager = SourceManager(self.engine)
    
    def generate_subscription_info(self) -> Dict[str, Any]:
        """生成订阅信息"""
        # 注册所有书源
        results = self.source_manager.register_all_sources()
        
        # 获取统计信息
        stats = self.source_manager.get_source_stats()
        
        # 生成订阅信息
        subscription_info = {
            "name": "独立书源系统 - 大灰狼融合书源独立版",
            "description": "免费、开源、无需登录的legado书源聚合服务",
            "version": "1.0.0",
            "author": "大灰狼开发团队",
            "updateTime": datetime.now().isoformat(),
            "sourceCount": stats["total_registered"],
            "sources": [],
            "categories": {},
            "urls": {
                "all": f"{self.base_url}/legado_sources.json",
                "individual": f"{self.base_url}/individual/",
                "subscription": f"{self.base_url}/subscription.json",
                "website": f"{self.base_url}/",
                "github": "https://github.com/your-username/independent-book-source"
            }
        }
        
        # 添加书源信息
        for source_name in self.source_manager.list_registered_sources():
            source_info = self.source_manager.get_source_info(source_name)
            if source_info:
                source_data = {
                    "name": source_info["name"],
                    "id": source_name,
                    "description": source_info["description"],
                    "group": source_info["group"],
                    "type": source_info["type"],
                    "enabled": source_info["enabled"],
                    "url": f"{self.base_url}/individual/{source_name}.json",
                    "author": source_info["author"],
                    "version": source_info["version"]
                }
                subscription_info["sources"].append(source_data)
                
                # 按分组统计
                group = source_info["group"]
                if group not in subscription_info["categories"]:
                    subscription_info["categories"][group] = []
                subscription_info["categories"][group].append(source_name)
        
        return subscription_info
    
    def generate_legado_subscription(self) -> Dict[str, Any]:
        """生成legado格式的订阅文件"""
        subscription_info = self.generate_subscription_info()
        
        # legado订阅格式
        legado_subscription = {
            "name": subscription_info["name"],
            "author": subscription_info["author"],
            "description": subscription_info["description"],
            "updateTime": subscription_info["updateTime"],
            "sourceUrls": [
                {
                    "name": "全部书源",
                    "url": subscription_info["urls"]["all"],
                    "description": f"包含所有 {subscription_info['sourceCount']} 个书源"
                }
            ]
        }
        
        # 添加分类订阅
        for category, sources in subscription_info["categories"].items():
            if len(sources) > 1:  # 只有多个书源的分类才单独提供订阅
                legado_subscription["sourceUrls"].append({
                    "name": f"{category}书源",
                    "url": f"{self.base_url}/categories/{category}.json",
                    "description": f"{category}分类，包含 {len(sources)} 个书源"
                })
        
        # 添加单独书源订阅
        for source in subscription_info["sources"]:
            legado_subscription["sourceUrls"].append({
                "name": source["name"],
                "url": source["url"],
                "description": source["description"]
            })
        
        return legado_subscription
    
    def generate_category_sources(self, output_dir: str = "output"):
        """生成分类书源文件"""
        subscription_info = self.generate_subscription_info()
        
        categories_dir = os.path.join(output_dir, "categories")
        os.makedirs(categories_dir, exist_ok=True)
        
        for category, source_names in subscription_info["categories"].items():
            if len(source_names) <= 1:
                continue
            
            # 收集该分类的所有书源
            category_sources = []
            for source_name in source_names:
                source = self.source_manager.get_source(source_name)
                if source and source.enabled:
                    category_sources.append(source.to_legado_format())
            
            # 保存分类书源文件
            if category_sources:
                category_file = os.path.join(categories_dir, f"{category}.json")
                with open(category_file, 'w', encoding='utf-8') as f:
                    json.dump(category_sources, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 生成分类书源: {category} ({len(category_sources)} 个书源)")
    
    def generate_all_subscription_files(self, output_dir: str = "output"):
        """生成所有订阅相关文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成订阅信息文件
        subscription_info = self.generate_subscription_info()
        with open(os.path.join(output_dir, "subscription_info.json"), 'w', encoding='utf-8') as f:
            json.dump(subscription_info, f, ensure_ascii=False, indent=2)
        
        # 生成legado订阅文件
        legado_subscription = self.generate_legado_subscription()
        with open(os.path.join(output_dir, "subscription.json"), 'w', encoding='utf-8') as f:
            json.dump(legado_subscription, f, ensure_ascii=False, indent=2)
        
        # 生成分类书源文件
        self.generate_category_sources(output_dir)
        
        # 生成README文件
        self.generate_readme(output_dir, subscription_info)
        
        print(f"✅ 所有订阅文件已生成到: {output_dir}")
    
    def generate_readme(self, output_dir: str, subscription_info: Dict[str, Any]):
        """生成README文件"""
        readme_content = f"""# 书源订阅链接

## 📚 全部书源（推荐）
```
{subscription_info["urls"]["all"]}
```

## 📋 分类书源

"""
        
        for category, sources in subscription_info["categories"].items():
            if len(sources) > 1:
                readme_content += f"### {category}\n"
                readme_content += f"```\n{self.base_url}/categories/{category}.json\n```\n\n"
        
        readme_content += "## 🔗 单独书源\n\n"
        
        for source in subscription_info["sources"]:
            readme_content += f"### {source['name']}\n"
            readme_content += f"```\n{source['url']}\n```\n"
            readme_content += f"{source['description']}\n\n"
        
        readme_content += f"""
## 📥 使用方法

1. 复制上面的书源链接
2. 打开legado阅读软件
3. 进入"书源管理"
4. 点击"网络导入"
5. 粘贴链接并导入

## 🔄 自动更新

书源文件每天自动更新，确保始终可用。

## 📞 联系方式

- GitHub: {subscription_info["urls"]["github"]}
- 网站: {subscription_info["urls"]["website"]}

---
最后更新: {subscription_info["updateTime"]}
"""
        
        with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme_content)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="生成书源订阅文件")
    parser.add_argument("--base-url", default="https://your-username.github.io/independent-book-source/sources", help="基础URL")
    parser.add_argument("--output", default="output", help="输出目录")
    
    args = parser.parse_args()
    
    # 创建订阅管理器
    manager = SubscriptionManager(args.base_url)
    
    # 生成所有订阅文件
    manager.generate_all_subscription_files(args.output)
    
    print("\n🎉 订阅文件生成完成！")
    print(f"📁 输出目录: {args.output}")
    print(f"🔗 订阅链接: {args.base_url}/subscription.json")


if __name__ == "__main__":
    main()
