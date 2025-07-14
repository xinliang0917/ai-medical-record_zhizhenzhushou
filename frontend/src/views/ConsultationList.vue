<template>
  <div>
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

    <!-- 分页组件放在右下角固定位置 -->
    <div class="pagination-container">
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

    <el-dialog
      v-model="dialogVisible"
      :show-close="true"
      width="70%" class="consultation-dialog"
      @closed="resetQuantifiedFormEdit"
    >
      <div v-if="selectedConsultation">
        <h3 style="margin-top: 0;">患者姓名：{{ selectedConsultation.patientName }}</h3>
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
              <strong>{{ key }}：</strong>
              <span v-if="typeof value === 'object' && value !== null">
                <ul>
                  <li v-for="(subValue, subKey) in value" :key="subKey">
                    <strong style="margin-left: 15px;">{{ subKey }}：</strong>{{ subValue }}
                  </li>
                </ul>
              </span>
              <span v-else>{{ value }}</span>
            </li>
          </ul>
          <div v-else>
            <el-form :model="editableQuantifiedForm" label-width="120px">
              <el-form-item label="患者姓名">
                <el-input v-model="editableQuantifiedForm.基本信息.患者姓名"></el-input>
              </el-form-item>
              <el-form-item label="性别">
                <el-input v-model="editableQuantifiedForm.基本信息.性别"></el-input>
              </el-form-item>
              <el-form-item label="年龄">
                <el-input v-model="editableQuantifiedForm.基本信息.年龄"></el-input>
              </el-form-item>
              <el-form-item label="就诊日期">
                <el-input v-model="editableQuantifiedForm.基本信息.就诊日期"></el-input>
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
              <el-form-item label="个人史">
                <el-input type="textarea" v-model="editableQuantifiedForm.个人史"></el-input>
              </el-form-item>
              <el-form-item label="家族史">
                <el-input type="textarea" v-model="editableQuantifiedForm.家族史"></el-input>
              </el-form-item>
              <el-form-item label="体温">
                <el-input v-model="editableQuantifiedForm.体格检查.体温"></el-input>
              </el-form-item>
              <el-form-item label="脉搏">
                <el-input v-model="editableQuantifiedForm.体格检查.脉搏"></el-input>
              </el-form-item>
              <el-form-item label="呼吸">
                <el-input v-model="editableQuantifiedForm.体格检查.呼吸"></el-input>
              </el-form-item>
              <el-form-item label="血压">
                <el-input v-model="editableQuantifiedForm.体格检查.血压"></el-input>
              </el-form-item>
              <el-form-item label="一般情况">
                <el-input type="textarea" v-model="editableQuantifiedForm.体格检查.一般情况"></el-input>
              </el-form-item>
              <el-form-item label="专科检查">
                <el-input type="textarea" v-model="editableQuantifiedForm.体格检查.专科检查"></el-input>
              </el-form-item>
              <el-form-item label="辅助检查">
                <el-input type="textarea" v-model="editableQuantifiedForm.辅助检查"></el-input>
              </el-form-item>
              <el-form-item label="初步诊断">
                <el-input v-model="editableQuantifiedForm.初步诊断"></el-input>
              </el-form-item>
              <el-form-item label="鉴别诊断">
                <el-input v-model="editableQuantifiedForm.鉴别诊断"></el-input>
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
import { ref, computed } from 'vue';
// import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import * as XLSX from 'xlsx'; // 导入 XLSX 库 

// 导入 Element Plus 图标 (保持不变)
// import { Tickets, Setting } from '@element-plus/icons-vue';

