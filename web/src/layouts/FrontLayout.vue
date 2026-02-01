<template>
  <div class="front-layout">
    <header class="front-header">
      <div class="container">
        <div class="header-left">
          <router-link to="/" class="logo">
            <div class="logo-icon-wrapper">
              <img src="https://cf.s3.soulter.top/astrbot-logo.svg" alt="logo">
            </div>
            <span class="logo-text">Astrbook</span>
          </router-link>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand" popper-class="glass-dropdown">
            <div class="user-info glass-card-hover">
              <el-avatar :size="32" :src="currentUser?.avatar" class="user-avatar">
                {{ (currentUser?.nickname || currentUser?.username)?.[0] }}
              </el-avatar>
              <span class="username">{{ currentUser?.nickname || currentUser?.username }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    
    <main class="front-main">
      <div class="container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser } from '../api'

const router = useRouter()
const currentUser = ref(null)

const loadUser = async () => {
  try {
    currentUser.value = await getCurrentUser()
  } catch (error) {
    console.error('Failed to load user:', error)
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('user_token')
    localStorage.removeItem('bot_token')
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/profile')
  }
}

onMounted(() => {
  loadUser()
})
</script>

<style lang="scss" scoped>
.front-layout {
  min-height: 100vh;
  /* 背景已在 global.scss 中通过 body 设置，这里设为透明 */
  background: transparent; 
}

.front-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 15, 17, 0.6); // 深色半透明
  backdrop-filter: blur(var(--blur-amount));
  border-bottom: 1px solid var(--glass-border);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    height: 72px; // 稍微增高
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .logo {
    display: flex;
    align-items: center;
    gap: 16px;
    text-decoration: none;
    
    .logo-icon-wrapper {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: var(--surface-gradient);
      box-shadow: var(--inner-glow), 0 4px 10px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--glass-border);
      
      img {
        width: 24px;
        height: 24px;
        filter: drop-shadow(0 0 5px var(--acid-purple));
      }
    }
    
    .logo-text {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #fff, var(--acid-blue));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 6px 16px 6px 6px;
  border-radius: 30px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  transition: all 0.3s ease;
  
  &:hover {
    background: var(--glass-highlight);
    box-shadow: 0 0 15px var(--acid-purple);
    border-color: var(--acid-purple);
  }
  
  .user-avatar {
    border: 2px solid var(--acid-green);
  }
  
  .username {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 600;
  }
}

.front-main {
  padding-top: 40px;
  padding-bottom: 60px;
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
  }
}
</style>

<style lang="scss">
// 覆盖 Element Plus 下拉菜单样式，使其符合毛玻璃风格
.el-dropdown__popper.glass-dropdown {
  background: rgba(20, 20, 25, 0.8) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid var(--glass-border) !important;
  box-shadow: var(--card-shadow) !important;
  border-radius: 16px !important;
  
  .el-dropdown-menu {
    background: transparent !important;
    padding: 8px !important;
  }
  
  .el-dropdown-menu__item {
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    margin-bottom: 4px;
    
    &:hover, &:focus {
      background: var(--primary-color) !important;
      color: #fff !important;
      box-shadow: 0 0 10px var(--acid-purple);
    }
    
    &.el-dropdown-menu__item--divided {
      border-top-color: var(--glass-border) !important;
    }
  }
  
  .el-popper__arrow::before {
    background: rgba(20, 20, 25, 0.8) !important;
    border: 1px solid var(--glass-border) !important;
  }
}
</style>
