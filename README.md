# Doubao STT & TTS

A comprehensive OOMOL package for speech-to-text (STT) and text-to-speech (TTS) capabilities powered by Doubao AI services. This package provides easy-to-use blocks for converting audio to text and text to audio with support for multiple languages and voice options.

[中文文档](./README_zh-CN.md)

## Features

- **Speech-to-Text (STT)**: Convert audio files or URLs to text with word-level timestamps
- **Text-to-Speech (TTS)**: Generate natural-sounding speech from text with 21 voice options
- **Multiple Input Formats**: Support for both local files and remote URLs
- **Flexible Output**: Get results as URLs or download directly to local files
- **Rich Voice Selection**: 21 different voices in Chinese and English

## Available Blocks

### Subflows (Ready-to-Use Workflows)

#### 1. File Doubao STT
Transcribe local audio files to text.

**Inputs:**
- `file`: Local audio file path (supports mp3, wav, m4a, etc.)
- `format`: Audio format (default: mp3)

**Outputs:**
- `text`: Full transcribed text
- `words`: Word-level transcription with timestamps

**Use Case:** Perfect for transcribing audio files you have stored locally, such as recordings, podcasts, or voice memos.

#### 2. URL Doubao STT
Transcribe audio from a URL to text.

**Inputs:**
- `audio_url`: URL of the audio file to transcribe
- `format`: Audio format (default: mp3)

**Outputs:**
- `text`: Full transcribed text
- `words`: Word-level transcription with timestamps

**Use Case:** Ideal for processing audio files hosted online without downloading them first.

#### 3. Doubao TTS to URL
Convert text to speech and get the audio URL.

**Inputs:**
- `text`: Text content to convert to speech
- `voice`: Voice selection (21 options available in Chinese and English)

**Outputs:**
- `audio_url`: URL of the generated audio file

**Use Case:** Generate speech audio for web applications, chatbots, or any scenario where you need a URL to the audio.

#### 4. Doubao TTS to File
Convert text to speech and download the audio file locally.

**Inputs:**
- `text`: Text content to convert to speech
- `voice`: Voice selection (21 options available)

**Outputs:**
- (Audio file downloaded locally)

**Use Case:** Generate audio files for offline use, local playback, or further processing.

## Voice Options

The TTS service supports 21 different voices across Chinese and English:

### Chinese Voices
- 冷酷哥哥 (Cool Brother)
- 甜心小美 (Sweet Mei)
- 高冷御姐 (Cool Lady)
- 傲娇霸总 (Proud CEO)
- 广州德哥 (Guangzhou Brother)
- 京腔侃爷 (Beijing Speaker)
- 邻居阿姨 (Neighbor Auntie)
- 优柔公子 (Gentle Young Master)
- 儒雅男友 (Elegant Boyfriend)
- 俊朗男友 (Handsome Boyfriend)
- 北京小爷 (Beijing Young Master)
- 柔美女友 (Soft Girlfriend)
- 阳光青年 (Sunny Youth)
- 魅力女友 (Charming Girlfriend)
- 深夜播客 (Late Night Podcaster)

### English Voices
- Candice (American English, Female)
- Serena (American English, Female)
- Glen (American English, Male)
- Sylus (American English, Male)
- Corey (British English, Male)
- Nadia (British English, Female)

## Usage Examples

### Example 1: Transcribe a Local Audio File

1. Add the **File Doubao STT** block to your workflow
2. Select your audio file using the file picker
3. Set the format (e.g., "mp3")
4. Run the workflow
5. Get the transcribed text and word timestamps in the output

### Example 2: Convert Text to Speech

1. Add the **Doubao TTS to URL** block to your workflow
2. Enter the text you want to convert
3. Choose a voice from the dropdown menu
4. Run the workflow
5. Receive the audio URL in the output

### Example 3: Audio Translation Pipeline

Combine STT and TTS blocks to create an audio translation workflow:
1. Use **URL Doubao STT** to transcribe audio to text
2. Add a translation block (from another package)
3. Use **Doubao TTS to File** to generate translated audio

## Technical Details

### Task Blocks

This package includes four core task blocks that power the subflows:

1. **Submit Doubao STT**: Submits audio for transcription and returns a task ID
2. **Get Doubao STT Result**: Retrieves transcription results using the task ID
3. **Submit Doubao TTS**: Submits text for speech synthesis and returns a task ID
4. **Get Doubao TTS Result**: Retrieves generated audio using the task ID

These task blocks use an asynchronous processing model with automatic polling and retry logic to ensure reliable results.

### Supported Audio Formats

- MP3
- WAV
- M4A
- And other common audio formats

### Dependencies

This package automatically installs required dependencies:
- `upload-to-cloud`: For uploading local files to cloud storage
- `downloader`: For downloading audio files from URLs

## Installation

This package is available in the OOMOL registry. Install it through the OOMOL package manager:

1. Search for "doubao-stt-tts" in the package registry
2. Click install
3. Add it to your workspace dependencies
4. Start using the blocks in your workflows

## Requirements

- OOMOL Platform
- Active Doubao API access (managed by OOMOL)
- Internet connection for API requests

## License

This package is part of the OOMOL ecosystem.

## Support

For issues, questions, or feature requests, please contact the package maintainer or visit the OOMOL community forums.
