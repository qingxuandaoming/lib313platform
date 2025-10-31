import request from '@/utils/request'

// 获取文件列表
export const getFiles = (params = {}) => {
  return request({
    url: '/files',
    method: 'get',
    params
  })
}

// 获取文件统计信息
export const getFileStats = () => {
  return request({
    url: '/files/stats',
    method: 'get'
  })
}

// 获取单个文件详情
export const getFile = (id) => {
  return request({
    url: `/files/${id}`,
    method: 'get'
  })
}

// 下载文件
export const downloadFile = (id) => {
  return request({
    url: `/files/${id}/download`,
    method: 'get',
    responseType: 'blob'
  })
}

// 上传文件
export const uploadFile = (formData) => {
  return request({
    url: '/files/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 批量上传文件
export const batchUploadFiles = (formData) => {
  return request({
    url: '/files/batch-upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 更新文件信息
export const updateFile = (id, data) => {
  return request({
    url: `/files/${id}`,
    method: 'put',
    data
  })
}

// 删除文件
export const deleteFile = (id) => {
  return request({
    url: `/files/${id}`,
    method: 'delete'
  })
}

// 文件API对象
export const fileApi = {
  getFiles,
  getFileStats,
  getFile,
  downloadFile,
  uploadFile,
  batchUploadFiles,
  updateFile,
  deleteFile
}

export default fileApi