<template>
  <div class="duty-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>值日安排</h2>
          <div>
            <el-button type="primary" @click="showAddDialog">
              <el-icon><Plus /></el-icon>
              安排值日
            </el-button>
            <el-button @click="generateSchedule" style="margin-left: 10px">
              <el-icon><Refresh /></el-icon>
              生成排班
            </el-button>
          </div>
        </div>
      </template>

      <!-- 日期筛选 -->
      <div class="filter-bar">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          @change="loadDutySchedules"
        />
      </div>

      <!-- 值日日历视图 -->
      <div class="calendar-view" v-loading="loading">
        <div class="calendar-header">
          <div class="calendar-cell">日期</div>
          <div class="calendar-cell">值日人员</div>
          <div class="calendar-cell">完成状态</div>
          <div class="calendar-cell">操作</div>
        </div>

        <div class="calendar-body">
          <div v-for="schedule in dutySchedules" :key="schedule.id" class="calendar-row">
            <div class="calendar-cell">
              <div class="date">{{ formatDate(schedule.duty_date) }}</div>
              <div class="weekday">{{ getWeekday(schedule.duty_date) }}</div>
            </div>
            <div class="calendar-cell">
              <div class="member-info">
                <el-avatar :size="32" :src="resolveMember(schedule)?.avatar" />
                <span class="member-name">{{ resolveMember(schedule)?.name || '—' }}</span>
              </div>
            </div>
            <div class="calendar-cell">
              <el-tag :type="schedule.is_completed ? 'success' : 'warning'">
                {{ schedule.is_completed ? '已完成' : '未完成' }}
              </el-tag>
              <div v-if="schedule.is_completed" class="completion-info">
                <small>完成于: {{ formatDate(schedule.completed_at) }}</small>
              </div>
            </div>
            <div class="calendar-cell actions">
              <el-button
                v-if="!schedule.is_completed"
                type="success"
                size="small"
                @click="completeDuty(schedule)"
              >
                标记完成
              </el-button>
              <el-button type="primary" size="small" @click="showEditDialog(schedule)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(schedule)">删除</el-button>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="!loading && dutySchedules.length === 0" description="暂无值日安排" />
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="值日人员" prop="member_id">
          <el-select v-model="form.member_id" filterable placeholder="选择值日人员" style="width: 100%">
            <el-option v-for="member in members" :key="member.id" :label="member.name" :value="member.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="值日日期" prop="duty_date">
          <el-date-picker v-model="form.duty_date" type="date" placeholder="选择值日日期" style="width: 100%" />
        </el-form-item>

        <el-form-item label="完成状态" prop="is_completed">
          <el-switch v-model="form.is_completed" />
        </el-form-item>

        <el-form-item label="完成备注" prop="completion_notes" v-if="form.is_completed">
          <el-input v-model="form.completion_notes" type="textarea" :rows="2" placeholder="请输入完成情况备注" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 标记完成对话框 -->
    <el-dialog v-model="completeDialogVisible" title="标记值日完成" width="400px">
      <el-form :model="completeForm" ref="completeFormRef" label-width="80px">
        <el-form-item label="完成备注">
          <el-input v-model="completeForm.completion_notes" type="textarea" :rows="3" placeholder="请输入完成情况备注" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="completeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleComplete">确定完成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDutySchedules, createDutySchedule, updateDutySchedule, deleteDutySchedule, completeDuty as apiCompleteDuty, generateDutySchedules } from '@/api/duty'
import { getMembers } from '@/api/member'

const loading = ref(false)
const dutySchedules = ref([])
const members = ref([])
const dateRange = ref([])

const dialogVisible = ref(false)
const completeDialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const completeFormRef = ref(null)
const currentSchedule = ref(null)

const form = reactive({
  member_id: null,
  duty_date: null,
  is_completed: false,
  completion_notes: ''
})

const completeForm = reactive({
  completion_notes: ''
})

const rules = {
  member_id: [{ required: true, message: '请选择值日人员', trigger: 'change' }],
  duty_date: [{ required: true, message: '请选择值日日期', trigger: 'change' }]
}

const dialogTitle = computed(() => isEdit.value ? '编辑值日安排' : '安排值日')

// 加载值日安排（兼容标准返回 { data, total } 与数组返回）
const loadDutySchedules = async () => {
  loading.value = true
  try {
    const params = {}
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    const response = await getDutySchedules(params)
    dutySchedules.value = Array.isArray(response) ? response : (response?.data ?? [])
  } catch (error) {
    ElMessage.error('加载值日安排失败')
    dutySchedules.value = []
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

// 根据后端返回的关系或本地成员表，解析显示用的成员信息
const resolveMember = (schedule) => {
  if (!schedule) return null
  if (schedule.member) return schedule.member
  const id = schedule.member_id
  if (!id || !Array.isArray(members.value)) return null
  return members.value.find(m => m.id === id) || null
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
    member_id: row.member_id ?? row.member?.id ?? null,
    duty_date: row.duty_date ? new Date(row.duty_date) : null,
    is_completed: !!row.is_completed,
    completion_notes: row.completion_notes || ''
  })
  dialogVisible.value = true
}

