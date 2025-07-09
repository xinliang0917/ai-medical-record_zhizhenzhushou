<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>智诊助手登录</span>
        </div>
      </template>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="verifyCode">
          <div class="verify-code-wrapper">
            <el-input v-model="loginForm.verifyCode" placeholder="请输入验证码" class="verify-code-input"></el-input>
            <VueCanvasVerify ref="canvasVerifyRef" @getCode="handleCodeChange"
                             :width="120" :height="40" class="canvas-verify-code"></VueCanvasVerify>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button @click="handleRegister">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'; // 移除 onMounted, 因为 VueCanvasVerify 不依赖它进行外部控制
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import VueCanvasVerify from '../components/VueCanvasVerify.vue'; // 导入自定义组件

const router = useRouter();
const loginFormRef = ref(null);
const canvasVerifyRef = ref(null); // 引用自定义验证码组件实例

const loginForm = reactive({
  username: '',
  password: '',
  verifyCode: '' // 用户输入的验证码
});

const currentVerifyCode = ref(''); // 存储当前组件生成的验证码

// 验证码组件通过 @getCode 事件将生成的验证码传递过来
const handleCodeChange = (code) => {
  currentVerifyCode.value = code;
  console.log('VueCanvasVerify 通过 @getCode 触发，新验证码:', currentVerifyCode.value);
};

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        console.log('校验中 - 用户输入:', value, ' 小写:', value.toLowerCase());
        console.log('校验中 - 生成验证码:', currentVerifyCode.value, ' 小写:', currentVerifyCode.value.toLowerCase());

        if (!currentVerifyCode.value) {
          // 如果 currentVerifyCode.value 为空，说明验证码没有被正确生成或获取
          callback(new Error('验证码未生成，请刷新页面或检查组件！'));
        } else if (value.toLowerCase() !== currentVerifyCode.value.toLowerCase()) {
          callback(new Error('验证码不正确'));
          loginForm.verifyCode = ''; // 清空输入
          // 注意：VueCanvasVerify 似乎没有外部刷新的方法，需要用户点击组件本身或者重新加载页面
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
};

// ... 在 handleLogin 方法内部
const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      if (loginForm.username === '111' && loginForm.password === '123456') { // 模拟固定用户
        ElMessage.success('登录成功！');
        localStorage.setItem('token', 'test_token'); // 存储模拟 token
        localStorage.setItem('username', loginForm.username); // <-- 新增：存储用户名
        router.push('/index');
      } else {
        ElMessage.error('用户名或密码错误！');
        loginForm.verifyCode = ''; // 清空验证码输入
      }
    } else {
      ElMessage.error('请检查输入信息！');
      if (loginForm.verifyCode && currentVerifyCode.value && loginForm.verifyCode.toLowerCase() !== currentVerifyCode.value.toLowerCase()) {
         loginForm.verifyCode = '';
      }
      return false;
    }
  });
};

const handleRegister = () => {
  ElMessage.info('请联系管理员进行注册或访问注册页面');
  console.log('跳转到注册页面或显示注册表单');
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}
.login-card {
  width: 400px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}
.verify-code-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}
.verify-code-input {
  flex-grow: 1;
}
/* 自定义验证码组件的样式 */
.canvas-verify-code {
  width: 120px; /* 验证码图片宽度 */
  height: 40px; /* 验证码图片高度 */
  cursor: pointer; /* 表示可点击刷新 */
  border: 1px solid #dcdfe6; /* 可选的边框，使其更明显 */
  border-radius: 4px; /* 可选的圆角 */
  background-color: #f5f5f5; /* 添加背景色，确保可见 */
}
</style>