// 模拟数据 (需要更新，使其与后端新格式匹配)
const mockConsultations = ref([
  {
    id: '001',
    patientName: '张三',
    doctorName: '李医生',
    date: '2025-07-08 10:30',
    summary: '患者张三，男性，50岁，主诉近期头痛、乏力。初步诊断：偏头痛可能性大。',
    originalTranscript: [
      { sender: 'doctor', text: '您好，请问您哪里不舒服？' },
      { sender: 'patient', text: '医生，我最近总是头痛，而且感觉很乏力。' },
      { sender: 'doctor', text: '头痛多久了？有什么伴随症状吗？' },
      { sender: 'patient', text: '大概有一个星期了，有时候会觉得恶心，但是没有吐。' }
    ],
    quantifiedForm: {
      "基本信息": {
        "患者姓名": "张三",
        "性别": "男",
        "年龄": "50岁",
        "就诊日期": "2025-07-08 10:30"
      },
      "主诉": "患者主诉头部搏动性疼痛，伴恶心、畏光。",
      "现病史": "头痛一周，呈间歇性发作，每次持续数小时，常伴有恶心感，对光线敏感。无发热，无咳嗽。",
      "既往史": "无特殊既往史。",
      "个人史": "无不良嗜好。",
      "家族史": "否认家族遗传病史。",
      "体格检查": {
        "体温": "36.8°C",
        "脉搏": "80次/分",
        "呼吸": "18次/分",
        "血压": "120/80mmHg",
        "一般情况": "神志清楚，精神可。",
        "专科检查": "神经系统检查未见明显异常。"
      },
      "辅助检查": "暂无。",
      "初步诊断": "偏头痛可能性大",
      "鉴别诊断": "紧张性头痛",
      "治疗方案": "建议口服布洛芬，注意休息，避免诱发因素，如熬夜、压力等。",
      "医嘱": "保持规律作息，清淡饮食，避免咖啡因和酒精。头痛发作时可适当休息，放松心情。",
      "复诊建议": "若症状无缓解或加重，请及时复诊。"
    }
  },
  {
    id: '002',
    patientName: '李四',
    doctorName: '王医生',
    date: '2025-07-07 14:00',
    summary: '患者李四，女性，30岁，主诉咳嗽、咽痛。初步诊断：急性上呼吸道感染。',
    originalTranscript: [
      { sender: 'doctor', text: '您好，请问您今天看什么病？' },
      { sender: 'patient', text: '医生，我咳嗽两天了，喉咙也很痛。' },
      { sender: 'doctor', text: '有发烧吗？痰多不多？' },
      { sender: 'patient', text: '没有发烧，痰有点多，黄色的。' }
    ],
    quantifiedForm: {
      "基本信息": {
        "患者姓名": "李四",
        "性别": "女",
        "年龄": "30岁",
        "就诊日期": "2025-07-07 14:00"
      },
      "主诉": "患者主诉咳嗽伴咽喉疼痛两天。",
      "现病史": "两天前无明显诱因出现咳嗽，咳少量白痰，咽部疼痛不适，无发热、流涕等。今日痰色转黄。",
      "既往史": "否认慢性病史，无特殊药物过敏史。",
      "个人史": "无烟酒嗜好。",
      "家族史": "无特殊家族病史。",
      "体格检查": {
        "体温": "37.2°C",
        "脉搏": "75次/分",
        "呼吸": "16次/分",
        "血压": "110/70mmHg",
        "一般情况": "精神尚可。",
        "专科检查": "咽部充血，扁桃体无肿大。"
      },
      "辅助检查": "血常规待查。",
      "初步诊断": "急性上呼吸道感染",
      "鉴别诊断": "急性咽炎，急性支气管炎",
      "治疗方案": "建议口服抗生素（如阿莫西林）和清热解毒口服液，同时进行对症治疗。",
      "医嘱": "多饮温水，饮食清淡，避免辛辣刺激食物。注意休息，避免劳累。戴口罩，防止交叉感染。",
      "复诊建议": "若症状加重或出现高热，请及时复诊。"
    }
  },
  {
    id: '003',
    patientName: '王五',
    doctorName: '赵医生',
    date: '2025-07-06 09:15',
    summary: '患者王五，男性，60岁，主诉胸闷、气短。初步诊断：冠心病待查。',
    originalTranscript: [
      { sender: 'doctor', text: '您好，有什么不舒服？' },
      { sender: 'patient', text: '医生，我最近老是觉得胸闷，有时候会喘不上气。' },
      { sender: 'doctor', text: '这种情况持续多久了？是在活动后加重吗？' },
      { sender: 'patient', text: '大概半个月了，活动后会更明显。' }
    ],
    quantifiedForm: {
      "基本信息": {
        "患者姓名": "王五",
        "性别": "男",
        "年龄": "60岁",
        "就诊日期": "2025-07-06 09:15"
      },
      "主诉": "患者主诉近半月出现胸闷、气短，活动后加重。",
      "现病史": "患者半个月前开始出现胸闷、气短症状，休息可缓解，无胸痛、心悸等不适。今日症状无明显缓解。",
      "既往史": "高血压病史10年，规律服用降压药。",
      "个人史": "吸烟史20年，已戒烟5年。",
      "家族史": "父亲有冠心病史。",
      "体格检查": {
        "体温": "36.5°C",
        "脉搏": "70次/分",
        "呼吸": "16次/分",
        "血压": "135/85mmHg",
        "一般情况": "神志清楚，无明显痛苦面容。",
        "专科检查": "心肺听诊未闻及明显异常。"
      },
      "辅助检查": "建议行心电图、心脏彩超、心肌酶谱检查。",
      "初步诊断": "冠心病待查",
      "鉴别诊断": "心功能不全，肺部疾病",
      "治疗方案": "建议完善相关检查以明确诊断，同时给予对症治疗，如吸氧、硝酸甘油等。",
      "医嘱": "清淡饮食，低盐低脂。保持情绪稳定，避免剧烈运动。监测血压，按时服用降压药。戒烟限酒。",
      "复诊建议": "完善检查后请及时复诊，以便明确诊断并调整治疗方案。"
    }
  }
]);

