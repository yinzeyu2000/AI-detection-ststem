# AI 目标检测系统 (AI Object Detection System)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/vue-3.4-brightgreen.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)

一个基于 Vue 3 + FastAPI + Supabase 的全栈式 AI 目标检测平台，具备用户管理、检测前后对比展示、数据存储以及参数阈值动态调节功能。系统支持自主切换本地模型，实现目标检测、分割、分类任务。目前集成的是 RT-DETR 无人机小目标检测模型权重。

## ✨ 功能特性

- 🎯 **AI 目标检测**：基于 RT-DETR 模型，支持无人机小目标检测
- 🖼️ **检测对比展示**：实时展示检测前后图片对比
- 👤 **用户认证系统**：支持用户注册、登录、会话管理（基于 Supabase Auth）
- 📊 **检测数据存储**：自动保存检测结果至 Supabase 数据库和对象存储
- 📜 **历史记录**：查看和管理过往检测记录
- 🎛️ **参数动态调节**：支持置信度阈值、IoU 阈值实时调整
- 🌙 **深色/浅色主题**：一键切换界面主题
- 📤 **结果导出**：支持 JSON、CSV、TXT 格式导出检测数据
- 🔌 **可扩展架构**：支持切换不同的 DETR 系列模型（STD-DETR、ISTD-DETR、RT-DETR-R18/R50）

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 (Vue 3)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Vue 3    │  │ Pinia    │  │ Vue      │  │ Element Plus │   │
│  │ Router   │  │ Store    │  │ Router   │  │ TailwindCSS  │   │
│  └──────────┴──┴──────────┴──┴──────────┴──┴──────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    业务后端 (FastAPI - 8080)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • 接收前端上传的图片                                     │   │
│  │  • 转发至 AI 推理服务器                                   │   │
│  │  • 将原图与结果图上传至 Supabase Storage                  │   │
│  │  • 将检测记录写入 Supabase Database                       │   │
│  │  • 用户认证与历史记录管理                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP POST /detect
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AI 推理服务器 (FastAPI - 8000)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  • 加载 RT-DETR 模型权重 (.pt)                            │   │
│  │  • 执行目标检测推理                                       │   │
│  │  • 返回检测结果 (JSON + Base64 可视化图片)                │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Supabase 云平台                             │
│  ┌──────────────┐              ┌──────────────────────────┐     │
│  │  PostgreSQL  │              │    Object Storage        │     │
│  │  Database    │              │    (images bucket)       │     │
│  │              │              │    • 原始图片            │     │
│  │  • detections│              │    • 检测结果图          │     │
│  │    表        │              │                          │     │
│  └──────────────┘              └──────────────────────────┘     │
│  ┌──────────────┐                                               │
│  │   Supabase   │                                               │
│  │     Auth     │                                               │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈

### 前端
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | ^3.4.0 | 渐进式 JavaScript 框架 |
| Vue Router | ^4.2.5 | 官方路由管理器 |
| Pinia | ^2.1.7 | Vue 状态管理库 |
| Element Plus | ^2.5.4 | Vue 3 组件库 |
| Axios | ^1.6.5 | HTTP 客户端 |
| Supabase JS | ^2.39.0 | Supabase 客户端 SDK |
| Vite | ^5.0.11 | 前端构建工具 |
| TailwindCSS | ^3.4.1 | 原子化 CSS 框架 |

### 后端
| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| FastAPI | 0.104+ | 高性能 Web 框架 |
| Uvicorn | - | ASGI 服务器 |
| Ultralytics | - | YOLO/RT-DETR 模型库 |
| Supabase Python | - | Supabase Python SDK |
| HTTPX | - | 异步 HTTP 客户端 |
| python-dotenv | - | 环境变量管理 |

## 📁 项目结构

```
AI-detection-system/
├── backend/                    # 业务后端 (FastAPI - 端口 8080)
│   ├── main.py                #   主入口：图片检测、历史记录 API
│   ├── ceshi.py               #   数据库连接测试
│   └── .env                   #   环境变量配置
├── frontend/                   # 前端 (Vue 3 + Vite)
│   ├── src/
│   │   ├── config/
│   │   │   └── supabase.js    #   Supabase 客户端配置
│   │   ├── router/
│   │   │   └── index.js       #   路由配置与守卫
│   │   ├── services/
│   │   │   └── api.js         #   API 请求封装
│   │   ├── stores/
│   │   │   ├── auth.js        #   认证状态管理
│   │   │   ├── detection.js   #   检测状态管理
│   │   │   └── theme.js       #   主题状态管理
│   │   ├── views/
│   │   │   ├── LoginView.vue  #   登录/注册页面
│   │   │   └── MainView.vue   #   主检测页面
│   │   ├── App.vue            #   根组件
│   │   └── main.js            #   入口文件
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
├── fastapi_app.py              # AI 推理服务器 (FastAPI - 端口 8000)
├── requirements.txt            # Python 依赖
└── README.md                   # 项目文档
```

