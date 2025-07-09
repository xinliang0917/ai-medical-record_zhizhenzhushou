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
            <el-menu-item index="/index">
              <el-icon><Tickets /></el-icon>
              <span>问诊记录</span>
            </el-menu-item>
            <el-menu-item index="/index/settings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main-content">
          <router-view v-if="activeMenu === '/index/settings'"></router-view>
          
          <div v-else>
            <h2 class="page-title">问诊记录列表</h2>
            <el-table :data="consultations" style="width: 100%" class="consultation-table">
              <el-table-column prop="id" label="ID" width="80"></el-table-column>
              <el-table-column prop="patientName" label="患者姓名" width="120"></el-table-column>
              <el-table-column prop="doctorName" label="医生姓名" width="120"></el-table-column>
              <el-table-column prop="date" label="问诊日期" width="180"></el-table-column>
              <el-table-column prop="summary" label="问诊摘要"></el-table-column>
              <el-table-column label="操作" width="100">
                <template #default="scope">
                  <el-button link type="primary" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-pagination
              class="pagination"
              background
              layout="prev, pager, next"
              :total="mockConsultations.length"
              :page-size="pageSize"
              :current-page="currentPage"
              @current-change="handlePageChange"
            ></el-pagination>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <el-dialog
      v-model="dialogVisible"
      width="60%"
      class="consultation-dialog"
      @closed="resetQuantifiedFormEdit"
    >
      <div v-if="selectedConsultation">
        <h3>患者姓名：{{ selectedConsultation.patientName }}</h3>
        <p><strong>医生姓名：</strong>{{ selectedConsultation.doctorName }}</p>
        <p><strong>问诊日期：</strong>{{ selectedConsultation.date }}</p>

        <h4>量化表内容：
          <el-button
            v-if="!isQuantifiedFormEditing"
            link
            type="primary"
            size="small"
            @click="startEditQuantifiedForm"
            style="margin-left: 10px;"
          >
            编辑
          </el-button>
          <span v-else>
            <el-button link type="success" size="small" @click="saveQuantifiedForm">保存</el-button>
            <el-button link type="info" size="small" @click="cancelEditQuantifiedForm">取消</el-button>
          </span>
        </h4>
        <div class="dialog-content">
          <ul v-if="!isQuantifiedFormEditing">
            <li v-for="(value, key) in selectedConsultation.quantifiedForm" :key="key">
              <strong>{{ key }}：</strong>{{ value }}
            </li>
          </ul>
          <div v-else>
            <el-form :model="editableQuantifiedForm" label-width="120px">
              <el-form-item label="诊断">
                <el-input v-model="editableQuantifiedForm.诊断"></el-input>
              </el-form-item>
              <el-form-item label="主诉">
                <el-input type="textarea" v-model="editableQuantifiedForm.主诉"></el-input>
              </el-form-item>
              <el-form-item label="现病史">
                <el-input type="textarea" v-model="editableQuantifiedForm.现病史"></el-input>
              </el-form-item>
              <el-form-item label="既往史">
                <el-input type="textarea" v-model="editableQuantifiedForm.既往史"></el-input>
              </el-form-item>
              <el-form-item label="治疗方案">
                <el-input type="textarea" v-model="editableQuantifiedForm.治疗方案"></el-input>
              </el-form-item>
              <el-form-item label="医嘱">
                <el-input type="textarea" v-model="editableQuantifiedForm.医嘱"></el-input>
              </el-form-item>
              <el-form-item label="复诊建议">
                <el-input v-model="editableQuantifiedForm.复诊建议"></el-input>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <h4>原始对话录音转写：
          <el-button link type="primary" size="small" @click="toggleOriginalTranscript" style="margin-left: 10px;">
            {{ showOriginalTranscript ? '隐藏' : '显示' }}
          </el-button>
        </h4>
        <div v-if="showOriginalTranscript" class="chat-container">
          <ul>
            <li v-for="(message, index) in selectedConsultation.originalTranscript" :key="index"
                :class="['chat-message', message.sender]">
              <span class="sender-label">{{ message.sender === 'doctor' ? '医生' : '患者' }}：</span>
              <div class="message-bubble">
                <p>{{ message.text }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="success" @click="exportQuantifiedFormToExcel(selectedConsultation)">导出量化表 Excel</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, computed, watchEffect, nextTick, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Tickets, Setting } from '@element-plus/icons-vue';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

const router = useRouter();
const route = useRoute();

