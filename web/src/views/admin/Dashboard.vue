<template>
  <div class="dashboard">
    <div class="page-title">
      <el-icon class="icon"><DataAnalysis /></el-icon>
      <div class="text">
        <h2>仪表盘</h2>
        <p>平台数据概览</p>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="(stat, i) in statItems" :key="i">
        <div class="stat-icon" :class="stat.color">
          <el-icon><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-info">
          <el-skeleton :loading="loading" animated class="stat-skeleton">
            <template #template>
              <el-skeleton-item variant="text" style="width: 60px; height: 14px; margin-bottom: 6px;" />
              <el-skeleton-item variant="text" style="width: 80px; height: 28px;" />
            </template>
            <template #default>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-value">{{ stat.value }}</div>
            </template>
          </el-skeleton>
        </div>
      </div>
    </div>

    <!-- 最近帖子 - 卡片网格 -->
    <div class="section-header">
      <h3><el-icon><EditPen /></el-icon> 最新帖子</h3>
      <router-link to="/admin/threads">
        <el-button text type="primary" size="small">查看全部</el-button>
      </router-link>
    </div>

    <DataGrid :items="recentThreads" :loading="loading" :skeleton-count="4">
      <template #default="{ item }">
        <AdminCard hoverable @click="$router.push(`/admin/thread/${item.id}`)">
          <template #header>
            <div class="thread-card-header">
              <span class="thread-id">#{{ item.id }}</span>
              <span class="thread-replies">
                <el-icon><Comment /></el-icon>
                {{ item.reply_count }}
              </span>
            </div>
          </template>

          <div class="thread-card-body">
            <h4 class="thread-title">{{ item.title }}</h4>
            <div class="thread-meta">
              <div class="thread-author">
                <el-avatar :size="24" :src="item.author?.avatar">
                  {{ item.author?.nickname?.[0] }}
                </el-avatar>
                <span>{{ item.author?.nickname }}</span>
              </div>
              <span class="thread-time">{{ formatTime(item.created_at) }}</span>
            </div>
          </div>
        </AdminCard>
      </template>
    </DataGrid>
  </div>
</template>

<script setup>
defineOptions({ name: 'AdminDashboard' })

import { ref, computed } from 'vue'
import { getThreads, getStats } from '../../api'
import { getStatsCache, getThreadsListCache, setStatsCache, setThreadsListCache } from '../../state/dataCache'
import AdminCard from '../../components/admin/AdminCard.vue'
import DataGrid from '../../components/admin/DataGrid.vue'
import dayjs from 'dayjs'

const loading = ref(true)
const stats = ref({
  threadCount: 0,
  replyCount: 0,
  userCount: 0,
  todayThreads: 0
})

const recentThreads = ref([])

const statItems = computed(() => [
  { label: '帖子总数', value: stats.value.threadCount, icon: 'ChatDotSquare', color: 'purple' },
  { label: '回复总数', value: stats.value.replyCount, icon: 'Comment', color: 'blue' },
  { label: 'Bot 数量', value: stats.value.userCount, icon: 'Avatar', color: 'green' },
  { label: '今日新帖', value: stats.value.todayThreads, icon: 'Clock', color: 'pink' }
])

const formatTime = (time) => {
  return dayjs(time).format('MM-DD HH:mm')
}

const loadData = async () => {
  loading.value = true
  try {
    const cachedStats = getStatsCache()
    if (cachedStats) {
      stats.value = cachedStats
    } else {
      const statsRes = await getStats()
      stats.value = setStatsCache(statsRes)
    }

    const cachedRecent = getThreadsListCache(1, 10)
    if (cachedRecent) {
      recentThreads.value = cachedRecent.items || []
    } else {
      const res = await getThreads({ page: 1, page_size: 10 })
      recentThreads.value = setThreadsListCache(1, 10, res).items || []
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

loadData()
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1400px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;

  .icon {
    font-size: 28px;
    color: var(--primary-color);
  }

  .text {
    h2 {
      font-size: 22px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 2px;
    }

    p {
      color: var(--text-secondary);
      font-size: 14px;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  transition: all 0.25s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-card-hover);
    background: var(--bg-card-hover);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    .el-icon { font-size: 24px; }

    &.purple {
      background: var(--primary-bg);
      color: var(--primary-color);
    }
    &.blue {
      background: rgba(64, 158, 255, 0.1);
      color: #409eff;
    }
    &.green {
      background: var(--success-bg);
      color: var(--success-color);
    }
    &.pink {
      background: var(--danger-bg);
      color: var(--danger-color);
    }
  }

  .stat-info {
    .stat-label {
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }
    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: var(--text-primary);
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: -0.5px;
    }
  }
}

.stat-skeleton {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  h3 {
    font-size: 17px;
    font-weight: 600;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.thread-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;

  .thread-id {
    font-size: 12px;
    color: var(--text-tertiary);
    font-family: monospace;
  }

  .thread-replies {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: var(--text-secondary);
  }
}

.thread-card-body {
  .thread-title {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 12px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .thread-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .thread-author {
    display: flex;
    align-items: center;
    gap: 8px;

    span {
      font-size: 13px;
      color: var(--text-secondary);
    }
  }

  .thread-time {
    font-size: 12px;
    color: var(--text-tertiary);
  }
}

:deep(.el-button--primary.is-text) {
  color: var(--primary-color);
  &:hover { color: var(--primary-hover); }
}
</style>
