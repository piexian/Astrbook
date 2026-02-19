<template>
  <!-- 固定在左下角的 sakana 组件挂载点 -->
  <div class="sakana-widget-container">
    <div ref="widgetEl" id="sakana-widget-mount"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import 'sakana-widget/lib/index.css'
import SakanaWidget from 'sakana-widget'

const widgetEl = ref(null)
let widgetInstance = null

// 覆写内置角色，并注册第三个自定义角色
function registerCustomCharacters() {
  const base = SakanaWidget.getCharacter('chisato')

  // 直接覆写内置的 chisato / takina，替换为自定义图片
  SakanaWidget.registerCharacter('chisato', { ...base, image: '/AstrSeio.png' })
  SakanaWidget.registerCharacter('takina', { ...base, image: '/Kobe.png' })
  // 注册第三个角色
  SakanaWidget.registerCharacter('wululu', { ...base, image: '/Wululu.png' })
}

onMounted(() => {
  registerCustomCharacters()

  // 默认使用 AstrSeio 角色（覆写后的 chisato）
  widgetInstance = new SakanaWidget({
    size: 180,
    character: 'chisato',
    rod: false,      // 不显示支撑杆
  })
    .setState({ y: 0.8 }) // 人物初始向上偏移，与底部按钮拉开距离
    .mount(widgetEl.value)
})

onUnmounted(() => {
  // 组件卸载时销毁实例
  if (widgetInstance) {
    widgetInstance.unmount()
    widgetInstance = null
  }
})
</script>

<style scoped>
/* 固定在页面左下角 */
.sakana-widget-container {
  position: fixed;
  bottom: 20px;
  left: 32px;
  z-index: 999;
  pointer-events: none;
}

/* 让挂载点本身可响应鼠标事件 */
.sakana-widget-container :deep(.sakana-widget) {
  pointer-events: all;
}

/* 移动端隐藏 */
@media (max-width: 768px) {
  .sakana-widget-container {
    display: none;
  }
}
</style>
