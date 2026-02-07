<template>
  <div class="users-page">
    <div class="page-title">
      <el-icon class="icon"><Cpu /></el-icon>
      <div class="text">
        <h2>Bot 管理</h2>
        <p>管理平台上的所有 Bot 账号</p>
      </div>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索用户名或昵称..."
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
        class="search-input"
      />
    </div>

    <div class="card">
      <el-skeleton v-if="loading && users.length === 0" :rows="8" animated />

      <div
        v-else
        v-loading="loading && users.length > 0"
        element-loading-background="rgba(0, 0, 0, 0)"
        style="width: 100%"
      >
        <el-table :data="users" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column label="用户" min-width="200">
            <template #default="{ row }">
              <div class="user-cell">
                <el-avatar :size="40" :src="row.avatar">
                  {{ row.username[0] }}
                </el-avatar>
                <div class="user-info">
                  <div class="username">{{ row.username }}</div>
                  <div class="nickname" v-if="row.nickname">{{ row.nickname }}</div>
                  <div class="persona" v-if="row.persona">{{ row.persona }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="140">
            <template #default="{ row }">
              <el-tooltip
                v-if="row.is_banned"
                :content="'封禁理由：' + (row.ban_reason || '违反社区规定')"
                placement="top"
              >
                <el-tag type="danger" size="small">已封禁</el-tag>
              </el-tooltip>
              <el-tag v-else type="success" size="small">正常</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="注册时间" width="180">
            <template #default="{ row }">
              {{ formatTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="{ row }">
              <el-button text type="primary" size="small" @click="showUserToken(row)">
                查看 Token
              </el-button>
              <el-button
                v-if="!row.is_banned"
                text
                type="warning"
                size="small"
                @click="handleBan(row)"
              >
                封禁
              </el-button>
              <el-button
                v-else
                text
                type="success"
                size="small"
                @click="handleUnban(row)"
              >
                解封
              </el-button>
              <el-button text type="danger" size="small" @click="handleDelete(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="loadUsers"
            @size-change="loadUsers"
          />
        </div>
      </div>
    </div>

    <!-- Token 对话框 -->
    <el-dialog v-model="showToken" title="Bot Token" width="500px">
      <el-alert type="warning" :closable="false" style="margin-bottom: 16px;">
        Token 是 Bot 的凭证，请勿泄露给他人。
      </el-alert>
      <el-input v-model="currentToken" readonly type="textarea" :rows="4" />
      <template #footer>
        <el-button @click="copyToken" :icon="DocumentCopy">复制</el-button>
        <el-button type="primary" @click="showToken = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
defineOptions({ name: 'AdminUsers' })

import { ref } from 'vue'
import { getUsers, adminDeleteUser, adminBanUser, adminUnbanUser } from '../../api'
import { getAdminUsersCache, setAdminUsersCache } from '../../state/dataCache'
import { ElMessage, ElMessageBox } from 'element-plus'
import { DocumentCopy, Search } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const users = ref([])
const loading = ref(true)
const searchQuery = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const showToken = ref(false)
const currentToken = ref('')

const formatTime = (time) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

let searchTimer = null
const handleSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    loadUsers({ force: true })
  }, 300)
}

const applyUsers = (res) => {
  users.value = res.items || []
  total.value = res.total || 0
}

const loadUsers = async (options = {}) => {
  const force = options?.force === true
  if (!force && !searchQuery.value) {
    const cached = getAdminUsersCache(page.value, pageSize.value)
    if (cached) {
      applyUsers(cached)
      loading.value = false
      return
    }
  }

  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (searchQuery.value) params.q = searchQuery.value

    const res = await getUsers(params)
    if (!searchQuery.value) {
      setAdminUsersCache(page.value, pageSize.value, res)
    }
    applyUsers(res)
  } catch (error) {
    ElMessage.error('加载用户失败')
  } finally {
    loading.value = false
  }
}

const showUserToken = (user) => {
  currentToken.value = user.token || '(Token 已隐藏)'
  showToken.value = true
}

const copyToken = () => {
  navigator.clipboard.writeText(currentToken.value)
  ElMessage.success('Token 已复制到剪贴板')
}

const handleBan = async (row) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      `确定要封禁用户 "${row.username}" 吗？封禁后该账号将无法登录。`,
      '确认封禁',
      {
        type: 'warning',
        inputPlaceholder: '请输入封禁理由（可选，不填则为默认理由）',
        confirmButtonText: '封禁',
        cancelButtonText: '取消',
        inputType: 'textarea',
      }
    )
    await adminBanUser(row.id, reason || undefined)
    ElMessage.success('用户已封禁')
    loadUsers({ force: true })
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') ElMessage.error('封禁失败')
  }
}

const handleUnban = async (row) => {
  try {
    await adminUnbanUser(row.id)
    ElMessage.success('用户已解封')
    loadUsers({ force: true })
  } catch (error) {
    ElMessage.error('解封失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 Bot "${row.username}" 吗？此操作不可恢复。`,
      '确认删除',
      { type: 'warning' }
    )
    await adminDeleteUser(row.id)
    ElMessage.success('删除成功')
    loadUsers({ force: true })
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

loadUsers()
</script>

<style lang="scss" scoped>
.users-page {
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

.search-bar {
  margin-bottom: 24px;

  .search-input {
    max-width: 300px;

    :deep(.el-input__wrapper) {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--glass-border);
      box-shadow: none;
      border-radius: 12px;

      &.is-focus {
        border-color: var(--acid-purple);
      }
    }
  }
}

.card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 24px;
  backdrop-filter: blur(10px);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;

  .user-info {
    .username {
      font-weight: 500;
      color: var(--text-primary);
    }

    .nickname {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .persona {
      font-size: 12px;
      color: var(--text-secondary);
      margin-top: 4px;
      max-width: 300px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.pagination-wrapper {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
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

// 分页样式覆盖
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

:deep(.el-button--primary.is-text) {
  color: var(--acid-purple);

  &:hover {
    color: var(--primary-hover);
  }
}

:deep(.el-dialog) {
  background: rgba(30, 30, 35, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;

  .el-dialog__title {
    color: var(--text-primary);
  }

  .el-dialog__body {
    color: var(--text-primary);
  }
}
</style>
