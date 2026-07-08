# 开发进度

更新时间：2026-07-08

## 阶段状态

| 阶段 | 状态 | 对应提交 |
|---|---|---|
| 阶段 0：环境与 Git | completed | `e060bef` |
| 阶段 1：Vue 3 与 Flask 最小闭环 | completed | `7bcb76a` |
| 阶段 2：SQLite 与任务管理 | completed | `529e5a6` |
| 阶段 3：安全图片上传与文件管理 | completed | 待提交 |

## 已实现功能

### 阶段 0

- 初始化 Git 仓库和 `main` 分支。
- 建立 `.gitignore`，排除密钥、上传文件、数据库、模型权重、依赖目录、日志和构建产物。
- 提供 `.env.example`、`environment.yml`、MIT License 和项目定位说明。
- 创建 Python 3.11 的 `rs-platform` Conda 环境定义。
- 明确项目是基于 2025 年实训方向进行的后续个人复现与工程化版本。

### 阶段 1

- 建立 Flask 应用工厂、配置类、健康检查 Blueprint 和统一成功响应。
- 实现 `GET /api/v1/health`。
- 建立 Vue 3、Vite、TypeScript、Vue Router、Axios 和 Element Plus 前端骨架。
- 实现 Dashboard 与 About 页面。
- Dashboard 支持后端健康检查的加载、成功和错误状态。
- Vite 将 `/api` 代理至本地 Flask 服务。
- 四个未来分析模块均标记为 `planned`，没有把未实现能力包装为已完成功能。

### 阶段 2

- 接入 Flask-SQLAlchemy、Flask-Migrate、Alembic 与 pytest。
- 建立 `analysis_tasks` 表、UUID 主键、任务类型约束和任务状态约束。
- 使用 SQLite 保存任务，并通过迁移版本 `20260706_0001` 管理表结构。
- 实现任务创建、分页列表、筛选、详情和单任务软删除 API。
- 建立 `pending → running → completed/failed` 状态转换规则；当前公共 API 不允许任意修改状态。
- 实现创建任务、历史任务和任务详情页面。
- 新建任务只保存为 `pending`，没有调用或模拟模型推理。

### 阶段 3

- 新增 `uploaded_files` 与 `task_input_files` 表，迁移版本为 `20260708_0002`。
- 实现 `POST /api/v1/files` 与 `GET /api/v1/files/{id}/content`。
- 支持 JPEG、PNG，默认请求上限 20 MB、像素上限 4000 万。
- 同时验证扩展名、MIME、实际图像格式、真实解码和图片尺寸。
- 使用 UUID 存储名，数据库只保存相对路径、SHA-256、宽高和文件元数据。
- 任务创建支持 `input_file_ids`，并通过关联表保存文件角色与顺序。
- 前端支持选择图片、本地预览、上传进度、服务端错误提示和任务详情图片展示。
- 当前仍不调用模型，新任务状态保持 `pending`。

## 本次已验证命令与结果

### 后端测试客户端

在 `backend/` 目录执行：

```powershell
conda run -n rs-platform python -c "from app import create_app; response=create_app().test_client().get('/api/v1/health'); assert response.status_code == 200; assert response.get_json()['data']['status'] == 'healthy'"
```

结果：通过，`GET /api/v1/health` 返回 HTTP 200，`data.status` 为 `healthy`。

### 前端生产构建

在 `frontend/` 目录执行：

```powershell
npm.cmd run build
```

结果：通过。TypeScript、Vue 类型检查与 Vite 构建成功，共转换 1664 个模块。

已知非阻塞警告：

- Rollup 移除了第三方依赖中位置不正确的 `PURE` 注释。
- 当前初始 JavaScript chunk 超过 500 kB，后续可在体验优化阶段考虑按需引入和代码分割。

### 运行中 API

请求 `http://127.0.0.1:5000/api/v1/health`。

结果：通过，运行中的服务返回 `healthy`。

### 阶段 2 后端测试

在 `backend/` 目录执行：

```powershell
python -m pytest -q
```

结果：`5 passed`。覆盖健康检查、创建/列表/详情、非法任务类型、软删除和状态转换规则。

### 数据库迁移一致性

```powershell
python -m flask --app run.py db upgrade
python -m flask --app run.py db check
```

结果：数据库升级至 `20260706_0001 (head)`，`No new upgrade operations detected.`。

### 浏览器任务闭环

结果：通过创建任务、详情展示、历史查询、软删除和空状态验证；浏览器控制台无错误。

### 阶段 3 文件测试

结果：后端共 `11 passed`。新增覆盖图片上传与读取、路径型文件名清理、非法扩展名、MIME 不匹配、伪图片、413 请求上限和任务文件关联。

### 阶段 3 浏览器验收

结果：上传页限制与提示正确；任务详情通过受控 API 加载 24×18 PNG，文件名、尺寸和角色正确，控制台无错误。

## 当前未实现

- MySQL 连接与 SQLite 到 MySQL 的兼容验证。
- 结果文件管理与孤立上传文件自动清理。
- YOLO、DINOv2、道路分割及任何真实模型推理。
- 变化检测 baseline。
- Leaflet 地图和结果图层。
- Redis、Celery、Docker 和正式部署。
- 登录、权限和多用户能力。
