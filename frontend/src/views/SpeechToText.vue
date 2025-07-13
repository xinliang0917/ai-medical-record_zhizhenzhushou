<template>
  <el-card class="speech-to-text-card">
    <template #header>
      <div class="card-header">
        <span>语音转文字</span>
      </div>
    </template>
    <div class="recorder-controls">
      <el-button
        type="primary"
        :icon="Microphone"
        @click="startRecording"
        :disabled="isRecording"
      >
        开始录音
      </el-button>
      <el-button
        type="danger"
        :icon="VideoPause"
        @click="stopRecording"
        :disabled="!isRecording"
      >
        停止录音
      </el-button>
      <el-button
        type="success"
        :icon="Upload"
        @click="generateForm"
        :disabled="!transcribedText"
      >
        生成量化表 (基于转写结果)
      </el-button>
    </div>

    <div v-if="transcribedText" class="transcribed-text-container">
      <h4>转写结果：</h4>
      <el-input
        type="textarea"
        :rows="5"
        v-model="transcribedText"
        placeholder="语音转写结果将显示在这里..."
        readonly
      ></el-input>
    </div>
    <div v-else class="transcribed-text-placeholder">
      <p>点击“开始录音”按钮，开始您的问诊对话，完成后点击“停止录音”。</p>
      <p>系统会将录音内容转换为文字，并自动填充到下方的文本框中。</p>
    </div>

    <el-dialog
      v-model="quantifiedFormDialogVisible"
      title="生成的量化表"
      width="70%"
      class="quantified-form-dialog"
    >
      <div v-if="generatedQuantifiedForm">
        <h4>量化表内容：</h4>
        <div class="dialog-content">
          <ul v-if="generatedQuantifiedForm">
            <li v-for="(value, key) in generatedQuantifiedForm" :key="key">
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
        </div>
      </div>
      <template #footer>
        <el-button type="primary" @click="quantifiedFormDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref } from 'vue';//computed, watchEffect, nextTick, onMounted
// import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'; // 确保导入 ElMessage, ElMessageBox
// import * as XLSX from 'xlsx';
// import { saveAs } from 'file-saver';
import axios from 'axios'; // 确保导入 axios
import { Microphone, VideoPause, Upload } from '@element-plus/icons-vue';

// const router = useRouter();
// const route = useRoute();
// 录音相关状态
const mediaRecorder = ref(null);
const audioChunks = ref([]);
const isRecording = ref(false);
const transcribedText = ref(''); // 用于显示转写结果的 ref
const isLoading = ref(false); // 用于显示加载状态

// 生成量化表弹窗相关
const quantifiedFormDialogVisible = ref(false);
const generatedQuantifiedForm = ref(null);

// 修改 startRecording 函数
const startRecording = async () => {
  transcribedText.value = ''; // 清空之前的转写结果
  audioChunks.value = [];
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // 尝试以 audio/wav 格式录制
    const preferredMimeType = 'audio/wav'; // 优先尝试 WAV 格式
    let mediaRecorderOptions = {};

    if (MediaRecorder.isTypeSupported(preferredMimeType)) {
      mediaRecorderOptions = { mimeType: preferredMimeType };
      console.log(`浏览器支持录制 ${preferredMimeType} 格式。`);
    } else {
      // 如果浏览器不支持 audio/wav，则退回默认格式（通常是 audio/webm 或 audio/ogg）
      // 在这种情况下，后端可能需要额外的处理来支持这些格式（如安装 ffmpeg）
      // 或者需要前端在发送前进行转换（更复杂）
      console.warn(`浏览器不支持录制 ${preferredMimeType} 格式。将使用默认格式。`);
      ElMessage.warning(`您的浏览器可能不支持直接录制 ${preferredMimeType} 格式。转写可能会失败，请联系管理员。`);
    }

    mediaRecorder.value = new MediaRecorder(stream, mediaRecorderOptions);

    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data);
    };

    mediaRecorder.value.onstop = async () => {
      // 使用 mediaRecorder 实际录制到的 MIME 类型来创建 Blob
      const audioBlob = new Blob(audioChunks.value, { type: mediaRecorder.value.mimeType });
      await uploadAudio(audioBlob);
      audioChunks.value = []; // 清空音频片段
    };

    mediaRecorder.value.start();
    isRecording.value = true;
    ElMessage.success('开始录音...');
  } catch (err) {
    console.error('无法访问麦克风或录音失败:', err);
    ElMessage.error('无法开始录音，请检查麦克风权限或设备。');
  }
};

// 修改 stopRecording 函数
const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop();
    isRecording.value = false;
    ElMessage.info('录音停止，正在处理...');
  }
};

// 添加 uploadAudio 函数
const uploadAudio = async (audioBlob) => {
  isLoading.value = true;
  try {
    const formData = new FormData();
    // 使用 Blob 实际的 MIME 类型来创建 File 对象
    // 文件名也尽量和实际类型匹配，或者使用通用名称
    const fileExtension = audioBlob.type.split('/')[1] || 'wav'; // 例如从 'audio/webm' 得到 'webm'
    const fileName = `recording.${fileExtension}`;

    const audioFile = new File([audioBlob], fileName, { type: audioBlob.type });
    formData.append('audio', audioFile);

    const response = await axios.post('http://127.0.0.1:5000/transcribe-audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    transcribedText.value = response.data.transcribedText;
    ElMessage.success('语音转写成功！');
  } catch (error) {
    console.error('语音转写失败:', error);
    let errorMessage = '后端转写失败，请检查后端日志。';
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage = `后端转写失败: ${error.response.data.error}`;
    } else if (error.message) {
      errorMessage = `语音转写过程中发生错误: ${error.message}`;
    }
    ElMessage.error(errorMessage);
  } finally {
    isLoading.value = false;
  }
};

/**
 * 根据转写结果生成量化表
 */
const generateForm = async () => {
  if (!transcribedText.value) {
    ElMessage.warning('没有可用于生成量化表的转写内容！');
    return;
  }

  ElMessage.info('正在根据转写内容生成量化表...');
  try {
    const response = await fetch('http://localhost:5000/generate-form', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ conversation_text: transcribedText.value }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`生成量化表失败: ${errorData.error || response.statusText}`);
    }

    const data = await response.json();
    generatedQuantifiedForm.value = data;
    quantifiedFormDialogVisible.value = true; // 显示量化表弹窗
    ElMessage.success('量化表生成成功！');
  } catch (error) {
    console.error('生成量化表失败:', error);
    ElMessage.error('量化表生成失败: ' + error.message);
    generatedQuantifiedForm.value = null;
  }
};
</script>

<style scoped>
.speech-to-text-card {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.recorder-controls {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.transcribed-text-container {
  margin-top: 20px;
}

.transcribed-text-container h4 {
  margin-bottom: 10px;
  color: #333;
}

.transcribed-text-placeholder {
  margin-top: 30px;
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  text-align: center;
  color: #666;
  font-size: 15px;
  line-height: 1.8;
}

.transcribed-text-placeholder p:last-child {
  margin-bottom: 0;
}

/* 量化表弹窗样式 */
.quantified-form-dialog .el-dialog__header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.quantified-form-dialog h4 {
  color: #333;
  margin-top: 20px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #ddd;
  padding-bottom: 5px;
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
  max-height: 400px;
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
</style>