// 显示完成对话框
const completeDuty = (row) => {
  currentSchedule.value = row
  completeForm.completion_notes = ''
  completeDialogVisible.value = true
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    member_id: null,
    duty_date: null,
    is_completed: false,
    completion_notes: ''
  })
  formRef.value?.clearValidate()
}

// 构建提交payload，格式化日期并移除空字符串字段
const buildSchedulePayload = () => {
  const payload = {
    member_id: form.member_id,
    duty_date: formatDateForApi(form.duty_date),
    is_completed: !!form.is_completed
  }
  const notes = form.completion_notes
  if (notes && notes.trim() !== '') {
    payload.completion_notes = notes.trim()
  }
  return payload
}

// 将日期规范化为 YYYY-MM-DD 字符串
const formatDateForApi = (val) => {
  if (!val) return ''
  if (typeof val === 'string') {
    // 可能已是 YYYY-MM-DD
    return val.length > 10 ? val.split('T')[0] : val
  }
  // Date 对象
  try {
    return new Date(val).toISOString().split('T')[0]
  } catch {
    return ''
  }
}

// 统一错误信息提取，避免向 ElMessage 传入数组/对象导致渲染异常
const getErrorMessage = (error) => {
  const detail = error?.response?.data?.detail
  if (!detail) return '操作失败'
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => (d?.msg || d?.message || JSON.stringify(d))).join('；')
  }
  return typeof detail === 'object' ? JSON.stringify(detail) : String(detail)
}

// 提交表单
const handleSubmit = async () => {
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const payload = buildSchedulePayload()
        if (isEdit.value) {
          await updateDutySchedule(form.id, payload)
          ElMessage.success('更新成功')
        } else {
          await createDutySchedule(payload)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadDutySchedules()
      } catch (error) {
        ElMessage.error(getErrorMessage(error))
      }
    }
  })
}

// 处理完成
const handleComplete = async () => {
  try {
    const id = currentSchedule.value?.id
    if (!id) {
      ElMessage.error('当前记录无效，无法标记完成')
      return
    }
    await apiCompleteDuty(id, completeForm.completion_notes)
    ElMessage.success('标记完成成功')
    completeDialogVisible.value = false
    loadDutySchedules()
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  }
}

// 删除值日安排
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `此操作将删除 ${formatDate(row.duty_date)} 的值日安排，操作不可恢复。若成员被删除时，此记录亦会被级联删除。是否继续？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteDutySchedule(row.id)
      ElMessage.success('删除成功')
      loadDutySchedules()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  })
}

// 生成排班（默认下周一开始，1 周，优先同年级一组）
const generateSchedule = async () => {
  try {
    await ElMessageBox.confirm('这将为接下来的一周自动生成值日排班，确定要继续吗？', '生成排班', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })

    const today = new Date()
    const dow = today.getDay() // 0=Sun,1=Mon,...
    const daysToNextMonday = ((1 - dow + 7) % 7) || 7
    const nextMonday = new Date(today)
    nextMonday.setDate(today.getDate() + daysToNextMonday)

    const payload = {
      start_date: nextMonday.toISOString().split('T')[0],
      weeks: 1,
      prefer_same_grade: true,
      skip_weekends: false
    }

    const resp = await generateDutySchedules(payload)
    const createdCount = Array.isArray(resp?.data) ? resp.data.length : (resp?.total ?? 0)
    ElMessage.success(`排班生成成功，共创建 ${createdCount} 条记录`)
    loadDutySchedules()
  } catch (error) {
    if (error === 'cancel') return
    ElMessage.error(getErrorMessage(error))
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 获取星期
const getWeekday = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `星期${weekdays[date.getDay()]}`
}

onMounted(() => {
  loadDutySchedules()
  loadMembers()
})
</script>

<style scoped>
.duty-container {
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

.calendar-view {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.calendar-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  border-bottom: 1px solid #ebeef5;
}

.calendar-row:last-child {
  border-bottom: none;
}

.calendar-cell {
  padding: 16px;
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  min-height: 80px;
}

.calendar-cell.actions {
  flex-direction: row;
  gap: 8px;
}

.date {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.weekday {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.member-name {
  font-weight: 500;
  color: #303133;
}

.completion-info {
  margin-top: 4px;
  color: #909399;
}
</style>
