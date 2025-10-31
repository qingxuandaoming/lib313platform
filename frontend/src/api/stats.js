import request from '@/utils/request'

export const statsApi = {
  // 获取系统统计数据
  getStats() {
    return request({
      url: '/stats',
      method: 'get'
    })
  }
}

export function getStats() {
  return statsApi.getStats()
}