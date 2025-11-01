<template>
  <div class="members-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>成员管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加成员
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选栏 -->
      <div class="search-bar">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索成员姓名或学号"
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
            <el-select v-model="filterRole" placeholder="筛选角色" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option label="负责人" value="leader" />
              <el-option label="成员" value="member" />
              <el-option label="校友" value="alumni" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="filterGrade" placeholder="筛选年级" clearable @change="handleSearch">
              <el-option label="全部" value="" />
              <el-option v-for="year in gradeOptions" :key="year" :label="`${year}级`" :value="year" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- 成员表格 -->
      <el-table :data="members" style="width: 100%" v-loading="loading" stripe>
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="name" label="姓名" width="120" show-overflow-tooltip />
        <el-table-column prop="student_id" label="学号" width="150" />
        <el-table-column prop="grade" label="年级" width="100">
          <template #default="{ row }">
            {{ row.grade }}级
          </template>
        </el-table-column>
        <el-table-column prop="major" label="专业" show-overflow-tooltip />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机" width="130" />
        <el-table-column prop="created_at" label="加入时间" width="120">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="showEditDialog(row)">
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
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学号" prop="student_id">
              <el-input v-model="form.student_id" :disabled="isEdit" placeholder="请输入学号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年级" prop="grade">
              <el-input-number v-model="form.grade" :min="2000" :max="2100" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="role">
              <el-select v-model="form.role" style="width: 100%">
                <el-option label="成员" value="member" />
                <el-option label="负责人" value="leader" />
                <el-option label="校友" value="alumni" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="专业" prop="major">
          <el-input v-model="form.major" placeholder="请输入专业" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="GitHub" prop="github">
          <el-input v-model="form.github" placeholder="请输入GitHub用户名" />
        </el-form-item>
        
        <el-form-item label="个人简介" prop="bio">
          <el-input v-model="form.bio" type="textarea" :rows="3" placeholder="请输入个人简介" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { memberApi } from '@/api/member'

const loading = ref(false)
const submitting = ref(false)
const members = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const filterRole = ref('')
const filterGrade = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
  id: null,
  name: '',
  student_id: '',
  grade: new Date().getFullYear(),
  major: '',
  role: 'member',
  email: '',
  phone: '',
  github: '',
  bio: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d+$/, message: '学号只能包含数字', trigger: 'blur' }
  ],
  grade: [{ required: true, message: '请选择年级', trigger: 'blur' }],
  major: [{ required: true, message: '请输入专业', trigger: 'blur' }],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ]
}

const dialogTitle = computed(() => isEdit.value ? '编辑成员' : '添加成员')

// 年级选项
const gradeOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let i = currentYear - 10; i <= currentYear + 1; i++) {
    years.push(i)
  }
  return years.reverse()
})

// 加载成员列表
const loadMembers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchQuery.value || undefined,
      role: filterRole.value || undefined,
      grade: filterGrade.value || undefined
    }
    
    const response = await memberApi.getMembers(params)
    // 兼容后端直接返回数组或返回对象{ data, total }
    if (Array.isArray(response)) {
      members.value = response
      total.value = response.length
    } else {
      members.value = response?.data ?? []
      const dataLen = Array.isArray(response?.data) ? response.data.length : 0
      total.value = response?.total ?? dataLen
    }
  } catch (error) {
    console.error('加载成员列表失败:', error)
    ElMessage.error('加载成员列表失败')
    members.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadMembers()
}

// 重置筛选
const resetFilters = () => {
  searchQuery.value = ''
  filterRole.value = ''
  filterGrade.value = ''
  currentPage.value = 1
  loadMembers()
}

// 页面大小改变
const handlePageSizeChange = () => {
  currentPage.value = 1
  loadMembers()
}

// 当前页改变
const handleCurrentPageChange = () => {
  loadMembers()
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
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    id: null,
    name: '',
    student_id: '',
    grade: new Date().getFullYear(),
    major: '',
    role: 'member',
    email: '',
    phone: '',
    github: '',
    bio: ''
  })
  formRef.value?.clearValidate()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          await memberApi.updateMember(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await memberApi.createMember(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadMembers()
      } catch (error) {
        console.error('操作失败:', error)
        const message = error.response?.data?.detail || '操作失败'
        ElMessage.error(message)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 删除成员
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `此操作将删除成员 "${row.name}"，并级联删除其项目成员关系与值日安排，同时解除其作为项目负责人、设备分配及文件上传者关联。不可恢复，是否继续？`,
    '级联删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await memberApi.deleteMember(row.id)
      ElMessage.success('删除成功')
      loadMembers()
    } catch (error) {
      console.error('删除失败:', error)
      const message = error?.response?.data?.detail || '删除失败'
      ElMessage.error(message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 角色标签类型
const getRoleType = (role) => {
  const types = {
    leader: 'danger',
    member: 'success',
    alumni: 'info'
  }
  return types[role] || 'info'
}

// 角色文本
const getRoleText = (role) => {
  const texts = {
    leader: '负责人',
    member: '成员',
    alumni: '校友'
  }
  return texts[role] || role
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.members-container {
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
