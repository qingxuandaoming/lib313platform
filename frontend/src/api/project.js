import request from '@/utils/request'

// 获取项目列表
export function getProjects(params) {
  return request({
    url: '/projects',
    method: 'get',
    params
  })
}

// 获取项目详情
export function getProject(id) {
  return request({
    url: `/projects/${id}`,
    method: 'get'
  })
}

// 创建项目
export function createProject(data) {
  return request({
    url: '/projects',
    method: 'post',
    data
  })
}

// 更新项目
export function updateProject(id, data) {
  return request({
    url: `/projects/${id}`,
    method: 'put',
    data
  })
}

// 删除项目
export function deleteProject(id) {
  return request({
    url: `/projects/${id}`,
    method: 'delete'
  })
}

// 添加项目成员
export function addProjectMember(projectId, memberId, role) {
  return request({
    url: `/projects/${projectId}/members/${memberId}`,
    method: 'post',
    params: { role }
  })
}

// 移除项目成员
export function removeProjectMember(projectId, memberId) {
  return request({
    url: `/projects/${projectId}/members/${memberId}`,
    method: 'delete'
  })
}
