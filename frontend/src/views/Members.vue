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

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchName"
          placeholder="搜索成员姓名或学号"
          style="width: 300px"
          clearable
          @clear="loadMembers"
        >
          <template #append>
            <el-button @click="loadMembers">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- 成员表格 -->
      <el-table :data="members" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="student_id" label="学号" width="150" />
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="major" label="专业" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">
              {{ getRoleText(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="手机" width="130" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="showEditDialog(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">
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
          @size-change="loadMembers"
          @current-change="loadMembers"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="form.student_id" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-input-number v-model="form.grade" :min="2000" :max="2100" />
        </el-form-item>
        <el-form-item label="专业" prop="major">
          <el-input v-model="form.major" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="成员" value="member" />
            <el-option label="负责人" value="leader" />
            <el-option label="校友" value="alumni" />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="GitHub" prop="github">
          <el-input v-model="form.github" />
        </el-form-item>
        <el-form-item label="个人简介" prop="bio">
          <el-input v-model="form.bio" type="textarea" :rows="3" />
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
import { getMembers, createMember, updateMember, deleteMember } from '@/api/member'

const loading = ref(false)
const members = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchName = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = reactive({
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
  student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  grade: [{ required: true, message: '请输入年级', trigger: 'blur' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑成员' : '添加成员')

// 加载成员列表
const loadMembers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    const data = await getMembers(params)
    members.value = data
    total.value = data.length
  } catch (error) {
    ElMessage.error('加载成员列表失败')
  } finally {
    loading.value = false
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
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateMember(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await createMember(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadMembers()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

// 删除成员
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除成员 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteMember(row.id)
      ElMessage.success('删除成功')
      loadMembers()
    } catch (error) {
      ElMessage.error('删除失败')
    }
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

onMounted(() => {
  loadMembers()
})
</script>

<style scoped>
.members-container {
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
</style>