// 模拟数据 (保持不变)
const mockConsultations = ref([
  {
    id: '001',
    patientName: '张三',
    doctorName: '李医生',
    date: '2025-07-08 10:30',
    summary: '患者张三，男性，50岁，主诉近期头痛、乏力。',
    originalTranscript: [ // 修改为数组
      { sender: 'doctor', text: '您好，张先生，请问您哪里不舒服？' },
      { sender: 'patient', text: '医生您好，我最近头有点痛，还有点乏力。' },
      { sender: 'doctor', text: '头痛持续多久了？伴有其他症状吗？' },
      { sender: 'patient', text: '大概一周了，有时候感觉恶心，但没有呕吐。' }
    ],
    structuredData: { /* ... */ },
    quantifiedForm: { /* ... */ }
  },
  {
    id: '002',
    patientName: '李四',
    doctorName: '王医生',
    date: '2025-07-07 14:00',
    summary: '患者李四，女性，28岁，主诉咳嗽、咽痛。',
    originalTranscript: [ // 修改为数组
      { sender: 'doctor', text: '请问您有什么不适？' },
      { sender: 'patient', text: '我咳嗽两天了，喉咙也很痛。' },
      { sender: 'doctor', text: '有发烧吗？' },
      { sender: 'patient', text: '没有发烧，就是有点流鼻涕。' }
    ],
    structuredData: { /* ... */ },
    quantifiedForm: { /* ... */ }
  },
  {
    id: '003',
    patientName: '王五',
    doctorName: '赵医生',
    date: '2025-07-06 09:15',
    summary: '患者王五，男性，65岁，主诉胸闷、气短。',
    originalTranscript: [ // 修改为数组
      { sender: 'doctor', text: '您好，王大爷，您今天哪里不舒服？' },
      { sender: 'patient', text: '我最近老是胸闷，走几步就气短。' },
      { sender: 'doctor', text: '这种情况持续多久了？有心慌吗？' },
      { sender: 'patient', text: '大概有半个月了，偶尔会感觉心跳加快。' }
    ],
    structuredData: { /* ... */ },
    quantifiedForm: { /* ... */ }
  },
  {
    id: '004',
    patientName: '赵六',
    doctorName: '李医生',
    date: '2025-07-05 11:00',
    summary: '患者赵六，女性，35岁，主诉皮肤瘙痒。',
    originalTranscript: [ // 修改为数组
      { sender: 'doctor', text: '您好，赵女士，请问您有什么问题？' },
      { sender: 'patient', text: '医生，我全身皮肤都很痒，晚上尤其厉害。' },
      { sender: 'doctor', text: '有没有起疹子？' },
      { sender: 'patient', text: '有的，手上和腿上有一些小红疹。' }
    ],
    structuredData: { /* ... */ },
    quantifiedForm: { /* ... */ }
  },
  {
    id: '005',
    patientName: '孙七',
    doctorName: '王医生',
    date: '2025-07-04 16:45',
    summary: '患者孙七，男性，42岁，主诉胃部不适、反酸。',
    originalTranscript: [ // 修改为数组
      { sender: 'doctor', text: '孙先生，您有什么不舒服？' },
      { sender: 'patient', text: '我最近胃老是胀气，还老是反酸水。' },
      { sender: 'doctor', text: '这种情况多久了？饭后症状会加重吗？' },
      { sender: 'patient', text: '大概两周了，吃完饭会更难受。' }
    ],
    structuredData: { /* ... */ },
    quantifiedForm: { /* ... */ }
  }
]);

// // 分页逻辑
const pageSize = 5;
const currentPage = ref(1);

const consultations = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return mockConsultations.value.slice(start, end);
});

onMounted(() => {
  console.log('Consultations data:', consultations.value);
  console.log('mockConsultations data:', mockConsultations.value); // 也打印一下原始模拟数据
});

const handlePageChange = (page) => {
  currentPage.value = page;
};

// // 菜单选择
const activeMenu = computed(() => route.path);

const handleMenuSelect = (key) => {
  console.log('菜单选择:', key);
};

// 动态显示用户名
const displayedUsername = ref(localStorage.getItem('username') || '用户');

watchEffect(() => {
  const usernameFromStorage = localStorage.getItem('username');
  if (usernameFromStorage) {
    displayedUsername.value = usernameFromStorage;
  } else {
    displayedUsername.value = '用户';
  }
  console.log('activeMenu (watchEffect):', activeMenu.value); // 添加这行
});

// // 退出登录
const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  localStorage.removeItem('password'); // 移除本地存储的密码
  ElMessage.success('已退出登录！');
  router.push('/');
};

// 问诊详情对话框
const dialogVisible = ref(false);
const selectedConsultation = ref(null);

// 量化表编辑状态
const isQuantifiedFormEditing = ref(false);
const editableQuantifiedForm = ref({}); // 用于编辑的量化表副本

// 控制原始对话录音转写显示/隐藏的状态
const showOriginalTranscript = ref(false);

const viewDetails = (row) => {
  selectedConsultation.value = row;
  isQuantifiedFormEditing.value = false;
  editableQuantifiedForm.value = JSON.parse(JSON.stringify(row.quantifiedForm));
  showOriginalTranscript.value = false; // 每次打开对话框时默认隐藏原始转写
  dialogVisible.value = true;
};

// 切换原始对话录音转写的显示状态
const toggleOriginalTranscript = () => {
  showOriginalTranscript.value = !showOriginalTranscript.value;
};

// 开始编辑量化表
const startEditQuantifiedForm = () => {
  isQuantifiedFormEditing.value = true;
  editableQuantifiedForm.value = JSON.parse(JSON.stringify(selectedConsultation.value.quantifiedForm));
  nextTick(() => {
    // 可以在这里做一些焦点设置等，如果需要
  });
};

