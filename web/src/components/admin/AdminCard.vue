<template>
  <div class="admin-card" :class="{ 'has-hover': hoverable, 'clickable': !!$attrs.onClick }">
    <div class="card-header" v-if="$slots.header || title">
      <div class="header-content">
        <slot name="header">
          <h3 v-if="title">{{ title }}</h3>
        </slot>
      </div>
      <div class="header-actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <div class="card-body">
      <slot></slot>
    </div>

    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  hoverable: { type: Boolean, default: false }
})
</script>

<style lang="scss" scoped>
.admin-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;

  &.has-hover:hover,
  &.clickable:hover {
    transform: translateY(-2px);
    background: var(--bg-card-hover);
    border-color: var(--border-hover);
    box-shadow: var(--shadow-card-hover);
  }

  &.clickable {
    cursor: pointer;
  }
}

.card-header {
  padding: 16px 20px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
  }
}

.card-body {
  padding: 16px 20px;
  flex: 1;
}

.card-footer {
  padding: 12px 20px;
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
</style>
