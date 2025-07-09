<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
// 使用 <script setup> 语法，不需要 export default
// 如果未来有组件级别的逻辑，可以在这里添加
</script>

<style>
/* 全局样式可以放在这里，或者在 main.js 中导入 */
/* 将 #app 的样式应用到 .app-container 或直接 body/html */
html, body, #app { /* 保持 #app 的样式，因为 main.js 挂载在这里 */
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
.app-container { /* 这是 App.vue 自身的根元素，可以给它一些样式 */
  height: 100%; /* 让它撑满 #app */
  width: 100%;
}
</style>