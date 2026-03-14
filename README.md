# Doubao STT TTS

## Project Overview

Comprehensive speech-to-text (STT) and text-to-speech (TTS) package powered by Doubao AI. Supports multiple voices (Chinese and English) and audio formats.

## Block Capabilities

### Subflow Blocks

| Block | Purpose | Key Input | Key Output |
|-------|---------|-----------|------------|
| `doubao-tts-to-file` | Text → Audio file | text, voice, saved_path | saved_path (MP3) |
| `url-doubao-stt` | Audio URL → Text | audio_url, format | text, words (with timestamps) |

### Task Blocks (Internal)

| Block | Purpose | Input | Output |
|-------|---------|-------|--------|
| `submit-doubao-tts` | Submit TTS request | text, voice | task_id |
| `get-doubao-tts-result` | Poll TTS result | task_id | audio_url |
| `submit-doubao-stt` | Submit STT request | audio_url, format | task_id |
| `get-doubao-stt-result` | Poll STT result | task_id | text, words |

## Block Combination Suggestions

- **Text to Audio Pipeline**: Use `doubao-tts-to-file` directly for complete text-to-audio conversion
- **Audio to Text Pipeline**: Use `url-doubao-stt` for direct URL-to-transcription
- **Custom Workflows**: Combine `submit-*` and `get-*` task blocks for fine-grained control with custom polling intervals

## Basic Usage

1. **Text to Speech**: Connect text input to `doubao-tts-to-file`, select voice from 21 options
2. **Speech to Text**: Provide audio URL to `url-doubao-stt`, specify format (mp3/wav/m4a)

## Examples

### Text to Audio File
```
Input: text = "Hello, this is a test"
       voice = "en_female_candice_emo_v2_mars_bigtts"
Output: saved_path = "/path/to/audio.mp3"
```

### Audio URL to Text
```
Input: audio_url = "https://example.com/audio.mp3"
       format = "mp3"
Output: text = "Transcribed content here"
        words = [{"word": "Transcribed", "start": 0.0, "end": 0.5}, ...]
```

## Voice Options

- **Chinese**: 15 voices (冷酷哥哥, 甜心小美, 高冷御姐, etc.)
- **English**: 6 voices (Candice, Serena, Glen, Sylus, Corey, Nadia)
- Includes American and British English variants
