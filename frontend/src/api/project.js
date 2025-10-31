import request from '@/utils/request'

export const projectApi = {
  // 获取项目列表
  getProjects(params) {
    return request({
      url: '/projects',
      method: 'get',
      params
    })
  },

  // 获取项目详情
  getProject(id) {
    return request({
      url: `/projects/${id}`,
      method: 'get'
    })
  },

  // 创建项目
  createProject(data) {
    return request({
      url: '/projects',
      method: 'post',
      data
    })
  },

  // 更新项目
  updateProject(id, data) {
    return request({
      url: `/projects/${id}`,
      method: 'put',
      data
    })
  },

  // 删除项目
  deleteProject(id) {
    return request({
      url: `/projects/${id}`,
      method: 'delete'
    })
  },

  // 添加项目成员
  addProjectMember(projectId, memberId, role) {
    return request({
      url: `/projects/${projectId}/members/${memberId}`,
      method: 'post',
      params: { role }
    })
  },

  // 移除项目成员
  removeProjectMember(projectId, memberId) {
    return request({
      url: `/projects/${projectId}/members/${memberId}`,
      method: 'delete'
    })
  },

  // 获取项目统计
  getProjectStats() {
    return request({
      url: '/projects/stats',
      method: 'get'
    })
  }
}

// 保持向后兼容的导出
export function getProjects(params) {
  return projectApi.getProjects(params)
}

export function getProject(id) {
  return projectApi.getProject(id)
}

export function createProject(data) {
  return projectApi.createProject(data)
}

export function updateProject(id, data) {
  return projectApi.updateProject(id, data)
}

export function deleteProject(id) {
  return projectApi.deleteProject(id)
}

export function addProjectMember(projectId, memberId, role) {
  return projectApi.addProjectMember(projectId, memberId, role)
}

export function removeProjectMember(projectId, memberId) {
  return projectApi.removeProjectMember(projectId, memberId)
}
