# 项目交接

## Git 状态

- 当前代码基线提交：`7bcb76a feat: establish Vue and Flask health check loop`
- 上一阶段提交：`e060bef chore: initialize remote sensing platform repository`
- 当前分支：`main`
- 远程跟踪分支：`origin/main`
- 本次交接开始前工作区：干净
- 本文档及其他交接文档尚未包含在上述代码基线提交中。

## 当前运行命令

首次准备后端环境：

```powershell
conda env create -f environment.yml
conda run -n rs-platform python -m pip install -r backend\requirements.txt
```

启动后端：

```powershell
conda run -n rs-platform python backend\run.py
```

首次准备前端：

```powershell
Set-Location frontend
npm.cmd install
```

启动前端：

```powershell
Set-Location frontend
npm.cmd run dev
```

验证前端构建：

```powershell
Set-Location frontend
npm.cmd run build
```

## 当前服务地址

- 前端 Dashboard：`http://127.0.0.1:5173/`
- 关于页：`http://127.0.0.1:5173/about`
- Flask API：`http://127.0.0.1:5000`
- 健康检查：`http://127.0.0.1:5000/api/v1/health`

本地服务不会在 Windows 重启后自动恢复，需要重新执行前后端启动命令。

## 核心文件

| 文件 | 作用 |
|---|---|
| `frontend/index.html` | 浏览器 HTML 入口 |
| `frontend/src/main.ts` | Vue 应用入口 |
| `frontend/src/App.vue` | 全局页面外壳 |
| `frontend/src/views/DashboardView.vue` | Dashboard 与健康状态逻辑 |
| `frontend/src/api/client.ts` | Axios 基础配置 |
| `frontend/src/api/system.ts` | 健康检查类型与请求函数 |
| `frontend/vite.config.ts` | Vite 端口与 API 代理 |
| `backend/run.py` | Flask 运行入口 |
| `backend/app/__init__.py` | Flask 应用工厂 |
| `backend/app/config.py` | 后端环境配置 |
| `backend/app/api/health.py` | 健康检查接口 |
| `backend/app/utils/responses.py` | 统一成功响应 |
| `.env.example` | 可提交的配置模板 |

## 已知问题

- Vite 开发服务在源码结构发生变化后可能保留旧模块缓存；若 HTML 能打开但页面空白，应先查看 Vite 错误日志并重启 `npm.cmd run dev`。
- Windows PowerShell 读取无 BOM UTF-8 文件时可能显示中文乱码；浏览器和源码文件本身不一定损坏。
- 前端生产构建存在初始 chunk 大于 500 kB 的警告，当前不影响阶段 1 功能。
- 当前只有成功响应辅助函数，错误响应规范尚未实现。
- 当前没有自动化测试文件；健康检查通过 Flask test client 命令验证。
- `.env.example` 已包含后续数据库和模型配置键，但对应功能尚未实现。

## 下一阶段建议目标

阶段 2 建议只实现 SQLite 与统一任务管理，不提前接入图片上传或模型：

1. 引入 Flask-SQLAlchemy 与 Flask-Migrate。
2. 默认使用 SQLite，并通过 `DATABASE_URL` 保留未来 MySQL 切换能力。
3. 建立最小任务模型和 `pending`、`running`、`completed`、`failed` 状态约束。
4. 实现任务创建、列表和详情 API。
5. 在前端增加历史任务与任务详情的最小页面。
6. 为任务 API 添加可重复执行的测试后，再提交阶段 2。

