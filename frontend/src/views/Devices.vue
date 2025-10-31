<template>
  <div class="devices-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>设备管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加设备
          </el-button>
        </div>
      </template>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-select v-model="filterType" placeholder="设备类型" clearable style="width: 150px" @change="loadDevices">
          <el-option label="电脑" value="computer" />
          <el-option label="服务器" value="server" />
          <el-option label="打印机" value="printer" />
          <el-option label="其他" value="other" />
        </el-select>
        <el-select v-model="filterStatus" placeholder="设备状态" clearable style="width: 150px" @change="loadDevices">
          <el-option label="可用" value="available" />
          <el-option label="使用中" value="in_use" />
          <el-option label="维护中" value="maintenance" />
          <el-option label="已退役" value="retired" />
        </el-select>
      </div>

      <!-- 设备表格 -->
      <el-table :data="devices" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="设备名称" width="150" />
        <el-table-column prop="device_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getDeviceTypeText(row.device_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="brand" label="品牌" width="120" />
        <el-table-column prop="model" label="型号" width="150" />
        <el-table-column prop="serial_number" label="序列号" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="位置" width="120" />
        <el-table-column prop="current_user" label="当前使用者" width="120">
          <template #default="{ row }">
            {{ row.current_user?.name || '无' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="warning" size="small" @click="showAssignDialog(row)" v-if="row.status === 'available'">
              分配
            </el-button>
            <el-button type="info" size="small" @click="showReturnDialog(row)" v-if="row.status === 'in_use'">
              归还
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && devices.length === 0" description="暂无设备数据" />
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入设备名称" />
        </el-form-item>

        <el-form-item label="设备类型" prop="device_type">
          <el-select v-model="form.device_type" style="width: 100%">
            <el-option label="电脑" value="computer" />
            <el-option label="服务器" value="server" />
            <el-option label="打印机" value="printer" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="品牌" prop="brand">
          <el-input v-model="form.brand" placeholder="请输入品牌" />
        </el-form-item>

        <el-form-item label="型号" prop="model">
          <el-input v-model="form.model" placeholder="请输入型号" />
        </el-form-item>

        <el-form-item label="序列号" prop="serial_number">
          <el-input v-model="form.serial_number" placeholder="请输入序列号" />
        </el-form-item>

        <el-form-item label="配置信息" prop="specifications">
          <el-input v-model="form.specifications" type="textarea" :rows="3" placeholder="请输入设备配置信息" />
        </el-form-item>

        <el-form-item label="设备状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="可用" value="available" />
            <el-option label="使用中" value="in_use" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="已退役" value="retired" />
          </el-select>
        </el-form-item>

        <el-form-item label="位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入设备位置" />
        </el-form-item>

        <el-form-item label="购买日期" prop="purchase_date">
          <el-date-picker v-model="form.purchase_date" type="date" placeholder="选择购买日期" style="width: 100%" />
        </el-form-item>

        <el-form-item label="备注" prop="notes">
          <el-input v-model="form.notes" type="textarea" :rows="2" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 分配设备对话框 -->
    <el-dialog v-model="assignDialogVisible" title="分配设备" width="400px">
      <el-form :model="assignForm" ref="assignFormRef" label-width="80px">
        <el-form-item label="使用者" prop="current_user_id">
          <el-select v-model="assignForm.current_user_id" filterable placeholder="选择使用者" style="width: 100%">
            <el-option v-for="member in members" :key="member.id" :label="member.name" :value="member.id" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssign">确定分配</el-button>
      </template>
    </el-dialog>

    <!-- 归还设备对话框 -->
    <el-dialog v-model="returnDialogVisible" title="归还设备" width="400px">
      <p>确定要将设备 "{{ currentDevice?.name }}" 标记为可用状态吗？</p>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleReturn">确定归还</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDevices, createDevice, updateDevice, deleteDevice } from '@/api/device'
import { getMembers } from '@/api/member'

const loading = ref(false)
const devices = ref([])
const members = ref([])
const filterType = ref('')
const filterStatus = ref('')

const dialogVisible = ref(false)
const assignDialogVisible = ref(false)
const returnDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const assignFormRef = ref(null)
const currentDevice = ref(null)

const form = reactive({
  name: '',
  device_type: 'computer',
  brand: '',
  model: '',
  serial_number: '',
  specifications: '',
  status: 'available',
  location: '',
  purchase_date: null,
  notes: ''
})

const assignForm = reactive({
  current_user_id: null
})

const rules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  device_type: [{ required: true, message: '请选择设备类型', trigger: 'change' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑设备' : '添加设备')

// 加载设备列表
const loadDevices = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterType.value) {
      params.device_type = filterType.value
    }
    if (filterStatus.value) {
      params.status = filterStatus.value
    }
    const response = await getDevices(params)
    devices.value = response?.data ?? []
  } catch (error) {
    ElMessage.error('加载设备列表失败')
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

// 显示分配对话框
const showAssignDialog = (row) => {
  currentDevice.value = row
  assignForm.current_user_id = null
  assignDialogVisible.value = true
}

// 显示归还对话框
const showReturnDialog = (row) => {
  currentDevice.value = row
  returnDialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    device_type: 'computer',
    brand: '',
    model: '',
    serial_number: '',
    specifications: '',
    status: 'available',
    location: '',
    purchase_date: null,
    notes: ''
  })
  formRef.value?.clearValidate()
}

// 提交表单
const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateDevice(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await createDevice(form)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadDevices()
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

// 分配设备
const handleAssign = async () => {
  if (!assignForm.current_user_id) {
    ElMessage.warning('请选择使用者')
    return
  }

  try {
    await updateDevice(currentDevice.value.id, {
      current_user_id: assignForm.current_user_id,
      status: 'in_use'
    })
    ElMessage.success('分配成功')
    assignDialogVisible.value = false
    loadDevices()
  } catch (error) {
    ElMessage.error('分配失败')
  }
}

// 归还设备
const handleReturn = async () => {
  try {
    await updateDevice(currentDevice.value.id, {
      current_user_id: null,
      status: 'available'
    })
    ElMessage.success('归还成功')
    returnDialogVisible.value = false
    loadDevices()
  } catch (error) {
    ElMessage.error('归还失败')
  }
}

// 删除设备
const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除设备 "${row.name}" 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteDevice(row.id)
      ElMessage.success('删除成功')
      loadDevices()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

// 状态标签类型
const getStatusType = (status) => {
  const types = {
    available: 'success',
    in_use: 'warning',
    maintenance: 'danger',
    retired: 'info'
  }
  return types[status] || 'info'
}

// 状态文本
const getStatusText = (status) => {
  const texts = {
    available: '可用',
    in_use: '使用中',
    maintenance: '维护中',
    retired: '已退役'
  }
  return texts[status] || status
}

// 设备类型文本
const getDeviceTypeText = (type) => {
  const texts = {
    computer: '电脑',
    server: '服务器',
    printer: '打印机',
    other: '其他'
  }
  return texts[type] || type
}

onMounted(() => {
  loadDevices()
  loadMembers()
})
</script>

<style scoped>
.devices-container {
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
</style>
