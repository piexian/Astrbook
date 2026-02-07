import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 默认深色模式 (true)
  const isDark = ref(localStorage.getItem('theme') !== 'light')

  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  const applyTheme = () => {
    const html = document.documentElement
    if (isDark.value) {
      html.classList.remove('light')
      html.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      html.classList.remove('dark')
      html.classList.add('light')
      localStorage.setItem('theme', 'light')
    }
  }

  // 监听变化并应用
  watch(isDark, applyTheme, { immediate: true })

  return {
    isDark,
    toggleTheme
  }
})
