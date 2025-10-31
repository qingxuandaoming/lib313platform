# 313实验室开放平台 - 部署指南

## 系统要求

### 后端要求

- Python 3.8+
- PostgreSQL 12+
- pip (Python包管理器)

### 前端要求

- Node.js 16+
- npm 或 yarn

### 运行环境要求

- 操作系统: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- 内存: 最少4GB，推荐8GB+
- 存储: 最少10GB可用空间

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd 313lib开放平台
```

### 2. 后端部署

#### 2.1 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 配置数据库

1. 安装PostgreSQL并创建数据库:
  
```sql
CREATE DATABASE lab313_platform;
CREATE USER lab313_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE lab313_platform TO lab313_user;
```

1. 复制环境配置文件:
  
```bash
cp .env.example .env
```

1. 编辑 `.env` 文件，配置数据库连接:
  
```env
DATABASE_URL=postgresql://lab313_user:your_password@localhost/lab313_platform
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=../uploads
MAX_UPLOAD_SIZE=52428800
FRONTEND_URL=http://localhost:5173
```

#### 2.3 初始化数据库

```bash
# 创建数据库表
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

#### 2.4 启动后端服务

```bash
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 3. 前端部署

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 启动开发服务器

```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动。

#### 3.3 构建生产版本

```bash
npm run build
```

构建后的文件将在 `dist` 目录中。

## 详细配置

### 后端配置

#### 环境变量说明

| 变量名 | 说明 | 默认值 | 必需 |
|--------|------|--------|------|
| DATABASE_URL | 数据库连接URL | - | 是 |
| SECRET_KEY | JWT密钥 | - | 是 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token过期时间(分钟) | 30 | 否 |
| UPLOAD_DIR | 文件上传目录 | ../uploads | 否 |
| MAX_UPLOAD_SIZE | 最大上传文件大小(字节) | 52428800 | 否 |
| FRONTEND_URL | 前端URL | <http://localhost:5173> | 否 |

#### 数据库迁移

如果需要更新数据库结构，可以使用以下命令:

```bash
# 备份数据库
pg_dump lab313_platform > backup.sql

# 删除所有表并重新创建
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
```

### 前端配置

#### Vite配置 (vite.config.js)

```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

#### 环境变量

创建 `.env.local` 文件配置环境变量:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 生产环境部署

### 使用Docker部署

#### 1. 创建Docker Compose文件

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: lab313_platform
      POSTGRES_USER: lab313_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://lab313_user:your_password@postgres/lab313_platform
      SECRET_KEY: your-secret-key-here
    depends_on:
      - postgres
    volumes:
      - ./uploads:/app/uploads

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### 2. 创建后端Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

#### 3. 创建前端Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 4. 启动服务

```bash
docker-compose up -d
```

### 使用传统方式部署

#### 后端部署 (使用Gunicorn)

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### 前端部署 (使用Nginx)

1. 构建前端:
  
```bash
npm run build
```

1. 配置Nginx:
  
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 数据备份与恢复

### 数据库备份

```bash
# 备份数据库
pg_dump -h localhost -U lab313_user lab313_platform > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
psql -h localhost -U lab313_user lab313_platform < backup_20240101_120000.sql
```

### 文件备份

```bash
# 备份上传的文件
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# 恢复文件
tar -xzf uploads_backup_20240101_120000.tar.gz
```

## 监控与日志

### 后端日志

后端使用Python的logging模块，日志级别可以通过环境变量 `LOG_LEVEL` 设置:

```env
LOG_LEVEL=INFO
```

### 前端错误监控

可以集成Sentry等错误监控服务:

```javascript
// main.js
import * as Sentry from "@sentry/vue";

Sentry.init({
  app,
  dsn: "YOUR_SENTRY_DSN",
});
```

### 性能监控

推荐使用以下工具:

- 后端: Prometheus + Grafana
- 前端: Google Analytics, Lighthouse
- 数据库: pgAdmin, pg_stat_statements

## 安全配置

### HTTPS配置

生产环境建议使用HTTPS:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # 其他配置...
}
```

### 防火墙配置

```bash
# 只开放必要端口
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

### 数据库安全

1. 修改默认端口
2. 设置强密码
3. 限制连接IP
4. 定期更新

## 故障排除

### 常见问题

#### 1. 数据库连接失败

- 检查数据库服务是否启动
- 验证连接字符串是否正确
- 确认防火墙设置

#### 2. 文件上传失败

- 检查上传目录权限
- 验证文件大小限制
- 确认磁盘空间

#### 3. 前端页面空白

- 检查API接口是否正常
- 查看浏览器控制台错误
- 验证路由配置

#### 4. 跨域问题

- 检查CORS配置
- 验证代理设置
- 确认域名配置

### 日志查看

```bash
# 查看后端日志
tail -f backend.log

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# 查看数据库日志
tail -f /var/log/postgresql/postgresql-13-main.log
```

## 性能优化

### 后端优化

1. 使用连接池
2. 添加数据库索引
3. 实现缓存机制
4. 优化SQL查询

### 前端优化

1. 代码分割
2. 图片懒加载
3. 启用Gzip压缩
4. 使用CDN

### 数据库优化

1. 定期VACUUM
2. 分析查询计划
3. 调整配置参数
4. 监控慢查询

## 更新升级

### 后端更新

```bash
# 备份数据
pg_dump lab313_platform > backup.sql

# 更新代码
git pull origin main

# 安装新依赖
pip install -r requirements.txt

# 重启服务
systemctl restart lab313-backend
```

### 前端更新

```bash
# 更新代码
git pull origin main

# 安装新依赖
npm install

# 构建新版本
npm run build

# 部署
cp -r dist/* /var/www/html/
```

## 联系支持

如果遇到问题，请通过以下方式联系:

- 邮箱: <support@313lab.com>
- 文档: <https://docs.313lab.com>
- 问题反馈: <https://github.com/313lab/platform/issues>

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。
