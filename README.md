# 313实验室开放平台

一个用于管理313实验室成员、项目、分享会、设备、值日安排和文档的综合管理平台。

## ✨ 特性

- 🧑‍💼 **成员管理**: 完整的成员信息管理，支持角色分配和搜索筛选
- 📁 **项目展示**: 项目全生命周期管理，支持卡片和列表双视图
- 🎤 **分享会管理**: 分享会资料和记录管理
- 💻 **设备管理**: 实验室设备借用和维护记录
- 📅 **值日安排**: 智能值日安排和状态跟踪
- 📄 **文档管理**: 文件上传、分类、下载和批量操作
- 🔍 **智能搜索**: 全局搜索和高级筛选功能
- 📱 **响应式设计**: 支持桌面和移动端访问
- 🚀 **高性能**: 基于现代技术栈，快速响应

## 🛠 技术栈

## 🛠 技术栈与架构

### 后端

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 项目结构

### 后端架构

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端技术

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 后端 & 前端结构

## 🛠 系统架构与技术选型

### 后端结构

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端技术栈

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 项目结构目录

313实验室开放平台/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/v1/         # API路由 (v1版本)
│   │   │   └── endpoints/  # 各模块API端点
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 应用配置
│   │   │   └── database.py # 数据库配置
│   │   ├── models/         # SQLAlchemy数据库模型
│   │   ├── schemas/        # Pydantic数据验证模型
│   │   └── services/       # 业务逻辑服务
│   ├── main.py             # FastAPI应用入口
│   ├── requirements.txt    # Python依赖
│   └── .env.example        # 环境变量模板
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API接口封装
│   │   ├── components/    # Vue组件
│   │   │   └── Layout.vue # 统一布局组件
│   │   ├── views/         # 页面组件
│   │   ├── router/        # Vue Router配置
│   │   ├── stores/        # Pinia状态管理
│   │   └── utils/         # 工具函数
│   ├── package.json       # Node.js依赖
│   └── vite.config.js     # Vite配置
├── docs/                  # 项目文档
│   ├── API.md            # API接口文档
│   ├── DEPLOYMENT.md     # 部署指南
│   └── GETTING_STARTED.md # 快速开始
├── uploads/              # 文件上传目录
│   ├── projects/         # 项目相关文件
│   ├── sessions/         # 分享会相关文件
│   └── others/           # 其他文件
└── README.md             # 项目说明

## 313实验室开放平台 | 313Lab Open Platform

一个用于管理313实验室成员、项目、分享会、设备、值日安排和文档的综合管理平台。

## ✨ 平台特性

- 🧑‍💼 **成员管理**: 完整的成员信息管理，支持角色分配和搜索筛选
- 📁 **项目展示**: 项目全生命周期管理，支持卡片和列表双视图
- 🎤 **分享会管理**: 分享会资料和记录管理
- 💻 **设备管理**: 实验室设备借用和维护记录
- 📅 **值日安排**: 智能值日安排和状态跟踪
- 📄 **文档管理**: 文件上传、分类、下载和批量操作
- 🔍 **智能搜索**: 全局搜索和高级筛选功能
- 📱 **响应式设计**: 支持桌面和移动端访问
- 🚀 **高性能**: 基于现代技术栈，快速响应

## 🛠 核心技术栈

## 🛠 技术栈与架构（总览）

### 后端技术细节

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端技术细节

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 项目目录结构

### 后端架构（技术细节）

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端技术（细节）

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 后端与前端目录结构

## 🛠 系统架构与技术选型（概览）

### 后端技术细节（核心组件）

- **框架**: FastAPI (Python 3.8+)
- **数据库**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **认证**: JWT (待实现)
- **文档**: 自动生成的OpenAPI文档

### 前端技术栈（详细）

- **框架**: Vue 3 (Composition API)
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

## 📁 项目目录结构（总览）

313实验室开放平台/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/v1/         # API路由 (v1版本)
│   │   │   └── endpoints/  # 各模块API端点
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 应用配置
│   │   │   └── database.py # 数据库配置
│   │   ├── models/         # SQLAlchemy数据库模型
│   │   ├── schemas/        # Pydantic数据验证模型
│   │   └── services/       # 业务逻辑服务
│   ├── main.py             # FastAPI应用入口
│   ├── requirements.txt    # Python依赖
│   └── .env.example        # 环境变量模板
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API接口封装
│   │   ├── components/    # Vue组件
│   │   │   └── Layout.vue # 统一布局组件
│   │   ├── views/         # 页面组件
│   │   ├── router/        # Vue Router配置
│   │   ├── stores/        # Pinia状态管理
│   │   └── utils/         # 工具函数
│   ├── package.json       # Node.js依赖
│   └── vite.config.js     # Vite配置
├── docs/                  # 项目文档
│   ├── API.md            # API接口文档
│   ├── DEPLOYMENT.md     # 部署指南
│   └── GETTING_STARTED.md # 快速开始
├── uploads/              # 文件上传目录
│   ├── projects/         # 项目相关文件
│   ├── sessions/         # 分享会相关文件
│   └── others/           # 其他文件
└── README.md             # 项目说明

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 1. 克隆项目

