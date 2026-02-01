<template>
  <div class="admin-layout">
    <Sidebar />
    <div class="main-content">
      <Header />
      <div class="page-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../components/admin/Sidebar.vue'
import Header from '../components/admin/Header.vue'
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: transparent;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  max-width: 1600px; // 限制最大宽度，避免在大屏上过于拉伸
  margin: 0 auto;
  width: 100%;
}
</style>
