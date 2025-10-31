import request from '@/utils/request'

export const authApi = {
  login(data) {
    return request({
      url: '/auth/login',
      method: 'post',
      data
    })
  },
  me() {
    return request({
      url: '/auth/me',
      method: 'get'
    })
  }
}