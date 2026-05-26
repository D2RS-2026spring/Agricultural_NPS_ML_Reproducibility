# 农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

> 基于论文: Machine Learning for Agricultural Nonpoint Source Pollution Analysis: Insights from 5 Year Site-Specific Tracking

## 在线报告

**研究报告已发布到 GitHub Pages：**
https://d2rs-2026spring.github.io/Agricultural_NPS_ML_Reproducibility/

直接点击上方链接即可查看完整的研究报告，包括：
- 可交互的图表
- 代码展示与分析流程
- 聚类分析和回归结果

## 项目简介

本研究对发表在 *Sustainability* 期刊上的论文《Machine Learning for Agricultural Nonpoint Source Pollution Analysis: Insights from 5 Year Site-Specific Tracking》进行了完整的可重复性研究评估。

**研究方法**：
- **K-Means聚类**：识别不同的气象模式/污染情景
- **多元线性回归（MLR）**：建立气象因子与水质参数的关系模型

## 快速复现指南

### 环境要求

- Python >= 3.10
- uv 或 pip（推荐使用uv管理包）

### 复现步骤

```powershell
# 1. 克隆仓库
git clone https://github.com/D2RS-2026spring/Agricultural_NPS_ML_Reproducibility.git
cd Agricultural_NPS_ML_Reproducibility

# 2. 创建虚拟环境
uv venv --python 3.10
.venv\Scripts\activate

# 3. 安装依赖
uv pip install -r requirements.txt

# 4. 运行分析
python code/01_data_preprocessing.py
python code/02_kmeans_clustering.py
python code/03_multiple_regression.py
python code/04_visualization.py

# 5. 生成报告（可选）
quarto render report/reproducibility_report.qmd
```

## 研究成果

| 指标 | 结果 |
|-----|------|
| 最佳回归模型 | 氨氮预测 R² = 0.573 |
| 数据规模 | 24个数据文件，~270个样本 |
| 可重复性评分 | 4.6/5 |

## 小组分工

| 成员 | GitHub | 主要职责 |
|-----|--------|---------|
| 蒋奕达 | @jiangyida666 | 项目初始化、数据预处理、K-Means聚类 |
| 马志慧 | @mazhihui | 多元线性回归、结果验证 |
| 马明玮 | @mamingwei | 报告撰写、可视化 |

## 参考资料

- **原始论文**：https://doi.org/10.3390/su18010013
- **原始代码仓库**：https://github.com/jr198868/Machine_Learning_Nonpoint_Source_Pollution
- **在线报告**：https://d2rs-2026spring.github.io/Agricultural_NPS_ML_Reproducibility/

---

*本项目为 D2RS 课程可重复性研究作业*