// 分页逻辑 (保持不变)
const pageSize = 5;
const currentPage = ref(1);
const consultations = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return mockConsultations.value.slice(start, end);
});

const handlePageChange = (page) => {
  currentPage.value = page;
};

// 详情对话框 (保持不变)
const dialogVisible = ref(false);
const selectedConsultation = ref(null);
const showOriginalTranscript = ref(false);

const viewDetails = (row) => {
  selectedConsultation.value = row;
  dialogVisible.value = true;
  showOriginalTranscript.value = false;
};

const toggleOriginalTranscript = () => {
  showOriginalTranscript.value = !showOriginalTranscript.value;
};

// 量化表编辑逻辑
const isQuantifiedFormEditing = ref(false);
const editableQuantifiedForm = ref({}); // 用于编辑的量化表数据

const startEditQuantifiedForm = () => {
  if (selectedConsultation.value && selectedConsultation.value.quantifiedForm) {
    // 进行深拷贝，确保修改editableQuantifiedForm不会影响selectedConsultation
    editableQuantifiedForm.value = JSON.parse(JSON.stringify(selectedConsultation.value.quantifiedForm));
    isQuantifiedFormEditing.value = true;
  }
};

const saveQuantifiedForm = () => {
  if (selectedConsultation.value) {
    // 实际项目中，这里会发送请求到后端保存修改
    // 将 editableQuantifiedForm 的值赋值回 selectedConsultation
    selectedConsultation.value.quantifiedForm = JSON.parse(JSON.stringify(editableQuantifiedForm.value));
    isQuantifiedFormEditing.value = false;
    ElMessage.success('量化表修改已保存（模拟）！');
  }
};

const cancelEditQuantifiedForm = () => {
  isQuantifiedFormEditing.value = false;
  editableQuantifiedForm.value = {}; // 清空编辑数据
};

const resetQuantifiedFormEdit = () => {
  isQuantifiedFormEditing.value = false;
  editableQuantifiedForm.value = {};
};

// 导出 Excel 功能
const exportQuantifiedFormToExcel = (consultation) => {
  if (!consultation || !consultation.quantifiedForm) {
    ElMessage.error('没有量化表数据可以导出！');
    return;
  }

  const data = [];
  data.push(['字段', '内容']); // 表头

  // 辅助函数：展平嵌套对象
  const flattenObject = (obj, parentKey = '') => {
    for (const key in obj) {
      if (Object.hasOwnProperty.call(obj, key)) {
        const currentKey = parentKey ? `${parentKey}.${key}` : key;
        if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
          // 如果是嵌套对象，递归调用
          flattenObject(obj[key], currentKey);
        } else {
          // 否则直接添加
          data.push([currentKey, obj[key]]);
        }
      }
    }
  };

  flattenObject(consultation.quantifiedForm);

  const ws = XLSX.utils.aoa_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "量化表");

  const patientName = consultation.patientName || '未知患者';
  const date = consultation.date ? consultation.date.split(' ')[0] : '未知日期';
  const filename = `${patientName}_${date}_量化表.xlsx`;
  XLSX.writeFile(wb, filename);
  ElMessage.success('量化表已成功导出！');
};
</script>

<style scoped>
/* 样式与之前保持一致 */
.page-title {
  color: #333;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.consultation-table {
  margin-bottom: 20px;
}

.pagination-container {
  position: fixed; /* 固定定位 */
  bottom: 20px; /* 距离底部20px */
  right: 20px; /* 距离右侧20px */
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1); /* 添加阴影，使其更突出 */
  z-index: 1000; /* 确保在其他内容之上 */
}

.consultation-dialog .el-dialog__header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.consultation-dialog h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 10px;
}

.consultation-dialog p {
  margin-bottom: 8px;
  color: #666;
}

.consultation-dialog h4 {
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #ddd;
  padding-bottom: 5px;
  display: flex;
  align-items: center;
}

.dialog-content {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 5px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.6;
  color: #444;
  max-height: 400px; /* 适当增加高度以容纳更多内容 */
  overflow-y: auto;
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
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  overflow-y: auto;
  max-height: 200px;
}

.chat-message {
  margin-bottom: 10px;
  display: flex;
  align-items: flex-start;
}

.chat-message.doctor {
  justify-content: flex-start;
}

.chat-message.patient {
  justify-content: flex-end;
}

.sender-label {
  font-weight: bold;
  margin-right: 8px;
  min-width: 40px;
  text-align: right;
}

.message-bubble {
  padding: 8px 12px;
  border-radius: 18px;
  max-width: 70%;
  word-wrap: break-word;
}

.chat-message.doctor .message-bubble {
  background-color: #e0f7fa;
  color: #263238;
  margin-right: auto;
}

.chat-message.patient .message-bubble {
  background-color: #dcedc8;
  color: #212121;
  margin-left: auto;
}

.chat-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
