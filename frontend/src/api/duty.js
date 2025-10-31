import request from '@/utils/request'

// 获取值日安排列表
export function getDutySchedules(params) {
  return request({
    url: '/duty',
    method: 'get',
    params
  })
}

// 获取值日安排详情
export function getDutySchedule(id) {
  return request({
    url: `/duty/${id}`,
    method: 'get'
  })
}

// 创建值日安排
export function createDutySchedule(data) {
  return request({
    url: '/duty',
    method: 'post',
    data
  })
}

// 更新值日安排
export function updateDutySchedule(id, data) {
  return request({
    url: `/duty/${id}`,
    method: 'put',
    data
  })
}

// 删除值日安排
export function deleteDutySchedule(id) {
  return request({
    url: `/duty/${id}`,
    method: 'delete'
  })
}

// 标记值日完成
export function completeDuty(id, completionNotes) {
  return request({
    url: `/duty/${id}/complete`,
    method: 'patch',
    params: { completion_notes: completionNotes }
  })
}
