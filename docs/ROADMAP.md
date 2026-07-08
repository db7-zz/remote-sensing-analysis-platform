
# 遥感影像智能分析平台：完整开发计划

## 1. 项目总体定位

### 1.1 基本定义

- **项目名称**：Remote Sensing Intelligent Analysis Platform
- **中文名称**：遥感影像智能分析平台
- **仓库建议名称**：`remote-sensing-analysis-platform`
- **一句话定位**：基于公开遥感数据、公开预训练模型和 Web 技术构建的个人遥感影像智能分析演示平台。
- **使用场景**：上传遥感图片，执行目标检测、土地覆盖分类、道路提取或变化检测，并查看、对比和保存分析结果。
- **主要受众**：招聘面试官、教师、同学，以及希望了解遥感 AI 工程化流程的开发者。

### 1.2 项目边界

**必须做**

- Vue3 + Flask 前后端应用。
- 统一的上传、任务创建、推理、结果保存和历史查询流程。
- 真实接入一个 YOLO 目标检测模型。
- 土地分类、道路提取、变化检测具备清晰的 MVP 或演示实现。
- SQLite 开局，并能通过配置切换 MySQL。
- CPU 可运行，GPU 可选。
- 完整披露数据、模型来源及项目性质。

**建议做**

- Leaflet 地图底图与结果图层叠加。
- 模型注册信息和系统运行信息。
- API、模型适配器和文件存储的模块化设计。
- Docker 部署说明。

**可选做**

- DINOv2 特征缓存与轻量分类器训练。
- 深度学习道路分割模型。
- Siamese/Transformer 变化检测扩展。
- 异步任务队列。

**暂不做**

- 用户、权限、支付、通知和复杂审计。
- Kubernetes、微服务和分布式推理。
- 科研级模型训练与精度承诺。
- 完整 GeoTIFF 投影、切片服务和矢量路网拓扑。
- 将普通 RGB 图片伪装成具有真实地理坐标的 GIS 数据。

### 1.3 MVP 与完整版本

**MVP**

用户上传单张图片，创建目标检测任务；后端真实调用 YOLO；前端显示检测框结果图、类别、置信度和历史记录。其他三类任务可以显示为“开发中”，或使用明确标注的 mock 演示结果。

**完整版本**

四类任务均具有可执行实现；包含统一任务管理、模型说明、结果对比、基础地图叠加、SQLite/MySQL 切换、测试、截图、演示材料和部署文档。

### 1.4 GitHub 中的准确描述

不得使用“复刻百度内部平台”“独立完成了 2025 年全部平台”等措辞。推荐表述：

> 本项目是基于本人 2025 年参与的遥感智能分析平台实训方向，在实训结束后使用公开数据、公开模型和个人技术栈进行的独立复现、功能完善与工程化实践。它不是原实训系统、任何企业内部系统或官方产品的源代码复刻。

### 1.5 中文项目简介

> 遥感影像智能分析平台是一个面向个人学习与作品集展示的全栈 AI 项目。平台采用 Vue3、Flask、PyTorch 和 SQLAlchemy，支持遥感图片上传、目标检测、土地覆盖分类、道路提取、基础变化检测、结果可视化和任务历史查询。本项目源于本人 2025 年参与的相关实训方向，当前仓库是实训结束后基于公开数据和公开模型独立完成的个人复现与工程化演示版本，不代表原实训项目或任何企业官方产品。

### 1.6 英文项目简介

> Remote Sensing Intelligent Analysis Platform is a personal full-stack AI portfolio project built with Vue 3, Flask, PyTorch, and SQLAlchemy. It demonstrates image upload, object detection, land-cover classification, road extraction, baseline change detection, result visualization, and task history management. The project was independently reproduced and extended after my participation in a related remote-sensing training project in 2025, using public datasets and public models. It is not the original training system or an official product of any organization.

---

## 2. 推荐技术架构

### 2.1 分层设计

| 层 | 推荐技术 | 职责 |
|---|---|---|
| 前端层 | Vue3、Vite、TypeScript、Vue Router、Pinia、Axios、Element Plus | 页面、表单、上传、状态展示、结果可视化 |
| API 层 | Flask、Flask-CORS、Flask-SQLAlchemy | 参数校验、任务管理、模型调用、响应封装 |
| 推理层 | 同进程同步推理，统一推理服务 | 选择模型适配器、更新任务状态、记录耗时和错误 |
| 模型层 | PyTorch、Ultralytics、Transformers/timm、OpenCV | 模型加载、预处理、推理、后处理 |
| 数据层 | SQLite → MySQL、SQLAlchemy、Alembic/Flask-Migrate | 保存文件、任务、模型和结果元数据 |
| 文件层 | 本地目录 | 保存原图、结果图和临时文件 |
| 地图层 | Leaflet、vue-leaflet | 底图、透明结果图层和基础交互 |
| 配置层 | `.env`、python-dotenv、前端环境变量 | 数据库、文件目录、模型路径和运行模式 |
| 测试层 | pytest、Flask test client、Vitest、Playwright 可选 | API、服务和关键页面测试 |
| 文档层 | README、`docs/`、截图、架构图 | 复现说明、来源披露、演示和项目定位 |

### 2.2 前端库

**必须做**

- Vue3、Vite、TypeScript。
- Vue Router：页面路由。
- Axios：API 请求。
- Element Plus：表格、上传、表单、提示和进度组件。
- Pinia：系统配置、模型信息等跨页面状态。

**建议做**

- ECharts：Dashboard 任务统计。
- Leaflet + `@vue-leaflet/vue-leaflet`：地图展示。
- `dayjs`：时间格式化。

不要同时引入多套 UI 框架。

### 2.3 Flask 基础库

- Flask：Web API。
- Flask-CORS：开发阶段跨域。
- Flask-SQLAlchemy：数据库抽象。
- Flask-Migrate：从阶段 2 开始管理表结构升级。
- python-dotenv：读取环境变量。
- Pillow、OpenCV：图片验证与处理。
- pytest：测试。
- PyMySQL：MySQL 驱动。
- Ultralytics：YOLO 推理。

参数校验初期可使用手写服务层校验；项目稳定后再考虑 Pydantic，不必第一天增加复杂度。

### 2.4 存储策略

文件按用途分开：

- `uploads/original/`：用户上传原图。
- `uploads/results/`：绘制后的结果图、掩膜图。
- `uploads/temp/`：暂存文件。
- 数据库仅保存文件 ID、相对存储路径、公开访问 URL、校验值和元数据。
- 不把图片二进制、模型权重或大型结果数组存入数据库。
- 文件名由 UUID 生成；原始文件名只作为元数据保存。
- API 根据文件 ID 返回内容，避免前端接触本机绝对路径。

### 2.5 数据库与基础设施选择

**SQLAlchemy：需要。**  
它能让 SQLite 和 MySQL 共享大部分模型及查询代码，适合作品集展示。

**Celery、Redis：MVP 不需要。**  
MVP 采用同步推理和状态字段。若单次推理持续超过约 10–20 秒、需要并发或任务恢复，再引入任务队列。

**Docker：MVP 不需要，阶段 11 可选。**  
先确保 Windows 原生环境可运行，再提供后端和数据库的容器化方案。

**MySQL：阶段 2 接入，第一周不作为阻塞条件。**

### 2.6 文本架构图

