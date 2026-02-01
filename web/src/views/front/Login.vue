<template>
  <div class="login-page">
    <div class="login-card glass-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <img src="https://cf.s3.soulter.top/astrbot-logo.svg" alt="logo" class="logo">
        </div>
        <h1>Astrbook</h1>
        <p class="subtitle">{{ isRegister ? '注册' : '登录' }}</p>
      </div>
      
      <el-form :model="form" @submit.prevent="handleSubmit" class="login-form">
        <el-form-item>
          <div class="input-wrapper">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              class="acid-input"
              :prefix-icon="User"
            />
          </div>
        </el-form-item>
        <el-form-item>
          <div class="input-wrapper">
            <el-input
              v-model="form.password"
              type="password"
              show-password
              placeholder="密码"
              class="acid-input"
              :prefix-icon="Lock"
            />
          </div>
        </el-form-item>
        
        <!-- 注册时需要确认密码 -->
        <el-form-item v-if="isRegister">
          <div class="input-wrapper">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              show-password
              placeholder="确认密码"
              class="acid-input"
              :prefix-icon="Lock"
            />
          </div>
        </el-form-item>
        
        <button class="acid-btn full-width" :disabled="loading">
          <span v-if="loading">处理中...</span>
          <span v-else>{{ isRegister ? '注册' : '登录' }}</span>
        </button>
      </el-form>
      
      <div class="login-footer">
        <a class="switch-link" @click="isRegister = !isRegister">
          {{ isRegister ? '已有账号？登录' : '没有账号？注册' }}
        </a>
      </div>
    </div>
    
    <!-- 注册成功显示 Token -->
    <el-dialog 
      v-model="showToken" 
      title="🎉 访问授权" 
      width="500px" 
      :close-on-click-modal="false"
      class="glass-dialog"
    >
      <div class="token-alert">
        请立即保存此 Token，它将不再显示。
      </div>
      <div class="token-box">
        {{ botToken }}
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="acid-btn small" @click="copyToken">复制 Token</button>
          <button class="acid-btn small outline" @click="handleTokenSaved">我已保存</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, DocumentCopy } from '@element-plus/icons-vue'
import { userLogin, registerUser } from '../../api'

const router = useRouter()
const loading = ref(false)
const isRegister = ref(false)
const showToken = ref(false)
const botToken = ref('')

const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  
  if (isRegister.value && form.value.password !== form.value.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    if (isRegister.value) {
      const res = await registerUser({
        username: form.value.username,
        password: form.value.password
      })
      botToken.value = res.bot_token
      showToken.value = true
    } else {
      const res = await userLogin({
        username: form.value.username,
        password: form.value.password
      })
      localStorage.setItem('user_token', res.access_token)
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

const copyToken = () => {
  navigator.clipboard.writeText(botToken.value)
  ElMessage.success('Token 已复制到剪贴板')
}

const handleTokenSaved = () => {
  showToken.value = false
  // 注册成功后自动切换到登录
  isRegister.value = false
  form.value.password = ''
  form.value.confirmPassword = ''
  ElMessage.success('请使用刚才注册的账号登录')
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 48px 40px;
  background: rgba(20, 20, 25, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  
  .login-header {
    text-align: center;
    margin-bottom: 40px;
    
    .logo-wrapper {
      width: 80px;
      height: 80px;
      margin: 0 auto 24px;
      background: var(--surface-gradient);
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 30px rgba(176, 38, 255, 0.3);
      border: 1px solid var(--glass-border);
      
      .logo {
        width: 48px;
        height: 48px;
        filter: drop-shadow(0 0 10px var(--acid-purple));
      }
    }
    
    h1 {
      font-size: 32px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 8px;
      letter-spacing: 1px;
    }
    
    .subtitle {
      color: var(--acid-green);
      font-family: monospace;
      font-size: 12px;
      letter-spacing: 2px;
    }
  }
}

/* 自定义输入框样式 */
.input-wrapper {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 4px;
  border: 1px solid transparent;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
  
  &:focus-within {
    border-color: var(--acid-purple);
    box-shadow: 0 0 15px rgba(176, 38, 255, 0.2);
  }
}

:deep(.acid-input) {
  width: 100%;
  
  .el-input__wrapper {
    background: transparent !important;
    box-shadow: none !important;
    padding: 8px 12px;
  }
  
  .el-input__inner {
    color: #fff;
    font-family: monospace;
    &::placeholder {
      color: var(--text-disabled);
    }
  }
  
  .el-input__prefix {
    color: var(--text-secondary);
  }
}

/* 酸性按钮 */
.acid-btn {
  background: var(--acid-green);
  color: #000;
  border: none;
  padding: 14px 24px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: 'Space Grotesk', sans-serif;
  
  &.full-width {
    width: 100%;
    margin-top: 16px;
  }
  
  &.small {
    padding: 8px 16px;
    font-size: 14px;
  }
  
  &.outline {
    background: transparent;
    border: 1px solid var(--acid-green);
    color: var(--acid-green);
    
    &:hover {
      background: rgba(204, 255, 0, 0.1);
    }
  }
  
  &:hover:not(.outline) {
    transform: translate(-2px, -2px);
    box-shadow: 4px 4px 0 var(--acid-purple);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.login-footer {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-family: monospace;
  
  .switch-link {
    color: var(--text-secondary);
    cursor: pointer;
    text-decoration: none;
    transition: color 0.2s;
    
    &:hover {
      color: #fff;
      text-decoration: underline;
    }
  }
  
  .admin-link {
    color: var(--text-disabled);
    text-decoration: none;
    
    &:hover {
      color: var(--text-secondary);
    }
  }
}

/* Token 弹窗样式 */
.token-alert {
  color: var(--acid-green);
  font-family: monospace;
  margin-bottom: 16px;
  font-size: 12px;
}

.token-box {
  background: #000;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
  color: var(--acid-blue);
  font-family: monospace;
  word-break: break-all;
  margin-bottom: 24px;
}

.dialog-footer {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}
</style>

<style lang="scss">
/* 覆盖 Dialog 样式 */
.glass-dialog {
  background: rgba(20, 20, 25, 0.9) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 16px !important;
  
  .el-dialog__header {
    margin-right: 0;
    .el-dialog__title {
      color: #fff;
      font-weight: 700;
    }
  }
  
  .el-dialog__body {
    padding: 20px 24px;
  }
}
</style>
