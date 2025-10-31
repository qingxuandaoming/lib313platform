<template>
  <div class="home">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>313实验室开放平台</h1>
          <el-menu mode="horizontal" :default-active="activeMenu" router>
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/members">成员管理</el-menu-item>
            <el-menu-item index="/projects">项目展示</el-menu-item>
            <el-menu-item index="/sessions">分享会</el-menu-item>
            <el-menu-item index="/devices">设备管理</el-menu-item>
            <el-menu-item index="/duty">值日安排</el-menu-item>
          </el-menu>
        </div>
      </el-header>

      <el-main>
        <div class="dashboard">
          <!-- 统计卡片 -->
          <div class="stats-cards">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon members">
                  <el-icon><User /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.members }}</div>
                  <div class="stat-label">实验室成员</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon projects">
                  <el-icon><Folder /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.projects }}</div>
                  <div class="stat-label">项目成果</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon sessions">
                  <el-icon><Calendar /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.sessions }}</div>
                  <div class="stat-label">分享会</div>
                </div>
              </div>
            </el-card>

            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon devices">
                  <el-icon><Monitor /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.devices }}</div>
                  <div class="stat-label">设备数量</div>
                </div>
              </div>
            </el-card>
          </div>

          <!-- 主要内容区域 -->
          <div class="main-content">
            <!-- 左侧：快速访问和近期活动 -->
            <div class="left-column">
              <!-- 快速访问 -->
              <el-card class="quick-access">
                <template #header>
                  <div class="card-header">
                    <h3>快速访问</h3>
                  </div>
                </template>
                <div class="access-buttons">
                  <el-button type="primary" @click="$router.push('/members')" class="access-btn">
                    <el-icon><User /></el-icon>
                    成员管理
                  </el-button>
                  <el-button type="success" @click="$router.push('/projects')" class="access-btn">
                    <el-icon><Folder /></el-icon>
                    项目展示
                  </el-button>
                  <el-button type="warning" @click="$router.push('/sessions')" class="access-btn">
                    <el-icon><Calendar /></el-icon>
                    分享会
                  </el-button>
                  <el-button type="info" @click="$router.push('/devices')" class="access-btn">
                    <el-icon><Monitor /></el-icon>
                    设备管理
                  </el-button>
                  <el-button type="danger" @click="$router.push('/duty')" class="access-btn">
                    <el-icon><List /></el-icon>
                    值日安排
                  </el-button>
                </div>
              </el-card>

              <!-- 近期活动 -->
              <el-card class="recent-activities">
                <template #header>
                  <div class="card-header">
                    <h3>近期活动</h3>
                  </div>
                </template>
                <div class="activities-list">
                  <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                    <div class="activity-icon">
                      <el-icon :color="activity.color">
                        <component :is="activity.icon" />
                      </el-icon>
                    </div>
                    <div class="activity-content">
                      <div class="activity-title">{{ activity.title }}</div>
                      <div class="activity-time">{{ activity.time }}</div>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 右侧：即将到来的事项 -->
            <div class="right-column">
              <!-- 即将到来的分享会 -->
              <el-card class="upcoming-sessions">
                <template #header>
                  <div class="card-header">
                    <h3>即将到来的分享会</h3>
                  </div>
                </template>
                <div class="sessions-list">
                  <div v-for="session in upcomingSessions" :key="session.id" class="session-item">
                    <div class="session-date">
                      <div class="date-day">{{ formatDay(session.date) }}</div>
                      <div class="date-month">{{ formatMonth(session.date) }}</div>
                    </div>
                    <div class="session-info">
                      <div class="session-title">{{ session.title }}</div>
                      <div class="session-speaker">主讲人: {{ session.speaker }}</div>
                    </div>
                  </div>
                </div>
              </el-card>

              <!-- 近期值日安排 -->
              <el-card class="upcoming-duty">
                <template #header>
                  <div class="card-header">
                    <h3>近期值日安排</h3>
                  </div>
                </template>
                <div class="duty-list">
                  <div v-for="duty in upcomingDuty" :key="duty.id" class="duty-item">
                    <div class="duty-date">{{ formatDate(duty.date) }}</div>
                    <div class="duty-member">{{ duty.member }}</div>
                    <el-tag :type="duty.status === 'completed' ? 'success' : 'warning'" size="small">
                      {{ duty.status === 'completed' ? '已完成' : '待完成' }}
                    </el-tag>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getMembers } from '@/api/member'
