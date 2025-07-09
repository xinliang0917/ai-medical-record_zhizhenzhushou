import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // 导入 Element Plus 样式

const app = createApp(App)

app.use(router)
app.use(ElementPlus) // 使用 Element Plus

app.mount('#app')