# 项目交接

## Git 状态

- 当前已提交基线：`c9083c7 docs: synchronize architecture progress and handoff status`
- 阶段 2：已实现并验证，包含在本阶段提交中
- 当前分支：`main`
- 远程跟踪分支：`origin/main`
- 阶段 2 提交包含任务管理代码、迁移、测试、页面和文档改动。

## 当前运行命令

首次准备后端环境：

```powershell
conda env create -f environment.yml
conda run -n rs-platform python -m pip install -r backend\requirements.txt
Set-Location backend
conda run -n rs-platform python -m flask --app run.py db upgrade
Set-Location ..
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
- 创建任务：`http://127.0.0.1:5173/analysis`
- 历史任务：`http://127.0.0.1:5173/tasks`

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
| `frontend/src/api/tasks.ts` | 任务类型与 API 请求函数 |
| `frontend/src/views/AnalysisView.vue` | 创建任务页面 |
| `frontend/src/views/HistoryView.vue` | 历史任务页面 |
| `frontend/src/views/TaskDetailView.vue` | 任务详情页面 |
| `frontend/vite.config.ts` | Vite 端口与 API 代理 |
| `backend/run.py` | Flask 运行入口 |
| `backend/app/__init__.py` | Flask 应用工厂 |
| `backend/app/config.py` | 后端环境配置 |
| `backend/app/api/health.py` | 健康检查接口 |
| `backend/app/api/tasks.py` | 任务 REST API |
| `backend/app/models/analysis_task.py` | 任务 ORM 模型 |
| `backend/app/services/task_service.py` | 任务业务规则与状态机 |
| `backend/migrations/` | 数据库迁移历史 |
| `backend/app/utils/responses.py` | 统一成功响应 |
| `.env.example` | 可提交的配置模板 |

## 已知问题

- Vite 开发服务在源码结构发生变化后可能保留旧模块缓存；若 HTML 能打开但页面空白，应先查看 Vite 错误日志并重启 `npm.cmd run dev`。
- Windows PowerShell 读取无 BOM UTF-8 文件时可能显示中文乱码；浏览器和源码文件本身不一定损坏。
- 前端生产构建存在初始 chunk 大于 500 kB 的警告，当前不影响阶段 1 功能。
- 当前只实现任务级统一错误响应，尚未添加全局异常处理器。
- pytest cacheprovider 在当前受控 Windows 临时目录中会阻塞退出，已通过 `backend/pytest.ini` 禁用该非必要缓存插件。
- `.env.example` 已包含后续数据库和模型配置键，但对应功能尚未实现。

## 下一阶段建议目标

下一阶段建议只实现安全图片上传与文件管理，不提前接入 YOLO：

1. 建立 `uploaded_files` 表和任务输入文件关联。
2. 仅允许 JPEG、PNG，并验证扩展名、MIME、实际解码和文件大小。
3. 使用 UUID 存储名，数据库只保存相对路径与元数据。
4. 实现上传、受控读取和图片预览。
5. 让任务通过文件 ID 引用输入图片。
6. 完成异常测试和浏览器上传闭环后再提交阶段 3。
