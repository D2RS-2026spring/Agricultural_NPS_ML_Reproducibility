# GitHub Pages 发布指南

## 自动发布设置

本项目已配置 GitHub Actions，代码 push 到 main 分支后会自动渲染 Quarto 报告并发布到 GitHub Pages。

### 发布地址

报告发布后访问：`https://d2rs-2026spring.github.io/Agricultural_NPS_ML_Reproducibility/`

（注意：需要将 `d2rs-2026spring` 替换为你们组织的名称）

### 首次启用 GitHub Pages

1. 进入仓库：https://github.com/D2RS-2026spring/Agricultural_NPS_ML_Reproducibility

2. 点击 **Settings**（设置）

3. 在左侧菜单找到 **Pages**

4. 设置 Source：
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** / **/ (root)**

5. 点击 **Save**

6. 等待 1-2 分钟，网页会自动生成

### 工作流程

```
代码 push (main 分支)
       ↓
GitHub Actions 自动触发
       ↓
安装 Quarto + Python 环境
       ↓
运行 quarto render
       ↓
发布到 gh-pages 分支
       ↓
GitHub Pages 显示网站
```

### 手动触发

如果需要手动触发发布：

1. 进入仓库页面
2. 点击 **Actions** 标签
3. 选择 **Quarto Publish** 工作流
4. 点击 **Run workflow** > **Run workflow**

### 注意事项

- 首次启用可能需要 2-3 分钟才能看到网页
- 如果网页空白，检查 Actions 是否有错误
- GitHub Pages 链接格式：`https://[org].github.io/[repo-name]/`