// 保存量化表修改
const saveQuantifiedForm = () => {
  ElMessageBox.confirm('确定要保存量化表修改吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    const index = mockConsultations.value.findIndex(c => c.id === selectedConsultation.value.id);
    if (index !== -1) {
      mockConsultations.value[index].quantifiedForm = { ...editableQuantifiedForm.value };
      selectedConsultation.value.quantifiedForm = { ...editableQuantifiedForm.value };
      ElMessage.success('量化表内容已保存！');
    } else {
      ElMessage.error('未能找到对应的问诊记录。');
    }
    isQuantifiedFormEditing.value = false;
  }).catch(() => {
    ElMessage.info('已取消保存。');
  });
};

// 取消编辑量化表
const cancelEditQuantifiedForm = () => {
  editableQuantifiedForm.value = JSON.parse(JSON.stringify(selectedConsultation.value.quantifiedForm));
  isQuantifiedFormEditing.value = false;
  ElMessage.info('已取消修改。');
};

// 对话框关闭时重置编辑状态
const resetQuantifiedFormEdit = () => {
  isQuantifiedFormEditing.value = false;
  showOriginalTranscript.value = false; // 关闭对话框时也重置原始转写显示状态
};

// 导出量化表 Excel
const exportQuantifiedFormToExcel = (consultation) => {
  if (!consultation || !consultation.quantifiedForm) {
    ElMessage.warning('没有可导出的量化表数据。');
    return;
  }

  const data = [];
  data.push(['项目', '内容']);

  for (const key in consultation.quantifiedForm) {
    if (Object.hasOwnProperty.call(consultation.quantifiedForm, key)) {
      data.push([key, consultation.quantifiedForm[key]]);
    }
  }

  const ws = XLSX.utils.aoa_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, '量化表');

  const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
  saveAs(blob, `${consultation.patientName}_${consultation.date.split(' ')[0]}_量化表.xlsx`);
  ElMessage.success('量化表已导出！');
};
</script>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #409eff; /* Element Plus Primary Color */
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px; /* 固定头部高度 */
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info span {
  margin-right: 15px;
  font-weight: bold; /* 让用户名更突出 */
}

.user-info .el-button {
  color: #fff;
}

.main-container {
  flex: 1;
  display: flex; /* 确保侧边栏和主内容区并排 */
}

.aside {
  background-color: #f4f5f7;
  padding-top: 20px;
}

.el-menu-vertical-demo {
  height: 100%; /* 让菜单填充侧边栏高度 */
}

.main-content {
  flex-grow: 1; /* 主内容区占据剩余空间 */
  padding: 20px;
  background-color: #ffffff;
  overflow-y: auto; /* 允许内容滚动 */
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.consultation-table {
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination {
  justify-content: flex-end; /* 分页器靠右对齐 */
  margin-top: 20px;
}

.consultation-dialog h3 {
  margin-top: 0;
  color: #333;
}

.consultation-dialog h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #555;
  border-bottom: 1px dashed #eee;
  padding-bottom: 5px;
  display: flex; /* 使得标题和按钮在同一行 */
  align-items: center;
}

.dialog-content {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 5px;
  white-space: pre-wrap; /* 保留空白符和换行符 */
  word-break: break-word; /* 允许长单词换行 */
  font-size: 14px;
  line-height: 1.6;
  color: #444;
  max-height: 250px; /* 控制内容高度 */
  overflow-y: auto; /* 内容溢出时滚动 */
}

.dialog-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dialog-content li {
  margin-bottom: 8px;
}

/* 聊天对话框样式 */
.chat-container {
  background-color: #f0f0f0; /* 浅灰色背景，模拟聊天界面 */
  padding: 10px;
  border-radius: 5px;
  overflow-y: auto;
  max-height: 200px; /* 控制聊天记录区域高度 */
}

.chat-message {
  margin-bottom: 10px;
  display: flex; /* 使用 flex 布局 */
  align-items: flex-start; /* 消息泡泡从顶部对齐 */
}

.chat-message.doctor {
  justify-content: flex-start; /* 医生消息靠左 */
}

.chat-message.patient {
  justify-content: flex-end; /* 患者消息靠右 */
}

.sender-label {
  font-weight: bold;
  margin-right: 8px;
  min-width: 40px; /* 确保标签有最小宽度对齐 */
  text-align: right; /* 让标签文字右对齐 */
}

.message-bubble {
  padding: 8px 12px;
  border-radius: 18px; /* 圆角消息泡泡 */
  max-width: 70%; /* 限制消息宽度 */
  word-wrap: break-word; /* 单词过长时换行 */
}

.chat-message.doctor .message-bubble {
  background-color: #e0f7fa; /* 医生消息泡泡颜色 (浅蓝色) */
  color: #263238; /* 文字颜色 */
  margin-right: auto; /* 靠左对齐 */
}

.chat-message.patient .message-bubble {
  background-color: #dcedc8; /* 患者消息泡泡颜色 (浅绿色) */
  color: #212121; /* 文字颜色 */
  margin-left: auto; /* 靠右对齐 */
}

/* 确保 ul 的 margin 和 padding 清零，避免额外的间距 */
.chat-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>