## 🚀 快速上手

### 环境要求（开发）

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 克隆项目

```bash
git clone <repository-url>
cd 313lib开放平台
```

### 2. 后端启动

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 启动后端服务
python main.py
```

后端服务运行在 <http://localhost:8000>

### 3. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装Node.js依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 <http://localhost:5173>

### 4. 数据库配置

在PostgreSQL中创建数据库:

```sql
CREATE DATABASE lab313_platform;
CREATE USER lab313_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE lab313_platform TO lab313_user;
```

## 📋 功能模块

### 1. 成员管理

- ✅ 成员信息的增删改查
- ✅ 角色管理 (负责人/成员/校友)
- ✅ 按姓名、学号、年级、角色搜索筛选
- ✅ 分页显示和批量操作

### 2. 项目管理

- ✅ 项目全生命周期管理
- ✅ 项目状态跟踪 (规划中/进行中/已完成/已归档)
- ✅ 项目成员管理
- ✅ GitHub和Demo链接管理
- ✅ 卡片和列表双视图模式
- ✅ 项目标签和分类

### 3. 分享会管理

- 🔄 分享会信息管理
- 🔄 分享者和主题记录
- 🔄 分享会资料上传
- 🔄 学期和期数管理

### 4. 设备管理

- 🔄 设备信息录入和更新
- 🔄 设备状态管理 (可用/使用中/维护中/已退役)
- 🔄 设备借用记录
- 🔄 设备规格和序列号管理

### 5. 值日安排

- 🔄 值日计划制定
- 🔄 值日状态跟踪
- 🔄 值日任务分配
- 🔄 值日完成情况统计

### 6. 文档管理

- ✅ 文件上传和下载
- ✅ 文件分类管理 (文档/图片/演示/视频/其他)
- ✅ 批量文件上传 (最多10个)
- ✅ 文件搜索和筛选
- ✅ 文件统计信息
- ✅ 项目和分享会文件关联
- ✅ 文件大小限制 (50MB)

### 7. 系统功能

- ✅ 统一的响应式布局
- ✅ 现代化的UI设计
- ✅ 实时数据更新
- ✅ 错误处理和用户提示
- 🔄 用户认证和权限管理
- 🔄 操作日志记录

## 📊 数据统计

平台提供丰富的数据统计功能:

- 成员统计 (按角色、年级分布)
- 项目统计 (按状态、时间分布)
- 文件统计 (按类型、大小分布)
- 活动统计 (分享会、设备使用等)

## 🔗 API文档

启动后端服务后，可以访问以下链接查看API文档:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **详细文档**: [docs/API.md](docs/API.md)

## 📖 文档

- [API接口文档](docs/API.md) - 完整的API接口说明
- [部署指南](docs/DEPLOYMENT.md) - 生产环境部署说明
- [快速开始](docs/GETTING_STARTED.md) - 开发环境搭建

## 🛣 开发计划

### 已完成 ✅

- [x] 项目初始化和架构设计
- [x] 数据库模型设计
- [x] 前端基础框架搭建
- [x] 成员管理API和前端页面
- [x] 项目管理API和前端页面
- [x] 文档管理API和前端页面
- [x] 统一布局和导航
- [x] 响应式设计
- [x] API文档编写

### 进行中 🔄

- [ ] 分享会管理功能
- [ ] 设备管理功能
- [ ] 值日安排功能
- [ ] 用户认证系统

### 计划中 📋

- [ ] 权限管理系统
- [ ] 数据导入导出
- [ ] 邮件通知功能
- [ ] 移动端适配优化
- [ ] 数据备份和恢复
- [ ] 性能监控和日志
- [ ] 单元测试和集成测试

## 🤝 贡献指南

欢迎实验室成员贡献代码和提出建议！

### 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- Python: 遵循 PEP 8 规范
- JavaScript: 使用 ESLint 和 Prettier
- 提交信息: 使用清晰的提交信息

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- 📧 邮箱: <lab313@example.com>
- 🌐 网站: <https://313lab.example.com>
- 📱 微信群: 扫码加入开发讨论群

## 🙏 致谢

感谢所有为这个项目做出贡献的实验室成员！

---

**313实验室开放平台** - 科技兴国，技术兴邦。打造国际先进实验室！
