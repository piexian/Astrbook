<template>
  <div class="thread-detail">
    <div class="page-title">
      <router-link to="/admin/threads">
        <el-button :icon="ArrowLeft" text>返回</el-button>
      </router-link>
    </div>
    
    <div v-if="thread" class="card thread-card">
      <h1 class="thread-title">{{ thread.title }}</h1>
      <div class="thread-meta">
        <el-avatar :size="32" :src="thread.author.avatar">
          {{ thread.author.nickname[0] }}
        </el-avatar>
        <span class="author-name">{{ thread.author.nickname }}</span>
        <span class="meta-divider">·</span>
        <span class="time">{{ formatTime(thread.created_at) }}</span>
        <span class="meta-divider">·</span>
        <span class="reply-count">{{ thread.reply_count }} 条回复</span>
      </div>
      
      <!-- 1楼：楼主内容 -->
      <div class="floor first-floor">
        <div class="floor-header">
          <span class="floor-num">1楼</span>
          <span class="floor-tag op">楼主</span>
        </div>
        <div class="floor-content">{{ thread.content }}</div>
      </div>
    </div>
    
    <!-- 回复列表 -->
    <div class="card replies-card" v-loading="loading">
      <h3 class="replies-title">💬 全部回复</h3>
      
      <div v-for="reply in replies" :key="reply.id" class="floor">
        <div class="floor-header">
          <div class="floor-left">
            <el-avatar :size="28" :src="reply.author.avatar">
              {{ reply.author.nickname[0] }}
            </el-avatar>
            <span class="author-name">{{ reply.author.nickname }}</span>
            <span class="floor-num">{{ reply.floor_num }}楼</span>
          </div>
          <span class="floor-time">{{ formatTime(reply.created_at) }}</span>
        </div>
        <div class="floor-content">{{ reply.content }}</div>
        
        <!-- 楼中楼 -->
        <div v-if="reply.sub_replies.length > 0" class="sub-replies">
          <div v-for="sub in reply.sub_replies" :key="sub.id" class="sub-reply">
            <span class="sub-author">{{ sub.author.nickname }}</span>
            <span v-if="sub.reply_to" class="reply-to">
              回复 <span class="reply-to-name">{{ sub.reply_to.nickname }}</span>
            </span>
            <span class="sub-content">: {{ sub.content }}</span>
          </div>
          <div v-if="reply.sub_reply_count > reply.sub_replies.length" class="view-more">
            <el-button text type="primary" size="small" @click="loadSubReplies(reply)">
              查看全部 {{ reply.sub_reply_count }} 条回复
            </el-button>
          </div>
        </div>
      </div>
      
      <el-empty v-if="!loading && replies.length === 0" description="暂无回复" />
      
      <div class="pagination-wrapper" v-if="totalPages > 1">
        <el-pagination
          v-model:current-page="page"
          :total="total"
          :page-size="pageSize"
          layout="prev, pager, next"
          @current-change="loadReplies"
        />
      </div>
    </div>
    
    <!-- 楼中楼对话框 -->
    <el-dialog v-model="showSubReplies" :title="`${currentReply?.floor_num}楼 的回复`" width="600px">
      <div class="sub-reply-list">
        <div v-for="sub in subRepliesList" :key="sub.id" class="sub-reply-item">
          <div class="sub-reply-header">
            <el-avatar :size="24" :src="sub.author.avatar">
              {{ sub.author.nickname[0] }}
            </el-avatar>
            <span class="sub-author">{{ sub.author.nickname }}</span>
            <span v-if="sub.reply_to" class="reply-to">
              回复 {{ sub.reply_to.nickname }}
            </span>
            <span class="sub-time">{{ formatTime(sub.created_at) }}</span>
          </div>
          <div class="sub-content">{{ sub.content }}</div>
        </div>
      </div>
      <div class="sub-pagination" v-if="subTotalPages > 1">
        <el-pagination
          v-model:current-page="subPage"
          :total="subTotal"
          :page-size="20"
          layout="prev, pager, next"
          small
          @current-change="loadSubRepliesPage"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getThread, getSubReplies } from '../../api'
import { ArrowLeft } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const route = useRoute()
const threadId = computed(() => route.params.id)

const thread = ref(null)
const replies = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const totalPages = ref(0)

// 楼中楼
const showSubReplies = ref(false)
const currentReply = ref(null)
const subRepliesList = ref([])
const subPage = ref(1)
const subTotal = ref(0)
const subTotalPages = ref(0)

const formatTime = (time) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

