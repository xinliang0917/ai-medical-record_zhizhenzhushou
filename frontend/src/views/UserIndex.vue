<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header">
        <div class="logo">智诊助手 AI 医疗病历自动化系统</div>
        <div class="user-info">
          <span>欢迎，{{ displayedUsername }}！</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-container class="main-container">
        <el-aside width="200px" class="aside">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            @select="handleMenuSelect"
            router
          >
            <el-menu-item index="/index"> <el-icon><Tickets /></el-icon>
              <span>问诊记录</span>
            </el-menu-item>
            <el-menu-item index="/index/speech-to-text"> 
              <el-icon><Microphone /></el-icon> 
              <span>语音转文字</span>
            </el-menu-item>
            <el-menu-item index="/index/settings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main-content">
          <router-view></router-view> 
        </el-main>
      </el-container>
    </el-container>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Tickets, Setting, Microphone } from '@element-plus/icons-vue'; // 确保导入 Microphone

const router = useRouter();
const route = useRoute(); // 用于获取当前路由信息

const displayedUsername = ref('');

// 确保 activeMenu 正确反映当前路由
const activeMenu = computed(() => route.path);

onMounted(() => {
  displayedUsername.value = localStorage.getItem('username') || '用户';
});

// const handleMenuSelect = (index) => {
  // router.push(index) 已经由 el-menu 的 router 属性处理，这里可以移除或用于其他逻辑
  // activeMenu.value = index; // 这一行现在通过 computed 属性自动更新
// };

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  router.push('/');
};
</script>

<style scoped>
.common-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #409eff;
  color: white;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info .el-button {
  color: white;
}

.main-container {
  flex: 1;
}

.aside {
  background-color: #f4f5f7;
  padding-top: 20px;
  border-right: 1px solid #ebeef5;
}

.el-menu-vertical-demo {
  border-right: none; /* 移除 ElMenu 默认的右边框 */
}

.main-content {
  padding: 20px;
  background-color: #ffffff;
  /* 确保 main-content 能够占据剩余空间，且其内容由 router-view 管理 */
}

/* 移除原有的问诊记录列表样式，因为它们现在在 ConsultationList.vue 中 */
</style>