<template>
  <el-container class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="layout-header glass-surface">
      <div class="header-content">
        <div class="logo">
          <h2 class="text-strong">313实验室开放平台</h2>
        </div>
        <el-menu
          :default-active="activeIndex"
          class="header-menu"
          mode="horizontal"
          @select="handleSelect"
        >
          <el-menu-item index="/home">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/members">
            <el-icon><User /></el-icon>
            <span>成员管理</span>
          </el-menu-item>
          <el-menu-item index="/projects">
            <el-icon><Folder /></el-icon>
            <span>项目展示</span>
          </el-menu-item>
          <el-menu-item index="/sessions">
            <el-icon><ChatDotRound /></el-icon>
            <span>分享会</span>
          </el-menu-item>
          <el-menu-item index="/devices">
            <el-icon><Monitor /></el-icon>
            <span>设备管理</span>
          </el-menu-item>
          <el-menu-item index="/files">
            <el-icon><Document /></el-icon>
            <span>文档管理</span>
          </el-menu-item>
          <el-menu-item index="/duty">
            <el-icon><Calendar /></el-icon>
            <span>值日安排</span>
          </el-menu-item>
        </el-menu>
        <div class="header-actions">
          <template v-if="isAuthenticated">
            <el-dropdown>
              <span class="el-dropdown-link">
                <el-icon><User /></el-icon>
                {{ userLabel }}
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goProfile">个人中心</el-dropdown-item>
                  <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="handleLogin">登录</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="layout-main">
      <router-view />
    </el-main>

    <!-- 底部 -->
    <el-footer class="layout-footer glass-surface">
      <div class="footer-content">
        <p class="text-soft">&copy; 2024 313实验室开放平台. All rights reserved.</p>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  House, 
  User, 
  Folder, 
  ChatDotRound, 
  Monitor, 
  Calendar,
  Document
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const activeIndex = computed(() => route.path)
const auth = useAuthStore()

const handleSelect = (key) => {
  router.push(key)
}

const handleLogin = () => {
  router.push('/login')
}

const isAuthenticated = computed(() => auth.isAuthenticated)
const userLabel = computed(() => auth.user?.username || '已登录')

const logout = () => {
  auth.logout()
  router.push('/home')
}

const goProfile = () => {
  router.push('/profile')
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.layout-header {
  background: transparent;
  border-bottom: 1px solid transparent;
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo h2 {
  margin: 0;
  color: var(--text-strong);
  font-weight: 600;
}

.header-menu {
  flex: 1;
  margin: 0 40px;
  border-bottom: none;
}

.header-actions {
  display: flex;
  align-items: center;
}

.layout-main {
  background-color: transparent;
  min-height: calc(100vh - 120px);
  padding: 20px;
}

.layout-footer {
  background: transparent;
  border-top: 1px solid transparent;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  text-align: center;
  color: var(--text-soft);
  font-size: 14px;
}
</style>