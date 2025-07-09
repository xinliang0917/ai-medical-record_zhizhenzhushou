import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/UserLogin.vue'
import Index from '../views/UserIndex.vue' // 稍后创建的主页
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
  history: createWebHistory(),
  routes
})

// 路由守卫：检查是否登录
router.beforeEach((to, from, next) => {
  // 假设我们用 localStorage 存储一个简单的 token 来模拟登录状态
  const isAuthenticated = localStorage.getItem('token');

  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果目标路由需要认证但用户未登录，则重定向到登录页
    // 在实际项目中，登录成功后会将 token 存入 localStorage
    // 这里为了演示，我们先放行 index 路由，或者你可以手动在浏览器控制台设置 localStorage.setItem('token', 'some_token');
    console.log('需要登录才能访问此页面！');
    // next('/'); // 暂时注释，方便测试，实际应该重定向到登录页
    next(); // 暂时放行，以便调试主页
  } else {
    next(); // 正常跳转
  }
});

export default router