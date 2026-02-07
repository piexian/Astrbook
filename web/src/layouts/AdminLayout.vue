<template>
  <div class="admin-layout">
    <!-- Desktop Sidebar -->
    <aside v-if="!isMobile" class="desktop-aside" :style="{ width: sidebarCollapsed ? '72px' : '256px' }">
      <Sidebar 
        mode="desktop" 
        v-model:collapsed="sidebarCollapsed"
      />
    </aside>

    <!-- Mobile Drawer -->
    <el-drawer
      v-else
      v-model="drawerVisible"
      direction="ltr"
      :size="280"
      :with-header="false"
      class="mobile-drawer"
    >
      <Sidebar mode="mobile" @item-click="drawerVisible = false" />
    </el-drawer>

    <div class="main-content">
      <Header 
        :is-mobile="isMobile" 
        @toggle-sidebar="drawerVisible = true"
      />
      <div class="page-content">
        <router-view v-slot="{ Component, route }">
          <transition name="route" mode="out-in">
            <keep-alive :include="keepAliveInclude">
              <component :is="Component" :key="route.fullPath" />
            </keep-alive>
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '../components/admin/Sidebar.vue'
import Header from '../components/admin/Header.vue'

const keepAliveInclude = ['AdminDashboard', 'AdminThreads', 'AdminUsers']
const isMobile = ref(false)
const drawerVisible = ref(false)
const sidebarCollapsed = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    drawerVisible.value = false
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  min-height: 100dvh;
  background: transparent;
}

.desktop-aside {
  flex-shrink: 0;
  transition: width 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
  overflow: hidden;
  height: 100vh;
  height: 100dvh;
  position: sticky;
  top: 0;
  z-index: 10;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

.page-content {
  flex: 1;
  padding: var(--page-padding);
  overflow-y: auto;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

:deep(.mobile-drawer) {
  background: var(--bg-sidebar) !important;

  .el-drawer__body {
    padding: 0;
  }
}

:deep(.el-overlay) {
  backdrop-filter: blur(4px);
}
</style>
