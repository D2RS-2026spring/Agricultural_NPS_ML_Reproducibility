[README.md](https://github.com/user-attachments/files/28203954/README.md)
# Agricultural NPS Machine Learning Reproducibility Project

## 农业面源污染K-Means聚类与多元回归分析 - 可重复性研究

---

## 一、项目概述

本项目对发表在 *Sustainability* 期刊上的论文《Machine Learning for Agricultural Nonpoint Source Pollution Analysis: Insights from 5 Year Site-Specific Tracking》进行完整的可重复性研究。

### 1.1 研究内容

- **研究区域**：美国北卡罗来纳州 NCSU Lake Wheeler Road Field Laboratory
- **监测时段**：2017-2021年（5年连续监测）
- **数据规模**：24个数据文件（6种污染物 × 4种作物）
- **核心方法**：K-Means聚类分析 + 多元线性回归（MLR）

### 1.2 参考论文

> Gao C-H et al. Machine Learning for Agricultural Nonpoint Source Pollution Analysis: Insights from 5 Year Site-Specific Tracking. *Sustainability* 2026, 18(1), 13.  
> DOI: https://doi.org/10.3390/su18010013  
> 原始代码：https://github.com/jr198868/Machine_Learning_Nonpoint_Source_Pollution

---

## 二、快速复现指南

### 2.1 环境要求

| 软件 | 版本要求 | 下载地址 |
|-----|---------|---------|
| Python | ≥ 3.10 | https://www.python.org/downloads/ |
| uv | 最新版 | `pip install uv` |

### 2.2 复现步骤（完整流程）

#### 第一步：克隆本仓库

```powershell
# 在终端中执行
git clone https://github.com/D2RS-2026spring/Agricultural_NPS_ML_Reproducibility.git
cd Agricultural_NPS_ML_Reproducibility
```

#### 第二步：创建Python虚拟环境

```powershell
# 使用uv创建虚拟环境（推荐）
uv venv --python 3.10
.venv\Scripts\activate

# 或使用conda
conda create -n nps_ml python=3.10
conda activate nps_ml
```

#### 第三步：安装依赖

```powershell
# 使用uv安装（推荐）
uv pip install -r requirements.txt

# 或使用pip
pip install -r requirements.txt
```

#### 第四步：运行分析代码

```powershell
# 依次运行以下4个脚本
python code/01_data_preprocessing.py
python code/02_kmeans_clustering.py
python code/03_multiple_regression.py
python code/04_visualization.py
```

**预期输出**：
- `results/01_data_summary/` - 数据摘要文件
- `results/02_clustering_results/` - 聚类结果（含散点图）
- `results/03_regression_results/` - 回归分析结果
- `results/04_visualizations/` - 可视化图表

#### 第五步：生成研究报告（可选）

```powershell
# 安装Quarto
# 下载地址：https://quarto.org/docs/get-started/

# 渲染HTML报告
quarto render report/reproducibility_report.qmd

# 或发布到GitHub Pages
quarto publish gh-pages
```

---

## 三、详细复现说明

### 3.1 数据预处理 (01_data_preprocessing.py)

**功能**：读取原始气象和水质数据，进行清洗和标准化

**输入**：
- `data/` 目录下的原始数据文件

**输出**：
- `results/01_data_summary/数据文件摘要.csv`

**运行**：
```powershell
python code/01_data_preprocessing.py
```

**预期运行时间**：约10秒

### 3.2 K-Means聚类分析 (02_kmeans_clustering.py)

**功能**：对6种污染物类型分别进行K-Means聚类，识别污染模式

**算法参数**：
- 聚类数量：K=3
- 特征：NPK, PK, NK, CK, OF（不同施肥处理）
- 降维：PCA（2维）用于可视化

**输出**：
- `results/02_clustering_results/scatter_plots/` - 25张聚类散点图
- `results/02_clustering_results/weather_summary_tables/` - 气象摘要表
- `results/02_clustering_results/*_anova.csv` - ANOVA分析结果

**运行**：
```powershell
python code/02_kmeans_clustering.py
```

**预期运行时间**：约2分钟

### 3.3 多元线性回归 (03_multiple_regression.py)

**功能**：建立气象因子与水质参数的回归模型

**回归公式**：
$$Y_j = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + ... + \beta_p X_p + \varepsilon$$

**因变量**：总氮(TN)、总磷(TP)、氨氮(NH₃-N)、硝态氮(NO₃-N)、溶解性磷、颗粒态磷

**自变量**：气象因子（温度、风速、降水量等）

**输出**：
- `results/03_regression_results/回归分析结果_*.csv` - 6个回归结果文件

**运行**：
```powershell
python code/03_multiple_regression.py
```

**预期运行时间**：约1分钟

### 3.4 可视化 (04_visualization.py)

**功能**：生成综合可视化图表

**输出**：
- `results/04_visualizations/技术路线图.png`
- `results/04_visualizations/方法对比图.png`
- `results/04_visualizations/结果汇总图.png`

**运行**：
```powershell
python code/04_visualization.py
```

---

## 四、常见问题与解决方案

### 4.1 依赖安装失败

**问题**：安装 `statsmodels` 时报错

**解决**：
```powershell
# Windows用户可能需要先安装Visual C++ Build Tools
# 或使用conda安装
conda install statsmodels
```

### 4.2 中文字体显示异常

**问题**：图表中文显示为方框

**解决**：
```python
# 在代码中添加
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```

### 4.3 数据文件缺失

**问题**：运行时报错找不到数据文件

**解决**：
```powershell
# 确保在项目根目录运行
cd Agricultural_NPS_ML_Reproducibility
python code/01_data_preprocessing.py
```

### 4.4 Quarto渲染失败

**问题**：quarto render 命令报错

**解决**：
```powershell
# 1. 检查Quarto是否正确安装
quarto --version

# 2. 如未安装，下载安装：https://quarto.org/docs/get-started/

# 3. 如渲染HTML，可直接用Python的markdown库生成
```

---

## 五、主要结果

### 5.1 聚类分析结果

| 评估指标 | 结果 |
|---------|------|
| 聚类数量 | 3类 |
| 覆盖作物 | 4种（玉米、水稻、柑橘、蔬菜） |
| 覆盖污染物 | 6种 |

**ANOVA分析**：部分气象因子在不同聚类间存在显著差异（p < 0.05）

### 5.2 回归分析结果

| 污染物类型 | 平均R² | 最佳R² | 最佳作物 |
|-----------|--------|--------|---------|
| 氨氮 | 0.205 | 0.573 | Corn |
| 溶解性磷 | 0.248 | 0.531 | Citrus |
| 硝态氮 | 0.213 | 0.509 | Rice |
| 颗粒态磷 | 0.188 | 0.328 | Corn |
| 总氮 | 0.196 | 0.415 | Vegetables |
| 总磷 | 0.198 | 0.411 | Citrus |

**结论**：气象因子对氨氮浓度具有较强的预测能力（R² = 0.573）

### 5.3 可重复性评估

| 评估维度 | 评分 | 说明 |
|---------|------|------|
| 数据可获取性 | ★★★★★ | 原始数据可从GitHub获取 |
| 代码可运行性 | ★★★★★ | 代码结构清晰，依赖明确 |
| 结果可复现性 | ★★★★☆ | 核心结果一致 |
| 文档完整性 | ★★★★★ | README详细，包含复现步骤 |

---

## 六、项目结构

```
Agricultural_NPS_ML_Reproducibility/
├── README.md                              # 本文件
├── requirements.txt                       # Python依赖包列表
├── LICENSE                                 # MIT许可证
├── .gitignore                              # Git忽略配置
├── data/                                   # 数据目录
│   └── README.md                          # 数据来源说明
├── code/                                   # 分析代码
│   ├── 01_data_preprocessing.py           # 数据预处理
│   ├── 02_kmeans_clustering.py            # K-Means聚类
│   ├── 03_multiple_regression.py         # 多元线性回归
│   └── 04_visualization.py                # 可视化
├── results/                                # 分析结果
│   ├── 01_data_summary/                  # 数据摘要
│   ├── 02_clustering_results/            # 聚类结果
│   ├── 03_regression_results/            # 回归结果
│   └── 04_visualizations/                # 可视化图表
├── report/                                 # 研究报告
│   └── reproducibility_report.qmd         # Quarto格式报告
└── logs/                                  # 执行日志
    └── analysis_log.txt
```

---

## 七、小组成员

| 成员 | 学号 | GitHub | 主要贡献 |
|-----|------|--------|---------|
| 蒋奕达 | 2025303110130 | @jiangyida666 | 项目初始化、代码整合 |
| 马志慧 | 2025303120061 | @mazhihui | 数据分析、结果验证 |
| 马明玮 | 2025303120062 | @mamingwei | 报告撰写、文档整理 |

---

## 八、复现环境信息

| 环境信息 | 内容 |
|---------|------|
| 操作系统 | Windows / macOS / Linux |
| Python版本 | 3.10+ |
| 包管理器 | uv (推荐) 或 pip |
| 分析工具 | pandas, numpy, scikit-learn, statsmodels |

**复现完成时间**：约5-10分钟（取决于电脑性能）

---

## 九、参考资料

1. **原始论文**：https://doi.org/10.3390/su18010013
2. **原始代码仓库**：https://github.com/jr198868/Machine_Learning_Nonpoint_Source_Pollution
3. **Python文档**：https://docs.python.org/
4. **scikit-learn文档**：https://scikit-learn.org/
5. **Quarto文档**：https://quarto.org/docs/

---

*本项目为D2RS课程可重复性研究作业，遵循MIT许可证*