## 📋 环境准备

### 前置要求
- **Python** 3.8 或更高版本
- **Node.js** 18 或更高版本
- **Supabase 账号**：[注册 Supabase](https://supabase.com/)
- **模型权重文件**：RT-DETR 训练后的 `.pt` 文件

### 1. 配置 Supabase

1. 在 Supabase 控制台创建新项目
2. 创建 `detections` 表：

```sql
CREATE TABLE detections (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  image_url TEXT,
  result_image_url TEXT,
  results JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

3. 创建 Storage Bucket：
   - 进入 Storage → 创建 Bucket `images`
   - 设置为 `Public`

4. 获取项目 URL 和 API Keys：
   - `SUPABASE_URL`：项目 URL
   - `SUPABASE_KEY`：service_role key（后端使用）
   - `VITE_SUPABASE_KEY`：anon key（前端使用）

### 2. 准备模型权重

将训练好的 RT-DETR 模型权重文件放置在服务器指定路径，例如：
```
runs/train/exp/weights/best.pt
```

或通过环境变量 `RTDETR_WEIGHTS` 自定义路径。

## 🚀 部署与运行

### 后端服务

1. **安装 Python 依赖**：
```bash
pip install -r requirements.txt
```

2. **配置环境变量**：

创建 `backend/.env` 文件：
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
REMOTE_SERVER_URL=http://your_ai_server_ip:8000/detect
```

3. **启动业务后端**（端口 8080）：
```bash
cd backend
python main.py
```

### AI 推理服务器

1. **配置模型权重路径**（可选，使用环境变量）：
```bash
export RTDETR_WEIGHTS=/path/to/your/best.pt
export RTDETR_PROJECT=runs/detect
export RTDETR_NAME=exp
```

2. **启动推理服务**（端口 8000）：
```bash
python fastapi_app.py
```

访问 `http://localhost:8000/health` 验证服务状态。

### 前端

1. **安装依赖**：
```bash
cd frontend
npm install
```

2. **配置环境变量**：

确保 `frontend/.env` 文件存在：
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_KEY=your_supabase_anon_key
```

3. **启动开发服务器**：
```bash
npm run dev
```

4. **构建生产版本**：
```bash
npm run build
```

## 🔌 API 接口

### AI 推理服务器 (端口 8000)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/detect` | 执行目标检测 |

**`/detect` 请求参数：**
- `file` (FormData): 图片文件
- `project` (Query): 输出目录（默认 `runs/detect`）
- `name` (Query): 输出名称（默认 `exp`）
- `save` (Query): 是否保存（默认 `true`）
- `visualize` (Query): 是否可视化（默认 `false`）
- `return_image` (Query): 是否返回 Base64 图片（默认 `false`）

### 业务后端 (端口 8080)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/detect` | 上传图片并检测 | 可选 Bearer Token |
| GET | `/api/history` | 获取历史记录 | 需要 Bearer Token |

## ⚙️ 环境变量说明

### 推理服务器 (`fastapi_app.py`)
| 变量 | 默认值 | 说明 |
|------|--------|------|
| `RTDETR_WEIGHTS` | `runs/train/exp/weights/best.pt` | 模型权重路径 |
| `RTDETR_PROJECT` | `runs/detect` | 默认输出项目目录 |
| `RTDETR_NAME` | `exp` | 默认输出名称 |

### 业务后端 (`backend/`)
| 变量 | 说明 |
|------|------|
| `SUPABASE_URL` | Supabase 项目 URL |
| `SUPABASE_KEY` | Supabase service_role key |
| `REMOTE_SERVER_URL` | AI 推理服务器地址 |

### 前端 (`frontend/`)
| 变量 | 说明 |
|------|------|
| `VITE_SUPABASE_URL` | Supabase 项目 URL |
| `VITE_SUPABASE_KEY` | Supabase anon key |

## 📸 界面预览

- **登录/注册**：支持邮箱密码认证，含粒子动画科技感背景
- **主界面**：左侧控制面板（模型选择、阈值调节、图片上传），右侧检测结果对比展示
- **历史记录**：表格形式展示过往检测记录，支持图片预览与快速加载
- **主题切换**：支持深色/浅色模式一键切换

## 🔮 扩展方向

- [ ] 接入更多检测模型（YOLO 系列、DETR 系列等）
- [ ] 实时视频流检测支持
- [ ] 检测模型热切换与 A/B 测试
- [ ] 多用户权限分级
- [ ] 检测数据可视化仪表盘
- [ ] 批量图片检测支持
- [ ] 检测模型性能监控与日志

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📬 联系方式

如有问题或建议，请通过 [GitHub Issues](https://github.com/yinzeyu2000/AI-detection-ststem/issues) 反馈。
