# 313实验室开放平台

一个用于管理313实验室成员、项目、分享会、设备和值日安排的综合管理平台。

## 技术栈

### 后端
- **框架**: FastAPI (Python)
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **认证**: JWT

### 前端
- **框架**: Vue 3
- **UI库**: Element Plus
- **状态管理**: Pinia
- **构建工具**: Vite

## 项目结构

```
313实验室开放平台/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic模型
│   │   └── services/    # 业务逻辑
│   ├── main.py          # 应用入口
│   └── requirements.txt # Python依赖
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── api/        # API接口
│   │   ├── components/ # 组件
│   │   ├── views/      # 页面
│   │   ├── router/     # 路由
│   │   └── stores/     # 状态管理
│   └── package.json    # Node依赖
└── uploads/            # 文件上传目录

```

## 功能模块

1. **成员管理**: 管理实验室成员信息
2. **项目展示**: 展示历届项目成果
3. **分享会**: 管理每学期13期分享会的资料
4. **设备管理**: 管理实验室电脑和服务器
5. **值日安排**: 安排和跟踪值日情况

## 快速开始

### 后端启动

1. 安装依赖:
```bash
cd backend
pip install -r requirements.txt
```

2. 配置数据库:
```bash
cp .env.example .env
# 编辑.env文件，配置数据库连接
```

3. 启动服务:
```bash
python main.py
```

后端服务运行在 http://localhost:8000

### 前端启动

1. 安装依赖:
```bash
cd frontend
npm install
```

2. 启动开发服务器:
```bash
npm run dev
```

前端服务运行在 http://localhost:5173

## 数据库配置

需要在PostgreSQL中创建数据库:

```sql
CREATE DATABASE lab313_platform;
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看自动生成的API文档。

## 开发计划

- [x] 项目初始化
- [x] 数据库模型设计
- [x] 前端基础框架搭建
- [ ] API接口开发
- [ ] 前端页面开发
- [ ] 文件上传功能
- [ ] 用户认证系统
- [ ] 权限管理

## 贡献

欢迎实验室成员贡献代码和提出建议！
