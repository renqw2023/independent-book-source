const fs = require('fs');
const path = require('path');

// 书源文件映射
const sourceFiles = {
    '71e56d4f.json': 'XIU2精品书源',
    '4dc410d1.json': '破冰书源', 
    'e29e19ee.json': 'shidahuilang书源',
    'e3e5d620.json': '关耳女频书源',
    '2a1f129b.json': '三舞313书源',
    '3bb7b751.json': '开源阅读软件书源',
    'b778fe6b.json': '全量书源(4026)'
};

// 处理单个书源文件
function processSourceFile(filename, displayName) {
    const filePath = path.join('legado-release/sources', filename);
    
    if (!fs.existsSync(filePath)) {
        console.log(`❌ ${displayName}: 文件不存在`);
        return null;
    }
    
    try {
        console.log(`📖 正在处理 ${displayName}...`);
        const content = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(content);
        
        if (!Array.isArray(data)) {
            console.log(`❌ ${displayName}: 不是有效的书源数组格式`);
            return null;
        }
        
        console.log(`✅ ${displayName}: ${data.length} 个书源`);
        
        // 显示前3个书源名称作为示例
        if (data.length > 0) {
            console.log(`   示例书源:`);
            data.slice(0, 3).forEach((source, i) => {
                const name = source.bookSourceName || source.sourceName || '未知';
                console.log(`     ${i+1}. ${name}`);
            });
        }
        
        return {
            filename,
            displayName,
            count: data.length,
            data: data,
            fileSize: (fs.statSync(filePath).size / 1024 / 1024).toFixed(2) + 'MB'
        };
        
    } catch (error) {
        console.log(`❌ ${displayName}: 解析失败 - ${error.message.substring(0, 100)}`);
        return null;
    }
}

// 主处理函数
function main() {
    console.log('🚀 开始处理legado书源文件...\n');
    
    const results = [];
    let totalSources = 0;
    
    // 处理每个书源文件
    Object.entries(sourceFiles).forEach(([filename, displayName]) => {
        const result = processSourceFile(filename, displayName);
        if (result) {
            results.push(result);
            totalSources += result.count;
        }
        console.log(''); // 空行分隔
    });
    
    // 输出统计信息
    console.log('📊 处理结果统计:');
    console.log('='.repeat(50));
    results.forEach(result => {
        console.log(`${result.displayName}: ${result.count} 个书源 (${result.fileSize})`);
    });
    console.log('='.repeat(50));
    console.log(`总计: ${totalSources} 个书源`);
    console.log(`成功处理: ${results.length} 个文件`);
    
    // 合并所有书源
    if (results.length > 0) {
        console.log('\n🔄 开始合并书源...');
        const allSources = [];
        const sourceStats = {};
        
        results.forEach(result => {
            allSources.push(...result.data);
            sourceStats[result.displayName] = result.count;
        });
        
        // 去重处理（基于bookSourceUrl）
        const uniqueSources = [];
        const seenUrls = new Set();
        
        allSources.forEach(source => {
            const url = source.bookSourceUrl || source.sourceUrl || '';
            if (url && !seenUrls.has(url)) {
                seenUrls.add(url);
                uniqueSources.push(source);
            } else if (!url) {
                uniqueSources.push(source); // 保留没有URL的书源
            }
        });
        
        console.log(`去重前: ${allSources.length} 个书源`);
        console.log(`去重后: ${uniqueSources.length} 个书源`);
        
        // 保存合并后的书源
        const outputDir = 'docs/sources/aoaostar_sources';
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
        
        // 保存完整合集
        const mergedFile = path.join(outputDir, 'merged_all_sources.json');
        fs.writeFileSync(mergedFile, JSON.stringify(uniqueSources, null, 2));
        console.log(`✅ 已保存合并书源到: ${mergedFile}`);
        
        // 保存统计信息
        const summaryInfo = {
            total: uniqueSources.length,
            originalTotal: allSources.length,
            duplicatesRemoved: allSources.length - uniqueSources.length,
            sources: sourceStats,
            created: new Date().toISOString(),
            description: '来自legado.aoaostar.com的优质书源合集'
        };
        
        const summaryFile = path.join(outputDir, 'sources_summary.json');
        fs.writeFileSync(summaryFile, JSON.stringify(summaryInfo, null, 2));
        console.log(`✅ 已保存统计信息到: ${summaryFile}`);
        
        // 分别保存各个书源集合
        results.forEach(result => {
            const individualFile = path.join(outputDir, `${result.displayName.replace(/[^a-zA-Z0-9]/g, '_')}.json`);
            fs.writeFileSync(individualFile, JSON.stringify(result.data, null, 2));
            console.log(`✅ 已保存 ${result.displayName} 到: ${individualFile}`);
        });
        
        console.log('\n🎉 所有书源处理完成！');
        return uniqueSources.length;
    }
    
    return 0;
}

// 运行主函数
if (require.main === module) {
    main();
}

module.exports = { processSourceFile, main };
