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
# 可选：默认管理员账号（未配置则使用 admin/admin123）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 5. 启动后端服务

```bash
python main.py
```

后端服务将运行在 <http://localhost:8000>

访问 [http://localhost:8000/docs](http://localhost:8000/docs) 查看API文档

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

前端服务将运行在 <http://localhost:5173>

### 4. 配置前端环境变量（网页端与桌面端通用）

在前端根目录创建（或更新）环境文件，例如：

```ini
# .env.local（开发指向本地后端）
VITE_API_BASE_URL=http://localhost:8000/api/v1

# .env.production（生产指向服务器后端）
VITE_API_BASE_URL=https://api.<your_domain>/api/v1

# 桌面端建议使用哈希路由，避免 file:// 刷新异常
VITE_ROUTER_MODE=hash
```

> 提示：`frontend/src/utils/request.js` 读取 `VITE_API_BASE_URL` 作为请求基础地址；`router/index.js` 可根据 `VITE_ROUTER_MODE` 切换 `createWebHistory` 或 `createWebHashHistory`。

## 四、验证安装

1. 打开浏览器访问 <http://localhost:5173>
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
- `GET /api/v1/files/{id}` - 获取文件详情
- `GET /api/v1/files/{id}/download` - 下载文件
- `PUT /api/v1/files/{id}` - 更新文件信息
- `POST /api/v1/files/batch-upload` - 批量上传文件（最多10个）
- `GET /api/v1/files/stats` - 获取文件统计（总数、总大小、按类型统计）

### 首页统计

- `GET /api/v1/stats` - 获取首页统计（成员数、项目数、分享会数、设备数、文件数）

### 认证

- `POST /api/v1/auth/login` - 管理员登录，返回访问令牌
  - 请求体示例：`{ "username": "admin", "password": "admin123" }`
- `GET /api/v1/auth/me` - 使用 Bearer Token 获取当前用户信息
  - 请求头：`Authorization: Bearer <access_token>`

> 提示：首次登录会自动创建或重置默认管理员（用户名/密码取自 `.env` 或默认 `admin/admin123`）。

> 返回结构说明：
> - 所有列表（成员、项目、分享会、设备、值日、文件）：统一返回 `{ data: [...], total: N }`
> - 批量上传 `POST /api/v1/files/batch-upload`：返回 `BatchUploadResponse`，包含 `uploaded_files`、`failed_files`（可为空）和 `message`

> 前端令牌使用：在 `frontend/src/utils/request.js` 的请求拦截器中为需要认证的请求添加 `Authorization: Bearer <token>`。

## 六、桌面端（Electron）快速说明

- 目标：不迁移数据到本地，统一由服务器维护数据库与文件；Electron 仅作为前端壳接入远程 API。
- 依赖：`electron`、`electron-builder`；打包生成 NSIS/MSI 安装包。
- 步骤摘要：
  1. `npm run build` 生成 `dist` 静态文件；
  2. 在 `frontend/electron/main.js` 创建窗口并加载 `dist/index.html`；
  3. 在 `package.json` 增加 `build` 字段配置安装器；
  4. `npx electron-builder --win nsis` 生成安装包；
  5. 启动前做 `GET https://api.<your_domain>/health` 健康检查，异常提示“服务器不可达”。

> 完整计划见 `docs/windows_desktop_plan.md`；服务器部署建议与规格见 `docs/DEPLOYMENT.md`。

## 七、常见问题

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

## 八、生产部署

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

## 九、下一步开发

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

## 十、技术支持

如有问题，请联系实验室管理员或查看：

- API文档：<http://localhost:8000/docs>
- 项目README：../README.md
