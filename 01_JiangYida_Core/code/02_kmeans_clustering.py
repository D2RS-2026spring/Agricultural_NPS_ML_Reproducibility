# -*- coding: utf-8 -*-
"""
K-Means聚类分析脚本
农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

功能：
1. 对各污染物类型进行K-Means聚类
2. 使用PCA进行降维可视化
3. 进行ANOVA显著性检验

作者：农业面源污染机器学习研究小组
日期：2026-03-30
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.stats import f_oneway
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 路径配置
PROJECT_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Agricultural_NPS_ML_Reproducibility")
DATA_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Machine_Learning_Nonpoint_Source_Pollution\data")
OUTPUT_DIR = PROJECT_ROOT / "results" / "02_clustering_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 聚类配置
N_CLUSTERS = 3
RANDOM_STATE = 42

def perform_clustering(data_file, pollutant_type):
    """
    对单个数据文件进行K-Means聚类
    """
    print(f"  处理: {data_file.name}")
    
    try:
        df = pd.read_csv(data_file)
        
        # 营养元素特征
        nutrient_features = ["NPK", "PK", "NK", "CK", "OF"]
        available_features = [f for f in nutrient_features if f in df.columns]
        
        if len(available_features) < 2:
            print(f"    警告: 可用特征不足")
            return None
        
        # 去除缺失值
        df_clean = df.dropna(subset=available_features)
        
        # 标准化
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_clean[available_features])
        
        # K-Means聚类
        os.environ["OMP_NUM_THREADS"] = "1"
        kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
        df_clean = df_clean.copy()
        df_clean["Cluster"] = kmeans.fit_predict(df_scaled)
        
        # PCA降维
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(df_scaled)
        df_clean["PCA1"] = pca_result[:, 0]
        df_clean["PCA2"] = pca_result[:, 1]
        
        # 聚类计数
        cluster_counts = df_clean["Cluster"].value_counts().to_dict()
        
        return df_clean, cluster_counts, available_features
        
    except Exception as e:
        print(f"    错误: {str(e)}")
        return None

def plot_clustering(df_clean, data_file, pollutant_type):
    """
    绘制聚类散点图
    """
    crop_name = data_file.stem.split('_')[-1] if len(data_file.stem.split('_')) > 3 else "Unknown"
    
    plt.figure(figsize=(10, 6))
    cluster_colors = {0: "red", 1: "green", 2: "blue"}
    
    sns.scatterplot(
        x="PCA1", y="PCA2", hue="Cluster", palette=cluster_colors,
        data=df_clean, alpha=0.7, s=150, edgecolor="black"
    )
    
    plt.xlabel("Principal Component 1", fontsize=14)
    plt.ylabel("Principal Component 2", fontsize=14)
    plt.title(f"K-Means Clustering (PCA) - {crop_name}", fontsize=14, fontweight='bold')
    plt.legend(title="Cluster", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    
    # 保存图片
    plot_dir = OUTPUT_DIR / "scatter_plots"
    plot_dir.mkdir(exist_ok=True)
    plot_path = plot_dir / f"{data_file.stem}_cluster.png"
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return plot_path

def analyze_clusters(df_clean, df_original):
    """
    分析各聚类的气象特征差异
    """
    weather_features = [
        "Dew Point Temperature (F)", "Visibility (mi)", "Average Wind Speed (knots)",
        "Maximum Sustained Wind Speed (knots)", "Maximum Gust (knots)", 
        "Maximum Temperature (F)", "Minimum Temperature (F)", "Precipitation (in)"
    ]
    
    available_weather = [f for f in weather_features if f in df_clean.columns]
    
    if not available_weather:
        return None
    
    # 计算各聚类的均值
    cluster_means = df_clean.groupby("Cluster")[available_weather].mean()
    
    # ANOVA分析
    anova_results = []
    for feature in available_weather:
        groups = [df_clean[df_clean["Cluster"] == c][feature].dropna() 
                  for c in df_clean["Cluster"].unique()]
        if all(len(g) > 0 for g in groups):
            try:
                stat, p = f_oneway(*groups)
                anova_results.append({
                    '特征': feature,
                    'F统计量': stat,
                    'p值': p,
                    '显著性': '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
                })
            except:
                pass
    
    return cluster_means, pd.DataFrame(anova_results)

def main():
    """
    主函数
    """
    print("=" * 60)
    print("K-Means聚类分析 - 开始")
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
        
        for data_file in csv_files:
            result = perform_clustering(data_file, pollutant)
            
            if result is not None:
                df_clean, cluster_counts, features = result
                
                # 保存聚类结果
                output_csv = OUTPUT_DIR / f"clustered_{data_file.name}"
                df_clean.to_csv(output_csv, index=False)
                
                # 绘制散点图
                plot_path = plot_clustering(df_clean, data_file, pollutant)
                
                # 分析聚类特征
                analysis = analyze_clusters(df_clean, df_clean)
                if analysis is not None:
                    cluster_means, anova_df = analysis
                    
                    # 保存ANOVA结果
                    anova_path = OUTPUT_DIR / f"{data_file.stem}_anova.csv"
                    anova_df.to_csv(anova_path, index=False, encoding='utf-8-sig')
                
                all_results.append({
                    '污染物类型': pollutant,
                    '文件': data_file.name,
                    '样本数': len(df_clean),
                    '聚类计数': str(cluster_counts),
                    '使用特征': ', '.join(features)
                })
    
    # 保存汇总
    if all_results:
        summary_df = pd.DataFrame(all_results)
        summary_path = OUTPUT_DIR / "聚类分析汇总.csv"
        summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
        print(f"\n聚类分析汇总已保存: {summary_path}")
    
    print("\n" + "=" * 60)
    print("K-Means聚类分析 - 完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
