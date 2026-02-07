<template>
  <div class="data-grid-container">
    <!-- Loading skeletons -->
    <div v-if="loading && (!items || items.length === 0)" class="data-grid">
      <div v-for="i in skeletonCount" :key="'sk-' + i" class="grid-skeleton">
        <el-skeleton animated>
          <template #template>
            <el-skeleton-item variant="text" style="width: 60%; height: 18px; margin-bottom: 12px;" />
            <el-skeleton-item variant="text" style="width: 40%; height: 14px; margin-bottom: 8px;" />
            <el-skeleton-item variant="text" style="width: 80%; height: 14px; margin-bottom: 8px;" />
            <el-skeleton-item variant="text" style="width: 50%; height: 14px;" />
          </template>
        </el-skeleton>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!items || items.length === 0" class="empty-state">
      <el-empty :description="emptyText" />
    </div>

    <!-- Data grid -->
    <div v-else class="data-grid" v-loading="loading && items.length > 0" element-loading-background="rgba(0, 0, 0, 0)">
      <slot v-for="item in items" :key="item.id || item._id" :item="item"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  emptyText: { type: String, default: '暂无数据' },
  skeletonCount: { type: Number, default: 6 }
})
</script>

<style lang="scss" scoped>
.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  width: 100%;
}

.grid-skeleton {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  padding: 20px;
}

.empty-state {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

@media (max-width: 768px) {
  .data-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .data-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}
</style>
