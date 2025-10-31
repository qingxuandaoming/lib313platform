# 313实验室开放平台 - 快速启动指南

## 一、环境准备

### 1. 安装依赖软件
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 2. 创建数据库

登录PostgreSQL，创建数据库：

```sql
CREATE DATABASE lab313_platform;
CREATE USER lab313user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE lab313_platform TO lab313user;
```

## 二、后端配置

### 1. 进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
复制 `.env.example` 为 `.env`：
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

编辑 `.env` 文件，配置数据库连接：
```ini
DATABASE_URL=postgresql://lab313user:yourpassword@localhost:5432/lab313_platform
SECRET_KEY=your-secret-key-here-change-in-production
```

### 5. 启动后端服务

```bash
python main.py
```

后端服务将运行在 http://localhost:8000

访问 http://localhost:8000/docs 查看API文档

## 三、前端配置

### 1. 进入前端目录
```bash
cd frontend
```

### 2. 安装依赖
```bash
npm install
```

### 3. 启动开发服务器
```bash
npm run dev
```

前端服务将运行在 http://localhost:5173

## 四、验证安装

1. 打开浏览器访问 http://localhost:5173
2. 应该能看到"313实验室开放平台"首页
3. 点击"成员管理"，可以添加、编辑、删除成员

## 五、API端点说明

### 成员管理
- `GET /api/v1/members` - 获取成员列表
- `POST /api/v1/members` - 创建成员
- `GET /api/v1/members/{id}` - 获取成员详情
- `PUT /api/v1/members/{id}` - 更新成员
- `DELETE /api/v1/members/{id}` - 删除成员

### 项目管理

- `GET /api/v1/projects` - 获取项目列表
- `POST /api/v1/projects` - 创建项目
- `PUT /api/v1/projects/{id}` - 更新项目
- `DELETE /api/v1/projects/{id}` - 删除项目

### 分享会

- `GET /api/v1/sessions` - 获取分享会列表
- `POST /api/v1/sessions` - 创建分享会
- `PUT /api/v1/sessions/{id}` - 更新分享会
- `DELETE /api/v1/sessions/{id}` - 删除分享会

### 设备管理

- `GET /api/v1/devices` - 获取设备列表
- `POST /api/v1/devices` - 添加设备
- `PUT /api/v1/devices/{id}` - 更新设备
- `DELETE /api/v1/devices/{id}` - 删除设备

### 值日管理

- `GET /api/v1/duty` - 获取值日安排
- `POST /api/v1/duty` - 创建值日安排
- `PATCH /api/v1/duty/{id}/complete` - 标记值日完成
- `DELETE /api/v1/duty/{id}` - 删除值日安排

### 文件管理

- `GET /api/v1/files` - 获取文件列表
- `POST /api/v1/files/upload` - 上传文件
- `DELETE /api/v1/files/{id}` - 删除文件

### 首页统计

- `GET /api/v1/stats` - 获取首页统计（项目数、成员数、会话数、设备数）

> 列表接口统一返回结构：`{ data: [...], total: N }`

## 六、常见问题

### 1. 数据库连接失败

- 确认PostgreSQL服务已启动
- 检查数据库用户名和密码是否正确
- 确认数据库已创建

### 2. 端口被占用

后端默认端口8000，前端默认端口5173，如果被占用可以修改：
- 后端：修改 `main.py` 中的 `port` 参数
- 前端：修改 `vite.config.js` 中的 `server.port`

### 3. CORS错误

确保后端 `main.py` 中的 CORS 配置包含了前端地址

## 七、生产部署

### 后端部署

```bash
# 使用gunicorn（推荐）
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 前端部署

```bash
npm run build
# 将dist目录部署到静态服务器（Nginx等）
```

## 八、下一步开发

当前已完成：
- ✅ 后端API接口（6个模块）
- ✅ 前端成员管理页面

待开发功能：
- [ ] 项目展示页面
- [ ] 分享会页面
- [ ] 设备管理页面
- [ ] 值日安排页面
- [ ] 用户认证系统
- [ ] 权限管理
- [ ] 数据统计和可视化

## 九、技术支持

如有问题，请联系实验室管理员或查看：
- API文档：http://localhost:8000/docs
- 项目README：../README.md