import { getProjects } from '@/api/project'
import { getSessions } from '@/api/session'
import { getDevices } from '@/api/device'
import { getDutySchedules } from '@/api/duty'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.path)

const stats = reactive({
  members: 0,
  projects: 0,
  sessions: 0,
  devices: 0
})

const recentActivities = ref([
  {
    id: 1,
    icon: 'User',
    color: '#409EFF',
    title: '新成员加入实验室',
    time: '2小时前'
  },
  {
    id: 2,
    icon: 'Folder',
    color: '#67C23A',
    title: '新项目立项',
    time: '1天前'
  },
  {
    id: 3,
    icon: 'Calendar',
    color: '#E6A23C',
    title: '分享会成功举办',
    time: '2天前'
  },
  {
    id: 4,
    icon: 'Monitor',
    color: '#909399',
    title: '设备分配完成',
    time: '3天前'
  }
])

const upcomingSessions = ref([
  {
    id: 1,
    date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
    title: '深度学习在图像识别中的应用',
    speaker: '张三'
  },
  {
    id: 2,
    date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    title: 'Web开发最佳实践',
    speaker: '李四'
  },
  {
    id: 3,
    date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000),
    title: '数据库优化技巧',
    speaker: '王五'
  }
])

const upcomingDuty = ref([
  {
    id: 1,
    date: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000),
    member: '张三',
    status: 'pending'
  },
  {
    id: 2,
    date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
    member: '李四',
    status: 'pending'
  },
  {
    id: 3,
    date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
    member: '王五',
    status: 'completed'
  }
])

// 加载统计数据
const loadStats = async () => {
  try {
    const [membersData, projectsData, sessionsData, devicesData] = await Promise.all([
      getMembers(),
      getProjects(),
      getSessions(),
      getDevices()
    ])

    stats.members = membersData.length || 0
    stats.projects = projectsData.length || 0
    stats.sessions = sessionsData.length || 0
    stats.devices = devicesData.length || 0
  } catch (error) {
    console.error('加载统计数据失败', error)
    ElMessage.error('加载统计数据失败')
  }
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化日期 - 获取日
const formatDay = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return d.getDate()
}

// 格式化日期 - 获取月
const formatMonth = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  return months[d.getMonth()]
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.el-header {
  background-color: #409eff;
  color: white;
  padding: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content h1 {
  color: white;
  margin: 10px 0;
}

.el-main {
  padding: 40px 20px;
  background-color: #f5f7fa;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

/* 统计卡片样式 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.members {
  background: linear-gradient(135deg, #409EFF, #66B1FF);
}

.stat-icon.projects {
  background: linear-gradient(135deg, #67C23A, #85CE61);
}

.stat-icon.sessions {
  background: linear-gradient(135deg, #E6A23C, #EBB563);
}

.stat-icon.devices {
  background: linear-gradient(135deg, #909399, #A6A9AD);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

/* 主要内容区域 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
}

/* 左侧列样式 */
.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header h3 {
  margin: 0;
  color: #303133;
}

/* 快速访问按钮 */
.access-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.access-btn {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
}

.access-btn .el-icon {
  font-size: 24px;
}

/* 近期活动 */
.activities-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

/* 右侧列样式 */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 即将到来的分享会 */
.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.session-item:last-child {
  border-bottom: none;
}

.session-date {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #409EFF, #66B1FF);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.date-day {
  font-size: 18px;
  line-height: 1;
}

.date-month {
  font-size: 12px;
  line-height: 1;
  margin-top: 2px;
}

.session-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
}

.session-speaker {
  font-size: 12px;
  color: #909399;
}

/* 近期值日安排 */
.duty-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.duty-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.duty-item:last-child {
  border-bottom: none;
}

.duty-date {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  min-width: 60px;
}

.duty-member {
  font-size: 14px;
  color: #606266;
  flex: 1;
  margin: 0 12px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }

  .access-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
