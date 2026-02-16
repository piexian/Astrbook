/**
 * 主题管理工具
 * 支持动态切换主题，便于后续扩展新主题
 */

// 可用主题配置
export const THEMES = {
  dark: {
    key: 'dark',
    name: '现代深色',
    description: '简洁扁平的深色风格，适合长时间阅读',
    icon: 'Moon',
    preview: '#121212',
  },
  light: {
    key: 'light',
    name: '现代浅色',
    description: '清爽明亮的浅色风格',
    icon: 'Sunny',
    preview: '#f5f7fa',
  },
  acid: {
    key: 'acid',
    name: '经典酸性',
    description: '毛玻璃 + 霓虹发光效果',
    icon: 'MagicStick',
    preview: 'linear-gradient(135deg, #b026ff, #00ffff)',
  },
  hub: {
    key: 'hub',
    name: '经典黑橙',
    description: '经典黑橙配色，醒目而不刺眼',
    icon: 'Star',
    preview: 'linear-gradient(135deg, #0b0b0b, #ff9900)',
  },
  // 未来扩展示例：
  // cyberpunk: {
  //   key: 'cyberpunk',
  //   name: '赛博朋克',
  //   description: '高对比度霓虹风格',
  //   icon: 'Monitor',
  //   preview: 'linear-gradient(135deg, #ff0080, #00ff00)',
  // },
}

// 默认主题
export const DEFAULT_THEME = 'dark'

// 本地存储 key
const STORAGE_KEY = 'theme'

/**
 * 获取所有可用主题列表
 * @returns {Array} 主题配置数组
 */
export function getAvailableThemes() {
  return Object.values(THEMES)
}

/**
 * 获取当前主题 key
 * @returns {string} 当前主题 key
 */
export function getCurrentTheme() {
  return localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME
}

/**
 * 获取当前主题配置
 * @returns {Object} 当前主题配置对象
 */
export function getCurrentThemeConfig() {
  const key = getCurrentTheme()
  return THEMES[key] || THEMES[DEFAULT_THEME]
}

/**
 * 设置主题
 * @param {string} themeKey - 主题 key
 * @returns {boolean} 是否设置成功
 */
export function setTheme(themeKey) {
  if (!THEMES[themeKey]) {
    console.warn(`Theme "${themeKey}" not found, falling back to "${DEFAULT_THEME}"`)
    themeKey = DEFAULT_THEME
  }

  // 更新 DOM 属性
  document.documentElement.setAttribute('data-theme', themeKey)
  
  // 持久化存储
  localStorage.setItem(STORAGE_KEY, themeKey)
  
  return true
}

/**
 * 初始化主题（页面加载时调用）
 * 从本地存储读取主题设置并应用
 */
export function initTheme() {
  const savedTheme = getCurrentTheme()
  setTheme(savedTheme)
}

/**
 * 判断当前是否为深色主题
 * @returns {boolean}
 */
export function isDarkTheme() {
  const theme = getCurrentTheme()
  return theme === 'dark' || theme === 'acid' || theme === 'hub'
}

/**
 * 切换到下一个主题（循环切换）
 * @returns {string} 切换后的主题 key
 */
export function toggleNextTheme() {
  const themes = Object.keys(THEMES)
  const currentIndex = themes.indexOf(getCurrentTheme())
  const nextIndex = (currentIndex + 1) % themes.length
  const nextTheme = themes[nextIndex]
  setTheme(nextTheme)
  return nextTheme
}
