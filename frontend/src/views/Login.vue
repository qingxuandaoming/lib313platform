<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>登录</h2>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="auth.loading" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>

      <el-alert v-if="auth.error" :title="auth.error" type="error" show-icon class="mt-10" />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()

const formRef = ref(null)
const form = ref({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    const ok = await auth.login(form.value.username, form.value.password)
    if (ok) {
      router.push('/home')
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}
.login-card {
  width: 420px;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.mt-10 { margin-top: 10px; }
</style>