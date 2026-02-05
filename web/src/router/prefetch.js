import { getCurrentUser, getStats, getThread, getThreads, getUsers } from '../api'
import {
  getAdminUsersCache,
  getCurrentUserCache,
  getStatsCache,
  getThreadDetailCache,
  getThreadsListCache,
  setAdminUsersCache,
  setCurrentUserCache,
  setStatsCache,
  setThreadDetailCache,
  setThreadsListCache
} from '../state/dataCache'

export const prefetchCurrentUser = async () => {
  // 如果没有 token，不需要预取
  if (!localStorage.getItem('user_token')) {
    return null
  }
  const cached = getCurrentUserCache()
  if (cached) return cached
  const res = await getCurrentUser()
  return setCurrentUserCache(res)
}

export const prefetchFrontHome = async () => {
  const page = 1
  const pageSize = 20
  const cached = getThreadsListCache(page, pageSize)
  if (cached) return cached
  const res = await getThreads({ page, page_size: pageSize })
  return setThreadsListCache(page, pageSize, res)
}

export const prefetchFrontThreadDetail = async (to) => {
  const id = to.params.id
  const page = 1
  const pageSize = 20
  const cached = getThreadDetailCache(id, page, pageSize)
  if (cached) return cached
  const res = await getThread(id, { page, page_size: pageSize })
  return setThreadDetailCache(id, page, pageSize, res)
}

export const prefetchAdminDashboard = async () => {
  const cachedStats = getStatsCache()
  if (!cachedStats) {
    const stats = await getStats()
    setStatsCache(stats)
  }

  // recent threads
  const page = 1
  const pageSize = 10
  const cachedThreads = getThreadsListCache(page, pageSize)
  if (!cachedThreads) {
    const res = await getThreads({ page, page_size: pageSize })
    setThreadsListCache(page, pageSize, res)
  }
}

export const prefetchAdminThreads = async () => {
  const page = 1
  const pageSize = 20
  const cached = getThreadsListCache(page, pageSize)
  if (cached) return cached
  const res = await getThreads({ page, page_size: pageSize })
  return setThreadsListCache(page, pageSize, res)
}

export const prefetchAdminUsers = async () => {
  const page = 1
  const pageSize = 20
  const cached = getAdminUsersCache(page, pageSize)
  if (cached) return cached
  const res = await getUsers({ page, page_size: pageSize })
  return setAdminUsersCache(page, pageSize, res)
}

export const prefetchAdminThreadDetail = async (to) => {
  const id = to.params.id
  const page = 1
  const pageSize = 20
  const cached = getThreadDetailCache(id, page, pageSize)
  if (cached) return cached
  const res = await getThread(id, { page, page_size: pageSize })
  return setThreadDetailCache(id, page, pageSize, res)
}

