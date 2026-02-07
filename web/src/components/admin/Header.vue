<template>
  <header class="header">
    <div class="header-left">
      <el-button 
        v-if="isMobile" 
        text 
        class="mobile-menu-btn" 
        @click="$emit('toggle-sidebar')"
      >
        <el-icon :size="20"><Menu /></el-icon>
      </el-button>

      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item :to="{ path: '/admin' }">后台</el-breadcrumb-item>
        <el-breadcrumb-item v-if="currentRoute.meta.title">
          {{ currentRoute.meta.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    
    <div class="header-right">
      <el-button circle class="theme-toggle" @click="themeStore.toggleTheme">
        <el-icon>
          <Moon v-if="themeStore.isDark" />
          <Sunny v-else />
        </el-icon>
      </el-button>

      <el-dropdown @command="handleCommand">
        <el-avatar :size="36" class="avatar">
          <el-icon><User /></el-icon>
        </el-avatar>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { clearAllCache } from '../../state/dataCache'
import { useThemeStore } from '../../stores/theme'
import { Moon, Sunny, Menu } from '@element-plus/icons-vue'

defineProps({
  isMobile: Boolean
})

defineEmits(['toggle-sidebar'])

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const currentRoute = computed(() => route)

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('admin_token')
    clearAllCache()
    router.push('/admin/login')
  }
}
</script>

<style lang="scss" scoped>
.header {
  height: var(--header-height);
  background: var(--bg-sidebar); // 复用侧边栏背景，保持一致性
  backdrop-filter: blur(var(--blur-amount));
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.3s, border-color 0.3s;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mobile-menu-btn {
  padding: 8px;
  margin-left: -8px;
  color: var(--text-primary);
  
  &:hover {
    background: var(--glass-bg);
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  
  .theme-toggle {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    
    &:hover {
      color: var(--primary-color);
      border-color: var(--primary-color);
      background: var(--glass-bg);
    }
  }

  .avatar {
    cursor: pointer;
    background: var(--primary-color);
    font-size: 14px;
    font-weight: 600;
    border: 2px solid var(--border-color);
    transition: all 0.2s;
    
    &:hover {
      transform: scale(1.05);
      border-color: var(--primary-color);
      box-shadow: 0 0 10px rgba(176, 38, 255, 0.3);
    }
  }
}

// 面包屑样式优化
:deep(.el-breadcrumb) {
  font-size: 14px;
  
  .el-breadcrumb__inner {
    color: var(--text-secondary);
    font-weight: 400;
    
    &.is-link:hover {
      color: var(--primary-color);
    }
  }
  
  .el-breadcrumb__item:last-child .el-breadcrumb__inner {
    color: var(--text-primary);
    font-weight: 500;
  }
  
  .el-breadcrumb__separator {
    color: var(--text-disabled);
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 16px;
  }
  
  .breadcrumb {
    display: none; // 移动端隐藏面包屑以节省空间
  }
}
</style>
