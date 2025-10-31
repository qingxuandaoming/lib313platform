<template>
  <el-container class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="layout-header">
      <div class="header-content">
        <div class="logo">
          <h2>313实验室开放平台</h2>
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
          <el-button type="primary" @click="handleLogin">登录</el-button>
        </div>
      </div>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="layout-main">
      <router-view />
    </el-main>

    <!-- 底部 -->
    <el-footer class="layout-footer">
      <div class="footer-content">
        <p>&copy; 2024 313实验室开放平台. All rights reserved.</p>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
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

const handleSelect = (key) => {
  router.push(key)
}

const handleLogin = () => {
  // TODO: 实现登录逻辑
  console.log('登录功能待实现')
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.layout-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
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
  color: #409eff;
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
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
  padding: 20px;
}

.layout-footer {
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  text-align: center;
  color: #909399;
  font-size: 14px;
}
</style>