---
sidebar_position: 0
title: "OpenAI 语音转文本集成"
---

# 使用 OpenAI 实现语音转文本

本指南介绍如何在 Open WebUI 中使用 OpenAI Whisper API 进行语音转文本。这种方式提供云端转录能力，无需本地 GPU 资源。

:::tip 想配置 TTS？
请查看配套指南：[使用 OpenAI 实现文本转语音](/features/chat-conversations/audio/text-to-speech/openai-tts-integration)
:::

## 前置要求

- 拥有可访问 Audio API 的 OpenAI API 密钥
- Open WebUI 已安装并正常运行

## 快速配置（UI）

1. 点击你的**头像图标**（左下角）
2. 选择 **管理面板**
3. 点击 **设置** → **音频** 标签
4. 按如下方式配置：

| 设置 | 值 |
|---------|-------|
| **语音转文本引擎** | `OpenAI` |
| **API 基础 URL** | `https://api.openai.com/v1` |
| **API 密钥** | 你的 OpenAI API 密钥 |
| **STT 模型** | `whisper-1` |
| **支持的内容类型** | 可留空使用默认值，或设置为 `audio/wav,audio/mpeg,audio/webm` |

5. 点击 **Save**

## 可用模型

| 模型 | 说明 |
|-------|-------------|
| `whisper-1` | OpenAI 在云端托管的 Whisper large-v2 模型 |

:::info
OpenAI 当前仅提供 `whisper-1`。如果你需要更多模型选择，可使用 Local Whisper（Open WebUI 内置）或 Deepgram 等其他提供商。
:::

## 环境变量配置

如果你更倾向于使用环境变量：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_STT_ENGINE=openai
      - AUDIO_STT_OPENAI_API_BASE_URL=https://api.openai.com/v1
      - AUDIO_STT_OPENAI_API_KEY=sk-...
      - AUDIO_STT_MODEL=whisper-1
    # ... 其他配置
```

### 全部 STT 环境变量（OpenAI）

| 变量 | 说明 | 默认值 |
|----------|-------------|---------|
| `AUDIO_STT_ENGINE` | 设置为 `openai` | empty（使用本地 Whisper） |
| `AUDIO_STT_OPENAI_API_BASE_URL` | OpenAI API 基础 URL | `https://api.openai.com/v1` |
| `AUDIO_STT_OPENAI_API_KEY` | 你的 OpenAI API 密钥 | empty |
| `AUDIO_STT_MODEL` | STT 模型 | `whisper-1` |
| `AUDIO_STT_SUPPORTED_CONTENT_TYPES` | 允许的音频 MIME 类型 | `audio/*,video/webm` |

### 支持的音频格式

默认情况下，Open WebUI 接受 `audio/*` 和 `video/webm` 进行转录。如果你想限制或扩展支持格式，可设置 `AUDIO_STT_SUPPORTED_CONTENT_TYPES`：

```yaml
environment:
  - AUDIO_STT_SUPPORTED_CONTENT_TYPES=audio/wav,audio/mpeg,audio/webm
```

OpenAI Whisper API 支持：`mp3`、`mp4`、`mpeg`、`mpga`、`m4a`、`wav`、`webm`

## 使用 STT

1. 点击聊天输入框中的**麦克风图标**
2. 说出你的内容
3. 再次点击麦克风，或等待静音检测结束
4. 你的语音会被转录并显示在输入框中

## OpenAI 与 Local Whisper 对比

| 特性 | OpenAI Whisper API | Local Whisper |
|---------|-------------------|---------------|
| **延迟** | 取决于网络 | 短音频通常更快 |
| **成本** | 按分钟计费 | 免费（使用你的硬件） |
| **隐私** | 音频发送到 OpenAI | 音频留在本地 |
| **需要 GPU** | 否 | 为了速度建议使用 |
| **模型选项** | 仅 `whisper-1` | tiny、base、small、medium、large |

在以下情况下推荐选择 **OpenAI**：
- 你没有 GPU
- 你希望获得稳定一致的表现
- 隐私不是首要顾虑

在以下情况下推荐选择 **Local Whisper**：
- 你想要免费转录
- 你需要音频保留在本地
- 你拥有可用于加速的 GPU

## 故障排查

### 麦克风无法工作

1. 确保你正在使用 HTTPS 或 localhost
2. 检查浏览器麦克风权限
3. 查看 [麦克风访问问题](/troubleshooting/audio#microphone-access-issues)

### 转录报错

1. 检查 OpenAI API key 是否有效
2. 确认 API Base URL 是否正确
3. 查看容器日志中的报错信息

### 语言识别问题

OpenAI Whisper API 会自动检测语言。如果你需要强制指定语言，请考虑改用 Local Whisper，并设置 `WHISPER_LANGUAGE` 环境变量。

更多排查信息请参阅 [音频故障排查指南](/troubleshooting/audio)。

## 成本说明

OpenAI 的 STT 按音频分钟数计费。当前价格请参阅 [OpenAI Pricing](https://platform.openai.com/docs/pricing)。

:::tip
如果想使用免费 STT，可选择 **Local Whisper**（默认方案）或浏览器 **Web API** 进行基础转录。
:::
