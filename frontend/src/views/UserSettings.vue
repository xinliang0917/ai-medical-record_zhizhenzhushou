<template>
  <div class="settings-container">
    <h2 class="page-title">用户设置</h2>

    <!-- 重新添加 el-card 组件 -->
    <el-card class="setting-card">
      <template #header>
        <div class="card-header">修改个人信息</div>
      </template>
      <el-form :model="userSettingsForm" :rules="rules" ref="settingsFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userSettingsForm.username" placeholder="请输入新用户名"></el-input>
        </el-form-item>
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input type="password" v-model="userSettingsForm.oldPassword" placeholder="请输入旧密码"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="userSettingsForm.newPassword" placeholder="请输入新密码"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmNewPassword">
          <el-input type="password" v-model="userSettingsForm.confirmNewPassword" placeholder="请再次输入新密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmitSettings">保存修改</el-button>
          <el-button @click="handleResetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
// import { useRouter } from 'vue-router';

// const router = useRouter();
const settingsFormRef = ref(null);

// 模拟当前用户信息（从 localStorage 获取或模拟）
const currentUsername = ref(localStorage.getItem('username') || '医生');
const currentPassword = ref('123456'); // 模拟的旧密码，实际不应该这样存储在前端

const userSettingsForm = reactive({
  username: currentUsername.value,
  oldPassword: '',
  newPassword: '',
  confirmNewPassword: ''
});

// 密码确认验证规则
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'));
  } else if (value !== userSettingsForm.newPassword) {
    callback(new Error('两次输入的密码不一致！'));
  } else {
    callback();
  }
};

const rules = {
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
  ],
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmNewPassword: [
    { required: true, validator: validatePass, trigger: 'blur' }
  ]
};

// 提交设置
const handleSubmitSettings = () => {
  settingsFormRef.value.validate((valid) => {
    if (valid) {
      if (userSettingsForm.oldPassword !== currentPassword.value) {
        ElMessage.error('旧密码不正确，请重新输入！');
        return;
      }

      // 模拟修改成功
      currentUsername.value = userSettingsForm.username;
      currentPassword.value = userSettingsForm.newPassword; // 模拟更新密码
      localStorage.setItem('username', userSettingsForm.username); // 模拟保存新用户名

      ElMessage.success('用户信息修改成功！');
      // 模拟清空密码字段
      userSettingsForm.oldPassword = '';
      userSettingsForm.newPassword = '';
      userSettingsForm.confirmNewPassword = '';

      // 在实际项目中，这里会调用后端 API 发送修改请求
    } else {
      ElMessage.error('请检查输入信息！');
      return false;
    }
  });
};

// 重置表单
const handleResetForm = () => {
  settingsFormRef.value.resetFields();
  userSettingsForm.username = currentUsername.value; // 重置用户名回当前值
};

// 组件加载时设置初始用户名
onMounted(() => {
  userSettingsForm.username = currentUsername.value;
});
</script>

<style scoped>
.settings-container {
  padding-top: 0px; /* 移除 padding，让 main-content 的 padding 生效 */
  background-color: transparent; 
  /* 移除 min-height 属性，让其自然适应父容器高度 */
  /* min-height: calc(100vh - 60px - 20px); */ 
}


.page-title {
  font-size: 24px; /* 统一页面标题大小 */
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.setting-card { /* 重新添加 el-card 的样式 */
  max-width: 100%; 
  margin-bottom: 20px;
  /* 恢复 el-card 默认的背景色、阴影和边框 */
  background-color: #ffffff; /* 默认白色背景 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 默认阴影 */
  border: 1px solid #ebeef5; /* 默认边框 */
  border-radius: 4px; /* 默认圆角 */
  padding: 20px; /* el-card 默认有 padding，这里可以根据需要调整 */
}

/* 移除 .setting-content 容器，因为 el-card 已经包裹了内容 */
/* .setting-content { 
  max-width: 100%; 
  margin-bottom: 20px;
  background-color: transparent;
  box-shadow: none;
  border: none;
} */

.card-header { /* 修改个人信息这个标题 */
  font-size: 18px;
  font-weight: bold;
  padding-bottom: 10px;
}

/* 确保表单项内的输入框能占据可用宽度 */
.el-form-item {
  width: 100%; /* 让表单项占满父容器宽度 */
}
.el-form-item .el-input {
  width: 100%; /* 让输入框占满表单项的可用宽度 */
}
</style>
