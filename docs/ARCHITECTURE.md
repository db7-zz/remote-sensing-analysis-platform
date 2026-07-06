# 当前系统架构

本文只描述阶段 0、阶段 1 已经存在并验证的代码，不把后续规划描述为已实现功能。

## 组件职责

### 浏览器

- 加载由 Vite 开发服务器提供的单页应用。
- 运行 Vue 3 生成的 JavaScript。
- 在 Dashboard 挂载后发起健康检查请求，并根据结果显示加载、成功或错误状态。

### Vue 3 与 TypeScript

- Vue 3 负责组件渲染、响应式状态和页面生命周期。
- TypeScript 为 API 响应、健康状态和组件逻辑提供静态类型检查。
- `frontend/src/main.ts` 是前端代码入口，在 `#app` 上挂载 Vue，并注册 Vue Router 与 Element Plus。
- `frontend/src/App.vue` 提供全局页面外壳。
- `frontend/src/views/DashboardView.vue` 在 `onMounted` 阶段调用健康检查，并维护 `loading`、`success`、`error` 三种状态。

### Vite

- `frontend/index.html` 是浏览器加载的 HTML 入口。
- `frontend/vite.config.ts` 配置 Vue 插件、开发服务器和 API 代理。
- 开发服务器实际端口为 `5173`。
- 开发阶段将浏览器发往 `/api` 的请求代理到 `http://127.0.0.1:5000`。
- `npm.cmd run build` 先执行 TypeScript/Vue 类型检查，再生成生产构建产物。

### Flask

- `backend/run.py` 是后端运行入口，通过 `create_app()` 创建应用。
- `backend/app/__init__.py` 是应用工厂，负责加载配置、配置 CORS、注册 Blueprint。
- `backend/app/config.py` 从根目录 `.env` 读取配置，并提供本地开发默认值。
- 后端默认监听 `127.0.0.1:5000`。
- 当前唯一业务 API 是 `GET /api/v1/health`。
- `backend/app/utils/responses.py` 生成统一的成功响应结构。

## 当前请求链路

```text
浏览器访问 http://127.0.0.1:5173/
  │
  ▼
Vite 开发服务器读取 frontend/index.html
  │
  ▼
frontend/src/main.ts 挂载 Vue 应用
  │
  ▼
DashboardView.vue 在 onMounted 中调用 getHealth()
  │
  ▼
Axios 客户端请求 /api/v1/health
  │
  ▼
Vite 将 /api 请求代理至 http://127.0.0.1:5000
  │
  ▼
Flask 应用匹配 /api/v1/health
  │
  ▼
health_check() 返回统一 JSON 响应
  │
  ▼
Vue 将页面状态更新为 success 或 error
```

## 当前入口与地址

| 项目 | 实际值 |
|---|---|
| 前端 HTML 入口 | `frontend/index.html` |
| 前端代码入口 | `frontend/src/main.ts` |
| 前端根组件 | `frontend/src/App.vue` |
| 前端开发端口 | `5173` |
| 前端页面 | `http://127.0.0.1:5173/` |
| Flask 运行入口 | `backend/run.py` |
| Flask 应用工厂 | `backend/app/__init__.py:create_app` |
| Flask 默认地址 | `http://127.0.0.1:5000` |
| 健康检查 API | `GET /api/v1/health` |
| 完整健康检查地址 | `http://127.0.0.1:5000/api/v1/health` |

## 当前边界

当前架构只证明 Vue 与 Flask 的 HTTP 闭环已经建立。数据库、图片上传、分析任务、模型推理、地图和部署均尚未实现。

