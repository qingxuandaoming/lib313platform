<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="glass-surface">
          <template #header>
            <div class="card-header text-strong">头像</div>
          </template>
          <div class="avatar-box">
            <el-avatar :size="120" :src="profile.avatar || defaultAvatar" />
          </div>
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :before-upload="handleAvatarUpload"
          >
            <el-button type="primary">上传头像</el-button>
          </el-upload>
          <div class="tip text-soft">仅本地保存，用于界面展示</div>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card class="glass-surface">
          <template #header>
            <div class="card-header text-strong">基本信息</div>
          </template>

          <el-form label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="readonlyUser.username" disabled />
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="readonlyUser.full_name" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profile.email" placeholder="填写联系邮箱" />
            </el-form-item>
            <el-form-item label="昵称">
              <el-input v-model="profile.nickname" placeholder="用于界面显示的昵称" />
            </el-form-item>
            <el-form-item label="简介">
              <el-input v-model="profile.bio" type="textarea" :rows="3" placeholder="一句话介绍你自己" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveProfile">保存信息</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="glass-surface mt-20">
          <template #header>
            <div class="card-header text-strong">个性化设置</div>
          </template>

          <div class="settings-grid">
            <div>
              <div class="text-soft">配色方案</div>
              <el-radio-group v-model="theme.scheme" @change="onSchemeChange">
                <el-radio-button label="qing">青釉</el-radio-button>
                <el-radio-button label="jiang">绛红</el-radio-button>
                <el-radio-button label="custom">自定义</el-radio-button>
              </el-radio-group>
            </div>
            <div>
              <div class="text-soft">玻璃模糊强度 (px)</div>
              <el-slider :min="6" :max="30" :step="1" v-model="theme.glassBlur" @change="onBlurChange" />
            </div>
            <div>
              <div class="text-soft">玻璃透明度</div>
              <el-slider :min="0.06" :max="0.25" :step="0.01" v-model="theme.glassOpacity" @change="onOpacityChange" />
            </div>
            <div>
              <div class="text-soft">光晕强度</div>
              <div class="glow-row">
                <el-radio-group v-model="glowIntensity" @change="onGlowIntensityChange" :disabled="theme.autoGlowByPage">
                  <el-radio-button label="low">弱</el-radio-button>
                  <el-radio-button label="medium">中</el-radio-button>
                  <el-radio-button label="high">强</el-radio-button>
                </el-radio-group>
                <el-switch v-model="theme.autoGlowByPage" @change="onAutoGlowChange" active-text="按页面自动" />
              </div>
            </div>
          </div>
        </el-card>

        <el-card v-if="theme.scheme === 'custom'" class="glass-surface mt-20">
          <template #header>
            <div class="card-header text-strong">自定义配色</div>
          </template>
          <div class="custom-grid">
            <div>
              <div class="text-soft">主色 (primary)</div>
              <el-color-picker v-model="palette.primary" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">成功 (success)</div>
              <el-color-picker v-model="palette.success" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">警告 (warning)</div>
              <el-color-picker v-model="palette.warning" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">危险 (danger)</div>
              <el-color-picker v-model="palette.danger" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">信息 (info)</div>
              <el-color-picker v-model="palette.info" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">强文字色</div>
              <el-color-picker v-model="palette.textStrong" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">弱文字色</div>
              <el-color-picker v-model="palette.textSoft" @change="onPaletteChange" />
            </div>
            <div>
              <div class="text-soft">背景渐变起始色</div>
              <el-color-picker v-model="customBg.start" @change="onCustomBgChange" />
            </div>
            <div>
              <div class="text-soft">背景渐变结束色</div>
              <el-color-picker v-model="customBg.end" @change="onCustomBgChange" />
            </div>
          </div>
          <div class="mt-20">
            <el-button type="primary" @click="saveCustomPalette">保存自定义方案</el-button>
            <el-button class="ml-10" @click="resetCustomPalette">恢复默认</el-button>
            <el-button class="ml-10" @click="saveCustomBackground">保存背景渐变</el-button>
            <el-button class="ml-10" @click="resetCustomBackground">恢复默认背景</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useProfileStore } from '@/stores/profile'
