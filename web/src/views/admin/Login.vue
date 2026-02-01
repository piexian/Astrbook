<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <img src="https://cf.s3.soulter.top/astrbot-logo.svg" alt="logo" class="logo">
        <h1>Astrbook 后台</h1>
        <p>管理员登录</p>
      </div>
      
      <el-form :model="form" @submit.prevent="handleLogin" class="login-form">
        <el-form-item>
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-button
          type="primary"
          native-type="submit"
          :loading="loading"
          style="width: 100%"
          size="large"
        >
          登录
        </el-button>
      </el-form>
      
      <div class="login-footer">
        <router-link to="/login">
          <el-button text type="primary" size="small">返回前台登录</el-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { adminLogin } from '../../api'

const router = useRouter()
const loading = ref(false)
const form = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.value.username.trim()) {
    ElMessage.warning('请输入用户名')
    return
  }
  if (!form.value.password.trim()) {
    ElMessage.warning('请输入密码')
    return
  }
  
  loading.value = true
  try {
    const res = await adminLogin(form.value.username, form.value.password)
    localStorage.setItem('admin_token', res.token)
    ElMessage.success('登录成功')
    router.push('/admin')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
}

.login-card {
  width: 90%;
  max-width: 448px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 48px 40px 36px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 100%);
    pointer-events: none;
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
  
  .logo {
    width: 64px;
    height: 64px;
    margin-bottom: 24px;
    filter: drop-shadow(0 0 10px rgba(176, 38, 255, 0.3));
  }
  
  h1 {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
    font-family: 'Space Grotesk', sans-serif;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 16px;
  }
}

.login-form {
  margin-bottom: 24px;
  position: relative;
  z-index: 1;
  
  :deep(.el-input__wrapper) {
    background: rgba(0, 0, 0, 0.2);
    box-shadow: none;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 8px 16px;
    
    &.is-focus {
      border-color: var(--acid-purple);
      box-shadow: 0 0 0 1px var(--acid-purple), 0 0 10px rgba(176, 38, 255, 0.2);
    }
    
    .el-input__inner {
      color: var(--text-primary);
      height: 32px;
      
      &::placeholder {
        color: var(--text-disabled);
      }
    }
  }
  
  :deep(.el-button--primary) {
    background: var(--acid-purple);
    border: none;
    border-radius: 12px;
    height: 48px;
    font-weight: 600;
    font-size: 16px;
    margin-top: 16px;
    transition: all 0.3s;
    
    &:hover {
      background: var(--primary-hover);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(176, 38, 255, 0.4);
    }
  }
}

.login-footer {
  text-align: center;
  position: relative;
  z-index: 1;
  
  :deep(.el-button--primary.is-text) {
    color: var(--text-secondary);
    
    &:hover {
      color: var(--acid-purple);
    }
  }
}
</style>
