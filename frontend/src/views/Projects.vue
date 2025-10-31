<template>
  <div class="projects-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>项目展示</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加项目
          </el-button>
        </div>
      </template>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-select v-model="filterStatus" placeholder="项目状态" clearable style="width: 150px" @change="loadProjects">
          <el-option label="规划中" value="planning" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
          <el-option label="已归档" value="archived" />
        </el-select>
      </div>

      <!-- 项目卡片展示 -->
      <div class="projects-grid" v-loading="loading">
        <el-card v-for="project in projects" :key="project.id" class="project-card" shadow="hover">
          <div class="project-cover" v-if="project.cover_image">
            <img :src="project.cover_image" :alt="project.name" />
          </div>
          <div class="project-cover placeholder" v-else>
            <el-icon :size="60"><FolderOpened /></el-icon>
          </div>

          <div class="project-info">
            <h3>{{ project.name }}</h3>
            <p class="description">{{ project.description || '暂无描述' }}</p>

            <div class="project-meta">
              <el-tag :type="getStatusType(project.status)" size="small">
                {{ getStatusText(project.status) }}
              </el-tag>
              <span class="tags" v-if="project.tags">
                <el-tag v-for="tag in project.tags.split(',')" :key="tag" size="small" style="margin-left: 5px">
                  {{ tag }}
                </el-tag>
              </span>
            </div>

            <div class="project-links">
              <el-link v-if="project.github_url" :href="project.github_url" target="_blank" type="primary">
                <el-icon><Link /></el-icon> GitHub
              </el-link>
              <el-link v-if="project.demo_url" :href="project.demo_url" target="_blank" type="success">
                <el-icon><View /></el-icon> Demo
              </el-link>
            </div>

            <div class="project-actions">
              <el-button type="primary" size="small" @click="showEditDialog(project)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(project)">删除</el-button>
            </div>
          </div>
        </el-card>
      </div>

      <el-empty v-if="!loading && projects.length === 0" description="暂无项目数据" />
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>

        <el-form-item label="项目描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入项目描述" />
        </el-form-item>

        <el-form-item label="项目状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="规划中" value="planning" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>

        <el-form-item label="项目负责人" prop="leader_id">
          <el-select v-model="form.leader_id" filterable placeholder="选择负责人" style="width: 100%">
            <el-option v-for="member in members" :key="member.id" :label="member.name" :value="member.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="datetime" placeholder="选择开始日期" style="width: 100%" />
        </el-form-item>

        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="datetime" placeholder="选择结束日期" style="width: 100%" />
        </el-form-item>

        <el-form-item label="GitHub地址" prop="github_url">
          <el-input v-model="form.github_url" placeholder="https://github.com/..." />
        </el-form-item>

        <el-form-item label="Demo地址" prop="demo_url">
          <el-input v-model="form.demo_url" placeholder="https://..." />
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <el-input v-model="form.tags" placeholder="多个标签用逗号分隔，如：Web,AI,Python" />
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
import { getProjects, createProject, updateProject, deleteProject } from '@/api/project'
import { getMembers } from '@/api/member'

const loading = ref(false)
const projects = ref([])
const members = ref([])
const filterStatus = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  description: '',
  status: 'planning',
  leader_id: null,
  start_date: null,
  end_date: null,
  github_url: '',
  demo_url: '',
  tags: ''
})

const rules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  leader_id: [{ required: true, message: '请选择项目负责人', trigger: 'change' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑项目' : '添加项目')

// 加载项目列表
const loadProjects = async () => {
  loading.value = true
  try {
    const data = await getProjects()
    projects.value = data
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  } finally {
    loading.value = false
  }
}

// 加载成员列表
const loadMembers = async () => {
  try {
    const data = await getMembers({ limit: 1000 })
    members.value = data
  } catch (error) {
    console.error('加载成员列表失败', error)
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
    name: '',
    description: '',
    status: 'planning',
    leader_id: null,
    start_date: null,
    end_date: null,
    github_url: '',
    demo_url: '',
    tags: ''
  })
  formRef.value?.clearValidate()
}

// 提交表单
const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateProject(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await createProject(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadProjects()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

// 删除项目
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除项目 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteProject(row.id)
      ElMessage.success('删除成功')
      loadProjects()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

// 状态标签类型
const getStatusType = (status) => {
  const types = {
    planning: 'info',
    in_progress: 'warning',
    completed: 'success',
    archived: 'info'
  }
  return types[status] || 'info'
}

// 状态文本
const getStatusText = (status) => {
  const texts = {
    planning: '规划中',
    in_progress: '进行中',
    completed: '已完成',
    archived: '已归档'
  }
  return texts[status] || status
}

onMounted(() => {
  loadProjects()
  loadMembers()
})
</script>

<style scoped>
.projects-container {
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
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.project-card {
  transition: transform 0.2s;
}

.project-card:hover {
  transform: translateY(-5px);
}

.project-cover {
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 15px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.project-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.project-cover.placeholder {
  color: #c0c4cc;
}

.project-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 10px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
}

.project-links {
  margin-bottom: 15px;
  display: flex;
  gap: 15px;
}

.project-actions {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.project-actions .el-button {
  flex: 1;
}
</style>