```text
Browser
  │
  ├─ Vue3 UI
  │    ├─ 上传与任务表单
  │    ├─ 任务状态/历史
  │    ├─ 图片结果对比
  │    └─ Leaflet 地图
  │
  └─ HTTP / REST API
       │
       └─ Flask API
            ├─ 参数与图片校验
            ├─ Task Service
            │    ├─ 创建/更新任务
            │    └─ 调用 Inference Service
            ├─ Model Registry
            │    ├─ YOLO Adapter
            │    ├─ DINOv2 Classifier Adapter
            │    ├─ Road Segmentation Adapter
            │    └─ Baseline Change Adapter
            ├─ Storage Service ── 本地文件目录
            └─ SQLAlchemy ── SQLite / MySQL
```

该架构规模适中，既能解释完整 AI 产品链路，也不会因基础设施过重而挤占模型和展示工作的时间。

---

## 3. 项目目录结构

标记：`[D1]` 第一天创建，`[L]` 后续创建，`[IGN]` 不提交。

```text
remote-sensing-analysis-platform/
├─ README.md                         [D1] 项目定位、启动方式、来源和截图
├─ LICENSE                           [D1] 仓库代码许可证
├─ .gitignore                        [D1] 排除环境、权重、上传和密钥
├─ .env.example                      [D1] 环境变量模板，不含真实密码
├─ docker-compose.yml                [L] 可选部署编排
│
├─ frontend/
│  ├─ package.json                   [D1] 前端依赖与脚本
│  ├─ vite.config.ts                 [D1] Vite 与开发代理配置
│  ├─ tsconfig.json                  [D1] TypeScript 配置
│  ├─ index.html                     [D1] SPA 入口
│  ├─ .env.example                   [D1] API 基础地址示例
│  └─ src/
│     ├─ main.ts                     [D1] Vue 启动入口
│     ├─ App.vue                     [D1] 根组件
│     ├─ router/index.ts             [D1] 页面路由
│     ├─ layouts/MainLayout.vue      [D1] 顶部导航与内容布局
│     ├─ views/
│     │  ├─ DashboardView.vue        [D1] 首页
│     │  ├─ AnalysisView.vue         [D1] 创建分析任务
│     │  ├─ TaskDetailView.vue       [D1] 结果详情
│     │  ├─ HistoryView.vue          [L] 历史任务
│     │  ├─ ModelsView.vue           [L] 模型说明
│     │  └─ AboutView.vue            [L] 项目声明
│     ├─ components/
│     │  ├─ ImageUploader.vue        [D1] 图片上传
│     │  ├─ TaskStatus.vue           [D1] 状态展示
│     │  ├─ ResultViewer.vue         [D1] 原图与结果对比
│     │  ├─ DetectionList.vue        [L] 检测列表
│     │  ├─ MaskOverlay.vue          [L] 掩膜叠加
│     │  └─ MapViewer.vue            [L] Leaflet 地图
│     ├─ api/
│     │  ├─ client.ts                [D1] Axios 实例
│     │  ├─ files.ts                 [D1] 上传接口
│     │  ├─ tasks.ts                 [D1] 任务接口
│     │  └─ models.ts                [L] 模型接口
│     ├─ stores/system.ts            [L] 全局系统信息
│     ├─ types/api.ts                [D1] 响应类型
│     └─ styles/index.css            [D1] 全局视觉样式
│
├─ backend/
│  ├─ requirements.txt               [D1] 运行依赖
│  ├─ requirements-dev.txt           [L] 测试开发依赖
│  ├─ run.py                         [D1] 本地入口
│  ├─ migrations/                    [L] 数据库迁移记录
│  ├─ app/
│  │  ├─ __init__.py                 [D1] 应用工厂
│  │  ├─ config.py                   [D1] 配置分类
│  │  ├─ extensions.py               [D1] 数据库、迁移等扩展
│  │  ├─ api/
│  │  │  ├─ health.py                [D1] 健康检查
│  │  │  ├─ files.py                 [L] 文件上传与读取
│  │  │  ├─ tasks.py                 [L] 任务接口
│  │  │  ├─ models.py                [L] 模型列表
│  │  │  └─ system.py                [L] 系统信息
│  │  ├─ models/
│  │  │  ├─ uploaded_file.py         [L] 文件 ORM
│  │  │  ├─ analysis_task.py         [L] 任务 ORM
│  │  │  ├─ task_result.py           [L] 结果 ORM
│  │  │  └─ model_registry.py        [L] 模型 ORM
│  │  ├─ schemas/                    [L] 请求与响应字段定义
│  │  ├─ services/
│  │  │  ├─ storage_service.py       [L] 文件存储
│  │  │  ├─ task_service.py          [L] 状态流转
│  │  │  └─ inference_service.py     [L] 推理入口
│  │  ├─ inference/
│  │  │  ├─ base.py                  [L] 适配器统一接口
│  │  │  ├─ registry.py              [L] 模型适配器注册
│  │  │  ├─ yolo_detector.py         [L] 目标检测
│  │  │  ├─ dinov2_classifier.py     [L] 分类
│  │  │  ├─ road_segmenter.py        [L] 道路提取
│  │  │  └─ change_baseline.py       [L] 基础变化检测
│  │  └─ utils/
│  │     ├─ responses.py             [D1] 统一响应
│  │     ├─ validators.py            [L] 文件和参数验证
│  │     └─ image_utils.py           [L] 图片处理
│  └─ tests/
│     ├─ conftest.py                 [L] 测试配置
│     ├─ test_health.py              [L] 健康检查测试
│     ├─ test_files.py               [L] 文件接口测试
│     └─ test_tasks.py               [L] 任务流程测试
│
├─ models/
│  ├─ README.md                      [L] 权重下载和许可说明
│  ├─ weights/                       [IGN] 本地模型权重
│  └─ classifiers/                   [IGN] 训练产生的小型分类器
├─ scripts/
│  ├─ download_models.ps1            [L] Windows 权重获取辅助脚本
│  ├─ seed_models.py                 [L] 初始化模型注册信息
│  └─ check_environment.py           [L] 环境检测
├─ sample_data/
│  ├─ README.md                      [L] 样例来源和许可
│  └─ demo/                          [L] 可合法提交的少量样例
├─ docs/
│  ├─ architecture.md                [L] 架构说明
│  ├─ api.md                         [L] API 文档
│  ├─ data-and-models.md             [L] 来源及许可
│  ├─ deployment.md                  [L] 部署说明
│  └─ limitations.md                 [L] 局限与降级说明
├─ screenshots/                      [L] README 使用的精选截图
├─ uploads/                          [IGN] 用户上传和生成结果
├─ instance/                         [IGN] SQLite 数据库
└─ logs/                             [IGN] 本地日志
```

### `.gitignore` 至少包含

- `.env`、`.env.local` 和真实密钥。
- `venv/`、`.venv/`、`node_modules/`。
- `__pycache__/`、pytest 和构建缓存。
- `dist/`、`logs/`、`uploads/`、`instance/`。
- `models/weights/`、`*.pt`、`*.pth`、`*.onnx`、`*.ckpt`。
- 大型数据集和数据库文件。
- IDE、操作系统临时文件。

`sample_data/demo/` 只能提交少量、许可允许、已记录来源的演示图片。

---

## 4. 分阶段 Roadmap

### 阶段 0：环境检查与仓库初始化

- **目标**：建立可追踪、无敏感信息的项目骨架。
- **工作量**：0.5 天。
- **前置条件**：Windows、Git、Python、Node.js 已安装。
- **文件**：根 README、LICENSE、`.gitignore`、`.env.example`、前后端基础目录。
- **依赖**：暂不接入模型；只确认包管理工具可用。
- **功能**：仓库初始化、项目定位声明、环境版本记录。
- **验证**：Git 状态干净；敏感文件、上传目录、模型权重不会进入暂存区。
- **风险**：中文或带空格路径引发工具兼容问题；建议仓库放在简短英文路径。
- **证据**：初始目录截图、环境版本记录。
- **提交**：适合。
- **Commit**：`chore: initialize project structure and documentation`

