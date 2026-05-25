# -*- coding: utf-8 -*-
"""
数据预处理脚本
农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

功能：
1. 读取原始水质和气象数据
2. 数据清洗和标准化
3. 生成数据摘要统计

作者：农业面源污染机器学习研究小组
日期：2026-03-30
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 路径配置
PROJECT_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Agricultural_NPS_ML_Reproducibility")
DATA_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Machine_Learning_Nonpoint_Source_Pollution\data")
OUTPUT_DIR = PROJECT_ROOT / "results" / "01_data_summary"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """
    加载所有水质和气象数据文件
    """
    print("开始加载数据...")
    
    runoff_dir = DATA_ROOT / "water_runoff_sample"
    pollutant_types = [
        'Total_Nitrogen', 'Total_Phosphorus', 'Ammoniacal_Nitrogen',
        'Nitrate_Nitrogen', 'Dissolved_Phosphorus', 'Particulate_Phosphorus'
    ]
    
    data_summary = []
    
    for pollutant in pollutant_types:
        pollutant_dir = runoff_dir / pollutant
        if not pollutant_dir.exists():
            print(f"警告: 目录不存在 - {pollutant_dir}")
            continue
            
        csv_files = list(pollutant_dir.glob("*.csv"))
        print(f"  {pollutant}: 找到 {len(csv_files)} 个文件")
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                data_summary.append({
                    '污染物类型': pollutant,
                    '文件名': csv_file.name,
                    '样本数': len(df),
                    '列数': len(df.columns),
                    '列名': ', '.join(df.columns.tolist()[:10]) + '...'
                })
            except Exception as e:
                print(f"  读取失败: {csv_file.name} - {str(e)}")
    
    return data_summary

def generate_summary(data_summary):
    """
    生成数据摘要报告
    """
    print("\n生成数据摘要报告...")
    
    summary_df = pd.DataFrame(data_summary)
    
    # 保存摘要
    summary_path = OUTPUT_DIR / "数据文件摘要.csv"
    summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
    print(f"数据摘要已保存: {summary_path}")
    
    # 生成统计信息
    stats = {
        '总文件数': len(data_summary),
        '污染物类型数': summary_df['污染物类型'].nunique(),
        '总样本数': summary_df['样本数'].sum(),
        '平均样本数': summary_df['样本数'].mean()
    }
    
    stats_df = pd.DataFrame([stats])
    stats_path = OUTPUT_DIR / "数据统计信息.csv"
    stats_df.to_csv(stats_path, index=False, encoding='utf-8-sig')
    print(f"统计信息已保存: {stats_path}")
    
    return summary_df, stats

def main():
    """
    主函数
    """
    print("=" * 60)
    print("数据预处理 - 开始")
    print("=" * 60)
    
    # 加载数据
    data_summary = load_data()
    
    # 生成摘要
    summary_df, stats = generate_summary(data_summary)
    
    print("\n数据预处理完成!")
    print(f"总文件数: {stats['总文件数']}")
    print(f"污染物类型: {stats['污染物类型数']}")
    print(f"总样本数: {stats['总样本数']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
