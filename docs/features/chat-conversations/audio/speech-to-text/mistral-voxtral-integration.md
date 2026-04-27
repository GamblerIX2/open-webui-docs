---
sidebar_position: 2
title: "Mistral Voxtral STT"
---

# 使用 Mistral Voxtral 实现语音转文本

本指南介绍如何在 Open WebUI 中使用 Mistral 的 Voxtral 模型进行 Speech-to-Text。Voxtral 是 Mistral 的语音转文本模型，可提供较准确的转录结果。

:::tip 想配置 TTS？
请查看配套指南：[使用 Mistral 实现文本转语音](/features/chat-conversations/audio/text-to-speech/mistral-tts-integration)
:::

## 前置要求

- 一个 Mistral API key
- Open WebUI 已安装并正常运行

## 快速配置（UI）

1. 点击你的**头像图标**（左下角）
2. 选择 **Admin Panel**
3. 点击 **Settings** → **Audio** 标签
4. 按如下方式配置：

| Setting | Value |
|---------|-------|
| **Speech-to-Text Engine** | `MistralAI` |
| **API Key** | 你的 Mistral API key |
| **STT Model** | `voxtral-mini-latest`（或留空使用默认值） |

5. 点击 **Save**

## 可用模型

| Model | Description |
|-------|-------------|
| `voxtral-mini-latest` | 默认转录模型（推荐） |

## 环境变量配置

如果你更倾向于使用环境变量：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_STT_ENGINE=mistral
      - AUDIO_STT_MISTRAL_API_KEY=your-mistral-api-key
      - AUDIO_STT_MODEL=voxtral-mini-latest
    # ... 其他配置
```

### 全部 Mistral STT 环境变量

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_STT_ENGINE` | 设置为 `mistral` | empty（使用本地 Whisper） |
| `AUDIO_STT_MISTRAL_API_KEY` | 你的 Mistral API key | empty |
| `AUDIO_STT_MISTRAL_API_BASE_URL` | Mistral API Base URL | `https://api.mistral.ai/v1` |
| `AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS` | 使用 chat completions endpoint | `false` |
| `AUDIO_STT_MODEL` | STT 模型 | `voxtral-mini-latest` |

## 转录方式

Mistral 支持两种转录方式：

### 标准转录（默认）

使用专用转录 endpoint。这是推荐方式。

### Chat Completions 方式

将 `AUDIO_STT_MISTRAL_USE_CHAT_COMPLETIONS=true` 后，可改用 Mistral 的 chat completions API 进行转录。该方式：
- 要求音频为 mp3 或 wav 格式（系统会尝试自动转换）
- 结果可能与标准 endpoint 有所不同

## 使用 STT

1. 点击聊天输入框中的**麦克风图标**
2. 说出你的内容
3. 再次点击麦克风，或等待静音检测结束
4. 你的语音会被转录并显示在输入框中

## 支持的音频格式

Voxtral 接受常见音频格式。系统默认允许 `audio/*` 和 `video/webm`。

如果使用 chat completions 方式，音频会自动转换为 mp3。

## 故障排查

### API key 错误

如果你看到 “Mistral API key is required”：
1. 确认 API key 填写正确
2. 检查 API key 是否已过期
3. 确认你的 Mistral 账号已开通 API 访问权限

### 转录无法工作

1. 检查容器日志：`docker logs open-webui -f`
2. 确认 STT Engine 设置为 `MistralAI`
3. 优先尝试标准转录方式（关闭 chat completions）

### 音频格式问题

如果你使用 chat completions 方式且音频转换失败：
- 确保容器中可用 FFmpeg
- 尝试录制为其他格式（wav 或 mp3）
- 切回标准转录方式

更多排查信息请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。

## 与其他 STT 方案对比

| Feature | Mistral Voxtral | OpenAI Whisper | Local Whisper |
|---------|-----------------|----------------|---------------|
| **Cost** | 按分钟计费 | 按分钟计费 | 免费 |
| **Privacy** | 音频发送到 Mistral | 音频发送到 OpenAI | 音频保留本地 |
| **Model Options** | voxtral-mini-latest | whisper-1 | tiny → large |
| **GPU Required** | 否 | 否 | 推荐 |

## 成本说明

Mistral 的 STT 按音频分钟数计费。当前价格请查看 [Mistral 定价页](https://mistral.ai/products/la-plateforme#pricing)。

:::tip
如果想使用免费 STT，可选择 **Local Whisper**（默认方案）或浏览器 **Web API** 进行基础转录。
:::
