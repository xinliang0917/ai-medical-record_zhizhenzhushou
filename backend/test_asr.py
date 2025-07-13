from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import os
import tempfile
from paddlespeech.cli.asr.infer import ASRExecutor # 导入 ASRExecutor

# 初始化 Flask 应用
app = Flask(__name__)
# 允许所有来源的跨域请求。在生产环境中，建议限制为特定前端域名。
CORS(app)

# 初始化 PaddleSpeech ASR Executor
# 这一步可能会在第一次运行时下载模型，请确保网络畅通
try:
    asr_executor = ASRExecutor()
    print("ASRExecutor 初始化成功！")
except Exception as e:
    print(f"ASRExecutor 初始化失败: {e}")
    # 根据需要，可以选择退出应用或进行其他错误处理

# 定义一个简单的根路由，用于测试 Flask 服务是否启动
@app.route('/')
def index():
    return "Flask API is running!"

# 定义语音转文字路由
@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    filename = audio_file.filename
    content_type = audio_file.content_type

    print(f"收到文件: {filename}")
    print(f"文件 MIME 类型: {content_type}")

    try:
        audio_data_stream = io.BytesIO(audio_file.read())
        audio_data_stream.seek(0)

        processed_audio_stream = io.BytesIO()

        try:
            # 使用 pydub 统一处理音频格式转换和重采样
            audio_segment = AudioSegment.from_file(audio_data_stream, format=content_type.split('/')[-1])
            audio_segment = audio_segment.set_frame_rate(16000).set_channels(1) # 统一采样率和声道
            audio_segment.export(processed_audio_stream, format="wav") # 导出为 WAV 格式
            processed_audio_stream.seek(0)

            print(f"音频文件已成功转换为 WAV 格式。")

        except Exception as e:
            print(f"pydub 处理音频失败: {e}，尝试使用 soundfile 直接读取。")
            try:
                # 如果 pydub 失败，尝试直接用 soundfile 读取（处理部分简单格式）
                audio_data_stream.seek(0)
                data, samplerate = sf.read(audio_data_stream)
                temp_wav_io = io.BytesIO()
                sf.write(temp_wav_io, data, samplerate, format='WAV')
                temp_wav_io.seek(0)
                processed_audio_stream = temp_wav_io
                print("soundfile 直接读取成功。")
            except Exception as sf_e:
                print(f"soundfile 也无法直接读取原始音频: {sf_e}")
                return jsonify({"error": f"处理音频文件或转写失败: {sf_e}，请检查音频格式或后端日志。"}), 500

        # 从处理后的流中读取数据，再次确认采样率
        data, samplerate = sf.read(processed_audio_stream)

        # 再次检查采样率，虽然 pydub 已处理，但以防万一
        if samplerate != 16000:
            print(f"警告：音频采样率仍不是16kHz，当前为{samplerate}Hz。PaddleSpeech可能需要16kHz。")
            # 如果需要，这里可以添加进一步的重采样逻辑，但pydub通常已搞定

        # 调用 PaddleSpeech 进行语音转写
        # 确保 asr_executor 已成功初始化
        if 'asr_executor' in globals() and asr_executor:
            result = asr_executor(audio_in=data, lang='zh', sample_rate=samplerate)
            transcribed_text = result[0]
            return jsonify({"transcribedText": transcribed_text})
        else:
            return jsonify({"error": "ASR Executor 未能成功初始化，无法进行转写。"}), 500

    except Exception as e:
        print(f"处理音频文件或转写失败: {e}")
        return jsonify({"error": f"处理音频文件或转写失败: {e}"}), 500

# 定义生成量化表路由 (此部分需要您根据实际逻辑填充)
@app.route('/generate-form', methods=['POST'])
def generate_form():
    data = request.get_json()
    conversation_text = data.get('conversation_text', '')

    if not conversation_text:
        return jsonify({"error": "No conversation text provided"}), 400

    print(f"收到待生成量化表的文本: {conversation_text[:50]}...") # 打印前50字符

    # 这里是生成量化表的核心逻辑
    # 您需要根据 conversation_text 分析并生成结构化的量化表数据
    # 这是一个示例，您需要根据您的需求实现具体的逻辑
    generated_form_data = {
        "基本信息": {
            "症状": "根据对话提取的症状",
            "性别": "根据对话提取的性别",
            "年龄": "根据对话提取的年龄",
            "婚姻情况": "根据对话提取的婚姻情况"
        },
        "疼痛评估": {
            "持续性疼痛部位": "根据对话提取的疼痛部位",
            "疼痛强度": "根据对话提取的疼痛强度",
            "疼痛性质": "根据对话提取的疼痛性质",
            "伴随症状": "根据对话提取的伴随症状"
        },
        "转写原文": conversation_text
    }
    return jsonify(generated_form_data)


# Flask 应用的启动入口
if __name__ == '__main__':
    # 确保 PaddleSpeech 模型下载和初始化完成后才启动 Flask
    # 如果 asr_executor 初始化失败，这里可以决定是否继续运行 Flask
    if 'asr_executor' in globals() and asr_executor:
        app.run(debug=True, port=5000)
    else:
        print("由于 ASRExecutor 初始化失败，Flask 应用未启动。")