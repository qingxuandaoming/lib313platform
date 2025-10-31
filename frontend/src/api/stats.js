import request from '@/utils/request'

// 获取首页统计数据
export function getStats() {
  return request({
    url: '/stats',
    method: 'get'
  })
}