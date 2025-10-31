import request from '@/utils/request'

// 获取成员列表
export function getMembers(params) {
  return request({
    url: '/members',
    method: 'get',
    params
  })
}

// 获取成员详情
export function getMember(id) {
  return request({
    url: `/members/${id}`,
    method: 'get'
  })
}

// 创建成员
export function createMember(data) {
  return request({
    url: '/members',
    method: 'post',
    data
  })
}

// 更新成员
export function updateMember(id, data) {
  return request({
    url: `/members/${id}`,
    method: 'put',
    data
  })
}

// 删除成员
export function deleteMember(id) {
  return request({
    url: `/members/${id}`,
    method: 'delete'
  })
}
