---
sidebar_position: 2
title: "环境变量"
---

## 环境变量清单

:::info

如需查看 Open WebUI 全部环境变量，请参阅 [Environment Variable Configuration](https://docs.openwebui.com/reference/env-configuration) 页面。

:::

下文汇总了语音转文本（STT）和文本转语音（TTS）相关的环境变量。

:::tip UI 配置
其中大多数设置也可以在 **Admin Panel → Settings → Audio** 中配置。环境变量会在启动时优先生效，但之后仍可在 UI 中覆盖。
:::

## 语音转文本（STT）环境变量

### 预处理

| Variable | Description | Default |
|----------|-------------|---------|
| `BYPASS_PYDUB_PREPROCESSING` | 在将音频发送到 STT 引擎前，跳过基于 pydub 的预处理（MP3 转换、压缩、分块切分）。适用于所有引擎。当上游提供商已处理这些步骤，或主机上没有 ffmpeg 时很有用。 | `false` |

### 本地 Whisper

| Variable | Description | Default |
|----------|-------------|---------|
| `WHISPER_MODEL` | Whisper 模型大小 | `base` |
| `WHISPER_MODEL_DIR` | Whisper 模型文件的存储目录 | `{CACHE_DIR}/whisper/models` |
| `WHISPER_COMPUTE_TYPE` | 推理使用的计算类型（见下方说明） | `int8` |
| `WHISPER_LANGUAGE` | ISO 639-1 语言代码（留空 = 自动检测） | empty |
| `WHISPER_MULTILINGUAL` | 使用多语言 Whisper 模型 | `false` |
| `WHISPER_MODEL_AUTO_UPDATE` | 自动下载模型更新 | `false` |
| `WHISPER_VAD_FILTER` | 启用语音活动检测过滤器 | `false` |

:::info WHISPER_COMPUTE_TYPE 选项
- `int8` —— CPU 默认值，速度最快，但在较老的 GPU 上可能不可用
- `float16` —— **CUDA / GPU 推荐值**
- `int8_float16` —— 混合模式（int8 权重，float16 计算）
- `float32` —— 兼容性最高，但最慢

如果你使用 `:cuda` Docker 镜像且 GPU 较旧，请设置 `WHISPER_COMPUTE_TYPE=float16` 以避免报错。
:::

### OpenAI 兼容 STT

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_STT_ENGINE` | STT 引擎：留空（本地 Whisper）、`openai`、`azure`、`deepgram`、`mistral` | empty |
| `AUDIO_STT_MODEL` | 外部提供商使用的 STT 模型 | empty |
| `AUDIO_STT_OPENAI_API_BASE_URL` | OpenAI 兼容 API Base URL | `https://api.openai.com/v1` |
| `AUDIO_STT_OPENAI_API_KEY` | OpenAI API key | empty |
| `AUDIO_STT_SUPPORTED_CONTENT_TYPES` | 支持的音频 MIME type，逗号分隔 | empty |

### Azure STT

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_STT_AZURE_API_KEY` | Azure Cognitive Services API key | empty |
| `AUDIO_STT_AZURE_REGION` | Azure 区域 | `eastus` |
| `AUDIO_STT_AZURE_LOCALES` | 地区列表，逗号分隔（例如 `en-US,de-DE`） | auto |
| `AUDIO_STT_AZURE_BASE_URL` | 自定义 Azure Base URL（可选） | empty |
| `AUDIO_STT_AZURE_MAX_SPEAKERS` | 说话人数上限（用于 diarization） | `3` |

### Deepgram STT

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPGRAM_API_KEY` | Deepgram API key | empty |

### Mistral STT

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_STT_MISTRAL_API_KEY` | Mistral API key | empty |
| `AUDIO_STT_MISTRAL_API_BASE_URL` | Mistral API Base URL | `https://api.mistral.ai/v1` |
| `AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS` | 使用 chat completions endpoint | `false` |

## 文本转语音（TTS）环境变量

### 通用 TTS

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_ENGINE` | TTS 引擎：留空（禁用）、`openai`、`mistral`、`elevenlabs`、`azure`、`transformers` | empty |
| `AUDIO_TTS_MODEL` | TTS 模型 | `tts-1` |
| `AUDIO_TTS_VOICE` | 默认语音 | `alloy` |
| `AUDIO_TTS_SPLIT_ON` | 文本切分方式：`punctuation`、`paragraphs` 或 `none` | `punctuation` |
| `AUDIO_TTS_API_KEY` | ElevenLabs 或 Azure TTS 使用的 API key | empty |

### OpenAI 兼容 TTS

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_OPENAI_API_BASE_URL` | OpenAI 兼容 TTS API Base URL | `https://api.openai.com/v1` |
| `AUDIO_TTS_OPENAI_API_KEY` | OpenAI TTS API key | empty |
| `AUDIO_TTS_OPENAI_PARAMS` | OpenAI TTS 附加 JSON 参数 | empty |

### Mistral TTS

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_MISTRAL_API_KEY` | Mistral TTS API key | empty |
| `AUDIO_TTS_MISTRAL_API_BASE_URL` | Mistral API Base URL | `https://api.mistral.ai/v1` |

:::info
当 `AUDIO_TTS_ENGINE=mistral` 且 `AUDIO_TTS_MODEL` 为空时，Open WebUI 会默认使用 `mistral-tts-latest`。
:::

### Azure TTS

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_AZURE_SPEECH_REGION` | Azure Speech 区域 | `eastus` |
| `AUDIO_TTS_AZURE_SPEECH_BASE_URL` | 自定义 Azure Speech Base URL（可选） | empty |
| `AUDIO_TTS_AZURE_SPEECH_OUTPUT_FORMAT` | 音频输出格式 | `audio-24khz-160kbitrate-mono-mp3` |

## 音频配置提示

### 使用本地 Whisper STT

如果你遇到 GPU 加速问题或使用较旧 GPU，可以尝试设置：
```yaml
environment:
  - WHISPER_COMPUTE_TYPE=float16
```

### 使用外部 TTS 服务

如果你在 Docker 中运行 Open WebUI 并接入外部 TTS 服务：

```yaml
environment:
  - AUDIO_TTS_ENGINE=openai
  - AUDIO_TTS_OPENAI_API_BASE_URL=http://host.docker.internal:5050/v1
  - AUDIO_TTS_OPENAI_API_KEY=your-api-key
```

:::tip
在 Docker Desktop（Windows / Mac）中可使用 `host.docker.internal` 访问宿主机服务；Linux 上请使用宿主机 IP 或容器网络。
:::

如需排查音频问题，请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。