### 阶段 1：前后端最小闭环（P0，重点）

- **目标**：Vue 页面能访问 Flask 健康检查，并显示后端状态。
- **工作量**：1 天。
- **前置条件**：阶段 0 完成。
- **文件**：
  - 前端入口、路由、主布局、Dashboard、Axios 客户端。
  - 后端应用工厂、配置、健康检查、统一响应、运行入口。
- **依赖**：
  - 前端：Vue、Vite、TypeScript、Router、Axios、Element Plus。
  - 后端：Flask、Flask-CORS、python-dotenv。
- **实施顺序**：
  1. 后端实现 `/api/v1/health`。
  2. 浏览器单独验证 API。
  3. 前端建立 Dashboard 和导航。
  4. Axios 读取 API 基础地址。
  5. 页面显示“后端在线/离线”和版本信息。
  6. 配置开发代理或严格限定本地 CORS 来源。
- **可验证标准**：
  - 前后端分别启动。
  - Dashboard 自动请求健康检查。
  - 后端关闭时显示可理解的错误状态。
  - 刷新任意前端路由不会出现设计层错误。
- **风险**：
  - 端口冲突：统一记录默认端口并允许环境变量覆盖。
  - CORS：优先使用 Vite 代理；CORS 只开放前端开发地址。
  - Axios 地址错误：在开发者工具检查实际请求 URL。
- **证据**：Dashboard 在线状态截图、浏览器 Network 成功响应。
- **提交**：适合。
- **Commit**：`feat: establish Vue and Flask development loop`

### 阶段 2：数据库与任务管理（P1，重点）

- **目标**：不依赖模型即可创建、查询和查看任务。
- **工作量**：1–1.5 天。
- **前置条件**：阶段 1 API 正常。
- **文件**：ORM 模型、数据库扩展、迁移目录、任务服务、任务 API、History 页面。
- **依赖**：Flask-SQLAlchemy、Flask-Migrate；MySQL 阶段再加 PyMySQL。
- **实施顺序**：
  1. 默认连接 SQLite。
  2. 建立四张核心表。
  3. 定义统一任务类型和状态。
  4. 实现任务列表、详情、创建和删除接口。
  5. 使用 mock 结果模拟 `pending → running → completed`。
  6. 前端实现历史表格和详情跳转。
  7. 再用环境变量验证 MySQL 连接，不改变业务代码。
- **验证**：
  - 创建任务后数据库出现记录。
  - 列表支持分页、状态和任务类型筛选。
  - 无效任务 ID 返回 404。
  - 重启后 SQLite 任务仍存在。
- **风险**：
  - SQLite 与 MySQL 的 JSON、布尔值和时间行为不同。
  - 迁移记录和 ORM 模型不同步。
  - MySQL 字符集必须使用 `utf8mb4`。
- **证据**：任务历史页、任务详情页、数据库记录截图。
- **提交**：适合。
- **Commit**：`feat: add persistent analysis task management`

### 阶段 3：图片上传与文件管理（P1，重点）

- **目标**：安全上传图片，保存元数据并在前端预览。
- **工作量**：1 天。
- **前置条件**：数据库和任务 API 可用。
- **文件**：文件 ORM、存储服务、验证器、上传 API、ImageUploader。
- **依赖**：Pillow、OpenCV（OpenCV 可在模型阶段加入）。
- **实施顺序**：
  1. 仅允许 JPEG、PNG；GeoTIFF 暂缓。
  2. 设置单文件大小上限，例如 20 MB。
  3. 同时检查扩展名、MIME 和图片解码。
  4. 使用 UUID 保存，不信任原始文件名。
  5. 保存尺寸、大小、SHA-256、原始名称和相对路径。
  6. 返回 `file_id` 与受控访问 URL。
  7. 任务通过 `file_id` 引用上传文件。
- **验证**：
  - 合法图片可预览。
  - 非图片、空文件、超限文件被明确拒绝。
  - 同名文件不会相互覆盖。
  - API 不暴露 Windows 绝对路径。
- **风险**：反斜杠路径、中文文件名、大图内存占用、孤立文件。
- **降级**：只支持 JPEG/PNG，上传后缩放生成推理副本，保留原图。
- **证据**：上传预览、失败提示、文件元数据截图。
- **提交**：适合。
- **Commit**：`feat: implement validated image upload and storage`

### 阶段 4：YOLO 目标检测（P2，MVP 核心）

- **目标**：形成首个真实模型端到端闭环。
- **工作量**：2–3 天。
- **前置条件**：上传和任务流程稳定。
- **文件**：推理基类、注册表、YOLO 适配器、推理服务、结果 ORM、结果展示组件、模型说明。
- **依赖**：PyTorch、torchvision、Ultralytics、OpenCV。
- **实施顺序**：
  1. 定义统一适配器接口：元信息、加载、预测、健康状态。
  2. 首次使用小型 YOLO 权重，CPU 默认。
  3. 应用输入尺寸、置信度和 NMS 配置。
  4. 保存结构化检测结果。
  5. 生成带框结果图。
  6. 更新任务状态和耗时。
  7. 前端显示原图、结果图、检测列表、模型名与推理设备。
  8. 使用遥感样例做演示，但明确通用权重不保证覆盖建筑等遥感类别。
- **验证**：
  - 一次真实上传可以完成推理。
  - 任务状态正确落库。
  - 检测 JSON 与结果图一致。
  - 无目标时正常完成并显示“未检测到目标”。
  - CPU 环境可运行。
- **风险**：
  - 通用 YOLO 对俯视小目标表现较弱。
  - 权重下载失败或 PyTorch 环境冲突。
  - 首次加载缓慢。
- **降级**：
  - 使用最小模型与较低输入分辨率。
  - 提供手动权重放置说明。
  - 预加载模型但不启动复杂常驻服务。
- **证据**：完整分析页、检测列表、历史详情、CPU 推理耗时。
- **提交**：适合，也是 MVP 里程碑。
- **Commit**：`feat: integrate real YOLO object detection pipeline`

### 阶段 5：土地覆盖分类（P3）

- **目标**：使用 DINOv2 特征和轻量分类头完成场景/局部分类。
- **工作量**：2–4 天。
- **前置条件**：统一推理适配器完成；准备合法标签样例。
- **文件**：DINOv2 适配器、分类器文件说明、特征准备脚本、分类结果组件。
- **依赖**：Transformers 或 torch.hub 二选一、scikit-learn、joblib。
- **功能**：
  - DINOv2 冻结，仅提取特征。
  - 使用少量公开样例训练 Logistic Regression 或线性分类头。
  - 输出前若干类别及置信分数。
- **验证**：模型和标签版本可追踪；未安装分类头时返回明确不可用状态。
- **风险**：用户要求的“水体、道路”等像素级类别与整图分类不是同一任务。
- **降级**：将 MVP 明确命名为“图块主导土地覆盖分类”；像素级土地覆盖作为未来语义分割方向。
- **证据**：分类卡片、类别概率、模型说明页。
- **提交**：适合。
- **Commit**：`feat: add DINOv2 feature-based land cover classification`

### 阶段 6：道路提取（P4）

