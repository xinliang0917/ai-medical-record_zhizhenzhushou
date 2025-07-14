# 导入 PaddleSpeech 的 ASR 执行器
from paddlespeech.cli.asr.infer import ASRExecutor
import os

def run_simple_asr_test(audio_file_path):
    """
    使用 PaddleSpeech 对指定的 WAV 文件进行语音转写。
    """
    print(f"正在初始化 ASRExecutor...")
    try:
        # 初始化 ASRExecutor。
        # 默认模型通常是 conformer_wenetspeech，支持中文。
        asr_executor = ASRExecutor()
        print("ASRExecutor 初始化成功！")
    except Exception as e:
        print(f"ASRExecutor 初始化失败: {e}")
        print("请检查 PaddleSpeech 和其依赖是否正确安装。")
        return

    # 检查音频文件是否存在
    if not os.path.exists(audio_file_path):
        print(f"错误: 音频文件 '{audio_file_path}' 不存在。")
        print("请确保文件路径正确，并已将 WAV 文件放置到指定位置。")
        return

    print(f"正在转写文件: {audio_file_path}")
    try:
        # 定义解码参数，尝试调整 VAD 相关的阈值
        # 这些参数通常在 PaddleSpeech 的配置文件或文档中可以找到更详细的说明
        # 这里我们尝试设置一个较低的语音起始/结束阈值，以避免过早截断
        decode_args = {
            "decoding_method": "ctc_greedy", # 默认使用贪心解码，因为BeamSearch依赖ctcdecoders
            # "alpha": 0.5, # BeamSearch 相关参数，暂时不启用
            # "beta": 0.0,  # BeamSearch 相关参数，暂时不启用
            # "lang_model_path": None, # 语言模型路径，暂时不启用
            # "lm_weight": 0.0, # 语言模型权重，暂时不启用
            # "max_active": 7000, # BeamSearch 相关参数，暂时不启用
            # "min_active": 200, # BeamSearch 相关参数，暂时不启用
            # "blank_penalty": 0.0, # BeamSearch 相关参数，暂时不启用
            # "beam_size": 10, # BeamSearch 相关参数，暂时不启用
            # "num_threads": 1, # 解码线程数
            # "chunk_size": 1440, # 流式识别的块大小，当前是整体识别，暂时不启用
            # "stride": 1440, # 流式识别的步长，当前是整体识别，暂时不启用
            # "enable_without_timestamps": False, # 是否启用无时间戳模式
            # "enable_timestamps": False, # 是否启用时间戳输出
            # "cutoff_prob": 0.99, # CTC 剪枝概率
            # "cutoff_topk": 40, # CTC 剪枝 topk
            # "hotword_file": None, # 热词文件
            # "hotword_weight": 1.0, # 热词权重
            # "vad_speech_th": 0.5, # 语音活动检测的语音阈值 (0-1, 越高越严格)
            # "vad_silence_th": 0.5, # 语音活动检测的静音阈值 (0-1, 越低越容易被识别为语音)
            # "vad_min_speech_duration": 0.1, # 最小语音持续时间 (秒)
            # "vad_min_silence_duration": 0.1, # 最小静音持续时间 (秒)
            # "vad_max_speech_duration": 10.0, # 最大语音持续时间 (秒)
        }

        # 调用 asr_executor 进行语音转写
        # lang='zh' 和 sample_rate=16000 是推荐的中文和采样率设置
        # 尝试传递 decode_args
        result = asr_executor(audio_file=audio_file_path, lang='zh', sample_rate=16000, decode_args=decode_args)
        transcribed_text = result[0]
        print(f"转写完成。结果: {transcribed_text}")
    except Exception as e:
        print(f"语音转写失败: {e}")
        # 打印更详细的错误信息，帮助调试
        import traceback
        traceback.print_exc()
        print("请检查音频文件格式是否为 16kHz 采样率的单声道 WAV，或查看 PaddleSpeech 内部错误。")

if __name__ == "__main__":
    # 请将这里的 'ezyZip.wav' 替换为您实际的 WAV 文件路径
    # 确保这个文件在 backend 目录下，或者提供完整路径
    test_audio_path = "ezyZip.wav" # 替换为您的WAV文件名

    run_simple_asr_test(test_audio_path)
