<template>
  <!-- 移除 el-card 组件，直接使用 div 作为根容器 -->
  <h2 class="page-title">语音转文字</h2>
  <div class="speech-to-text-content">
    <div class="card-header"> <!-- 保持 card-header，作为页面标题样式 -->
    </div>
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

    <!-- 新增：WAV 文件上传区域 -->
    <el-divider>或上传 WAV 文件</el-divider>
    <div class="upload-controls">
      <input type="file" ref="fileInput" @change="handleFileChange" accept="audio/wav" style="display: none;">
      <el-button type="info" @click="triggerFileInput">
        选择 WAV 文件
      </el-button>
      <span v-if="selectedFile">{{ selectedFile.name }}</span>
      <el-button 
        type="success" 
        :icon="Upload" 
        @click="uploadSelectedFile" 
        :disabled="!selectedFile"
        style="margin-left: 10px;"
      >
        上传并转写 WAV
      </el-button>
    </div>
    <!-- 结束新增 -->

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
      <p>您也可以通过“选择 WAV 文件”按钮直接上传本地 WAV 音频进行转写。</p>
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElLoading, ElMessage } from 'element-plus';
import axios from 'axios';
import { Microphone, VideoPause, Upload } from '@element-plus/icons-vue';

// 录音相关状态
let mediaStream = null; // 用于存储媒体流对象
const mediaRecorder = ref(null); // MediaRecorder 实例
const audioChunks = ref([]); // 存储录音数据块
const isRecording = ref(false); // 录音状态
const transcribedText = ref(''); // 转写结果
let loadingInstance = null; // Element Plus 加载服务的实例

// 新增：文件上传相关状态
const fileInput = ref(null); // 用于引用文件输入框
const selectedFile = ref(null); // 存储选中的文件

// 生成量化表弹窗相关
const quantifiedFormDialogVisible = ref(false);
const generatedQuantifiedForm = ref(null);

/**
 * 将音频数据上传到后端进行转写
 * @param {Blob|File} audioData 包含音频数据的 Blob 或 File 对象
 * @param {string} fileName 上传到后端的文件名
 */
const uploadAudio = async (audioData, fileName) => {
  // 显示加载提示
  loadingInstance = ElLoading.service({
    lock: true,
    text: '正在处理语音并进行转写，请稍候...',
    background: 'rgba(0, 0, 0, 0.7)',
  });

  try {
    const formData = new FormData();
    // audioData 可以是 Blob (来自录音) 也可以是 File (来自文件选择)
    formData.append('audio', audioData, fileName);

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
    // 无论成功或失败，最后都关闭加载提示
    if (loadingInstance) {
      loadingInstance.close();
    }
    audioChunks.value = []; // 清空录音数据块
    selectedFile.value = null; // 清空选中的文件
  }
};


/**
 * 开始录音
 */
