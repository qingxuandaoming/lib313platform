import request from '@/utils/request'

// 获取分享会列表
export function getSessions(params) {
  return request({
    url: '/sessions',
    method: 'get',
    params
  })
}

// 获取分享会详情
export function getSession(id) {
  return request({
    url: `/sessions/${id}`,
    method: 'get'
  })
}

// 创建分享会
export function createSession(data) {
  return request({
    url: '/sessions',
    method: 'post',
    data
  })
}

// 更新分享会
export function updateSession(id, data) {
  return request({
    url: `/sessions/${id}`,
    method: 'put',
    data
  })
}

// 删除分享会
export function deleteSession(id) {
  return request({
    url: `/sessions/${id}`,
    method: 'delete'
  })
}
