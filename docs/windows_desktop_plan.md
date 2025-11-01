# Windows 桌面端计划（Electron）

本计划旨在：不迁移数据到本地，统一由服务器维护数据库与文件，Windows 桌面端通过 Electron 封装前端并远程访问服务器 API，从而保证数据一致性与权限统一。

## 目标
- 桌面端与网页端共用同一后端与数据库（PostgreSQL）。
- 桌面端安装包（NSIS/MSI），可离线安装，启动后强制使用 HTTPS 接入服务器。
- 认证与权限统一（JWT），后端集中控制。

## 架构概览
- 服务器：Nginx (TLS 终止) → FastAPI/Uvicorn → PostgreSQL → 上传存储（本地卷或对象存储）。
- 网页端：Vite 构建的静态站点，访问 `https://api.<domain>/api/v1`。
- 桌面端：Electron 渲染进程加载本地打包的前端静态文件，所有请求指向 `https://api.<domain>/api/v1`。

## 前端改造要点
- 接口基础地址：在 `frontend/src/utils/request.js` 使用环境变量：
  - `VITE_API_BASE_URL=https://api.<your_domain>/api/v1`
- 路由模式：Electron 加载 `file://` 时建议使用哈希路由，避免刷新/深链接问题：
  - 在 `router/index.js` 通过 `VITE_ROUTER_MODE` 切换 `createWebHistory` / `createWebHashHistory`。
  - 桌面端 `.env.desktop` 中设置：`VITE_ROUTER_MODE=hash`。

## CORS 与安全
- 后端 `CORSMiddleware` 允许网页端域名与桌面端场景：
  - `allow_origins=[FRONTEND_URL, 'https://<your_domain>', 'null']` 或使用 `allow_origin_regex` 进行精确匹配。
- 强制使用 HTTPS；后端仅监听内网或 127.0.0.1，由反向代理暴露 443。
- 令牌存储：默认 `localStorage`；如需增强可后续使用 `keytar` 通过 `preload` 注入。

## Electron 实施步骤
1. 在 `frontend` 目录安装依赖：
   - `npm i -D electron electron-builder`
2. 新增主进程与构建配置：
   - `frontend/electron/main.js` 创建窗口并加载打包后的 `dist/index.html`。
   - `package.json` 增加 `build` 字段，配置 `appId`、`productName`、`nsis` 安装器行为。
3. 构建前端并打包：
   - `npm run build` 生成 `dist`。
   - `npx electron-builder --win nsis` 生成安装包（可选 `--win msi`）。
4. 健康检查：启动时请求 `GET https://api.<domain>/health`，异常则提示“服务器不可达”。

示例 `build` 片段（置于 `frontend/package.json`）：
```json
{
  "build": {
    "appId": "org.lab313.platform",
    "productName": "Lib313 Platform",
    "files": ["dist/**/*", "electron/**/*"],
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,
      "artifactName": "Lib313Platform-${version}-Setup.exe"
    }
  }
}
```

## 服务器配合（摘要）
- 反代：Nginx 终止 TLS，反向代理到 `127.0.0.1:8000`，开启 `http2` 与 `gzip`。
- 并发与规格（≥50 并发、≥100GB）：
  - 应用：`8 vCPU / 16GB RAM / 256–512GB NVMe`，`gunicorn -w 6`（或 `uvicorn --workers 6`）。
  - 数据库：`8 vCPU / 32GB RAM / ≥1TB NVMe`，合理的 `shared_buffers`、连接池与备份策略。
  - 上传：本地卷或对象存储（MinIO/S3）；每日快照与归档备份。

## 发布与更新
- 安装包：NSIS/MSI，创建桌面与开始菜单快捷方式。
- 代码签名：使用组织证书签名安装包，提升可信度。
- 自动更新（选做）：后续接入 `electron-updater`。

## 分阶段路线图
- P0（MVP）：前端改造、CORS 调整、Electron 打包、端到端验证。
- P1（稳定性）：健康检查、错误提示、日志与崩溃上报、安装器细节（图标、版本）。
- P2（运维增强）：自动更新、对象存储迁移、性能优化与监控仪表盘。

## 常见问题与规避
- 路由刷新 404：使用 `hash` 路由或注册自定义协议。
- Axios 相对路径失效：桌面端需完整 `https://api.<domain>/api/v1`。
- 端口占用与 CORS：仅开放 443；后端 `allow_origins` 明确授权网页端与桌面端。
- 上传大文件：按 `MAX_UPLOAD_SIZE` 严格限制并做进度提示；服务端设反代超时。

---
如需改为 Tauri（体积更小，需 Rust），可作为后续备选方案推进，流程与约束类似，后端仍集中部署于服务器。