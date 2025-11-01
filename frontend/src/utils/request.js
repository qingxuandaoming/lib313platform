import axios from 'axios'

// 通过环境变量控制 API 基础地址；
// 桌面端（Electron）应指定完整的 https://api.<domain>/api/v1
const baseURL = import.meta.env?.VITE_API_BASE_URL || '/api/v1'

const request = axios.create({
  baseURL,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 附加鉴权令牌
    const token = localStorage.getItem('token')
    if (token) {
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

export default request