- **目标**：输出道路概率或二值掩膜，并支持透明叠加。
- **工作量**：2–4 天。
- **前置条件**：掩膜结果格式确定。
- **文件**：道路分割适配器、掩膜工具、MaskOverlay。
- **依赖**：segmentation-models-pytorch 可选。
- **功能**：加载公开许可的轻量 U-Net/DeepLabV3 权重；缩放、推理、阈值化、形态学清理。
- **验证**：原图、掩膜、叠加图尺寸一致；无可用权重时不生成伪结果。
- **风险**：通用预训练分割模型通常没有“道路”类别。
- **降级**：若无法获得许可明确且兼容的权重，将本模块标记为实验性 Demo，并使用少量公开道路数据微调轻量 U-Net，或延后真实接入。
- **证据**：原图/掩膜/叠加三联图。
- **提交**：适合。
- **Commit**：`feat: add experimental road segmentation workflow`

### 阶段 7：变化检测（P5）

- **目标**：实现明确标注的可解释 baseline。
- **工作量**：1.5–3 天。
- **前置条件**：上传支持两个输入文件。
- **文件**：变化检测适配器、双图上传表单、对齐与差分工具。
- **依赖**：OpenCV、scikit-image。
- **功能**：
  - 检查两图尺寸。
  - 可选特征匹配与单应性粗配准。
  - 使用绝对差分或 SSIM 差异。
  - 阈值化、去噪和区域高亮。
- **验证**：同一图片输入应接近零变化；明显编辑区域能被标记。
- **风险**：季节、光照、视角和错位会产生大量伪变化。
- **降级**：要求用户提供已对齐、相近成像条件的 RGB 图片；显示明确限制。
- **证据**：前图、后图、差异图、掩膜四联图。
- **提交**：适合。
- **Commit**：`feat: implement explainable baseline change detection`

### 阶段 8：地图交互与结果可视化（P6）

- **目标**：展示基础底图和半透明分析图层。
- **工作量**：1.5–2 天。
- **前置条件**：结果图片可访问。
- **文件**：MapViewer、图层配置、地图说明。
- **依赖**：Leaflet、vue-leaflet。
- **功能**：
  - 底图缩放和平移。
  - 使用演示边界将结果图作为 ImageOverlay 叠加。
  - 提供透明度滑块和图层开关。
  - 明示无地理信息图片的范围是演示坐标，不代表真实定位。
- **验证**：图层显示、隐藏、透明度调整有效。
- **风险**：在线底图受网络和服务条款影响。
- **降级**：地图不可用时仍保留普通图片对比视图。
- **证据**：地图图层叠加截图。
- **提交**：适合。
- **Commit**：`feat: add Leaflet-based result overlay visualization`

### 阶段 9：测试、错误处理与体验优化（P7）

- **目标**：让演示路径稳定且错误可解释。
- **工作量**：2–3 天。
- **文件**：后端测试、前端组件测试、错误边界和日志配置。
- **依赖**：pytest、Vitest；Playwright 可选。
- **功能**：API 测试、状态流测试、文件校验、404/500、加载骨架、按钮防重复提交。
- **验证**：关键测试通过；断网、无模型、错误文件时页面不崩溃。
- **风险**：只测试成功路径。
- **证据**：测试结果、错误状态页面。
- **提交**：适合。
- **Commit**：`test: cover core upload task and inference workflows`

### 阶段 10：GitHub 文档、截图与包装（P7）

- **目标**：陌生人可以理解、安装、演示并准确判断个人贡献。
- **工作量**：2 天。
- **文件**：README、来源说明、架构图、限制说明、截图和演示 GIF。
- **依赖**：无需新增运行依赖。
- **验证**：在新目录按 README 可以运行 MVP；所有截图与当前界面一致。
- **风险**：文档夸大模型能力或遗漏许可。
- **证据**：README 预览、演示录屏。
- **提交**：适合。
- **Commit**：`docs: complete reproducibility and portfolio documentation`

### 阶段 11：可选部署与 Docker 化

- **目标**：提供可复现部署路径，不影响本地原生运行。
- **工作量**：2–3 天。
- **文件**：Dockerfile、Compose、部署说明。
- **依赖**：Docker Desktop，可选。
- **功能**：前端构建、Flask 服务、MySQL；权重通过卷挂载。
- **验证**：干净环境能启动健康检查和前端。
- **风险**：镜像巨大、Windows 文件挂载慢、GPU 配置复杂。
- **降级**：只容器化 Web 与数据库，模型权重保持本地挂载；CPU 为默认。
- **证据**：容器状态和运行页面。
- **提交**：适合。
- **Commit**：`chore: add optional Docker deployment workflow`

---

## 5. MVP 功能定义

### 5.1 必须页面

1. **Dashboard**
   - 项目定位、模块入口、系统在线状态、最近任务。
2. **智能分析任务页**
   - 任务类型选择、图片上传、图片预览、模型与阈值设置、提交按钮。
3. **任务详情页**
   - 状态、输入图、结果图、检测列表、模型和耗时。
4. **历史任务页**
   - 任务 ID、类型、状态、缩略图、创建时间和详情入口。
5. **模型说明页**
   - 真实接入与 mock/规划中的能力必须区分。
6. **关于项目页**
   - 个人复现声明、来源、限制和技术栈。

### 5.2 MVP 任务范围

- **必须真实接入**：YOLO 目标检测。
- **允许 mock**：土地分类、道路提取。
- **建议真实 baseline**：变化检测；若第一周时间不足可延期。
- 所有 mock 必须在 UI 和返回数据中显示 `implementation: mock`，不得伪装成模型推理。

### 5.3 用户流程

1. 打开 Dashboard，确认后端和 YOLO 状态。
2. 进入智能分析页，选择“目标检测”。
3. 上传 JPEG/PNG 并预览。
4. 选择模型和置信度，创建任务。
5. 页面显示上传、运行、完成状态。
6. 跳转详情页，查看带框图片和检测列表。
7. 返回历史页重新打开任务。

### 5.4 MVP 验收标准

- CPU 环境可完成一次真实目标检测。
- 上传、任务、结果、历史记录重启后仍可查询。
- 检测结果包含类别、置信度和边界框。
- 无目标、模型缺失、图片非法时均有明确提示。
- 数据库和 API 不保存或暴露绝对本机路径。
- README 能指导另一台电脑运行 MVP。
- 页面明确披露项目性质和模型限制。

---

## 6. 前端页面与交互设计

统一视觉方向：浅色背景、深蓝灰文字、遥感绿/蓝作为强调色，大留白、轻阴影、圆角适中。采用“作品展示站 + 分析工作台”，避免密集企业后台菜单。

### 6.1 Dashboard

- **目标**：30 秒内说明项目是什么、能做什么。
- **组件**：标题区、四模块卡片、系统状态、任务统计、最近任务。
- **数据**：系统信息、模型列表、任务列表。
- **API**：`GET /health`、`GET /system`、`GET /models`、`GET /tasks?limit=5`。
- **空状态**：引导创建第一个任务。
- **加载**：卡片骨架屏。
- **错误**：后端离线提示和检查建议。
- **截图**：四模块、在线状态、真实最近任务同时出现。

### 6.2 智能分析任务页

- **目标**：最短路径创建任务。
- **组件**：任务选项卡、上传区、预览、模型参数、提交按钮。
- **数据**：模型列表、上传结果。
- **API**：上传文件、创建任务。
- **空状态**：上传示例和格式限制。
- **加载**：上传进度、提交禁用、推理状态。
- **错误**：文件、网络、模型不可用分别提示。
- **截图**：上传预览、已选目标检测、模型与参数。