import { useThemeStore } from '@/stores/theme'

const auth = useAuthStore()
const profile = useProfileStore()
const theme = useThemeStore()

const readonlyUser = reactive({ username: '', full_name: '', email: '' })

const defaultAvatar = 'https://cdn.jsdelivr.net/gh/identicons/jasonlong@latest/identicon.png'

onMounted(async () => {
  if (!auth.user) {
    await auth.fetchMe()
  }
  if (auth.user) {
    readonlyUser.username = auth.user.username || ''
    readonlyUser.full_name = auth.user.full_name || ''
    readonlyUser.email = auth.user.email || ''
    if (!profile.email) profile.setEmail(readonlyUser.email)
  }
  theme.applyTheme()
})

const saveProfile = () => {
  // 本地持久化即可
}

const handleAvatarUpload = async (file) => {
  const toDataUrl = (f) => new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(f)
  })
  try {
    const dataUrl = await toDataUrl(file)
    profile.setAvatar(dataUrl)
    return false // 阻止默认上传
  } catch (e) {
    return false
  }
}

const onSchemeChange = (val) => {
  theme.setScheme(val)
}
const onBlurChange = (val) => {
  theme.setGlassBlur(val)
}
const onOpacityChange = (val) => {
  theme.setGlassOpacity(val)
}

// 光晕强度与按页面自动
const glowIntensity = ref(theme.glowIntensity || 'medium')
const onGlowIntensityChange = (val) => {
  glowIntensity.value = val
  theme.setGlowIntensity(val)
}
const onAutoGlowChange = (val) => {
  theme.setAutoGlowByPage(val)
}

// 自定义配色
const palette = reactive({
  primary: theme.customPalette?.primary || '#1E6D74',
  success: theme.customPalette?.success || '#4EA691',
  warning: theme.customPalette?.warning || '#E8A955',
  danger: theme.customPalette?.danger || '#D46055',
  info: theme.customPalette?.info || '#7FB3B0',
  textStrong: theme.customPalette?.textStrong || '#EAF4F2',
  textSoft: theme.customPalette?.textSoft || '#B7D3CF'
})

const onPaletteChange = () => {
  theme.setCustomPalette(palette)
}

const saveCustomPalette = () => {
  theme.setScheme('custom')
}

const resetCustomPalette = () => {
  palette.primary = '#409EFF'
  palette.success = '#67C23A'
  palette.warning = '#E6A23C'
  palette.danger = '#F56C6C'
  palette.info = '#909399'
  palette.textStrong = '#ECECEC'
  palette.textSoft = '#CFCFCF'
  onPaletteChange()
}

// 自定义背景渐变（两端色）
const customBg = reactive({
  start: theme.customBgStart || '#0a1a1f',
  end: theme.customBgEnd || '#050f13'
})
const onCustomBgChange = () => {
  // 实时预览但不持久化，保存按钮执行持久化
  theme.setCustomBackgroundGradient(customBg.start, customBg.end)
}
const saveCustomBackground = () => {
  theme.setScheme('custom')
  theme.setCustomBackgroundGradient(customBg.start, customBg.end)
}
const resetCustomBackground = () => {
  customBg.start = '#0a1a1f'
  customBg.end = '#050f13'
  theme.setCustomBackgroundGradient(customBg.start, customBg.end)
}
</script>

<style scoped>
.profile-container {
  padding: 10px;
}
.card-header {
  font-weight: 600;
}
.avatar-box {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0 16px;
}
.avatar-uploader {
  display: flex;
  justify-content: center;
}
.tip {
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
}
.settings-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
.glow-row { display: flex; align-items: center; gap: 12px; }
.mt-20 { margin-top: 20px; }
.ml-10 { margin-left: 10px; }
.custom-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
</style>