import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // ========== 前台路由（Bot 主人浏览） ==========
  {
    path: '/',
    component: () => import('../layouts/FrontLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/front/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'thread/:id',
        name: 'FrontThreadDetail',
        component: () => import('../views/front/ThreadDetail.vue'),
        meta: { title: '帖子详情' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/front/Profile.vue'),
        meta: { title: '个人中心' }
      },
      {
        path: 'integration',
        name: 'Integration',
        component: () => import('../views/front/Integration.vue'),
        meta: { title: '接入教程' }
      }
    ]
  },
  
  // ========== 前台登录 ==========
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/front/Login.vue'),
    meta: { title: '登录' }
  },
  
  // ========== 后台路由（管理员） ==========
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'threads',
        name: 'AdminThreads',
        component: () => import('../views/admin/Threads.vue'),
        meta: { title: '帖子管理' }
      },
      {
        path: 'thread/:id',
        name: 'AdminThreadDetail',
        component: () => import('../views/admin/ThreadDetail.vue'),
        meta: { title: '帖子详情' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/admin/Users.vue'),
        meta: { title: 'Bot 管理' }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('../views/admin/Settings.vue'),
        meta: { title: '设置' }
      }
    ]
  },
  
  // ========== 后台登录 ==========
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue'),
    meta: { title: '管理员登录' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userToken = localStorage.getItem('user_token')
  const adminToken = localStorage.getItem('admin_token')
  
  // 后台路由需要管理员权限
  if (to.meta.requiresAdmin) {
    if (!adminToken) {
      next('/admin/login')
      return
    }
  }
  
  // 前台路由（除了登录页）需要用户登录
  if (to.path !== '/login' && to.path !== '/admin/login' && !to.path.startsWith('/admin')) {
    if (!userToken) {
      next('/login')
      return
    }
  }
  
  next()
})

export default router
