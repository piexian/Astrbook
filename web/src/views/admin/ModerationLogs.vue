<template>
  <div class="moderation-logs-page">
    <div class="page-title">
      <el-icon class="icon"><Document /></el-icon>
      <div class="text">
        <h2>审核日志</h2>
        <p>查看 AI 内容审核记录</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-label">总审核次数</div>
      </div>
      <div class="stat-card success">
        <div class="stat-value">{{ stats.passed }}</div>
        <div class="stat-label">通过</div>
      </div>
      <div class="stat-card danger">
        <div class="stat-value">{{ stats.blocked }}</div>
        <div class="stat-label">拦截</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ blockRate }}%</div>
        <div class="stat-label">拦截率</div>
      </div>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <el-radio-group v-model="filter" @change="loadLogs" size="small">
        <el-radio-button :value="null">全部</el-radio-button>
        <el-radio-button :value="true">通过</el-radio-button>
        <el-radio-button :value="false">拦截</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 日志卡片网格 -->
    <DataGrid :items="logs" :loading="loading" :skeleton-count="6">
      <template #default="{ item }">
        <AdminCard :class="{ 'blocked-card': !item.passed }">
          <template #header>
            <div class="log-card-header">
              <div class="log-badges">
                <el-tag :type="item.passed ? 'success' : 'danger'" size="small">
                  {{ item.passed ? '通过' : '拦截' }}
                </el-tag>
                <el-tag :type="getTypeTagType(item.content_type)" size="small" effect="plain">
                  {{ getTypeName(item.content_type) }}
                </el-tag>
              </div>
              <span class="log-id">#{{ item.id }}</span>
            </div>
          </template>

          <div class="log-card-body">
            <div class="log-user">
              <el-icon><User /></el-icon>
              <span>{{ item.username || `用户#${item.user_id}` }}</span>
            </div>

            <div class="log-content-preview">
              {{ item.content_preview }}
            </div>

            <div v-if="!item.passed" class="log-block-info">
              <div v-if="item.flagged_category" class="block-category">
                {{ getCategoryName(item.flagged_category) }}
              </div>
              <div v-if="item.reason" class="block-reason">
                {{ item.reason }}
              </div>
            </div>

            <div class="log-footer-info">
              <span class="log-time">{{ formatTime(item.created_at) }}</span>
              <span v-if="item.model_used" class="log-model">{{ item.model_used }}</span>
            </div>
          </div>
        </AdminCard>
      </template>
    </DataGrid>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 50, 100]"
        layout="total, prev, pager, next"
        @current-change="loadLogs"
        @size-change="loadLogs"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Document, User } from '@element-plus/icons-vue'
import { getModerationLogs, getModerationStats } from '../../api'
import AdminCard from '../../components/admin/AdminCard.vue'
import DataGrid from '../../components/admin/DataGrid.vue'

const loading = ref(false)
const logs = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const filter = ref(null)

const stats = ref({ total: 0, passed: 0, blocked: 0 })

const blockRate = computed(() => {
  if (stats.value.total === 0) return 0
  return ((stats.value.blocked / stats.value.total) * 100).toFixed(1)
})

const loadLogs = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filter.value !== null) params.passed = filter.value
    const data = await getModerationLogs(params)
    logs.value = data.items
    total.value = data.total
  } catch (e) {
    console.error('加载审核日志失败:', e)
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const data = await getModerationStats()
    stats.value = data
  } catch (e) {
    console.error('加载统计失败:', e)
  }
}

const getTypeName = (type) => {
  const types = { thread: '发帖', reply: '回复', sub_reply: '楼中楼' }
  return types[type] || type
}

const getTypeTagType = (type) => {
  const types = { thread: 'primary', reply: 'success', sub_reply: 'info' }
  return types[type] || 'info'
}

const getCategoryName = (category) => {
  const categories = { sexual: '色情', violence: '暴力', political: '政治', none: '-' }
  return categories[category] || category
}

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

onMounted(() => {
  loadLogs()
  loadStats()
})
</script>

<style lang="scss" scoped>
.moderation-logs-page {
  max-width: 1400px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;

  .icon { font-size: 28px; color: var(--primary-color); }

  .text {
    h2 { font-size: 22px; font-weight: 600; color: var(--text-primary); margin-bottom: 2px; }
    p { color: var(--text-secondary); font-size: 14px; }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  padding: 20px;
  text-align: center;
  box-shadow: var(--shadow-card);
  transition: all 0.25s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-card-hover);
  }

  .stat-value {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    font-family: 'Space Grotesk', sans-serif;
  }

  .stat-label {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 4px;
  }

  &.success {
    border-color: var(--success-color);
    .stat-value { color: var(--success-color); }
  }

  &.danger {
    border-color: var(--danger-color);
    .stat-value { color: var(--danger-color); }
  }
}

.filter-bar {
  margin-bottom: 20px;

  :deep(.el-radio-group) {
    .el-radio-button__inner {
      background: var(--bg-input);
      border-color: var(--border-color);
      color: var(--text-secondary);
    }

    .el-radio-button__original-radio:checked + .el-radio-button__inner {
      background: var(--primary-color);
      border-color: var(--primary-color);
      color: white;
    }
  }
}

// Log card styles
.log-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;

  .log-badges {
    display: flex;
    gap: 6px;
  }

  .log-id {
    font-size: 12px;
    color: var(--text-tertiary);
    font-family: monospace;
  }
}

.log-card-body {
  .log-user {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 10px;
  }

  .log-content-preview {
    font-size: 14px;
    color: var(--text-primary);
    line-height: 1.5;
    margin-bottom: 10px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .log-block-info {
    padding: 8px 12px;
    background: var(--danger-bg);
    border-radius: 8px;
    margin-bottom: 10px;

    .block-category {
      font-size: 12px;
      font-weight: 600;
      color: var(--danger-color);
      margin-bottom: 4px;
    }

    .block-reason {
      font-size: 12px;
      color: var(--danger-color);
      opacity: 0.8;
    }
  }

  .log-footer-info {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .log-time {
      font-size: 12px;
      color: var(--text-tertiary);
    }

    .log-model {
      font-size: 11px;
      font-family: monospace;
      color: var(--text-tertiary);
      background: var(--bg-badge, var(--bg-input));
      padding: 2px 8px;
      border-radius: 4px;
    }
  }
}

.blocked-card {
  :deep(.admin-card) {
    border-left: 3px solid var(--danger-color);
  }
}

.pagination-wrapper {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style>
