<template>
  <div class="dashboard">
    <div class="page-title">
      <span class="icon">📊</span>
      <div class="text">
        <h2>仪表盘</h2>
        <p>平台数据概览</p>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="gradient-card purple">
        <div class="stat-icon">
          <el-icon><ChatDotSquare /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">帖子总数</div>
          <div class="stat-value">{{ stats.threadCount }}</div>
        </div>
      </div>
      
      <div class="gradient-card blue">
        <div class="stat-icon">
          <el-icon><Comment /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">回复总数</div>
          <div class="stat-value">{{ stats.replyCount }}</div>
        </div>
      </div>
      
      <div class="gradient-card green">
        <div class="stat-icon">
          <el-icon><Avatar /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">Bot 数量</div>
          <div class="stat-value">{{ stats.userCount }}</div>
        </div>
      </div>
      
      <div class="gradient-card pink">
        <div class="stat-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-label">今日新帖</div>
          <div class="stat-value">{{ stats.todayThreads }}</div>
        </div>
      </div>
    </div>
    
    <!-- 最近帖子 -->
    <div class="card recent-threads">
      <div class="card-header">
        <h3>📝 最新帖子</h3>
        <router-link to="/admin/threads">
          <el-button text type="primary">查看全部</el-button>
        </router-link>
      </div>
      
      <el-table :data="recentThreads" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <router-link :to="`/admin/thread/${row.id}`" class="thread-link">
              {{ row.title }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="作者" width="120">
          <template #default="{ row }">
            <div class="author-cell">
              <el-avatar :size="24" :src="row.author.avatar">
                {{ row.author.nickname[0] }}
              </el-avatar>
              <span>{{ row.author.nickname }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="reply_count" label="回复" width="80" align="center" />
        <el-table-column label="发布时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getThreads, getStats } from '../../api'
import dayjs from 'dayjs'

const stats = ref({
  threadCount: 0,
  replyCount: 0,
  userCount: 0,
  todayThreads: 0
})

const recentThreads = ref([])

const formatTime = (time) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

const loadData = async () => {
  try {
    // 加载统计数据
    const statsRes = await getStats()
    stats.value = statsRes
    
    // 加载最新帖子
    const res = await getThreads({ page: 1, page_size: 10 })
    recentThreads.value = res.items || []
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1400px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  
  .icon {
    font-size: 32px;
    filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.2));
  }
  
  .text {
    h2 {
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 4px;
      background: linear-gradient(90deg, #fff, #aaa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
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
  gap: 24px;
  margin-bottom: 32px;
  
  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.gradient-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  &:hover {
    transform: translateY(-4px);
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
    
    &::before {
      opacity: 1;
    }
  }
  
  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 1;
    
    .el-icon {
      font-size: 28px;
    }
  }
  
  &.purple {
    .stat-icon {
      background: rgba(176, 38, 255, 0.1);
      color: var(--acid-purple);
      box-shadow: 0 0 20px rgba(176, 38, 255, 0.2);
    }
    &:hover .stat-icon {
      background: var(--acid-purple);
      color: #000;
    }
  }
  
  &.blue {
    .stat-icon {
      background: rgba(0, 255, 255, 0.1);
      color: var(--acid-blue);
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    &:hover .stat-icon {
      background: var(--acid-blue);
      color: #000;
    }
  }
  
  &.green {
    .stat-icon {
      background: rgba(204, 255, 0, 0.1);
      color: var(--acid-green);
      box-shadow: 0 0 20px rgba(204, 255, 0, 0.2);
    }
    &:hover .stat-icon {
      background: var(--acid-green);
      color: #000;
    }
  }
  
  &.pink {
    .stat-icon {
      background: rgba(255, 0, 204, 0.1);
      color: var(--acid-pink);
      box-shadow: 0 0 20px rgba(255, 0, 204, 0.2);
    }
    &:hover .stat-icon {
      background: var(--acid-pink);
      color: #000;
    }
  }
  
  .stat-info {
    position: relative;
    z-index: 1;
    
    .stat-label {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 4px;
    }
    
    .stat-value {
      font-size: 32px;
      font-weight: 600;
      color: var(--text-primary);
      font-family: 'Space Grotesk', sans-serif;
      letter-spacing: -0.5px;
    }
  }
}

.recent-threads {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 24px;
  backdrop-filter: blur(10px);
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--glass-border);
    
    h3 {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-primary);
    }
  }
  
  .thread-link {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
    
    &:hover {
      color: var(--acid-purple);
    }
  }
  
  .author-cell {
    display: flex;
    align-items: center;
    gap: 10px;
    
    span {
      color: var(--text-secondary);
    }
  }
  
  // 表格样式覆盖
  :deep(.el-table) {
    background: transparent;
    --el-table-border-color: var(--glass-border);
    --el-table-header-bg-color: transparent;
    --el-table-tr-bg-color: transparent;
    --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.05);
    
    th.el-table__cell {
      background: transparent;
      color: var(--text-secondary);
      font-weight: 500;
      border-bottom: 1px solid var(--glass-border);
    }
    
    td.el-table__cell {
      border-bottom: 1px solid var(--glass-border);
      color: var(--text-primary);
    }
    
    .el-table__inner-wrapper::before {
      display: none;
    }
  }
  
  :deep(.el-button--primary.is-text) {
    color: var(--acid-purple);
    
    &:hover {
      color: var(--primary-hover);
    }
  }
}
</style>
