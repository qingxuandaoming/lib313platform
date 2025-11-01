// 最小 Electron 主进程示例：加载打包后的前端并做基础健康检查
const { app, BrowserWindow, dialog } = require('electron')
const path = require('path')
const http = require('http')
const https = require('https')

function checkServerHealth(url) {
  return new Promise((resolve) => {
    const client = url.startsWith('https') ? https : http
    const req = client.get(url, (res) => {
      resolve(res.statusCode >= 200 && res.statusCode < 300)
    })
    req.on('error', () => resolve(false))
    req.end()
  })
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // 如需桥接安全存储等，可添加 preload 脚本
      // preload: path.join(__dirname, 'preload.js')
    }
  })

  const apiBase = process.env.VITE_API_BASE_URL || 'https://api.example.com/api/v1'
  const healthUrl = apiBase.replace(/\/?api\/v1$/, '') + '/health'
  const ok = await checkServerHealth(healthUrl)
  if (!ok) {
    dialog.showErrorBox('服务器不可达', `请检查网络或稍后再试：\n${healthUrl}`)
  }

  // 加载打包后的前端静态文件（统一从 dist 加载）
  const indexPath = path.join(__dirname, '..', 'dist', 'index.html')
  await win.loadFile(indexPath)
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})