<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

// 配置 marked
marked.setOptions({
  breaks: true,  // 支持换行
  gfm: true      // 支持 GitHub Flavored Markdown
})

// 渲染并净化 HTML
const renderedContent = computed(() => {
  if (!props.content) return ''
  const html = marked.parse(props.content)
  return DOMPurify.sanitize(html)
})
</script>

<style lang="scss">
.markdown-content {
  line-height: 1.8;
  word-wrap: break-word;
  
  h1, h2, h3, h4, h5, h6 {
    margin: 16px 0 8px;
    font-weight: 600;
    line-height: 1.4;
  }
  
  h1 { font-size: 1.5em; }
  h2 { font-size: 1.3em; }
  h3 { font-size: 1.2em; }
  
  p {
    margin: 8px 0;
  }
  
  a {
    color: #409EFF;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  code {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 2px 6px;
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
    font-size: 0.9em;
    color: var(--acid-green);
  }
  
  pre {
    background: #050507;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 14px 16px;
    border-radius: 12px;
    overflow: auto;
    margin: 14px 0;
    
    code {
      background: none;
      padding: 0;
      color: rgba(255, 255, 255, 0.9);
      display: block;
      line-height: 1.6;
    }
  }
  
  blockquote {
    border-left: 4px solid #dcdfe6;
    padding-left: 16px;
    margin: 12px 0;
    color: #909399;
  }
  
  ul, ol {
    padding-left: 24px;
    margin: 8px 0;
    
    li {
      margin: 4px 0;
    }
  }
  
  img {
    max-width: 100%;
    max-height: 500px; // 限制最大高度
    width: auto;
    height: auto;
    border-radius: 12px;
    margin: 16px 0;
    display: block;
    object-fit: contain; // 保持图片比例
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    
    &:hover {
      transform: scale(1.02);
      box-shadow: 0 8px 30px rgba(176, 38, 255, 0.3);
    }
  }
  
  // 移动端图片适配
  @media (max-width: 768px) {
    img {
      max-height: 400px;
      border-radius: 8px;
    }
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    
    th, td {
      border: 1px solid #dcdfe6;
      padding: 8px 12px;
      text-align: left;
    }
    
    th {
      background: #f5f7fa;
      font-weight: 600;
    }
  }
  
  hr {
    border: none;
    border-top: 1px solid #dcdfe6;
    margin: 16px 0;
  }
}
</style>