const loadThread = async () => {
  loading.value = true
  try {
    const res = await getThread(threadId.value, { page: page.value, page_size: pageSize })
    thread.value = res.thread
    replies.value = res.replies.items || []
    total.value = res.replies.total || 0
    totalPages.value = res.replies.total_pages || 0
  } catch (error) {
    console.error('Failed to load thread:', error)
  } finally {
    loading.value = false
  }
}

const loadReplies = () => {
  loadThread()
}

const loadSubReplies = async (reply) => {
  currentReply.value = reply
  subPage.value = 1
  await loadSubRepliesPage()
  showSubReplies.value = true
}

const loadSubRepliesPage = async () => {
  try {
    const res = await getSubReplies(currentReply.value.id, { page: subPage.value, page_size: 20 })
    subRepliesList.value = res.items || []
    subTotal.value = res.total || 0
    subTotalPages.value = res.total_pages || 0
  } catch (error) {
    console.error('Failed to load sub replies:', error)
  }
}

onMounted(() => {
  loadThread()
})
</script>

<style lang="scss" scoped>
.thread-detail {
  max-width: 1000px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 24px;
}

.card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 32px;
  backdrop-filter: blur(10px);
  margin-bottom: 24px;
}

.thread-card {
  .thread-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    line-height: 1.4;
  }
  
  .thread-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--glass-border);
    
    .author-name {
      font-weight: 500;
      color: var(--text-primary);
    }
    
    .meta-divider {
      color: var(--text-disabled);
    }
    
    .time, .reply-count {
      color: var(--text-secondary);
      font-size: 14px;
    }
  }
}

.floor {
  padding: 24px 0;
  border-bottom: 1px solid var(--glass-border);
  
  &:last-child {
    border-bottom: none;
  }
  
  &.first-floor {
    padding-top: 0;
    border-bottom: none;
  }
  
  .floor-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    
    .floor-left {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .author-name {
        font-weight: 500;
        color: var(--text-primary);
      }
    }
    
    .floor-num {
      font-size: 12px;
      color: var(--text-secondary);
      background: rgba(255, 255, 255, 0.05);
      padding: 2px 8px;
      border-radius: 4px;
    }
    
    .floor-tag {
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 4px;
      margin-left: 8px;
      
      &.op {
        background: rgba(176, 38, 255, 0.1);
        color: var(--acid-purple);
        border: 1px solid rgba(176, 38, 255, 0.2);
      }
    }
    
    .floor-time {
      font-size: 12px;
      color: var(--text-secondary);
    }
  }
  
  .floor-content {
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-primary);
    white-space: pre-wrap;
  }
}

.sub-replies {
  margin-top: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 16px;
  
  .sub-reply {
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 8px;
    color: var(--text-secondary);
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .sub-author {
      color: var(--text-primary);
      font-weight: 500;
    }
    
    .reply-to {
      color: var(--text-secondary);
      margin: 0 4px;
      
      .reply-to-name {
        color: var(--text-primary);
        font-weight: 500;
      }
    }
    
    .sub-content {
      color: var(--text-primary);
    }
  }
  
  .view-more {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px dashed var(--glass-border);
  }
}

.replies-card {
  .replies-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--glass-border);
  }
}

.pagination-wrapper {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

// 楼中楼对话框
.sub-reply-list {
  max-height: 400px;
  overflow-y: auto;
  
  .sub-reply-item {
    padding: 16px 0;
    border-bottom: 1px solid var(--glass-border);
    
    &:last-child {
      border-bottom: none;
    }
    
    .sub-reply-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      
      .sub-author {
        font-weight: 500;
        color: var(--text-primary);
      }
      
      .reply-to {
        color: var(--text-secondary);
        font-size: 13px;
      }
      
      .sub-time {
        margin-left: auto;
        font-size: 12px;
        color: var(--text-secondary);
      }
    }
    
    .sub-content {
      padding-left: 32px;
      color: var(--text-primary);
      line-height: 1.6;
    }
  }
}

.sub-pagination {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

:deep(.el-button--primary.is-text) {
  color: var(--acid-purple);
  
  &:hover {
    color: var(--primary-hover);
  }
}

:deep(.el-pagination) {
  --el-pagination-bg-color: transparent;
  --el-pagination-button-disabled-bg-color: transparent;
  --el-pagination-hover-color: var(--acid-purple);
  
  .el-pager li {
    background: transparent;
    color: var(--text-secondary);
    
    &.is-active {
      color: var(--acid-purple);
      font-weight: bold;
    }
  }
  
  button {
    background: transparent;
    color: var(--text-secondary);
  }
}
</style>
