// 自动对比工具：根据背景亮度选择合适的文字颜色
// 适配 Element Plus 表格：行与表头

function srgbToLinear(c) {
  c = c / 255
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
}

function luminance([r, g, b]) {
  const R = srgbToLinear(r)
  const G = srgbToLinear(g)
  const B = srgbToLinear(b)
  return 0.2126 * R + 0.7152 * G + 0.0722 * B
}

function parseColor(str) {
  if (!str) return null
  str = str.trim()
  // rgb/rgba
  const m = str.match(/^rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)$/i)
  if (m) {
    return [parseInt(m[1], 10), parseInt(m[2], 10), parseInt(m[3], 10), m[4] ? parseFloat(m[4]) : 1]
  }
  // #rrggbb
  const h = str.match(/^#([0-9a-f]{6})$/i)
  if (h) {
    const n = parseInt(h[1], 16)
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255, 1]
  }
  // transparent
  if (/transparent/i.test(str)) return [0, 0, 0, 0]
  return null
}

function composite(top, bottom) {
  // top、bottom: [r,g,b,a]
  const a = top[3]
  const b = bottom[3]
  const outA = a + b * (1 - a)
  const outR = a * top[0] + (1 - a) * bottom[0]
  const outG = a * top[1] + (1 - a) * bottom[1]
  const outB = a * top[2] + (1 - a) * bottom[2]
  return [outR, outG, outB, outA]
}

function getEffectiveBgColor(el, maxDepth = 8) {
  let cur = el
  // 初始为完全透明的背景
  let acc = [0, 0, 0, 0]
  for (let i = 0; i < maxDepth && cur; i++) {
    const cs = window.getComputedStyle(cur)
    const parsed = parseColor(cs.backgroundColor) || [0, 0, 0, 0]
    acc = composite(parsed, acc)
    if (acc[3] >= 0.98) break
    cur = cur.parentElement
  }
  if (acc[3] < 0.98) {
    // 尝试从全局背景变量或 body 背景补全
    const root = document.documentElement
    const body = document.body
    const rootBgColor = parseColor(window.getComputedStyle(root).backgroundColor)
    const bodyBgColor = parseColor(window.getComputedStyle(body).backgroundColor)
    const fallbackVar = window.getComputedStyle(root).getPropertyValue('--el-bg-color')
    const fallbackVarParsed = parseColor(fallbackVar)
    const fallback = rootBgColor || bodyBgColor || fallbackVarParsed || [0, 0, 0, 1]
    acc = composite(fallback, acc)
  }
  // 归一化到 0-255 范围
  return [Math.round(acc[0]), Math.round(acc[1]), Math.round(acc[2]), acc[3]]
}

function classifyBg(el) {
  const [r, g, b] = getEffectiveBgColor(el)
  const L = luminance([r, g, b])
  // WCAG 阈值约 0.5 之间，结合项目风格略微提升到 0.4
  return L >= 0.4 ? 'light' : 'dark'
}

function setRowContrast(row) {
  const type = classifyBg(row)
  row.setAttribute('data-bg', type)
}

function setHeaderContrast(th) {
  const type = classifyBg(th)
  th.setAttribute('data-bg', type)
}

function scanTables(root = document) {
  const tables = root.querySelectorAll('.el-table')
  tables.forEach((table) => {
    const rows = table.querySelectorAll('.el-table__row')
    rows.forEach(setRowContrast)
    const ths = table.querySelectorAll('.el-table__header-wrapper th')
    ths.forEach(setHeaderContrast)
  })
}

export function setupAutoContrast(root = document) {
  // 初次扫描
  scanTables(root)
  // 观察表格结构变化
  const observer = new MutationObserver((mutations) => {
    let needScan = false
    for (const m of mutations) {
      if (
        (m.target && m.target instanceof HTMLElement && m.target.matches('.el-table')) ||
        Array.from(m.addedNodes).some((n) => n instanceof HTMLElement && n.matches && n.matches('.el-table, .el-table__row, .el-table__header-wrapper')) ||
        Array.from(m.removedNodes).some((n) => n instanceof HTMLElement && n.matches && n.matches('.el-table, .el-table__row, .el-table__header-wrapper'))
      ) {
        needScan = true
        break
      }
    }
    if (needScan) scanTables(root)
  })

  observer.observe(root.body || root, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: ['class', 'style'],
  })

  return observer
}

export default {
  setupAutoContrast,
}