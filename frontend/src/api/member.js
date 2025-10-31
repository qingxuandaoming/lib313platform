import request from '@/utils/request'

export const memberApi = {
  // 获取成员列表
  getMembers(params) {
    return request({
      url: '/members',
      method: 'get',
      params
    })
  },

  // 获取成员详情
  getMember(id) {
    return request({
      url: `/members/${id}`,
      method: 'get'
    })
  },

  // 创建成员
  createMember(data) {
    return request({
      url: '/members',
      method: 'post',
      data
    })
  },

  // 更新成员
  updateMember(id, data) {
    return request({
      url: `/members/${id}`,
      method: 'put',
      data
    })
  },

  // 删除成员
  deleteMember(id) {
    return request({
      url: `/members/${id}`,
      method: 'delete'
    })
  },

  // 获取成员统计
  getMemberStats() {
    return request({
      url: '/members/stats',
      method: 'get'
    })
  }
}

// 保持向后兼容的导出
export function getMembers(params) {
  return memberApi.getMembers(params)
}

export function getMember(id) {
  return memberApi.getMember(id)
}

export function createMember(data) {
  return memberApi.createMember(data)
}

export function updateMember(id, data) {
  return memberApi.updateMember(id, data)
}

export function deleteMember(id) {
  return memberApi.deleteMember(id)
}
