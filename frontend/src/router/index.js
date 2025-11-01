import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/Login.vue')
      },
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: 'members',
        name: 'Members',
        component: () => import('@/views/Members.vue')
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/Projects.vue')
      },
      {
        path: 'sessions',
        name: 'Sessions',
        component: () => import('@/views/Sessions.vue')
      },
      {
        path: 'devices',
        name: 'Devices',
        component: () => import('@/views/Devices.vue')
      },
      {
        path: 'duty',
        name: 'Duty',
        component: () => import('@/views/Duty.vue')
      },
      {
        path: 'files',
        name: 'Files',
        component: () => import('@/views/Files.vue')
      }
    ]
  }
]

// 根据环境变量决定路由模式：桌面端建议使用哈希路由
const routerMode = (import.meta.env?.VITE_ROUTER_MODE || 'history').toLowerCase()
const history = routerMode === 'hash' ? createWebHashHistory() : createWebHistory()

const router = createRouter({
  history,
  routes
})

// 兜底路由：将未知路径重定向到首页，避免外部脚本导航导致告警
router.addRoute({ path: '/:pathMatch(.*)*', redirect: '/home' })

export default router
