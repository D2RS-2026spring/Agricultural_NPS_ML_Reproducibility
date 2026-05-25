# -*- coding: utf-8 -*-
"""
多元线性回归分析脚本
农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

功能：
1. 建立气象因子与水质参数的关系模型
2. 计算R², MAE, RMSE等评估指标
3. 对不同污染物和作物类型进行分析

作者：农业面源污染机器学习研究小组
日期：2026-03-30
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import statsmodels.api as sm
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'

# 路径配置
PROJECT_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Agricultural_NPS_ML_Reproducibility")
DATA_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Machine_Learning_Nonpoint_Source_Pollution\data")
OUTPUT_DIR = PROJECT_ROOT / "results" / "03_regression_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 排序顺序
CROP_ORDER = ['Rice', 'Vegetables', 'Corn', 'Citrus']

def get_crop_name(filename):
    """从文件名提取作物名称"""
    parts = filename.split('_')
    return parts[3] if len(parts) > 3 else 'Unknown'

def perform_regression(data_file, pollutant_type):
    """
    对单个数据文件进行多元线性回归分析
    """
    print(f"  处理: {data_file.name}")
    
    try:
        # 读取数据
        data = pd.read_csv(data_file, encoding='latin1')
        
        # 自变量：气象数据（从第7列开始）
        X = data.iloc[:, 6:]
        if len(X.columns) > 1:
            X = X.drop(X.columns[1], axis=1)  # 删除温度列
        X = sm.add_constant(X)
        
        # 因变量
        dependent_columns = ['NPK', 'PK', 'NK', 'CK', 'OF']
        results = []
        
        crop_name = get_crop_name(data_file.name)
        
        for column in dependent_columns:
            if column not in data.columns:
                continue
            
            y = data[column].dropna()
            X_filtered, y_filtered = X.align(y, join="inner", axis=0)
            
            if len(y_filtered) < 10:
                continue
            
            # 划分训练集和测试集
            X_train, X_test, y_train, y_test = train_test_split(
                X_filtered, y_filtered, test_size=0.2, random_state=42
            )
            
            # 拟合OLS模型
            model = sm.OLS(y_train, X_train).fit()
            R2 = round(model.rsquared, 3)
            
            # 预测
            y_pred = model.predict(X_test)
            
            # 计算误差
            MAE = round(mean_absolute_error(y_test, y_pred), 3)
            MSE = round(mean_squared_error(y_test, y_pred), 3)
            RMSE = round(np.sqrt(MSE), 3)
            
            results.append({
                '污染物类型': pollutant_type,
                '作物': crop_name,
                '因变量': column,
                'R-squared': R2,
                'MAE': MAE,
                'MSE': MSE,
                'RMSE': RMSE,
                '样本数': len(y_filtered)
            })
        
        return results
        
    except Exception as e:
        print(f"    错误: {str(e)}")
        return []

def plot_regression_comparison(results_df, pollutant_type):
    """
    绘制回归结果对比图
    """
    if results_df is None or results_df.empty:
        return None
    
    # 过滤有效数据
    results_df = results_df[results_df['R-squared'].notna() & (results_df['R-squared'] > 0)]
    if results_df.empty:
        return None
    
    try:
        plt.figure(figsize=(12, 6))
        
        # 按作物和因变量分组
        pivot_df = results_df.pivot_table(index='作物', columns='因变量', values='R-squared')
        
        # 按指定顺序排列
        pivot_df = pivot_df.reindex([c for c in CROP_ORDER if c in pivot_df.index])
        
        pivot_df.plot(kind='bar', width=0.8)
        
        plt.xlabel('作物类型', fontsize=12)
        plt.ylabel('R$^2$ 值', fontsize=12)
        plt.title(f'多元线性回归 R$^2$ 值对比 - {pollutant_type}', fontsize=14, fontweight='bold')
        plt.legend(title='因变量', fontsize=10)
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图片
        plot_dir = OUTPUT_DIR / "regression_plots"
        plot_dir.mkdir(exist_ok=True)
        plot_path = plot_dir / f"回归R2对比_{pollutant_type}.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return plot_path
    except Exception as e:
        print(f"    绘图错误: {str(e)}")
        return None

def main():
    """
    主函数
    """
    print("=" * 60)
    print("多元线性回归分析 - 开始")
    print("=" * 60)
    
    runoff_dir = DATA_ROOT / "water_runoff_sample"
    pollutant_types = [
        'Total_Nitrogen', 'Total_Phosphorus', 'Ammoniacal_Nitrogen',
        'Nitrate_Nitrogen', 'Dissolved_Phosphorus', 'Particulate_Phosphorus'
    ]
    
    all_results = []
    
    for pollutant in pollutant_types:
        print(f"\n污染物类型: {pollutant}")
        pollutant_dir = runoff_dir / pollutant
        
        if not pollutant_dir.exists():
            print(f"  警告: 目录不存在")
            continue
        
        csv_files = list(pollutant_dir.glob("*.csv"))
        
        # 按作物名称排序
        csv_files = sorted(csv_files, key=lambda x: CROP_ORDER.index(get_crop_name(x.name)) 
                          if get_crop_name(x.name) in CROP_ORDER else 999)
        
        pollutant_results = []
        
        for data_file in csv_files:
            results = perform_regression(data_file, pollutant)
            pollutant_results.extend(results)
        
        if pollutant_results:
            # 保存污染物结果
            pollutant_df = pd.DataFrame(pollutant_results)
            output_csv = OUTPUT_DIR / f"回归结果_{pollutant}.csv"
            pollutant_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
            
            # 绘制对比图
            plot_path = plot_regression_comparison(pollutant_df, pollutant)
            
            all_results.extend(pollutant_results)
    
    # 保存总体汇总
    if all_results:
        summary_df = pd.DataFrame(all_results)
        summary_path = OUTPUT_DIR / "回归分析汇总.csv"
        summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
        
        # 打印统计信息
        print(f"\n回归分析统计:")
        print(f"  总模型数: {len(summary_df)}")
        print(f"  平均R²: {summary_df['R-squared'].mean():.3f}")
        print(f"  最佳R²: {summary_df['R-squared'].max():.3f}")
        print(f"  汇总已保存: {summary_path}")
    
    print("\n" + "=" * 60)
    print("多元线性回归分析 - 完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
