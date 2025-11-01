<template>
  <div class="home">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <h1>欢迎来到313实验室开放平台</h1>
        <p>管理实验室成员、项目、分享会、设备和值日安排的综合平台</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section" v-loading="loading.stats">
      <el-row :gutter="20">
        <el-col :span="6">
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
        </el-col>
        
        <el-col :span="6">
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
        </el-col>
        
        <el-col :span="6">
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
        </el-col>
        
        <el-col :span="6">
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
        </el-col>
      </el-row>
      <el-alert v-if="error.stats" :title="error.stats" type="error" show-icon class="mt-10" />
    </div>

    <!-- 快速操作 -->
    <div class="quick-actions">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>快速操作</span>
          </div>
        </template>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-button type="primary" size="large" @click="$router.push('/members')" block>
              <el-icon><User /></el-icon>
              <span>管理成员</span>
            </el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="success" size="large" @click="$router.push('/projects')" block>
              <el-icon><Folder /></el-icon>
              <span>查看项目</span>
            </el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="info" size="large" @click="$router.push('/sessions')" block>
              <el-icon><Calendar /></el-icon>
              <span>分享会</span>
            </el-button>
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- 最新动态 -->
    <el-row :gutter="20" class="recent-section">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最新项目</span>
              <el-button type="text" @click="$router.push('/projects')">查看更多</el-button>
            </div>
          </template>
          <div v-loading="loading.projects">
            <div v-if="recentProjects.length === 0" class="empty-state">
              暂无项目数据
            </div>
            <div v-else>
              <div v-for="project in recentProjects" :key="project.id" class="recent-item">
                <h4>{{ project.name }}</h4>
                <p>{{ project.description }}</p>
                <div class="item-meta">
                  <el-tag :type="getProjectStatusType(project.status)">
                    {{ getProjectStatusText(project.status) }}
                  </el-tag>
                  <span class="date">{{ formatDate(project.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最新成员</span>
              <el-button type="text" @click="$router.push('/members')">查看更多</el-button>
            </div>
          </template>
          <div v-loading="loading.members">
            <div v-if="recentMembers.length === 0" class="empty-state">
              暂无成员数据
            </div>
            <div v-else>
              <div v-for="member in recentMembers" :key="member.id" class="recent-item">
                <div class="member-info">
                  <el-avatar :src="member.avatar" :size="40">
                    {{ member.name.charAt(0) }}
                  </el-avatar>
                  <div class="member-details">
                    <h4>{{ member.name }}</h4>
                    <p>{{ member.major }} - {{ member.grade }}级</p>
                  </div>
                </div>
                <div class="item-meta">
                  <el-tag :type="getRoleType(member.role)">
                    {{ getRoleText(member.role) }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, Folder, Calendar, Monitor } from '@element-plus/icons-vue'
import { memberApi } from '@/api/member'
import { projectApi } from '@/api/project'
import { getStats } from '@/api/stats'

// 响应式数据
const stats = ref({
  members: 0,
  projects: 0,
  sessions: 0,
  devices: 0
})

const loading = ref({
  stats: false,
  members: false,
  projects: false
})
const error = ref({
  stats: '',
  members: '',
  projects: ''
})

const recentProjects = ref([])
const recentMembers = ref([])

// 获取统计数据
const fetchStats = async () => {
  loading.value.stats = true
  error.value.stats = ''
  try {
    const response = await getStats()
    stats.value = {
      members: response?.members ?? 0,
      projects: response?.projects ?? 0,
      sessions: response?.sessions ?? 0,
      devices: response?.devices ?? 0
    }
  } catch (err) {
    console.error('获取统计数据失败:', err)
    error.value.stats = '获取统计数据失败'
  } finally {
    loading.value.stats = false
  }
}

// 获取最新项目
const fetchRecentProjects = async () => {
  loading.value.projects = true
  try {
    const response = await projectApi.getProjects({ limit: 3 })
    recentProjects.value = response?.data ?? []
  } catch (error) {
    console.error('获取最新项目失败:', error)
  } finally {
    loading.value.projects = false
  }
}

// 获取最新成员
const fetchRecentMembers = async () => {
  loading.value.members = true
  try {
    const response = await memberApi.getMembers({ limit: 3 })
    recentMembers.value = response?.data ?? []
  } catch (error) {
    console.error('获取最新成员失败:', error)
  } finally {
    loading.value.members = false
  }
}

// 工具函数
const getProjectStatusType = (status) => {
  const statusMap = {
    'planning': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'archived': 'info'
  }
  return statusMap[status] || 'info'
}

const getProjectStatusText = (status) => {
  const statusMap = {
    'planning': '规划中',
    'in_progress': '进行中',
    'completed': '已完成',
    'archived': '已归档'
  }
  return statusMap[status] || status
}

const getRoleType = (role) => {
  const roleMap = {
    'leader': 'danger',
    'member': 'primary',
    'alumni': 'info'
  }
  return roleMap[role] || 'primary'
}

const getRoleText = (role) => {
  const roleMap = {
    'leader': '负责人',
    'member': '成员',
    'alumni': '校友'
  }
  return roleMap[role] || role
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 生命周期
onMounted(() => {
  fetchStats()
  fetchRecentProjects()
  fetchRecentMembers()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-banner {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: white;
  padding: 60px 40px;
  border-radius: 8px;
  margin-bottom: 30px;
  text-align: center;
}

.banner-content h1 {
  font-size: 2.5rem;
  margin-bottom: 16px;
  font-weight: 600;
}

.banner-content p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  height: 120px;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 24px;
  color: white;
}

.stat-icon.members {
  background: linear-gradient(135deg, #409eff, #36a3f7);
}

.stat-icon.projects {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.stat-icon.sessions {
  background: linear-gradient(135deg, #e6a23c, #ebb563);
}

.stat-icon.devices {
  background: linear-gradient(135deg, #f56c6c, #f78989);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 600;
  color: var(--text-strong);
  margin-bottom: 4px;
}

.stat-label {
  color: var(--text-soft);
  font-size: 14px;
}

.quick-actions {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-section {
  margin-bottom: 30px;
}

.recent-item {
  padding: 16px 0;
  border-bottom: 1px solid var(--glass-border);
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-item h4 {
  margin: 0 0 8px 0;
  color: var(--text-strong);
}

.recent-item p {
  margin: 0 0 12px 0;
  color: var(--text-soft);
  font-size: 14px;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date {
  color: var(--text-soft);
  font-size: 12px;
}

.member-info {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.member-details {
  margin-left: 12px;
  flex: 1;
}

.member-details h4 {
  margin: 0 0 4px 0;
}

.member-details p {
  margin: 0;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  color: var(--text-soft);
  padding: 40px 0;
}
</style>
