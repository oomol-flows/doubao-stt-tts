# 豆包 STT TTS

## 项目概述

由豆包 AI 驱动的语音转文字(STT)和文字转语音(TTS)功能包。支持多种音色(中英文)和音频格式。

## 功能块能力

### 子流程块

| 功能块 | 用途 | 主要输入 | 主要输出 |
|-------|------|---------|---------|
| `doubao-tts-to-file` | 文字 → 音频文件 | text, voice, saved_path | saved_path (MP3) |
| `url-doubao-stt` | 音频URL → 文字 | audio_url, format | text, words (含时间戳) |

### 任务块 (内部使用)

| 功能块 | 用途 | 输入 | 输出 |
|-------|------|-----|------|
| `submit-doubao-tts` | 提交TTS请求 | text, voice | task_id |
| `get-doubao-tts-result` | 轮询TTS结果 | task_id | audio_url |
| `submit-doubao-stt` | 提交STT请求 | audio_url, format | task_id |
| `get-doubao-stt-result` | 轮询STT结果 | task_id | text, words |

## 功能块组合建议

- **文字转音频流程**: 直接使用 `doubao-tts-to-file` 完成文字到音频的完整转换
- **音频转文字流程**: 直接使用 `url-doubao-stt` 完成URL到转写的完整流程
- **自定义工作流**: 组合 `submit-*` 和 `get-*` 任务块实现精细控制(自定义轮询间隔)

## 基本用法

1. **文字转语音**: 将文字输入连接到 `doubao-tts-to-file`,从21种音色中选择
2. **语音转文字**: 向 `url-doubao-stt` 提供音频URL,指定格式(mp3/wav/m4a)

## 使用示例

### 文字转音频文件
```
输入: text = "你好,这是一个测试"
      voice = "zh_female_tianxinxiaomei_emo_v2_mars_bigtts"
输出: saved_path = "/path/to/audio.mp3"
```

### 音频URL转文字
```
输入: audio_url = "https://example.com/audio.mp3"
      format = "mp3"
输出: text = "转写内容在这里"
      words = [{"word": "转写", "start": 0.0, "end": 0.5}, ...]
```

## 音色选项

- **中文**: 15种音色(冷酷哥哥、甜心小美、高冷御姐等)
- **英文**: 6种音色(Candice、Serena、Glen、Sylus、Corey、Nadia)
- 包含美式和英式英语变体