变化检测选择后切换为双上传区；其他页面结构不变。

### 6.3 任务详情页

- **目标**：完整解释一次分析。
- **组件**：状态头、结果摘要、原图/结果图对比、检测列表、模型元信息。
- **数据**：任务详情和文件资源。
- **API**：`GET /tasks/{id}`、文件访问接口。
- **空状态**：无目标、尚未产生结果或结果已清理。
- **加载**：运行中自动轮询；建议 2 秒一次，完成后停止。
- **错误**：显示失败原因和重试入口；不展示 Python 堆栈。
- **截图**：结果框、检测列表、模型名、CPU/GPU、耗时。

### 6.4 历史任务页

- **目标**：查询和复现过去的演示结果。
- **组件**：筛选器、表格/卡片、分页、删除确认。
- **API**：任务列表、详情、删除。
- **空状态**：创建任务按钮。
- **加载**：表格骨架。
- **错误**：保留当前筛选条件并允许重试。
- **截图**：四类任务和不同状态；不得使用伪造成功任务冒充真实模型。

### 6.5 模型说明页

- **目标**：解释每个模型的来源、状态、限制和设备要求。
- **组件**：模型卡片、实现状态徽标、来源链接、许可、输入输出。
- **API**：模型列表。
- **空状态**：显示“未注册模型”及配置提示。
- **加载/错误**：卡片骨架、静态说明回退。
- **截图**：YOLO 标为真实；变化检测标为 baseline；未来模型标为 planned。

### 6.6 关于项目页

- **目标**：披露项目背景、个人贡献和非官方性质。
- **组件**：项目说明、架构、时间线、来源、限制。
- **数据**：以静态文档为主。
- **API**：通常不需要。
- **截图**：项目声明和架构图。

---

## 7. 后端 API 设计

### 7.1 统一响应格式

成功：

```json
{
  "success": true,
  "code": "OK",
  "message": "Task created",
  "data": {},
  "request_id": "uuid"
}
```

失败：

```json
{
  "success": false,
  "code": "MODEL_UNAVAILABLE",
  "message": "所选模型当前不可用",
  "details": {
    "model_key": "yolo_default"
  },
  "request_id": "uuid"
}
```

分页响应在 `data` 中包含 `items`、`page`、`page_size`、`total`。

### 7.2 接口清单

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/api/v1/health` | 进程健康检查 |
| GET | `/api/v1/system` | Python、设备、数据库和存储状态 |
| GET | `/api/v1/models` | 可用模型列表 |
| POST | `/api/v1/files` | 上传图片 |
| GET | `/api/v1/files/{id}/content` | 读取受控文件内容 |
| POST | `/api/v1/tasks` | 创建分析任务 |
| GET | `/api/v1/tasks` | 分页查询任务 |
| GET | `/api/v1/tasks/{id}` | 获取任务详情和结果 |
| DELETE | `/api/v1/tasks/{id}` | 删除单个任务及其明确关联文件 |
| POST | `/api/v1/tasks/{id}/retry` | 可选：重试失败任务 |

删除接口只处理指定任务，不提供无条件批量清空接口。若需管理清理，应先做 dry-run 列表和人工确认。

### 7.3 上传图片

**请求**

- `multipart/form-data`
- `file`：图片文件。
- `purpose`：`analysis_input` 或 `change_before/change_after`。

**返回字段**

- `id`、`original_name`、`content_type`、`size_bytes`。
- `width`、`height`、`sha256`。
- `content_url`、`created_at`。

失败场景：无文件、类型不支持、解码失败、尺寸或体积超限。

### 7.4 创建任务

**请求字段**

```json
{
  "task_type": "object_detection",
  "model_key": "yolo_default",
  "input_file_ids": ["file-uuid"],
  "parameters": {
    "confidence": 0.35,
    "iou_threshold": 0.45
  }
}
```

变化检测要求两个文件 ID。任务类型枚举：

- `object_detection`
- `land_cover_classification`
- `road_segmentation`
- `change_detection`

**返回**

- `id`、`task_type`、`status`、`created_at`。
- 同步 MVP 可以请求内完成推理，但仍按状态流记录。
- 更稳妥的同步设计：创建任务后立即执行，响应最终返回 `completed/failed`；前端仍按统一状态处理。

### 7.5 任务详情结果

公共字段：

- 任务 ID、类型、状态。
- 输入文件列表。
- 模型 key、名称、版本。
- 参数、运行设备、创建/开始/完成时间、耗时。
- 错误码和用户可读错误消息。
- 结果对象和结果资源 URL。

各任务 `result_data`：

- 检测：`detections[{class_id,label,confidence,bbox}]`。
- 分类：`predictions[{label,score}]`。
- 分割：`mask_file_id`、`overlay_file_id`、阈值和覆盖比例。
- 变化：`method`、`alignment`、`change_ratio`、掩膜和高亮图。
- 增加 `implementation`：`real_model`、`baseline` 或 `mock`。

边界框推荐统一为原图像素坐标 `[x_min,y_min,x_max,y_max]`，并记录原图宽高。

### 7.6 状态机

合法流转：

```text
pending → running → completed
                  └→ failed
