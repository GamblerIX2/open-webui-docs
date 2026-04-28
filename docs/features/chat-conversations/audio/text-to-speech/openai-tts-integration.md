---
sidebar_position: 0
title: "OpenAI TTS 集成"
---

# 使用 OpenAI 实现文本转语音

本指南介绍如何在 Open WebUI 中使用 OpenAI 官方 Text-to-Speech API。如果你已经拥有 OpenAI API key，这是最简单的配置方式。

:::tip 想配置 STT？
请查看配套指南：[使用 OpenAI 实现语音转文本](/features/chat-conversations/audio/speech-to-text/openai-stt-integration)
:::

## 前置要求

- 拥有可访问 Audio API 的 OpenAI API key
- Open WebUI 已安装并正常运行

## 快速配置（UI）

1. 点击你的**头像图标**（左下角）
2. 选择 **Admin Panel**
3. 点击 **Settings** → **Audio** 标签
4. 按如下方式配置：

| Setting | Value |
|---------|-------|
| **Text-to-Speech Engine** | `OpenAI` |
| **API Base URL** | `https://api.openai.com/v1` |
| **API Key** | 你的 OpenAI API key |
| **TTS Model** | `tts-1` 或 `tts-1-hd` |
| **TTS Voice** | 从可用语音中选择 |

5. 点击 **Save**

## 可用模型

| Model | Description | Best For |
|-------|-------------|----------|
| `tts-1` | 标准音质、延迟更低 | 实时应用、更快响应 |
| `tts-1-hd` | 更高音质 | 预录内容、高品质音频 |

## 可用语音

OpenAI 提供 6 种内置语音：

| Voice | Description |
|-------|-------------|
| `alloy` | 中性、均衡 |
| `echo` | 温暖、偏对话风格 |
| `fable` | 表现力更强、英式口音 |
| `onyx` | 低沉、权威感强 |
| `nova` | 友好、轻快 |
| `shimmer` | 柔和、轻柔 |

:::tip
你可以多试几种语音，找到最适合自己场景的一种。也可以在 OpenAI 文档中预览相关语音。
:::

## 按模型设置 TTS Voice

你可以为单个模型指定专属 TTS Voice，让不同 AI persona 拥有不同声音。该设置位于 Model Editor 中。

### 设置模型专属语音

1. 前往 **Workspace > Models**
2. 点击要配置模型上的 **Edit**（铅笔）图标
3. 向下滚动找到 **TTS Voice** 字段
4. 输入语音名称（例如 `alloy`、`echo`、`shimmer`、`onyx`、`nova`、`fable`）
5. 点击 **Save**

### 语音优先级

播放 TTS 音频时，Open WebUI 按以下优先级选择语音：

1. **模型专属 TTS Voice**（如果在 Model Editor 中已设置）
2. **用户个人语音设置**（如果已在用户设置中配置）
3. **系统默认语音**（由管理员配置）

这样管理员就可以为每个 AI persona 设定稳定的声音，同时仍允许用户在没有模型专属语音时使用自己的偏好设置。

### 使用场景

- **角色化 persona**：例如让 “British Butler” 模型使用 `fable`，而 “Energetic Assistant” 使用 `nova`
- **语言学习**：为不同语言教师分配合适的声音
- **无障碍场景**：为无障碍用途模型设置更清晰的语音

## 环境变量配置

如果你更倾向于通过环境变量配置：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_TTS_ENGINE=openai
      - AUDIO_TTS_OPENAI_API_BASE_URL=https://api.openai.com/v1
      - AUDIO_TTS_OPENAI_API_KEY=sk-...
      - AUDIO_TTS_MODEL=tts-1
      - AUDIO_TTS_VOICE=alloy
    # ... 其他配置
```

### 全部 TTS 环境变量

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDIO_TTS_ENGINE` | 设置为 `openai` | empty |
| `AUDIO_TTS_OPENAI_API_BASE_URL` | OpenAI API Base URL | `https://api.openai.com/v1` |
| `AUDIO_TTS_OPENAI_API_KEY` | 你的 OpenAI API key | empty |
| `AUDIO_TTS_MODEL` | TTS 模型（`tts-1` 或 `tts-1-hd`） | `tts-1` |
| `AUDIO_TTS_VOICE` | 使用的语音 | `alloy` |

## 测试 TTS

1. 新建一个聊天
2. 向任意模型发送一条消息
3. 点击 AI 回复上的**扬声器图标**，听它朗读内容

## 响应切分

朗读较长回复时，Open WebUI 可以在发送到 TTS 引擎前先把文本拆分成多个片段。该设置位于 **Admin Panel > Settings > Audio** 下的 **Response Splitting**。

| Option | Description |
|--------|-------------|
| **Punctuation**（默认） | 按句子边界切分：句号（`.`）、感叹号（`!`）、问号（`?`）和换行。自然感最佳。 |
| **Paragraphs** | 仅按段落分隔（双换行）切分。生成的音频块更长。 |
| **None** | 整段回复作为一个整体发送。长回复可能会导致音频启动延迟。 |

:::tip
大多数场景建议使用 **Punctuation** 模式。它在流式性能（更快开始播放）和自然语音节奏之间取得了最好平衡。
:::

## 故障排查

### 没有音频播放

1. 检查 OpenAI API key 是否有效，并确认已开通 Audio API
2. 确认 API Base URL 是否正确（`https://api.openai.com/v1`）
3. 检查浏览器控制台（F12）是否有报错

### 音质问题

- 将 `tts-1` 切换为 `tts-1-hd` 可获得更高音质
- 注意：`tts-1-hd` 延迟会略高

### 速率限制

OpenAI Audio API 有速率限制。如果你经常触发限制：
- 可考虑缓存常用短语
- 使用 `tts-1` 代替 `tts-1-hd`（消耗更少 token）

更多排查信息请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。

## 成本说明

OpenAI 的 TTS 按字符数计费。当前价格请查看 [OpenAI Pricing](https://platform.openai.com/docs/pricing)。注意 `tts-1-hd` 的价格高于 `tts-1`。

:::info
如果你想要免费替代方案，可考虑 [OpenAI Edge TTS](/features/chat-conversations/audio/text-to-speech/openai-edge-tts-integration)，它利用微软 Edge 浏览器的免费 TTS 能力。
:::
