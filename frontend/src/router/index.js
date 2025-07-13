import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../views/UserLogin.vue';
import UserIndex from '../views/UserIndex.vue';
import UserSettings from '../views/UserSettings.vue';
import SpeechToText from '../views/SpeechToText.vue'; 
import ConsultationList from '../views/ConsultationList.vue'; // 导入新的问诊列表组件

const routes = [
  {
    path: '/',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/index',
    name: 'UserIndex', // 父路由，用于渲染侧边栏和顶部栏
    component: UserIndex,
    children: [
      {
        path: '', // 默认子路由，访问 /index 时显示
        name: 'ConsultationList',
        component: ConsultationList
      },
      {
        path: 'settings', // 访问路径为 /index/settings
        name: 'UserSettings',
        component: UserSettings
      },
      {
        path: 'speech-to-text', // 访问路径为 /index/speech-to-text
        name: 'SpeechToText',
        component: SpeechToText
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(process.env.NODE_ENV === 'production' ? '/ai-medical-record_zhizhenzhoushou/' : '/'), 
  routes
});

// 导航守卫 (保持不变)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
  } else if (to.name === 'Login' && token) { // 如果已登录且尝试访问登录页
    next({ name: 'ConsultationList' }); // 重定向到问诊记录列表页
  } else {
    next();
  }
});

export default router;