pending → failed
failed → 新建 retry task
```

不要直接把原失败记录改成成功。重试创建新任务，并用 `parent_task_id` 关联。

### 7.7 删除语义

默认软删除任务记录：

- 设置 `deleted_at`。
- 列表默认排除已删除记录。
- 物理文件清理由单独维护流程处理。
- 单任务明确清理时，只删除该任务唯一拥有的文件；共享输入文件不得误删。
- 不提供“删除全部任务”的 MVP 按钮。

### 7.8 错误码

- `VALIDATION_ERROR`：400
- `UNSUPPORTED_FILE_TYPE`：400
- `FILE_TOO_LARGE`：413
- `FILE_NOT_FOUND`：404
- `TASK_NOT_FOUND`：404
- `MODEL_NOT_FOUND`：404
- `MODEL_UNAVAILABLE`：503
- `INFERENCE_FAILED`：500
- `DATABASE_UNAVAILABLE`：503
- `STORAGE_ERROR`：500
- `INTERNAL_ERROR`：500

日志记录内部异常；API 不返回堆栈和本机路径。

---

## 8. 数据库设计

### 8.1 `uploaded_files`

| 字段 | 类型 | 说明 |
|---|---|---|
| id | CHAR(36) / UUID 字符串 | 主键 |
| original_name | VARCHAR(255) | 原始文件名 |
| stored_name | VARCHAR(255) | UUID 文件名 |
| relative_path | VARCHAR(500) | 相对存储路径 |
| content_type | VARCHAR(100) | MIME |
| extension | VARCHAR(20) | 扩展名 |
| size_bytes | BIGINT | 文件大小 |
| width | INT | 宽 |
| height | INT | 高 |
| sha256 | CHAR(64) | 完整性和去重参考 |
| purpose | VARCHAR(50) | 输入、结果、掩膜等 |
| metadata_json | JSON/TEXT | 可选图像信息 |
| created_at | DATETIME | 创建时间 |
| deleted_at | DATETIME NULL | 软删除 |

索引：`sha256`、`created_at`、`purpose`。

### 8.2 `model_registry`

| 字段 | 类型 | 说明 |
|---|---|---|
| id | CHAR(36) | 主键 |
| model_key | VARCHAR(100) UNIQUE | 稳定标识 |
| display_name | VARCHAR(150) | 展示名 |
| task_type | VARCHAR(50) | 任务类型 |
| framework | VARCHAR(50) | PyTorch、OpenCV 等 |
| version | VARCHAR(100) | 模型或配置版本 |
| implementation | VARCHAR(30) | real_model/baseline/mock/planned |
| source_url | VARCHAR(500) | 来源 |
| license_name | VARCHAR(100) | 许可 |
| weight_relative_path | VARCHAR(500) NULL | 权重相对路径 |
| enabled | BOOLEAN | 是否启用 |
| metadata_json | JSON/TEXT | 类别、输入尺寸等 |
| created_at/updated_at | DATETIME | 时间 |

不要保存访问令牌、云密钥或外部服务密码。

### 8.3 `analysis_tasks`

| 字段 | 类型 | 说明 |
|---|---|---|
| id | CHAR(36) | 主键 |
| task_type | VARCHAR(50) | 任务类型 |
| status | VARCHAR(20) | 状态 |
| model_id | CHAR(36) NULL | 外键 |
| parameters_json | JSON/TEXT | 阈值、尺寸等 |
| input_summary_json | JSON/TEXT | 输入文件 ID 列表 |
| device | VARCHAR(30) NULL | cpu/cuda |
| progress | INT | 0–100 |
| parent_task_id | CHAR(36) NULL | 重试来源 |
| error_code | VARCHAR(100) NULL | 错误码 |
| error_message | TEXT NULL | 可读错误 |
| created_at/started_at/completed_at | DATETIME | 生命周期 |
| duration_ms | BIGINT NULL | 推理耗时 |
| deleted_at | DATETIME NULL | 软删除 |

索引：`status`、`task_type`、`created_at`、`model_id`。

若需要严格多输入关系，建议增加 `task_input_files` 关联表；为保持用户指定的四张核心表，MVP 可先用 JSON 文件 ID 列表，阶段 7 前升级为关联表。

### 8.4 `task_results`

| 字段 | 类型 | 说明 |
|---|---|---|
| id | CHAR(36) | 主键 |
| task_id | CHAR(36) UNIQUE | 外键 |
| result_type | VARCHAR(50) | detections/classification/mask/change |
| result_json | JSON/TEXT | 结构化结果 |
| primary_output_file_id | CHAR(36) NULL | 主结果文件 |
| preview_file_id | CHAR(36) NULL | 预览图 |
| metrics_json | JSON/TEXT | 数量、比例等 |
| created_at | DATETIME | 创建时间 |

`result_json` 不存 Base64 图片、模型权重、超大像素数组或完整日志。

### 8.5 ER 图

```text
model_registry 1 ─── N analysis_tasks
analysis_tasks 1 ─── 0..1 task_results
uploaded_files 1 ─── N task references
uploaded_files 1 ─── N task_results output references
analysis_tasks 0..1 ─── N analysis_tasks (retry relation)
```

### 8.6 SQLite → MySQL 注意事项

- UUID 统一保存为字符串，避免数据库专用类型差异。
- 所有时间以 UTC 存储，前端转换为 Asia/Shanghai。
- JSON 字段通过 SQLAlchemy 类型或序列化层统一处理。
- 不依赖 SQLite 宽松类型转换。
- MySQL 使用 InnoDB 和 `utf8mb4`。
- 先在备份数据库执行迁移，再切换连接字符串。
- 文件仍保存在文件系统，不随数据库迁移自动搬迁。

---

## 9. 模型与数据方案

### 9.1 目标检测

- **MVP 模型**：Ultralytics 小型 YOLO 通用预训练权重。
- **推荐定位**：先验证真实推理链路，不宣称专门遥感检测性能。
- **后续升级**：在 DOTA、DIOR、xView 等许可允许的数据子集上微调小型检测器；处理旋转框时再研究 OBB 模型。
- **训练**：MVP 不训练；升级版可微调。
- **输入**：RGB JPEG/PNG。
- **输出**：类别、置信度、像素坐标框和结果图。
- **预处理**：EXIF 方向修正、RGB 转换、尺寸限制、模型内部 letterbox。
- **后处理**：置信度过滤、NMS、坐标映射、绘框。
- **CPU**：可运行，优先小模型和 640 左右输入。
- **GPU**：批量、高分辨率或微调时推荐。
- **权重管理**：权重目录忽略；提供来源、哈希、手动下载和自动下载说明。
- **风险**：俯视小目标、类别域差异、建筑通常不属于通用检测标签。
- **准确描述**：

> 接入了 YOLO 推理适配器并完成任务状态、预处理、结构化结果和可视化闭环；通用权重用于工程演示，遥感专项精度需要领域数据微调。

### 9.2 土地覆盖分类

- **MVP 模型**：冻结 DINOv2 小型 backbone，提取图块特征；使用 Logistic Regression 或线性分类头。
- **标签建议**：先做水体、植被、建成区、裸地等“主导地物类别”；道路不适合稳定的整图分类，可留在分割任务。
- **后续升级**：滑窗分类热力图、轻量语义分割、多尺度特征。
- **训练**：DINOv2 不训练；轻量分类器需用少量标注特征训练。
- **直接推理**：仅在分类头和标签映射准备完成后。
- **数据来源类型**：EuroSAT 等许可明确的公开场景分类数据，或少量合法遥感图块。
- **输入**：单图或裁剪区域。
- **输出**：Top-K 类别和分数。
- **预处理**：RGB、裁剪、缩放、模型标准化。
- **后处理**：softmax/分类器概率、Top-K、低置信提示。
- **CPU**：可运行，首次加载较慢。
- **GPU**：批量特征提取时推荐。
- **权重管理**：预训练 backbone 走缓存或说明下载；分类器单独版本化但避免提交过大的文件。
- **风险**：类别体系不一致、概率校准不足、整图多地物共存。
- **准确描述**：

> 使用冻结的 DINOv2 提取遥感图块特征，并训练轻量分类器完成主导土地覆盖类别识别；未从零训练或微调 DINOv2。

### 9.3 道路提取

- **MVP 模型**：轻量 U-Net，前提是获得许可明确且架构匹配的道路分割权重。
- **后续升级**：DeepLabV3+、SegFormer、拓扑约束或矢量化后处理。
- **训练**：若找不到可靠权重，需要在小型道路数据子集上微调；不作为第一周要求。
- **数据来源类型**：公开道路分割数据、SpaceNet 道路任务等；使用前逐项核查许可和下载条件。
- **输入**：RGB 图片。
- **输出**：概率图、二值掩膜、透明叠加图。
- **预处理**：尺寸统一、归一化、必要时切片。
- **后处理**：阈值化、去除小区域、形态学连接；不宣称生成路网。
- **CPU**：小图和轻量模型可运行。
- **GPU**：大图切片和训练推荐。
- **风险**：阴影、建筑边缘、窄路断裂、训练域差异。
- **准确描述**：

> 接入/实现了轻量道路语义分割流程，包括图像预处理、掩膜生成和结果叠加；当前版本侧重演示，不包含道路矢量拓扑重建。

### 9.4 变化检测

- **MVP 模型**：非深度学习 baseline，采用对齐、绝对差分/SSIM、阈值和形态学处理。
- **后续升级**：Siamese U-Net、BIT、ChangeFormer 等，但需单独评估权重许可和硬件需求。
- **训练**：baseline 不需要。
- **直接推理**：可以。
- **数据来源类型**：公开双时相变化检测样例；也可自行对合法图片做局部编辑用于功能测试，并标明是合成测试。
- **输入**：同一区域、尽量同尺寸且已对齐的前后 RGB 图。
- **输出**：差异图、二值掩膜、高亮图和变化比例。
- **预处理**：尺寸检查、颜色归一、可选粗配准。
- **后处理**：阈值化、去噪、连通区域框选。
- **CPU**：适合。
- **GPU**：baseline 不需要。
- **风险**：错位、季节和光照变化被误判。
- **准确描述**：

> 实现了可解释的传统变化检测 baseline，并为后续 Siamese 或 Transformer 模型预留统一适配器；当前 baseline 不等同于深度学习变化检测。

---

## 10. 逐周时间安排

### 10.1 四周版本

#### 第 1 周：完成可演示 MVP

- **必须完成**：阶段 0–4；SQLite、上传、真实 YOLO、结果和历史。
- **可选增强**：基础 Dashboard 统计。
- **产出**：前后端、统一任务 API、首个真实模型、MVP README。
- **截图/录制**：上传至检测结果的完整流程。
- **周末状态**：可以进行 2–3 分钟稳定演示。
- **可延期**：MySQL、地图、其他三类真实模型。

#### 第 2 周：补齐任务能力

- **必须完成**：MySQL 切换验证、DINOv2 分类、变化检测 baseline。
- **可选增强**：分类特征缓存。
- **产出**：模型说明、数据来源初稿、双图任务。
- **截图**：分类概率和变化四联图。
- **可延期**：道路真实模型。

#### 第 3 周：分割、地图和体验

- **必须完成**：道路模块的真实或明确实验版本、掩膜叠加、Leaflet 基础地图。
- **可选增强**：透明度控制、结果下载。
- **产出**：四模块统一结果格式。
- **截图**：道路掩膜、地图叠加。
- **可延期**：矢量道路、GeoTIFF 坐标。

#### 第 4 周：测试与作品包装

- **必须完成**：关键测试、错误页面、README、来源、限制、截图和演示。
- **可选增强**：Docker、英文文档、GIF。
- **产出**：`v1.0.0` 可展示版本。
- **周末状态**：陌生人可按文档运行。
- **可延期**：Docker 和深度变化检测。

### 10.2 六周版本

#### 第 1 周

阶段 0–3；完成上传、任务和历史的 mock 闭环。

#### 第 2 周

真实 YOLO、结果可视化、MVP 演示与 `v0.1.0`。

#### 第 3 周

DINOv2 特征分类、模型来源与实验记录。

#### 第 4 周

道路分割和变化检测 baseline，统一掩膜展示。

#### 第 5 周

Leaflet、MySQL 验证、错误处理和自动化测试。

#### 第 6 周

README、架构图、截图、演示视频、可选 Docker 和 `v1.0.0`。

六周方案每周均保留：

- 一次可运行提交。
- 一组最新截图。
- 一段本周已实现/未实现能力记录。
- 若落后，依次延期 Docker、地图、道路真实权重、DINOv2 高级热力图；不得延期 MVP 目标检测闭环。

---

## 11. GitHub 规范与作品集包装

### 11.1 README 章节

1. 项目标题与状态徽标。
2. 中文/英文一句话简介。
3. 项目性质与非官方声明。
4. 演示 GIF 和关键截图。
5. 功能列表及实现状态。
6. 系统架构。
7. 技术栈。
8. 快速开始：CPU 默认。
9. 配置与 SQLite/MySQL 切换。
10. 模型权重获取方式。
11. 数据和模型来源、许可。
12. API 概览。
13. 项目目录。
14. 测试方式。
15. 已知限制。
16. Roadmap。
17. 个人贡献与项目背景。
18. License 与致谢。

### 11.2 截图类型

- Dashboard 全景。
- 图片上传与任务参数。
- YOLO 检测结果及列表。
- 分类概率结果。
- 道路掩膜与叠加。
- 变化检测四联图。
- 历史任务和错误状态。
- Leaflet 结果图层。

截图中避免显示本机用户名、绝对路径、数据库密码和私人文件。

### 11.3 架构图内容

必须包含浏览器、Vue、Flask API、任务服务、模型适配器、SQLAlchemy、SQLite/MySQL、本地文件存储和模型权重边界。Celery/Redis 不应画入当前架构，除非真正实现。

### 11.4 Issues、Milestones 与提交

- **Issues：建议做**，用于记录模型来源核查、功能缺陷和增强项。
- **Milestones：建议设置**
  - `MVP v0.1`
  - `Four-task Demo v0.5`
  - `Portfolio Release v1.0`
- 每次提交只解决一个清晰主题。
- 不提交“半坏状态”；提交前至少完成对应手工验证。
- 不伪造 2025 年提交历史，不修改提交时间制造项目经历。

推荐 Release：

- `v0.1.0`：YOLO MVP。
- `v0.5.0`：四任务演示。
- `v1.0.0`：文档、测试和作品集完整。
- `v1.1.0`：可选 Docker 或模型升级。

### 11.5 A. 中文 README 简介草稿

> 本仓库实现了一个面向学习与作品集展示的遥感影像智能分析 Web 平台，涵盖图片上传、目标检测、土地覆盖分类、道路提取、基础变化检测、结果可视化和历史任务管理。项目采用 Vue3、Flask、PyTorch 与 SQLAlchemy，默认支持 CPU 和 SQLite，并可配置 MySQL。  
>
> 本项目基于本人 2025 年参与的遥感智能分析平台实训方向，在实训结束后使用公开数据、公开模型独立复现并逐步工程化完善。仓库不是原实训系统的源代码，也不代表任何企业、机构或官方产品。各模型、数据和第三方资源的来源与许可均在文档中单独说明。

### 11.6 B. 英文 README 简介草稿

> This repository contains a personal, portfolio-oriented web platform for remote-sensing image analysis. It demonstrates image upload, object detection, land-cover classification, road extraction, baseline change detection, result visualization, and task history management using Vue 3, Flask, PyTorch, and SQLAlchemy. The default setup supports CPU inference and SQLite, with optional MySQL configuration.
>
> The work was independently reproduced and extended after my participation in a related remote-sensing analysis training project in 2025. This repository is not the original training system, does not contain proprietary source code, and is not an official product of any company or organization. Public model and dataset sources are documented separately.

### 11.7 C. 简历中文表述

> 基于 2025 年遥感智能分析平台实训方向，使用公开数据和预训练模型独立复现并工程化实现个人演示平台；采用 Vue3、Flask、PyTorch 与 SQLAlchemy，完成图片上传、统一任务管理、YOLO 目标检测、DINOv2 特征分类、道路分割实验、基础变化检测及结果可视化，并支持 SQLite/MySQL 配置切换。

仅保留实际完成的模块；没有完成 DINOv2 或道路分割时必须删除对应措辞。

### 11.8 D. 简历英文表述

> Independently reproduced and engineered a personal remote-sensing image analysis demo after participating in a related training project in 2025. Built a Vue 3/Flask/PyTorch platform covering image upload, unified task management, YOLO inference, DINOv2 feature-based classification, experimental road segmentation, baseline change detection, and result visualization, with configurable SQLite/MySQL persistence.

### 11.9 E. 面试时 1 分钟介绍稿

> 这个项目是我在 2025 年参与遥感智能分析相关实训后，使用公开数据和公开模型独立复现的个人工程化版本，不是原实训系统的代码。我的重点不是从零训练大型模型，而是把遥感模型做成一个可运行、可解释的完整 Web 产品。前端使用 Vue3，后端使用 Flask，任务和结果通过 SQLAlchemy 保存到 SQLite 或 MySQL。当前核心闭环是用户上传图片、创建任务、后端选择模型适配器执行推理、保存结构化结果和可视化图片，再由前端展示并支持历史查询。目标检测接入真实 YOLO；土地分类使用冻结的 DINOv2 特征和轻量分类器；变化检测明确采用传统 baseline；更复杂的深度学习变化检测属于后续扩展。这个项目主要体现了我把模型推理、后端 API、文件管理、数据库和前端可视化串成完整系统的能力。

### 11.10 F. “你具体做了什么”回答框架

按五层回答：

1. **架构**：设计统一任务和可插拔模型适配器。
2. **后端**：上传校验、状态流、推理调用、结果持久化和异常处理。
3. **模型**：说明哪些直接接入、哪些训练轻量头、哪些是 baseline。
4. **前端**：任务创建、状态、结果对比和历史。
5. **工程化**：CPU/GPU选择、权重管理、SQLite/MySQL、测试和文档。

最后主动划界：

> 我没有从零训练 DINOv2，也没有把 baseline 变化检测描述成 Transformer 模型；我负责的是个人复现版本中的系统设计、模型接入与工程化闭环。

### 11.11 G. “DINOv2、YOLO、Transformer 如何使用”回答框架

- **YOLO**：真实承担目标检测推理；输出检测框、类别和置信度。MVP 使用通用预训练权重，遥感专项效果需要微调。
- **DINOv2**：冻结作为特征提取器，后接轻量分类器；没有从零训练 DINOv2。
- **Transformer 变化检测**：当前版本没有将其作为已实现能力；只在适配器层预留接口。现有变化检测是对齐、差分和 SSIM baseline。
- **若道路模型或变化 Transformer 尚未完成**：直接说“这是 Roadmap，而不是当前功能”。

### 11.12 不应上传

- 模型权重、大型数据集、未经授权图片。
- `.env`、数据库密码、令牌。
- 上传内容、日志、本地数据库。
- 训练缓存、虚拟环境、Node 依赖。
- 企业内部文档、代码、截图、数据或品牌素材。
- 含个人隐私的绝对路径和调试日志。

---

## 12. 风险清单与最小降级方案

| 风险 | 处理方式 | 最小可行降级 |
|---|---|---|
| Python/CUDA/PyTorch 冲突 | 先建立 CPU 环境；锁定已验证依赖组合 | 只安装 CPU 版 PyTorch |
| Windows 环境问题 | 使用短英文路径、虚拟环境、PowerShell 文档 | 暂不使用 Docker/CUDA |
| 前后端跨域 | Vite 开发代理，CORS 限定本地来源 | 前后端使用固定端口 |
| 图片上传失败 | 限制格式/大小，三重校验，友好错误 | 仅支持 JPEG/PNG、20 MB |
| 文件路径问题 | 数据库存相对路径，内部使用路径库 | 将仓库移到短英文目录 |
| MySQL 连接失败 | 环境变量、连接健康检查、迁移测试 | 自动/手动切回 SQLite |
| YOLO 权重下载失败 | 文档提供来源、预期文件名和哈希 | 手动下载放入权重目录 |
| 没有 GPU | 默认设备自动选择 CPU | 小模型、较低输入分辨率 |
| 推理太慢 | 模型单例、限制尺寸、记录耗时 | 只允许单图同步推理 |
| 遥感图过大 | 读取前检查像素数，生成推理副本 | 将长边缩放到限定尺寸 |
| 训练数据不足 | 使用预训练特征和小型分类器 | 限制类别并标注演示性质 |
| 分割效果不好 | 检查域差异、阈值和权重来源 | 标记实验模块，展示限制 |
| 双时相未对齐 | 提供尺寸检查和可选粗配准 | 仅接受已对齐图片 |
| Git 仓库过大 | `.gitignore`、权重外置、提交前检查 | 样例图只保留少量压缩版 |
| 权重不能上传 | 下载说明、环境变量或挂载路径 | 用户手动放置权重 |
| 功能太多 | 严格按 P0–P7；保护 MVP | 延期地图、Docker、深度变化检测 |
| 描述与实现不一致 | 模型页显示 real/baseline/mock/planned | 从 README 和简历删除未实现模块 |
| 通用 YOLO 遥感效果差 | 使用公开遥感样例并解释域差异 | 演示车辆/船等可识别类别 |
| DINOv2 分类概念混淆 | 定义为图块主导类别分类 | 不宣称像素级土地覆盖 |
| 道路权重许可不明确 | 保存来源、许可和版本记录 | 不分发权重，只写获取流程 |
| 地图叠加无坐标 | 显示“演示范围”标识 | 普通图片叠加代替地图 |
| 同步请求超时 | 限制模型和图片大小 | 结果轮询与异步队列延后 |
| 删除误伤文件 | 软删除、引用检查、单任务清理 | 只隐藏任务，不物理删除 |
| 样例许可不明 | 优先官方公开数据并记录许可 | 使用自己生成的合成测试图 |

---

## 13. 开始实施前检查清单

### 软件

- [ ] Windows 10/11。
- [ ] Git。
- [ ] Python：建议 3.10 或 3.11；以目标 PyTorch/模型库兼容性验证为准。
- [ ] Node.js：建议当前维护中的 LTS 版本，并在 README 锁定实际验证版本。
- [ ] npm。
- [ ] VS Code 或其他编辑器。
- [ ] MySQL 8.x：阶段 2 后可选，不阻塞第一周。
- [ ] Docker Desktop：阶段 11 可选，不需要第一天安装。
- [ ] NVIDIA 驱动/CUDA：只有计划 GPU 加速时需要；CPU MVP 不需要 CUDA Toolkit。

### 账号或服务

- [ ] GitHub 账号。
- [ ] 可选：公开模型托管平台账号，仅在下载条款要求时创建。
- [ ] 不需要购买云服务器。
- [ ] 使用公开数据前记录来源、许可和访问日期。

### 第一天下载和准备

- [ ] 只准备前后端基础依赖。
- [ ] 选择 2–3 张许可明确的小型演示图。
- [ ] 不下载大型数据集。
- [ ] 不在平台壳完成前配置 CUDA。
- [ ] 不把真实数据库密码写入仓库。

### 第一天完成标准

- [ ] 建立仓库骨架和非官方声明。
- [ ] 完成 Vue → Flask 健康检查。
- [ ] 页面能显示后端在线/离线状态。
- [ ] `.gitignore` 已覆盖权重、上传、数据库和环境变量。
- [ ] README 写明项目目标、技术栈和当前状态。
- [ ] 完成第一次提交。

### 模型接入时点

- 第 1–2 天：平台壳、API、数据库和上传。
- 第 3–5 天：接入真实 YOLO。
- YOLO 闭环稳定后：DINOv2、道路分割和变化检测。
- 不应在上传、任务状态和结果格式尚未稳定时同时接入四个模型。

### 第一次 Git commit

在以下条件同时满足后提交：

- 初始目录和说明已完成。
- `.gitignore` 已验证。
- 前后端健康检查可以运行。
- 仓库中不存在密钥、权重、上传内容或不明来源数据。

推荐消息：

`feat: initialize remote sensing platform with frontend backend health check`

---

# 现在最应该先做的 3 件事

1. **确定并记录 MVP 的唯一主线**：第一周只保护“上传图片 → YOLO 推理 → 结果展示 → 历史查询”，其他模块不得阻塞它。
2. **准备安全的项目骨架与来源声明**：先完成仓库结构、`.gitignore`、环境模板和“个人复现、非官方项目”说明。
3. **跑通最小前后端闭环**：先让 Vue 正确读取 Flask 健康检查，再依次加入 SQLite 任务、图片上传和真实 YOLO；不要第一天处理 CUDA、MySQL、地图或模型训练。

