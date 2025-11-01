import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    scheme: localStorage.getItem('theme_scheme') || 'qing', // 'qing'、'jiang' 或 'custom'
    glassBlur: Number(localStorage.getItem('glass_blur') || 16),
    glassOpacity: Number(localStorage.getItem('glass_opacity') || 0.12),
    customPalette: JSON.parse(localStorage.getItem('custom_palette') || '{}'),
    // 自定义背景渐变（两端色）
    customBgStart: localStorage.getItem('custom_bg_start') || '#0a1a1f',
    customBgEnd: localStorage.getItem('custom_bg_end') || '#050f13',
    // 光晕强度：low / medium / high
    glowIntensity: localStorage.getItem('glow_intensity') || 'medium',
    // 是否按页面类型自动应用光晕等级
    autoGlowByPage: (localStorage.getItem('glow_auto') || 'true') === 'true'
  }),
  actions: {
    setScheme(scheme) {
      this.scheme = scheme
      localStorage.setItem('theme_scheme', scheme)
      this.applyTheme()
    },
    setGlassBlur(px) {
      this.glassBlur = Number(px)
      localStorage.setItem('glass_blur', String(this.glassBlur))
      this.applyTheme()
    },
    setGlassOpacity(opacity) {
      this.glassOpacity = Number(opacity)
      localStorage.setItem('glass_opacity', String(this.glassOpacity))
      this.applyTheme()
    },
    setCustomPalette(palette) {
      this.customPalette = { ...this.customPalette, ...palette }
      localStorage.setItem('custom_palette', JSON.stringify(this.customPalette))
      if (this.scheme === 'custom') {
        this.applyTheme()
      }
    },
    setCustomBackgroundGradient(start, end) {
      if (start) this.customBgStart = start
      if (end) this.customBgEnd = end
      localStorage.setItem('custom_bg_start', this.customBgStart)
      localStorage.setItem('custom_bg_end', this.customBgEnd)
      if (this.scheme === 'custom') {
        this.applyTheme()
      }
    },
    setGlowIntensity(level) {
      this.glowIntensity = level || 'medium'
      localStorage.setItem('glow_intensity', this.glowIntensity)
      // 若开启自动按页面，则仍更新变量以适配当前页
      this.applyGlowIntensity(this.glowIntensity)
    },
    setAutoGlowByPage(enabled) {
      this.autoGlowByPage = !!enabled
      localStorage.setItem('glow_auto', String(this.autoGlowByPage))
      if (!this.autoGlowByPage) {
        this.applyGlowIntensity(this.glowIntensity)
      }
    },
    applyTheme() {
      const root = document.documentElement
      root.setAttribute('data-theme', this.scheme)
      root.style.setProperty('--glass-blur', `${this.glassBlur}px`)
      root.style.setProperty('--glass-opacity', `${this.glassOpacity}`)

      // 覆盖 Element Plus 颜色变量
      if (this.scheme === 'custom') {
        const p = this.customPalette || {}
        const primary = p.primary || '#409EFF'
        const success = p.success || '#67C23A'
        const warning = p.warning || '#E6A23C'
        const danger = p.danger || '#F56C6C'
        const info = p.info || '#909399'
        const textStrong = p.textStrong || '#ECECEC'
        const textSoft = p.textSoft || '#CFCFCF'

        root.style.setProperty('--el-color-primary', primary)
        root.style.setProperty('--el-color-success', success)
        root.style.setProperty('--el-color-warning', warning)
        root.style.setProperty('--el-color-danger', danger)
        root.style.setProperty('--el-color-info', info)
        root.style.setProperty('--text-strong', textStrong)
        root.style.setProperty('--text-soft', textSoft)
        // 背景渐变（自定义方案）
        const start = this.customBgStart || '#0a1a1f'
        const end = this.customBgEnd || '#050f13'
        const appBg = `radial-gradient(1200px 600px at 50% 0%, ${start}, ${end}), linear-gradient(180deg, ${start}, ${end})`
        root.style.setProperty('--app-bg', appBg)

        // 常用背景与边框（与玻璃风格协调）
        root.style.setProperty('--el-bg-color', 'rgba(255,255,255,0.06)')
        root.style.setProperty('--el-bg-color-overlay', 'rgba(255,255,255,0.10)')
        root.style.setProperty('--el-text-color-primary', textStrong)
        root.style.setProperty('--el-text-color-regular', textSoft)
        root.style.setProperty('--el-text-color-secondary', 'rgba(235,235,235,0.7)')
        root.style.setProperty('--el-border-color', 'rgba(255,255,255,0.22)')
      }
      // 应用光晕强度（所有方案）
      this.applyGlowIntensity(this.glowIntensity)
    }
    ,
    applyGlowIntensity(level = 'medium') {
      const root = document.documentElement
      const alphaMap = { low: 0.35, medium: 0.55, high: 0.75 }
      const sizeMap = {
        low: { btnOffset: '6px', btnBlur: '12px', cardOffset: '10px', cardBlur: '22px', menuOffset: '6px', menuBlur: '14px', tableOffset: '4px', tableBlur: '12px' },
        medium: { btnOffset: '8px', btnBlur: '18px', cardOffset: '14px', cardBlur: '34px', menuOffset: '8px', menuBlur: '22px', tableOffset: '6px', tableBlur: '18px' },
        high: { btnOffset: '10px', btnBlur: '26px', cardOffset: '16px', cardBlur: '42px', menuOffset: '10px', menuBlur: '28px', tableOffset: '8px', tableBlur: '22px' }
      }

      // 解析主色为 rgba
      const getPrimary = () => {
        const computedPrimary = getComputedStyle(root).getPropertyValue('--el-color-primary').trim()
        return computedPrimary || '#409EFF'
      }
      const hexToRgb = (hex) => {
        const h = hex.replace('#','')
        const bigint = parseInt(h.length === 3 ? h.split('').map(c=>c+c).join('') : h, 16)
        const r = (bigint >> 16) & 255
        const g = (bigint >> 8) & 255
        const b = bigint & 255
        return { r, g, b }
      }
      const toRgba = (color, alpha) => {
        if (color.startsWith('#')) {
          const { r, g, b } = hexToRgb(color)
          return `rgba(${r}, ${g}, ${b}, ${alpha})`
        }
        if (color.startsWith('rgb')) {
          const nums = color.replace(/rgba?\(|\)/g,'').split(',').map(v=>v.trim())
          const [r,g,b] = nums
          return `rgba(${r}, ${g}, ${b}, ${alpha})`
        }
        return color
      }
      const alpha = alphaMap[level] || 0.55
      const primary = getPrimary()
      const glow = toRgba(primary, alpha)
      root.style.setProperty('--glow-color', glow)
      root.setAttribute('data-glow', level)

      const sizes = sizeMap[level] || sizeMap.medium
      root.style.setProperty('--glow-offset-btn', sizes.btnOffset)
      root.style.setProperty('--glow-elev-btn', sizes.btnBlur)
      root.style.setProperty('--glow-offset-card', sizes.cardOffset)
      root.style.setProperty('--glow-elev-card', sizes.cardBlur)
      root.style.setProperty('--glow-offset-menu', sizes.menuOffset)
      root.style.setProperty('--glow-elev-menu', sizes.menuBlur)
      root.style.setProperty('--glow-offset-table', sizes.tableOffset)
      root.style.setProperty('--glow-elev-table', sizes.tableBlur)
    }
  }
})