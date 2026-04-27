---
sidebar_position: 2
title: "Mistral TTS 集成"
---

# 使用 Mistral 实现文本转语音

本指南介绍如何在 Open WebUI 中使用 Mistral 的 Text-to-Speech API。

:::tip 想配置 STT？
请查看配套指南：[使用 Mistral Voxtral 实现语音转文本](/features/chat-conversations/audio/speech-to-text/mistral-voxtral-integration)
:::

## 前置要求

- 一个 Mistral API key
- Open WebUI 已安装并正常运行

## 快速配置（UI）

1. 点击你的**头像图标**（左下角）
2. 选择 **Admin Panel**
3. 点击 **Settings** -> **Audio** 标签
4. 按如下方式配置：

| Setting | Value |
|---------|-------|
| **Text-to-Speech Engine** | `MistralAI` |
| **API Base URL** | `https://api.mistral.ai/v1` |
| **API Key** | 你的 Mistral API key |
| **TTS Model** | `mistral-tts-latest`（或留空使用默认值） |
| **TTS Voice** | 从可用语音中选择 |

5. 点击 **Save**

## 可用模型

| Model | Description |
|-------|-------------|
| `mistral-tts-latest` | Mistral TTS 默认使用的模型 |

:::info
如果 `AUDIO_TTS_MODEL` 为空，Open WebUI 在使用 Mistral TTS 时会默认回退到 `mistral-tts-latest`。
:::

## 环境变量配置

如果你更倾向于通过环境变量配置：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_TTS_ENGINE=mistral
      - AUDIO_TTS_MISTRAL_API_KEY=your-mistral-api-key
      - AUDIO_TTS_MISTRAL_API_BASE_URL=https://api.mistral.ai/v1
      - AUDIO_TTS_MODEL=mistral-tts-latest
      - AUDIO_TTS_VOICE=<voice-id>
    # ... 其他配置
```

### 全部 Mistral TTS 环境变量

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_ENGINE` | 设置为 `mistral` | empty（仅使用浏览器侧 TTS） |
| `AUDIO_TTS_MISTRAL_API_KEY` | 你的 Mistral API key | empty |
| `AUDIO_TTS_MISTRAL_API_BASE_URL` | Mistral API Base URL | `https://api.mistral.ai/v1` |
| `AUDIO_TTS_MODEL` | TTS 模型 | `mistral-tts-latest`（Mistral 引擎的有效默认值） |
| `AUDIO_TTS_VOICE` | Voice ID | empty |

## 选择语音

Open WebUI 会向已配置的 Mistral endpoint 请求可用语音列表，并在 **TTS Voice** 选择器中展示它们。

如果语音列表没有显示：
- 确认 API key 有效
- 确认 Open WebUI 服务器 / 容器可以访问 API Base URL
- 查看 `/audio/voices` 请求相关日志

## 测试 TTS

1. 新建一个聊天
2. 向任意模型发送一条消息
3. 点击 AI 回复上的**扬声器图标**，听它朗读内容

## 故障排查

### “Mistral API key is required for Mistral TTS”

1. 确认 `AUDIO_TTS_MISTRAL_API_KEY` 已设置（或已在 Admin Audio 设置中填写）
2. 保存设置后重试

### 下拉框中没有语音

1. 确认 Open WebUI 到 `AUDIO_TTS_MISTRAL_API_BASE_URL` 的网络访问正常
2. 查看 Open WebUI 日志中与 Mistral 语音列表相关的错误
3. 确认你的 key 有权限访问 Mistral 音频 API

### TTS 请求失败

1. 确认 `AUDIO_TTS_ENGINE=mistral`
2. 尝试将模型留空（会使用 `mistral-tts-latest`）
3. 尝试切换为已获取列表中的其他 voice ID

更广泛的音频调试请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。
