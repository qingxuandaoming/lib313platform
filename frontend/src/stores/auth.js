import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const res = await authApi.login({ username, password })
        const token = res.access_token
        this.token = token
        localStorage.setItem('token', token)
        this.user = await authApi.me()
        return true
      } catch (err) {
        this.error = err?.response?.data?.detail || '登录失败'
        return false
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      if (!this.token) return null
      try {
        this.user = await authApi.me()
        return this.user
      } catch (err) {
        this.logout()
        return null
      }
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
    }
  }
})