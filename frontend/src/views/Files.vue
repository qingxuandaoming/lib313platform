<template>
  <div class="files-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>文档管理</h2>
          <div class="header-actions">
            <el-button type="primary" @click="showUploadDialog">
              <el-icon><Upload /></el-icon>
              上传文件
            </el-button>
            <el-button type="success" @click="showBatchUploadDialog">
              <el-icon><FolderAdd /></el-icon>
              批量上传
            </el-button>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="stats-section" v-if="stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-statistic title="总文件数" :value="stats.total_files">
              <template #suffix>
                <el-icon><Document /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="总大小" :value="stats.total_size_mb" suffix="MB">
              <template #suffix>
                <el-icon><Folder /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="文档数" :value="stats.type_stats?.document || 0">
              <template #suffix>
                <el-icon><Reading /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="图片数" :value="stats.type_stats?.image || 0">
              <template #suffix>
                <el-icon><Picture /></el-icon>
              </template>
            </el-statistic>
          </el-col>
        </el-row>
      </div>

      <!-- 搜索和筛选栏 -->
      <div class="filter-bar">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文件名或描述"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="filterType" placeholder="文件类型" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="文档" value="document" />
              <el-option label="图片" value="image" />
              <el-option label="演示文稿" value="presentation" />
              <el-option label="视频" value="video" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="filterProject" placeholder="关联项目" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option v-for="project in projects" :key="project.id" :label="project.name" :value="project.id" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 视图切换 -->
      <div class="view-toggle">
        <el-radio-group v-model="viewMode" @change="handleViewChange">
          <el-radio-button label="grid">
            <el-icon><Grid /></el-icon>
            卡片视图
          </el-radio-button>
          <el-radio-button label="list">
            <el-icon><List /></el-icon>
            列表视图
          </el-radio-button>
        </el-radio-group>
      </div>

      <!-- 文件卡片展示 -->
      <div v-if="viewMode === 'grid'" class="files-grid" v-loading="loading">
        <el-card v-for="file in files" :key="file.id" class="file-card" shadow="hover">
          <div class="file-preview">
            <div class="file-icon">
              <el-icon :size="60" :color="getFileTypeColor(file.file_type)">
                <component :is="getFileTypeIcon(file.file_type)" />
              </el-icon>
            </div>
            <div class="file-type-badge">
              <el-tag :type="getFileTypeTagType(file.file_type)" size="small">
                {{ getFileTypeText(file.file_type) }}
              </el-tag>
            </div>
          </div>

          <div class="file-info">
            <h4 class="file-name" :title="file.original_filename">
              {{ file.original_filename }}
            </h4>
            <p class="file-description" v-if="file.description">
              {{ file.description }}
            </p>
            
            <div class="file-meta">
              <div class="meta-item">
                <el-icon><Calendar /></el-icon>
                {{ formatDate(file.created_at) }}
              </div>
              <div class="meta-item">
                <el-icon><Coin /></el-icon>
                {{ formatFileSize(file.file_size) }}
              </div>
            </div>

            <div class="file-actions">
              <el-button type="primary" size="small" @click="handleDownload(file)">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
              <el-button type="info" size="small" @click="showEditDialog(file)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(file)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 文件列表展示 -->
      <div v-else>
        <el-table :data="files" style="width: 100%" v-loading="loading" stripe>
          <el-table-column type="index" label="#" width="60" />
          <el-table-column prop="original_filename" label="文件名" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="file-name-cell">
                <el-icon :color="getFileTypeColor(row.file_type)">
                  <component :is="getFileTypeIcon(row.file_type)" />
                </el-icon>
                <span>{{ row.original_filename }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="file_type" label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="getFileTypeTagType(row.file_type)" size="small">
                {{ getFileTypeText(row.file_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="file_size" label="大小" width="100">
            <template #default="{ row }">
              {{ formatFileSize(row.file_size) }}
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" show-overflow-tooltip />
          <el-table-column prop="created_at" label="上传时间" width="150">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleDownload(row)">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
              <el-button type="info" size="small" @click="showEditDialog(row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handlePageSizeChange"
            @current-change="handleCurrentPageChange"
          />
        </div>
      </div>

      <el-empty v-if="!loading && files.length === 0" description="暂无文件数据" />
    </el-card>

    <!-- 上传文件对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef" label-width="100px">
        <el-form-item label="选择文件" prop="file" required>
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            drag
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 jpg/png/gif/pdf/doc/docx/ppt/pptx/mp4 等格式，文件大小不超过 50MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item label="关联项目" prop="project_id">
          <el-select v-model="uploadForm.project_id" placeholder="选择关联项目" style="width: 100%" clearable>
            <el-option v-for="project in projects" :key="project.id" :label="project.name" :value="project.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="文件描述" prop="description">
          <el-input v-model="uploadForm.description" type="textarea" :rows="3" placeholder="请输入文件描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">
          上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 批量上传对话框 -->
    <el-dialog
      v-model="batchUploadDialogVisible"
      title="批量上传文件"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form :model="batchUploadForm" label-width="100px">
        <el-form-item label="选择文件" required>
          <el-upload
            ref="batchUploadRef"
            :auto-upload="false"
            :limit="10"
            multiple
            drag
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                最多可同时上传 10 个文件，每个文件大小不超过 50MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item label="关联项目" prop="project_id">
          <el-select v-model="batchUploadForm.project_id" placeholder="选择关联项目" style="width: 100%" clearable>
            <el-option v-for="project in projects" :key="project.id" :label="project.name" :value="project.id" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="batchUploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBatchUpload" :loading="batchUploading">
          批量上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑文件对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑文件信息"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="文件名" prop="original_filename">
          <el-input v-model="editForm.original_filename" placeholder="请输入文件名" />
        </el-form-item>

        <el-form-item label="文件描述" prop="description">
          <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="请输入文件描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEdit" :loading="editing">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Upload, FolderAdd, Document, Folder, Reading, Picture, Search, Grid, List,
  Calendar, Coin, Download, Edit, Delete, UploadFilled
} from '@element-plus/icons-vue'
import { fileApi } from '@/api/file'
import { projectApi } from '@/api/project'

const loading = ref(false)
const uploading = ref(false)
const batchUploading = ref(false)
const editing = ref(false)

const files = ref([])
const projects = ref([])
const stats = ref(null)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const searchQuery = ref('')
const filterType = ref('')
const filterProject = ref('')
const viewMode = ref('grid')

const uploadDialogVisible = ref(false)
const batchUploadDialogVisible = ref(false)
const editDialogVisible = ref(false)

const uploadFormRef = ref(null)
const batchUploadRef = ref(null)
const editFormRef = ref(null)
const uploadRef = ref(null)

const uploadForm = reactive({
  file: null,
  project_id: null,
  description: ''
})

const batchUploadForm = reactive({
  project_id: null
})

const editForm = reactive({
  id: null,
  original_filename: '',
  description: ''
})

const uploadRules = {
  file: [{ required: true, message: '请选择要上传的文件', trigger: 'change' }]
}

const editRules = {
  original_filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }]
}

// 加载文件列表
const loadFiles = async () => {
  loading.value = true
  try {
    const params = {
      skip: viewMode.value === 'list' ? (currentPage.value - 1) * pageSize.value : 0,
      limit: viewMode.value === 'list' ? pageSize.value : 1000,
      search: searchQuery.value || undefined,
      file_type: filterType.value || undefined,
      project_id: filterProject.value || undefined
    }
    
    const response = await fileApi.getFiles(params)
    if (Array.isArray(response)) {
      files.value = response
      total.value = response.length
    } else {
      files.value = response?.data ?? []
      const dataLen = Array.isArray(response?.data) ? response.data.length : 0
      total.value = response?.total ?? dataLen
    }
  } catch (error) {
    console.error('加载文件列表失败:', error)
    ElMessage.error('加载文件列表失败')
    files.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 加载统计信息
const loadStats = async () => {
  try {
    stats.value = await fileApi.getFileStats()
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

// 加载项目列表
const loadProjects = async () => {
  try {
    const response = await projectApi.getProjects({ limit: 1000 })
    projects.value = Array.isArray(response) ? response : (response?.data ?? [])
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadFiles()
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  filterType.value = ''
  filterProject.value = ''
  currentPage.value = 1
  loadFiles()
}

// 视图模式切换
const handleViewChange = () => {
  currentPage.value = 1
  loadFiles()
}

// 页面大小改变
const handlePageSizeChange = () => {
  currentPage.value = 1
  loadFiles()
}

// 当前页改变
const handleCurrentPageChange = () => {
  loadFiles()
}

// 显示上传对话框
const showUploadDialog = () => {
  uploadForm.file = null
  uploadForm.project_id = null
  uploadForm.description = ''
  uploadDialogVisible.value = true
}

// 显示批量上传对话框
const showBatchUploadDialog = () => {
  batchUploadForm.project_id = null
  batchUploadDialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (file) => {
  editForm.id = file.id
  editForm.original_filename = file.original_filename
  editForm.description = file.description || ''
  editDialogVisible.value = true
}

// 文件选择处理
const handleFileChange = (file) => {
  uploadForm.file = file.raw
}

// 文件移除处理
const handleFileRemove = () => {
  uploadForm.file = null
}

// 上传文件
const handleUpload = async () => {
  if (!uploadFormRef.value) return
  
  await uploadFormRef.value.validate(async (valid) => {
    if (valid && uploadForm.file) {
      uploading.value = true
      try {
        const formData = new FormData()
        formData.append('file', uploadForm.file)
        if (uploadForm.project_id) {
          formData.append('project_id', uploadForm.project_id)
        }
        if (uploadForm.description) {
          formData.append('description', uploadForm.description)
        }
        
        await fileApi.uploadFile(formData)
        ElMessage.success('文件上传成功')
        uploadDialogVisible.value = false
        loadFiles()
        loadStats()
      } catch (error) {
        console.error('文件上传失败:', error)
        const message = error.response?.data?.detail || '文件上传失败'
        ElMessage.error(message)
      } finally {
        uploading.value = false
      }
    }
  })
}

// 批量上传文件
const handleBatchUpload = async () => {
  const fileList = batchUploadRef.value?.uploadFiles || []
  if (fileList.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }
  
  batchUploading.value = true
  try {
    const formData = new FormData()
    fileList.forEach(file => {
      formData.append('files', file.raw)
    })
    if (batchUploadForm.project_id) {
      formData.append('project_id', batchUploadForm.project_id)
    }
    
    const result = await fileApi.batchUploadFiles(formData)
    
    if (result.failed_files && result.failed_files.length > 0) {
      ElMessage.warning(result.message)
    } else {
      ElMessage.success('批量上传成功')
    }
    
    batchUploadDialogVisible.value = false
    loadFiles()
    loadStats()
  } catch (error) {
    console.error('批量上传失败:', error)
    const message = error.response?.data?.detail || '批量上传失败'
    ElMessage.error(message)
  } finally {
    batchUploading.value = false
  }
}

// 编辑文件
const handleEdit = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      editing.value = true
      try {
        await fileApi.updateFile(editForm.id, {
          original_filename: editForm.original_filename,
          description: editForm.description
        })
        ElMessage.success('文件信息更新成功')
        editDialogVisible.value = false
        loadFiles()
      } catch (error) {
        console.error('更新失败:', error)
        const message = error.response?.data?.detail || '更新失败'
        ElMessage.error(message)
      } finally {
        editing.value = false
      }
    }
  })
}

// 下载文件
const handleDownload = async (file) => {
  try {
    const response = await fileApi.downloadFile(file.id)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.original_filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('文件下载成功')
  } catch (error) {
    console.error('文件下载失败:', error)
    ElMessage.error('文件下载失败')
  }
}

// 删除文件
const handleDelete = (file) => {
  ElMessageBox.confirm(`确定要删除文件 ${file.original_filename} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await fileApi.deleteFile(file.id)
      ElMessage.success('删除成功')
      loadFiles()
      loadStats()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 获取文件类型图标
const getFileTypeIcon = (fileType) => {
  const icons = {
    document: 'Document',
    image: 'Picture',
    presentation: 'Reading',
    video: 'VideoPlay',
    other: 'Document'
  }
  return icons[fileType] || 'Document'
}

// 获取文件类型颜色
const getFileTypeColor = (fileType) => {
  const colors = {
    document: '#409EFF',
    image: '#67C23A',
    presentation: '#E6A23C',
    video: '#F56C6C',
    other: '#909399'
  }
  return colors[fileType] || '#909399'
}

// 获取文件类型标签类型
const getFileTypeTagType = (fileType) => {
  const types = {
    document: 'primary',
    image: 'success',
    presentation: 'warning',
    video: 'danger',
    other: 'info'
  }
  return types[fileType] || 'info'
}

// 获取文件类型文本
const getFileTypeText = (fileType) => {
  const texts = {
    document: '文档',
    image: '图片',
    presentation: '演示',
    video: '视频',
    other: '其他'
  }
  return texts[fileType] || '其他'
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '-'
  
  const units = ['B', 'KB', 'MB', 'GB']
  let index = 0
  let fileSize = size
  
  while (fileSize >= 1024 && index < units.length - 1) {
    fileSize /= 1024
    index++
  }
  
  return `${fileSize.toFixed(1)} ${units[index]}`
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadFiles()
  loadStats()
  loadProjects()
})
</script>

<style scoped>
.files-container {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.stats-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-bar {
  margin-bottom: 20px;
}

.view-toggle {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.file-card {
  transition: transform 0.2s;
  height: fit-content;
}

.file-card:hover {
  transform: translateY(-5px);
}

.file-preview {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.file-icon {
  margin-bottom: 10px;
}

.file-type-badge {
  position: absolute;
  top: 10px;
  right: 10px;
}

.file-info h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.file-meta {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #909399;
  font-size: 12px;
}

.file-actions {
  display: flex;
  gap: 8px;
}

.file-actions .el-button {
  flex: 1;
}

.file-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-dialog .el-form {
  padding: 0 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-upload {
  width: 100%;
}

.el-upload__tip {
  color: #606266;
  font-size: 12px;
  margin-top: 10px;
}
</style>