<template>
  <div class="projects-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>项目管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加项目
          </el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchName"
              placeholder="搜索项目名称"
              clearable
              @keyup.enter="loadProjects"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6">
            <el-select v-model="searchStatus" placeholder="选择状态" clearable>
              <el-option label="规划中" value="planning" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已完成" value="completed" />
              <el-option label="已归档" value="archived" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="loadProjects">搜索</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 项目表格 -->
      <el-table :data="projects" v-loading="loading" stripe>
        <el-table-column prop="name" label="项目名称" min-width="150" />
        <el-table-column prop="description" label="项目描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="leader_id" label="负责人" width="120">
          <template #default="{ row }">
            {{ getMemberName(row.leader_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120">
          <template #default="{ row }">
            {{ row.start_date ? new Date(row.start_date).toLocaleDateString() : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="end_date" label="结束日期" width="120">
          <template #default="{ row }">
            {{ row.end_date ? new Date(row.end_date).toLocaleDateString() : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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
          @size-change="loadProjects"
          @current-change="loadProjects"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>

        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入项目描述"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目状态" prop="status">
              <el-select v-model="form.status" placeholder="选择状态" style="width: 100%">
                <el-option label="规划中" value="planning" />
                <el-option label="进行中" value="in_progress" />
                <el-option label="已完成" value="completed" />
                <el-option label="已归档" value="archived" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="项目负责人" prop="leader_id">
              <el-select v-model="form.leader_id" placeholder="选择负责人" style="width: 100%">
                <el-option
                  v-for="member in members"
                  :key="member.id"
                  :label="member.name"
                  :value="member.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始日期" prop="start_date">
              <el-date-picker
                v-model="form.start_date"
                type="date"
                placeholder="选择开始日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期" prop="end_date">
              <el-date-picker
                v-model="form.end_date"
                type="date"
                placeholder="选择结束日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

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
import { Plus, Search } from '@element-plus/icons-vue'
import { getProjects, createProject, updateProject, deleteProject } from '@/api/project'
import { getMembers } from '@/api/member'

const loading = ref(false)
const projects = ref([])
const members = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')
const searchStatus = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  description: '',
  status: 'planning',
  leader_id: null,
  start_date: '',
  end_date: '',
  github_url: '',
  demo_url: '',
  tags: ''
})

const rules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入项目描述', trigger: 'blur' }],
  leader_id: [{ required: true, message: '请选择项目负责人', trigger: 'change' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑项目' : '添加项目')

// 加载项目列表
const loadProjects = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    const response = await getProjects(params)
    projects.value = response?.data ?? []
    total.value = response?.total ?? 0
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  } finally {
    loading.value = false
  }
}

// 加载成员列表
const loadMembers = async () => {
  try {
    const response = await getMembers({ limit: 1000 })
    members.value = Array.isArray(response) ? response : (response?.data ?? [])
  } catch (error) {
    ElMessage.error('加载成员列表失败')
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
  Object.assign(form, {
    ...row,
    start_date: row.start_date ? new Date(row.start_date).toISOString().split('T')[0] : '',
    end_date: row.end_date ? new Date(row.end_date).toISOString().split('T')[0] : ''
  })
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    description: '',
    status: 'planning',
    leader_id: null,
    start_date: '',
    end_date: '',
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
        const submitData = {
          ...form,
          start_date: form.start_date ? new Date(form.start_date).toISOString() : null,
          end_date: form.end_date ? new Date(form.end_date).toISOString() : null
        }
        
        if (isEdit.value) {
          await updateProject(form.id, submitData)
          ElMessage.success('更新成功')
        } else {
          await createProject(submitData)
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
    archived: 'danger'
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

// 获取成员姓名
const getMemberName = (memberId) => {
  const member = members.value.find(m => m.id === memberId)
  return member ? member.name : '未知'
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

.search-bar {
  margin-bottom: 20px;
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
</style>
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

.search-bar {
  margin-bottom: 20px;
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
