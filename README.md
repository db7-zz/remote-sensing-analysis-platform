# Remote Sensing Intelligent Analysis Platform

遥感影像智能分析平台是一个面向学习与作品集展示的个人全栈 AI 项目。计划采用 Vue 3、Flask、PyTorch 与 SQLAlchemy，实现遥感图片上传、目标检测、土地覆盖分类、道路提取、基础变化检测、结果可视化和任务历史管理。

> [!IMPORTANT]
> 本项目基于本人 2025 年参与的遥感智能分析平台实训方向，在实训结束后使用公开数据、公开模型独立复现并逐步工程化完善。本仓库不是原实训系统的源代码，不代表任何企业、机构或官方产品。

## 当前开发状态

- 当前阶段：阶段 2 已完成，准备实现安全图片上传与文件管理。
- 已完成：仓库安全边界、Vue 3 与 Flask 闭环、SQLite 任务数据库、数据库迁移、任务 CRUD、历史任务和任务详情页面。
- 尚未实现：图片上传、文件元数据、模型推理和分析结果展示。

当前架构、阶段验证与交接信息见：

- [系统架构](docs/ARCHITECTURE.md)
- [开发进度](docs/PROGRESS.md)
- [项目交接](docs/HANDOFF.md)
- [技术决策](docs/DECISIONS.md)

所有能力会按实际完成状态标记为：

- `real_model`：已接入并验证的真实模型推理。
- `baseline`：已实现的传统或简化基线方法。
- `mock`：仅用于验证平台流程的模拟结果。
- `planned`：规划中，尚未实现。

## 开发顺序

1. Vue 3 与 Flask 健康检查闭环。
2. SQLite 任务管理与安全图片上传。
3. 真实 YOLO 目标检测 MVP。
4. DINOv2 特征分类、道路分割和变化检测 baseline。
5. Leaflet、MySQL、测试、文档与可选 Docker。

## 开发环境

- Python 3.11（通过 `environment.yml` 创建独立 Conda 环境）。
- Node.js 24 与 npm 11（前端将在阶段 1 初始化）。
- Git 2.x。

当前阶段只安装了 Flask 与 Vue 最小闭环所需依赖，尚未安装数据库或模型依赖。后续依赖会随对应功能接入并记录，避免引入暂时不用的软件包。

## 本地启动

创建并准备后端环境：

```powershell
conda env create -f environment.yml
conda run -n rs-platform python -m pip install -r backend\requirements.txt
Set-Location backend
conda run -n rs-platform python -m flask --app run.py db upgrade
Set-Location ..
```

启动 Flask API：

```powershell
conda run -n rs-platform python backend\run.py
```

在另一个终端安装并启动前端：

```powershell
Set-Location frontend
npm.cmd install
npm.cmd run dev
```

打开 `http://127.0.0.1:5173`。Dashboard 应显示“后端服务正常”；健康检查接口位于 `http://127.0.0.1:5000/api/v1/health`。

任务管理页面：

- 创建任务：`http://127.0.0.1:5173/analysis`
- 历史任务：`http://127.0.0.1:5173/tasks`

阶段 2 创建的任务只会保存为 `pending`，不会伪装成已经执行模型推理。

## 安全与仓库规则

- 不提交 `.env`、数据库密码或访问令牌。
- 不提交模型权重、大型数据集、用户上传文件或本地数据库。
- 模型和数据来源、许可及使用限制将在接入时逐项记录。
- 默认提供 CPU 可运行方案，GPU 仅作为可选加速。

## License

本仓库自行编写的代码使用 MIT License。模型、数据集、底图和第三方依赖分别遵循其各自许可证；MIT License 不会覆盖这些外部资源。
