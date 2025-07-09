import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/UserLogin.vue'
import Index from '../views/UserIndex.vue' 
import UserSettings from '../views/UserSettings.vue'
const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/index',
    name: 'Index',
    component: Index,
    meta: { requiresAuth: true }, // 标记需要认证
    children: [ // 添加子路由
      {
        path: 'settings', 
        name: 'UserSettings',
        component: UserSettings
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.NODE_ENV === 'production' ? '/ai-medical-record_zhizhenzhushou/' : '/'), // 注意这里的 publicPath
  routes
});

// 可选：添加路由守卫，实现未登录重定向
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.path !== '/' && !token) { // 如果不是登录页且没有token
    next('/'); // 重定向到登录页
  } else if (to.path === '/' && token) { // 如果已登录且尝试访问登录页
    next('/index'); // 重定向到主页
  } else {
    next(); // 正常放行
  }
});

export default router