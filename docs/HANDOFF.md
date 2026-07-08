# 项目交接

## Git 状态

- 当前已提交基线：`529e5a6 feat: add SQLite-backed analysis task management`
- 阶段 3：已实现并验证，尚未提交
- 当前分支：`main`
- 远程跟踪分支：`origin/main`
- 当前工作区包含安全上传、文件关联、迁移、测试、页面和文档改动。

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
| `frontend/src/api/files.ts` | 图片上传 API 与文件元数据类型 |
| `frontend/src/components/ImageUploader.vue` | 图片选择、预览和上传进度 |
| `frontend/src/views/AnalysisView.vue` | 创建任务页面 |
| `frontend/src/views/HistoryView.vue` | 历史任务页面 |
| `frontend/src/views/TaskDetailView.vue` | 任务详情页面 |
| `frontend/vite.config.ts` | Vite 端口与 API 代理 |
| `backend/run.py` | Flask 运行入口 |
| `backend/app/__init__.py` | Flask 应用工厂 |
| `backend/app/config.py` | 后端环境配置 |
| `backend/app/api/health.py` | 健康检查接口 |
| `backend/app/api/tasks.py` | 任务 REST API |
| `backend/app/api/files.py` | 文件上传与读取 REST API |
| `backend/app/models/analysis_task.py` | 任务 ORM 模型 |
| `backend/app/services/task_service.py` | 任务业务规则与状态机 |
| `backend/app/services/storage_service.py` | 图片验证、存储和安全路径解析 |
| `backend/app/models/uploaded_file.py` | 文件元数据与任务输入关联模型 |
| `backend/migrations/` | 数据库迁移历史 |
| `backend/app/utils/responses.py` | 统一成功响应 |
| `.env.example` | 可提交的配置模板 |

## 已知问题

- Vite 开发服务在源码结构发生变化后可能保留旧模块缓存；若 HTML 能打开但页面空白，应先查看 Vite 错误日志并重启 `npm.cmd run dev`。
- Windows PowerShell 读取无 BOM UTF-8 文件时可能显示中文乱码；浏览器和源码文件本身不一定损坏。
- 前端生产构建存在初始 chunk 大于 500 kB 的警告，当前不影响阶段 1 功能。
- 当前只实现任务级统一错误响应，尚未添加全局异常处理器。
- pytest cacheprovider 在当前受控 Windows 临时目录中会阻塞退出，已通过 `backend/pytest.ini` 禁用该非必要缓存插件。
- `.env.example` 中数据库与上传配置已生效；模型路径和推理设备配置尚未使用。
- 图片上传成功但任务创建失败时会留下未关联文件；当前没有自动清理孤立文件。
- 文件存储仍是本地目录，不适用于多实例部署。
- 当前只支持 JPEG、PNG，不支持 GeoTIFF、地理坐标或大图切片。

## 下一阶段建议目标

下一阶段建议只接入真实 YOLO 目标检测，其他三类任务继续保持 `planned`：

1. 定义统一模型适配器接口和模型注册机制。
2. 接入小型 YOLO 权重，默认 CPU，自动检测可用设备。
3. 将任务按 `pending → running → completed/failed` 更新。
4. 保存结构化检测框、类别和置信度，并生成结果预览图。
5. 在任务详情展示原图、检测图和检测列表。
6. 覆盖无目标、模型缺失、推理失败和 CPU 推理测试后再提交阶段 4。
