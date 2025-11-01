import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import './assets/themes.css'
import './assets/element-override.css'
import { useThemeStore } from './stores/theme'
import { setupAutoContrast } from './utils/contrast'

const app = createApp(App)
const pinia = createPinia()

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 初始化主题
const theme = useThemeStore()
theme.applyTheme()

// 根据路由自动应用光晕强度（弱/中/强）
let __contrastObserver = null
router.afterEach((to) => {
  if (theme.autoGlowByPage) {
    const path = to.path || ''
    let level = 'medium'
    let clarity = 'normal'
    if (/^(\/)?$/.test(path) || /home|dashboard|stats/.test(path)) {
      level = 'medium'
      clarity = 'normal'
    } else if (/members|devices|projects|project|sessions|files|list|display|overview/.test(path)) {
      level = 'low'
      clarity = 'high' // 列表页启用高清晰模式
    } else if (/profile|settings|config/.test(path)) {
      level = 'high'
      clarity = 'normal'
    }
    theme.setGlowIntensity(level)
    document.documentElement.setAttribute('data-clarity', clarity)
  }
  // 初始化或重置自动对比观察器
  if (__contrastObserver) {
    try { __contrastObserver.disconnect() } catch {}
  }
  // 等待路由渲染完成后再扫描
  setTimeout(() => {
    __contrastObserver = setupAutoContrast(document)
  }, 0)
})

app.mount('#app')