const startRecording = async () => {
  transcribedText.value = ''; // 清空之前的转写结果
  audioChunks.value = []; // 清空之前的录音数据块
  selectedFile.value = null; // 清空选中的文件
  try {
    // 请求麦克风权限
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // 尝试优先使用 audio/webm;codecs=opus 格式，因为它在现代浏览器中通常效果最好
    const preferredMimeType = 'audio/webm;codecs=opus';
    let mediaRecorderOptions = {};

    if (MediaRecorder.isTypeSupported(preferredMimeType)) {
      mediaRecorderOptions = { mimeType: preferredMimeType };
      console.log(`浏览器支持录制 ${preferredMimeType} 格式。`);
    } else if (MediaRecorder.isTypeSupported('audio/webm')) {
      // 如果不支持带 Opus 编解码器的 WebM，则尝试通用 WebM 格式
      mediaRecorderOptions = { mimeType: 'audio/webm' };
      console.warn(`浏览器不支持录制 ${preferredMimeType} 格式，将尝试 audio/webm。`);
      ElMessage.warning(`您的浏览器可能不支持直接录制 ${preferredMimeType} 格式。转写可能会失败，请联系管理员。`);
    } else {
      // 如果都不支持，则回退到浏览器默认格式
      console.warn(`浏览器不支持录制 ${preferredMimeType} 或 audio/webm。将使用默认格式。`);
      ElMessage.warning(`您的浏览器可能不支持常见的音频录制格式。转写可能会失败，请联系管理员。`);
    }
    
    // 初始化 MediaRecorder，并根据支持的 MIME 类型设置选项
    mediaRecorder.value = new MediaRecorder(mediaStream, mediaRecorderOptions);

    mediaRecorder.value.ondataavailable = (event) => {
      audioChunks.value.push(event.data);
    };

    mediaRecorder.value.onstop = async () => {
      isRecording.value = false; // 录音状态设为 false
      // 停止媒体流轨道，释放麦克风资源
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
      }
      
      // 使用 MediaRecorder 实际录制到的 MIME 类型来创建 Blob，确保类型匹配
      const audioBlob = new Blob(audioChunks.value, { type: mediaRecorder.value.mimeType });
      
      // 调用上传函数处理音频数据
      // 文件名使用默认的 recording.webm
      await uploadAudio(audioBlob, 'recording.webm'); 
    };

    mediaRecorder.value.start(); // 开始录音
    isRecording.value = true; // 更新录音状态
    ElMessage.success('开始录音...');
  } catch (err) {
    console.error('无法访问麦克风或录音失败:', err);
    ElMessage.error('无法开始录音，请检查麦克风权限或设备。');
  }
};

/**
 * 停止录音 (此函数仅停止录音，实际上传逻辑在 mediaRecorder.onstop 事件中)
 */
const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop(); // 调用 stop() 会触发 onstop 事件
    // isRecording.value 会在 onstop 回调中更新
    // 加载提示会在 uploadAudio 函数中处理
  }
};

/**
 * 触发文件输入框点击
 */
const triggerFileInput = () => {
  fileInput.value.click();
};

/**
 * 处理文件选择
 * @param {Event} event 文件选择事件
 */
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file && file.type === 'audio/wav') {
    selectedFile.value = file;
    transcribedText.value = ''; // 清空之前的转写结果
    ElMessage.info(`已选择文件: ${file.name}`);
  } else {
    selectedFile.value = null;
    ElMessage.error('请选择一个 WAV 格式的音频文件。');
  }
};

/**
 * 上传选中的 WAV 文件
 */
const uploadSelectedFile = async () => {
  if (selectedFile.value) {
    await uploadAudio(selectedFile.value, selectedFile.value.name);
  } else {
    ElMessage.warning('请先选择一个 WAV 文件。');
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
    const response = await axios.post('http://127.0.0.1:5000/generate-form', {
      conversation_text: transcribedText.value,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    generatedQuantifiedForm.value = response.data;
    quantifiedFormDialogVisible.value = true; // 显示量化表弹窗
    ElMessage.success('量化表生成成功！');
  } catch (error) {
    console.error('生成量化表失败:', error);
    let errorMessage = '生成量化表失败，请检查后端日志。';
    if (error.response && error.response.data && error.response.data.error) {
      errorMessage = `生成量化表失败: ${error.response.data.error}`;
    } else if (error.message) {
      errorMessage = `生成量化表过程中发生错误: ${error.message}`;
    }
    ElMessage.error(errorMessage);
    generatedQuantifiedForm.value = null;
  }
};
</script>

<style scoped>
.page-title {
  color: #333;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.speech-to-text-content {
  /* 确保内容区域有与 main-content 相同的内边距，或根据需要调整 */
  padding: 0px; /* main-content 已经有20px padding，这里可以设为0或根据需要调整 */
  max-width: 100%; /* 确保占满父容器宽度 */
  margin: 0 auto; /* 居中内容 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  padding-bottom: 15px;
  margin-bottom: 20px; /* 增加与下方内容的间距 */
}

.recorder-controls {
  margin-bottom: 20px;
  display: flex;
  justify-content: center; /* 按钮居中 */
  gap: 10px;
}

.upload-controls { /* 新增样式 */
  margin-top: 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center; /* 上传控件居中 */
  gap: 10px;
  padding: 15px;
  border: 1px dashed #dcdfe6;
  border-radius: 8px;
  background-color: #f8f8f8;
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
