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

          <button class="theme-toggle-btn" @click="toggleTheme" :title="theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'">
            <el-icon v-if="theme === 'dark'"><Moon /></el-icon>
            <el-icon v-else><Sunny /></el-icon>
          </button>

          <!-- 未登录状态显示登录按钮 -->
          <template v-if="!isLoggedIn && !userLoading">
            <router-link to="/login" class="login-btn glass-card-hover">
              <span>登录</span>
            </router-link>
          </template>
          <!-- 已登录状态显示用户下拉菜单 -->
          <el-dropdown
            v-else
            :disabled="userLoading"
            @command="handleCommand"
            popper-class="glass-dropdown"
          >
            <div class="user-info glass-card-hover">
              <template v-if="userLoading">
                <div class="skeleton-avatar"></div>
                <div class="skeleton-username"></div>
              </template>
              <template v-else>
                <CachedAvatar :size="32" :src="currentUser?.avatar" avatar-class="user-avatar">
                  {{ (currentUser?.nickname || currentUser?.username)?.[0] }}
                </CachedAvatar>
                <span class="username">{{ currentUser?.nickname || currentUser?.username }}</span>
              </template>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="imagebed">图床</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    
    <main class="front-main">
      <div class="container">
        <router-view v-slot="{ Component, route }">
          <transition name="route" mode="out-in">
            <keep-alive :include="keepAliveInclude">
              <component :is="Component" :key="route.fullPath" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Moon, Sunny } from '@element-plus/icons-vue'
import { getCurrentUser } from '../api'
import { clearAllCache, getCurrentUserCache, setCurrentUserCache } from '../state/dataCache'
import CachedAvatar from '../components/CachedAvatar.vue'

const router = useRouter()
const currentUser = ref(null)
const userLoading = ref(true)
const keepAliveInclude = ['FrontHome', 'FrontProfile']
const theme = ref('dark')

// 判断是否已登录
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('user_token') && !!currentUser.value
})

const loadUser = async () => {
  // 如果没有 token，直接结束加载
  if (!localStorage.getItem('user_token')) {
    userLoading.value = false
    return
  }
  
  userLoading.value = true
  const cached = getCurrentUserCache()
  if (cached) {
    currentUser.value = cached
    userLoading.value = false
    return
  }
  try {
    const res = await getCurrentUser()
    currentUser.value = setCurrentUserCache(res)
  } catch (error) {
    console.error('Failed to load user:', error)
    // 加载失败时清除状态
    currentUser.value = null
  } finally {
    userLoading.value = false
  }
}

const toggleTheme = () => {
  const newTheme = theme.value === 'dark' ? 'light' : 'dark'
  theme.value = newTheme
  document.documentElement.setAttribute('data-theme', newTheme)
  localStorage.setItem('theme', newTheme)
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('user_token')
    localStorage.removeItem('bot_token')
    clearAllCache()
    currentUser.value = null
    router.push('/login')
  } else if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'imagebed') {
    router.push('/imagebed')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'dark'
  theme.value = savedTheme
  document.documentElement.setAttribute('data-theme', savedTheme)
  loadUser()
})
</script>

<style lang="scss" scoped>
.front-layout {
  min-height: 100vh;
  background: transparent; 
}

.front-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding-top: var(--safe-top);
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 calc(var(--page-padding) + var(--safe-right)) 0
      calc(var(--page-padding) + var(--safe-left));
    height: var(--header-height);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    
    .logo-icon-wrapper {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background: transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }
    
    .logo-text {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-primary);
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;

    .theme-toggle-btn {
      width: 36px;
      height: 36px;
      padding: 0;
      border: none;
      background: transparent;
      color: var(--text-primary);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: all 0.2s ease;
      font-size: 18px;
            
      &:hover {
        background: var(--bg-tertiary);
        color: var(--primary-color);
      }
    }
  }
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  
  &:hover {
    background: var(--primary-color);
    border-color: var(--acid-purple);
    box-shadow: 0 0 15px var(--acid-purple);
    color: #fff;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 4px 12px 4px 4px;
  border-radius: 30px;
  background: var(--bg-tertiary);
  border: 1px solid transparent;
  transition: all 0.2s ease;
  
  &:hover {
    background: var(--bg-elevated);
  }
  
  .user-avatar {
    border: 2px solid var(--primary-color);
  }
  
  .username {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 600;
  }

  .skeleton-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--primary-color);
    background: var(--el-skeleton-color);
    position: relative;
    overflow: hidden;
  }

  .skeleton-username {
    width: 90px;
    height: 12px;
    border-radius: 999px;
    background: var(--el-skeleton-color);
    position: relative;
    overflow: hidden;
  }

  .skeleton-avatar::after,
  .skeleton-username::after {
    content: '';
    position: absolute;
    inset: 0;
    transform: translateX(-100%);
    background: linear-gradient(90deg, transparent, var(--el-skeleton-to-color), transparent);
    animation: skeleton-shimmer 1.2s ease-in-out infinite;
  }
}

@keyframes skeleton-shimmer {
  100% {
    transform: translateX(100%);
  }
}

.front-main {
  padding-top: 24px;
  padding-bottom: calc(40px + var(--safe-bottom));
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 calc(var(--page-padding) + var(--safe-right)) 0
      calc(var(--page-padding) + var(--safe-left));
  }
}

@media (max-width: 768px) {
  .front-header .container,
  .front-main .container {
    padding-left: 16px;
    padding-right: 16px;
  }
  
  .front-header .logo .logo-text {
    display: block;
    font-size: 18px;
  }
  
  .user-info {
    padding: 2px;
    background: transparent;
    border: none;
    
    .username {
      display: none;
    }
    
    .skeleton-username {
      display: none;
    }
    
    .user-avatar {
        border-width: 0;
    }
  }
}
</style>

<style lang="scss">
// 覆盖 Element Plus 下拉菜单样式，使其符合扁平风格
.el-dropdown__popper.glass-dropdown {
  background: var(--bg-elevated) !important;
  backdrop-filter: none !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: var(--card-shadow) !important;
  border-radius: 4px !important;
  
  .el-dropdown-menu {
    background: transparent !important;
    padding: 4px !important;
  }
  
  .el-dropdown-menu__item {
    color: var(--text-primary) !important;
    border-radius: 4px !important;
    margin-bottom: 2px;
    padding: 8px 16px !important;
    
    &:hover, &:focus {
      background: var(--bg-tertiary) !important;
      color: var(--text-primary) !important;
      box-shadow: none !important;
    }
    
    &.el-dropdown-menu__item--divided {
      border-top-color: var(--border-light) !important;
    }
  }
  
  .el-popper__arrow {
    display: none !important;
  }
}
</style>
