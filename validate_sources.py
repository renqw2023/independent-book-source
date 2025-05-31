#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书源文件验证脚本
验证JSON文件格式和基本结构
"""

import json
import os
import sys

def validate_json_file(file_path):
    """验证JSON文件格式"""
    print(f"\n🔍 验证文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON格式正确")
        
        if isinstance(data, list):
            print(f"✅ 数据格式正确 (列表)")
            print(f"📊 包含 {len(data)} 个书源")
            
            # 验证每个书源的基本结构
            valid_sources = 0
            for i, source in enumerate(data):
                if validate_source_structure(source, i):
                    valid_sources += 1
            
            print(f"✅ 有效书源: {valid_sources}/{len(data)}")
            return True
        else:
            print(f"❌ 数据格式错误: 期望列表，得到 {type(data)}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}")
        return False

def validate_source_structure(source, index):
    """验证单个书源结构"""
    required_fields = ['bookSourceName', 'bookSourceUrl', 'bookSourceType']
    
    if not isinstance(source, dict):
        print(f"   ❌ 书源 {index}: 不是字典格式")
        return False
    
    missing_fields = []
    for field in required_fields:
        if field not in source:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"   ❌ 书源 {index}: 缺少必需字段 {missing_fields}")
        return False
    
    name = source.get('bookSourceName', f'书源{index}')
    print(f"   ✅ {name} - 结构正确")
    return True

def main():
    """主函数"""
    print("📚 书源文件验证工具")
    print("=" * 50)
    
    # 要验证的文件列表
    files_to_validate = [
        'docs/sources/premium_sources.json',
        'docs/sources/jjwxc_sources.json',
        'docs/sources/legado_sources.json',
        'docs/sources/fanqie_collection.json'
    ]
    
    results = {}
    
    for file_path in files_to_validate:
        results[file_path] = validate_json_file(file_path)
    
    # 生成总结报告
    print(f"\n{'='*50}")
    print(f"📋 验证总结")
    print(f"{'='*50}")
    
    total_files = len(files_to_validate)
    valid_files = sum(1 for valid in results.values() if valid)
    
    print(f"📊 总计文件: {total_files}")
    print(f"✅ 有效文件: {valid_files}")
    print(f"❌ 无效文件: {total_files - valid_files}")
    
    print(f"\n📝 详细结果:")
    for file_path, is_valid in results.items():
        status = "✅" if is_valid else "❌"
        filename = os.path.basename(file_path)
        print(f"{status} {filename}")
    
    if valid_files == total_files:
        print(f"\n🎉 所有文件验证通过！")
        return 0
    else:
        print(f"\n⚠️ 有 {total_files - valid_files} 个文件需要修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
