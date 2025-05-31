#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精品书源测试脚本
测试各个书源的可用性和基本功能
"""

import json
import requests
import time
from urllib.parse import urljoin, urlparse
import sys
import os

class BookSourceTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
        
    def test_url_accessibility(self, url, description=""):
        """测试URL可访问性"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                print(f"✅ {description} - 可访问 ({response.status_code})")
                return True
            else:
                print(f"⚠️ {description} - 状态码: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ {description} - 访问失败: {str(e)}")
            return False
    
    def test_search_functionality(self, source_config):
        """测试搜索功能"""
        if 'searchUrl' not in source_config or not source_config['searchUrl']:
            print("   ⚠️ 未配置搜索URL")
            return False
            
        search_url = source_config['searchUrl']
        base_url = source_config['bookSourceUrl']
        
        # 简单的URL格式检查
        if '{{key}}' in search_url:
            test_url = search_url.replace('{{key}}', '斗罗大陆').replace('{{page}}', '1')
            if not test_url.startswith('http'):
                test_url = urljoin(base_url, test_url)
            
            return self.test_url_accessibility(test_url, "搜索功能")
        else:
            print("   ⚠️ 搜索URL格式异常")
            return False
    
    def test_explore_functionality(self, source_config):
        """测试发现功能"""
        if 'exploreUrl' not in source_config or not source_config['exploreUrl']:
            print("   ⚠️ 未配置发现URL")
            return False
            
        explore_url = source_config['exploreUrl']
        base_url = source_config['bookSourceUrl']
        
        # 处理复杂的发现URL配置
        if isinstance(explore_url, str) and explore_url.startswith('['):
            print("   ℹ️ 发现功能使用复杂配置，跳过测试")
            return True
        elif '{{page}}' in explore_url:
            test_url = explore_url.replace('{{page}}', '1')
            if not test_url.startswith('http'):
                test_url = urljoin(base_url, test_url)
            
            return self.test_url_accessibility(test_url, "发现功能")
        else:
            print("   ⚠️ 发现URL格式异常")
            return False
    
    def test_book_source(self, source_config):
        """测试单个书源"""
        name = source_config.get('bookSourceName', '未知书源')
        url = source_config.get('bookSourceUrl', '')
        
        print(f"\n📚 测试书源: {name}")
        print(f"   🌐 地址: {url}")
        
        results = {
            'name': name,
            'url': url,
            'base_accessible': False,
            'search_working': False,
            'explore_working': False,
            'overall_status': 'failed'
        }
        
        # 测试基础URL可访问性
        if url:
            results['base_accessible'] = self.test_url_accessibility(url, "基础地址")
        
        # 测试搜索功能
        if source_config.get('enabled', True):
            results['search_working'] = self.test_search_functionality(source_config)
            results['explore_working'] = self.test_explore_functionality(source_config)
        else:
            print("   ⚠️ 书源已禁用")
        
        # 综合评估
        if results['base_accessible'] and (results['search_working'] or results['explore_working']):
            results['overall_status'] = 'good'
            print(f"   ✅ 整体状态: 良好")
        elif results['base_accessible']:
            results['overall_status'] = 'partial'
            print(f"   ⚠️ 整体状态: 部分可用")
        else:
            results['overall_status'] = 'failed'
            print(f"   ❌ 整体状态: 不可用")
        
        return results
    
    def test_sources_file(self, file_path):
        """测试书源文件"""
        print(f"\n🔍 测试书源文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sources = json.load(f)
        except Exception as e:
            print(f"❌ 读取文件失败: {str(e)}")
            return []
        
        if not isinstance(sources, list):
            print(f"❌ 文件格式错误: 期望列表格式")
            return []
        
        print(f"📊 发现 {len(sources)} 个书源")
        
        results = []
        for i, source in enumerate(sources, 1):
            print(f"\n{'='*50}")
            print(f"测试进度: {i}/{len(sources)}")
            
            result = self.test_book_source(source)
            results.append(result)
            
            # 添加延迟避免请求过快
            time.sleep(1)
        
        return results
    
    def generate_report(self, results, file_name):
        """生成测试报告"""
        print(f"\n{'='*60}")
        print(f"📋 测试报告 - {file_name}")
        print(f"{'='*60}")
        
        total = len(results)
        good = len([r for r in results if r['overall_status'] == 'good'])
        partial = len([r for r in results if r['overall_status'] == 'partial'])
        failed = len([r for r in results if r['overall_status'] == 'failed'])
        
        print(f"📊 总计: {total} 个书源")
        if total > 0:
            print(f"✅ 良好: {good} 个 ({good/total*100:.1f}%)")
            print(f"⚠️ 部分可用: {partial} 个 ({partial/total*100:.1f}%)")
            print(f"❌ 不可用: {failed} 个 ({failed/total*100:.1f}%)")
        else:
            print("⚠️ 没有找到有效的书源数据")
        
        print(f"\n📝 详细结果:")
        for result in results:
            status_icon = {
                'good': '✅',
                'partial': '⚠️',
                'failed': '❌'
            }.get(result['overall_status'], '❓')
            
            print(f"{status_icon} {result['name']}")
            if result['overall_status'] == 'failed':
                print(f"   原因: 基础地址不可访问")
            elif result['overall_status'] == 'partial':
                print(f"   原因: 搜索或发现功能异常")

def main():
    """主函数"""
    tester = BookSourceTester()
    
    # 测试文件列表
    test_files = [
        'docs/sources/premium_sources.json',
        'docs/sources/jjwxc_sources.json',
        'docs/sources/legado_sources.json'
    ]
    
    all_results = {}
    
    for file_path in test_files:
        if os.path.exists(file_path):
            results = tester.test_sources_file(file_path)
            all_results[file_path] = results
            tester.generate_report(results, os.path.basename(file_path))
        else:
            print(f"⚠️ 文件不存在: {file_path}")
    
    # 生成总体报告
    print(f"\n{'='*60}")
    print(f"🎯 总体测试报告")
    print(f"{'='*60}")
    
    total_sources = sum(len(results) for results in all_results.values())
    total_good = sum(len([r for r in results if r['overall_status'] == 'good']) 
                    for results in all_results.values())
    
    print(f"📊 总计测试: {total_sources} 个书源")
    if total_sources > 0:
        print(f"✅ 可用率: {total_good/total_sources*100:.1f}%")
    else:
        print("⚠️ 没有测试到任何书源")
    
    print(f"\n💡 使用建议:")
    print(f"1. 优先使用状态为'良好'的书源")
    print(f"2. '部分可用'的书源可能需要特殊配置")
    print(f"3. 定期重新测试以确保书源可用性")
    print(f"4. 如遇问题请查看使用指南: docs/USAGE.md")

if __name__ == "__main__":
    main()
