<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header">
        <div class="logo">智诊助手 AI 医疗病历自动化系统</div>
        <div class="user-info">
          <!-- “欢迎，xxx！”保持在顶部最右侧 -->
          <span class="user-welcome-text">欢迎，{{ displayedUsername }}！</span>
          <!-- 退出登录按钮已移动到侧边栏底部 -->
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
          <!-- 退出登录按钮移动到侧边栏底部 -->
          <div class="logout-container">
            <el-button type="info" @click="handleLogout" class="logout-button">退出登录</el-button>
          </div>
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
  height: 100%;
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
  /* 确保 logo 垂直居中 */
  line-height: 60px; /* 与 header 高度一致 */
}

.user-info {
  display: flex;
  align-items: center; /* 确保内容垂直居中对齐 */
  /* vertical-align: middle; /* 移除此行，因为 flexbox 的 align-items 已经处理 */
  gap: 15px;
}

.user-welcome-text {
  /* 调整字体大小和行高，使其与 logo 对齐 */
  font-size: 16px; /* 调整字体大小 */
  line-height: 16px; 
  color: white; /* 确保颜色一致 */
}

/* 移除 .user-info .el-button 的样式，因为它已不再这里 */

.main-container {
  flex: 1;
}

.aside {
  background-color: #f4f5f7;
  padding-top: 20px;
  border-right: 1px solid #ebeef5;
  display: flex; /* 使用 flex 布局 */
  flex-direction: column; /* 垂直排列子元素 */
  justify-content: space-between; /* 将菜单和退出按钮推到两端 */
}

.el-menu-vertical-demo {
  border-right: none; /* 移除 ElMenu 默认的右边框 */
  flex-grow: 1; /* 让菜单占据可用空间 */
}

/* 确保导航栏图标和文字对齐 */
.el-menu-vertical-demo .el-menu-item {
  display: flex;
  align-items: center; /* 确保图标和文字垂直居中对齐 */
  height: 50px; /* 增加菜单项高度，提供更多垂直空间 */
}

.el-menu-vertical-demo .el-menu-item .el-icon {
  margin-right: 8px; /* 增加图标和文字之间的间距 */
  /* 确保图标垂直居中 */
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-menu-vertical-demo .el-menu-item span {
  /* 确保文字垂直居中 */
  display: flex;
  align-items: center;
  height: 100%; /* 让 span 占满菜单项高度，辅助对齐 */
}

.logout-container {
  padding: 20px; /* 为按钮提供内边距 */
  border-top: 1px solid #ebeef5; /* 添加顶部边框，与菜单项分隔 */
  text-align: center; /* 按钮居中 */
}

.logout-button {
  width: 100%; /* 按钮宽度占满容器 */
  background-color: #409eff; /* 设置与顶部栏相同的背景色 */
  border-color: #409eff; /* 确保边框颜色也一致 */
  color: white; /* 确保文字颜色为白色 */
}
/* 覆盖 ElButton 默认的 hover/active 样式，确保颜色一致性 */
.logout-button:hover,
.logout-button:focus {
  background-color: #66b1ff; /* Element Plus primary 类型的 hover 色 */
  border-color: #66b1ff;
  color: white;
}
.logout-button:active {
  background-color: #3a8ee6; /* Element Plus primary 类型的 active 色 */
  border-color: #3a8ee6;
  color: white;
}


.main-content {
  padding: 20px;
  background-color: #ffffff;
  /* 确保 main-content 能够占据剩余空间，且其内容由 router-view 管理 */
}

/* 定义统一的页面标题样式 */
.main-content .page-title {
  font-size: 24px; /* 统一页面标题大小 */
  font-weight: bold;
  color: #333;
  margin-top: 0px; /* 确保与 main-content 的 padding-top 对齐 */
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}
</style>
