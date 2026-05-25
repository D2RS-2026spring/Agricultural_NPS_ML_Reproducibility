# -*- coding: utf-8 -*-
"""
可视化脚本
农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

功能：
1. 创建技术路线图
2. 创建方法对比图
3. 创建结果汇总图

作者：农业面源污染机器学习研究小组
日期：2026-03-30
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置绘图
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'

# 路径配置
PROJECT_ROOT = Path(r"e:\高老师作业\02-可重复性研究项目\Agricultural_NPS_ML_Reproducibility")
OUTPUT_DIR = PROJECT_ROOT / "results" / "04_visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def create_tech_flowchart():
    """
    创建技术路线图
    """
    print("创建技术路线图...")
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, '农业面源污染K-Means聚类与多元回归分析技术路线', 
            fontsize=16, ha='center', fontweight='bold')
    
    # 定义流程框
    boxes = [
        (0.5, 7.5, 2.5, 1, '数据获取\n(GitHub仓库)', 'lightblue'),
        (3.5, 7.5, 2.5, 1, '数据预处理\n(清洗、标准化)', 'lightgreen'),
        (6.5, 7.5, 2.5, 1, '特征工程\n(气象+水质)', 'lightyellow'),
        (9.5, 7.5, 2.5, 1, '数据分割\n(训练/测试)', 'lightcoral'),
        
        (2, 5.5, 2.5, 1, 'K-Means聚类\n(n=3类)', 'lightgreen'),
        (5, 5.5, 2.5, 1, 'PCA降维\n(可视化)', 'lightyellow'),
        (8, 5.5, 2.5, 1, 'ANOVA分析\n(显著性检验)', 'lightcoral'),
        
        (3.5, 3.5, 2.5, 1, '多元线性回归\n(OLS)', 'lightgreen'),
        (6.5, 3.5, 2.5, 1, '模型评估\n(R², MAE, RMSE)', 'lightyellow'),
        (9.5, 3.5, 2.5, 1, '结果可视化\n(图表生成)', 'lightcoral'),
        
        (5, 1.5, 3, 1, '可重复性研究报告', 'lightsteelblue'),
    ]
    
    for x, y, w, h, text, color in boxes:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # 添加箭头
    arrows = [
        ((3, 8), (3.5, 8)),
        ((6, 8), (6.5, 8)),
        ((9, 8), (9.5, 8)),
        ((2.25, 7.5), (2, 6.5)),
        ((5.25, 7.5), (5, 6.5)),
        ((8.25, 7.5), (8, 6.5)),
        ((3.25, 5.5), (3.5, 4.5)),
        ((6.25, 5.5), (6.5, 4.5)),
        ((9.25, 5.5), (9.5, 4.5)),
        ((6.5, 3.5), (6.5, 2.5)),
    ]
    
    for (x1, y1), (x2, y2) in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # 添加说明
    ax.text(1.5, 0.8, '输入数据: 气象数据 + 水质数据', fontsize=9)
    ax.text(10, 0.8, '输出结果: 聚类 + 回归模型', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "技术路线图.png", dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  已保存: 技术路线图.png")

def create_method_comparison():
    """
    创建方法对比图
    """
    print("创建方法对比图...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # K-Means聚类示意
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('K-Means聚类方法', fontsize=14, fontweight='bold')
    
    np.random.seed(42)
    for i, (cx, cy, color, label) in enumerate([
        (3, 7, 'red', '聚类0'),
        (7, 7, 'green', '聚类1'),
        (5, 3, 'blue', '聚类2')
    ]):
        x = np.random.normal(cx, 1, 30)
        y = np.random.normal(cy, 1, 30)
        ax1.scatter(x, y, c=color, alpha=0.6, s=50, label=label)
        ax1.scatter([cx], [cy], c=color, s=200, marker='*', edgecolors='black', linewidths=2)
    
    ax1.legend(loc='upper right')
    ax1.text(5, 0.5, 'PCA降维后的聚类可视化', ha='center', fontsize=10)
    
    # 多元线性回归示意
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('多元线性回归方法', fontsize=14, fontweight='bold')
    
    x = np.linspace(1, 9, 50)
    y = 0.8 * x + 1 + np.random.normal(0, 0.5, 50)
    ax2.scatter(x, y, c='steelblue', alpha=0.6, s=50, label='实际值')
    ax2.plot(x, 0.8 * x + 1, 'r-', linewidth=2, label='回归线')
    ax2.legend(loc='upper left')
    ax2.text(5, 0.5, 'Y = β₀ + β₁X₁ + β₂X₂ + ... + ε', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "方法对比图.png", dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  已保存: 方法对比图.png")

def create_results_summary():
    """
    创建结果汇总图
    """
    print("创建结果汇总图...")
    
    fig = plt.figure(figsize=(14, 10))
    
    # 各污染物类型R²对比
    ax1 = fig.add_subplot(2, 2, 1)
    pollutants = ['Total\nNitrogen', 'Total\nPhosphorus', 'Ammoniacal\nNitrogen', 
                 'Nitrate\nNitrogen', 'Dissolved\nPhosphorus', 'Particulate\nPhosphorus']
    avg_r2 = [0.196, 0.198, 0.205, 0.213, 0.248, 0.188]
    best_r2 = [0.415, 0.411, 0.573, 0.509, 0.531, 0.328]
    
    x = np.arange(len(pollutants))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, avg_r2, width, label='平均R²', color='steelblue')
    bars2 = ax1.bar(x + width/2, best_r2, width, label='最佳R²', color='coral')
    
    ax1.set_ylabel('R² 值', fontsize=11)
    ax1.set_title('各污染物类型回归性能对比', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(pollutants, fontsize=8)
    ax1.legend()
    ax1.set_ylim(0, 0.7)
    ax1.grid(axis='y', alpha=0.3)
    
    # 样本分布
    ax2 = fig.add_subplot(2, 2, 2)
    crops = ['玉米\n(Corn)', '水稻\n(Rice)', '柑橘\n(Citrus)', '蔬菜\n(Vegetables)']
    samples = [69, 69, 72, 60]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    bars = ax2.bar(crops, samples, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('样本数量', fontsize=11)
    ax2.set_title('各作物类型样本分布', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, samples):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(val), ha='center', fontsize=11, fontweight='bold')
    
    # 可重复性评估
    ax3 = fig.add_subplot(2, 2, 3)
    eval_items = ['数据可获取性', '代码可运行性', '结果可复现性', '文档完整性']
    scores = [5, 5, 4, 4]
    colors = ['#2ECC71', '#3498DB', '#F39C12', '#9B59B6']
    
    bars = ax3.barh(eval_items, scores, color=colors)
    ax3.set_xlim(0, 5.5)
    ax3.set_xlabel('评分 (1-5)', fontsize=11)
    ax3.set_title('可重复性评估', fontsize=12, fontweight='bold')
    ax3.grid(axis='x', alpha=0.3)
    
    for bar, val in zip(bars, scores):
        ax3.text(val + 0.1, bar.get_y() + bar.get_height()/2, 
                str(val), va='center', fontsize=11, fontweight='bold')
    
    # 方法总结
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')
    
    summary_text = """
    ┌─────────────────────────────────────┐
    │           分析结果总结               │
    ├─────────────────────────────────────┤
    │  聚类分析:                          │
    │  • 识别3类污染模式                   │
    │  • ANOVA显示部分气象因子显著         │
    │                                     │
    │  回归分析:                          │
    │  • 最佳模型: 氨氮 (R²=0.573)        │
    │  • 平均R² ≈ 0.20                    │
    │                                     │
    │  可重复性评分: 4.4/5                │
    └─────────────────────────────────────┘
    """
    ax4.text(0.5, 0.5, summary_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='center', horizontalalignment='center',
            family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "结果汇总图.png", dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  已保存: 结果汇总图.png")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("可视化图表生成 - 开始")
    print("=" * 60)
    
    create_tech_flowchart()
    create_method_comparison()
    create_results_summary()
    
    print("\n" + "=" * 60)
    print("可视化图表生成 - 完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
