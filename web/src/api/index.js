import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器 - 添加 token
api.interceptors.request.use(config => {
  // 根据当前路由或上下文判断使用哪个 Token
  // 这里简单处理：如果是 /admin 开头的请求，使用 admin_token
  // 否则使用 user_token
  
  let token = null
  if (config.url.startsWith('/admin')) {
    token = localStorage.getItem('admin_token')
  } else {
    token = localStorage.getItem('user_token')
  }
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ========== 认证 API ==========
export const getCurrentUser = () => api.get('/auth/me')
export const userLogin = (data) => 
  api.post('/auth/login', data)
export const registerUser = (data) => api.post('/auth/register', data)
export const updateProfile = (data) => api.put('/auth/profile', data)
export const refreshBotToken = () => api.post('/auth/refresh-token')
export const changeUserPassword = (oldPassword, newPassword) => 
  api.post('/auth/change-password', { old_password: oldPassword, new_password: newPassword })

// ========== 上传 API ==========
export const uploadAvatar = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// ========== 管理员 API ==========
export const adminLogin = (username, password) => 
  api.post('/admin/login', { username, password })
export const getAdminInfo = () => api.get('/admin/me')

// ========== 统计 API ==========
export const getStats = () => api.get('/admin/stats')

// ========== 用户 API (管理员) ==========
export const getUsers = (params) => api.get('/admin/users', { params })
export const adminDeleteUser = (id) => api.delete(`/admin/users/${id}`)

// ========== 帖子 API ==========
export const getThreads = (params) => api.get('/threads', { params: { ...params, format: 'json' } })
export const getThread = (id, params) => api.get(`/threads/${id}`, { params: { ...params, format: 'json' } })
export const adminDeleteThread = (id) => api.delete(`/admin/threads/${id}`)

// ========== 回复 API ==========
export const getSubReplies = (replyId, params) => api.get(`/replies/${replyId}/sub_replies`, { params: { ...params, format: 'json' } })

export default api
