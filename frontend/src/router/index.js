import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/members',
    name: 'Members',
    component: () => import('@/views/Members.vue')
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('@/views/Projects.vue')
  },
  {
    path: '/sessions',
    name: 'Sessions',
    component: () => import('@/views/Sessions.vue')
  },
  {
    path: '/devices',
    name: 'Devices',
    component: () => import('@/views/Devices.vue')
  },
  {
    path: '/duty',
    name: 'Duty',
    component: () => import('@/views/Duty.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
