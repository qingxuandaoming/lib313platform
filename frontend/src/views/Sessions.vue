<template>
  <div class="sessions-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>分享会管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加分享会
          </el-button>
        </div>
      </template>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-input
          v-model="searchSemester"
          placeholder="搜索学期，如：2024-1"
          style="width: 200px"
          clearable
          @clear="loadSessions"
        />
        <el-button @click="loadSessions">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
      </div>

      <!-- 分享会列表 -->
      <div class="sessions-list" v-loading="loading">
        <el-timeline>
          <el-timeline-item
            v-for="session in sessions"
            :key="session.id"
            :timestamp="formatDate(session.session_date)"
            placement="top"
          >
            <el-card class="session-card" shadow="hover">
              <div class="session-header">
                <div class="session-title">
                  <h3>{{ session.title }}</h3>
                  <div class="session-meta">
                    <el-tag type="primary" size="small">第{{ session.session_number }}期</el-tag>
                    <el-tag size="small">{{ session.semester }}</el-tag>
                    <el-tag v-if="session.location" size="small">{{ session.location }}</el-tag>
                  </div>
                </div>
                <div class="session-actions">
                  <el-button type="primary" size="small" @click="showEditDialog(session)">编辑</el-button>
                  <el-button type="danger" size="small" @click="handleDelete(session)">删除</el-button>
                </div>
              </div>

              <div class="session-content">
                <p class="description">{{ session.description || '暂无描述' }}</p>
                <div class="speaker-info">
                  <el-avatar :size="32" :src="session.speaker?.avatar" />
                  <span class="speaker-name">{{ session.speaker?.name || '未知分享人' }}</span>
                </div>
              </div>

              <div class="session-files" v-if="session.files && session.files.length > 0">
                <el-divider />
                <h4>相关文件</h4>
                <div class="file-list">
                  <el-tag
                    v-for="file in session.files"
                    :key="file.id"
                    type="info"
                    size="small"
                    style="margin-right: 8px; margin-bottom: 8px"
                  >
                    <el-icon><Document /></el-icon>
                    {{ file.original_filename }}
                  </el-tag>
                </div>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>

      <el-empty v-if="!loading && sessions.length === 0" description="暂无分享会数据" />
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="期数" prop="session_number">
          <el-input-number v-model="form.session_number" :min="1" :max="100" />
        </el-form-item>

        <el-form-item label="学期" prop="semester">
          <el-input v-model="form.semester" placeholder="如：2024-1" />
        </el-form-item>

        <el-form-item label="分享主题" prop="title">
          <el-input v-model="form.title" placeholder="请输入分享主题" />
        </el-form-item>

        <el-form-item label="分享人" prop="speaker_id">
          <el-select v-model="form.speaker_id" filterable placeholder="选择分享人" style="width: 100%">
            <el-option v-for="member in members" :key="member.id" :label="member.name" :value="member.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="分享时间" prop="session_date">
          <el-date-picker
            v-model="form.session_date"
            type="datetime"
            placeholder="选择分享时间"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="地点" prop="location">
          <el-input v-model="form.location" placeholder="如：313实验室" />
        </el-form-item>

        <el-form-item label="分享描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入分享内容描述" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getSessions, createSession, updateSession, deleteSession } from '@/api/session'
import { getMembers } from '@/api/member'

const loading = ref(false)
const sessions = ref([])
const members = ref([])
const searchSemester = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  session_number: 1,
  semester: '',
  title: '',
  speaker_id: null,
  session_date: null,
  location: '',
  description: ''
})

const rules = {
  session_number: [{ required: true, message: '请输入期数', trigger: 'blur' }],
  semester: [{ required: true, message: '请输入学期', trigger: 'blur' }],
  title: [{ required: true, message: '请输入分享主题', trigger: 'blur' }],
  speaker_id: [{ required: true, message: '请选择分享人', trigger: 'change' }],
  session_date: [{ required: true, message: '请选择分享时间', trigger: 'change' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑分享会' : '添加分享会')

// 加载分享会列表
const loadSessions = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchSemester.value) {
      params.semester = searchSemester.value
    }
    const response = await getSessions(params)
    sessions.value = response?.data ?? []
  } catch (error) {
    ElMessage.error('加载分享会列表失败')
  } finally {
    loading.value = false
  }
}

// 加载成员列表（兼容标准返回 { data, total } 与数组返回）
const loadMembers = async () => {
  try {
    const response = await getMembers({ limit: 1000 })
    members.value = Array.isArray(response) ? response : (response?.data ?? [])
  } catch (error) {
    console.error('加载成员列表失败', error)
    members.value = []
  }
}

// 显示添加对话框
const showAddDialog = () => {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (row) => {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    session_number: 1,
    semester: '',
    title: '',
    speaker_id: null,
    session_date: null,
    location: '',
    description: ''
  })
  formRef.value?.clearValidate()
}

// 提交表单
const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateSession(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await createSession(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadSessions()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

// 删除分享会
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `此操作将删除分享会 "${row.title}"，并级联删除其关联文件（物理文件也会被删除），不可恢复。是否继续？`,
    '级联删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteSession(row.id)
      ElMessage.success('删除成功')
      loadSessions()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  })
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadSessions()
  loadMembers()
})
</script>

<style scoped>
.sessions-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.sessions-list {
  margin-top: 20px;
}

.session-card {
  margin-bottom: 20px;
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.session-title h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 18px;
}

.session-meta {
  display: flex;
  gap: 8px;
}

.session-actions {
  display: flex;
  gap: 8px;
}

.session-content {
  margin-bottom: 15px;
}

.description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 15px;
}

.speaker-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.speaker-name {
  color: #409eff;
  font-weight: 500;
}

.session-files h4 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 14px;
}

.file-list {
  display: flex;
  flex-wrap: wrap;
}
</style>
