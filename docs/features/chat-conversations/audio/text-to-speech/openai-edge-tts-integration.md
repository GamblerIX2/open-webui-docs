---
sidebar_position: 1
title: "使用 Docker 部署 Edge TTS"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

# 将 `openai-edge-tts` 🗣️ 集成到 Open WebUI

## 什么是 `openai-edge-tts`？

[OpenAI Edge TTS](https://github.com/travisvn/openai-edge-tts) 是一个模拟 OpenAI API endpoint 的文本转语音 API。在像 Open WebUI 这样可自定义 endpoint URL 的场景中，它可以作为直接替代方案。

它基于 [edge-tts](https://github.com/rany2/edge-tts) 包实现，通过调用 Edge 浏览器免费的 “Read Aloud” 能力，模拟向 Microsoft / Azure 发起请求，从而免费获得高质量文本转语音。

[试听语音样本](https://tts.travisvn.com)

<!-- markdownlint-disable-next-line MD033 -->
<details>
  <!-- markdownlint-disable-next-line MD033 -->
  <summary>它和 `openedai-speech` 有什么不同？</summary>

与 [openedai-speech](https://github.com/matatonic/openedai-speech) 类似，[openai-edge-tts](https://github.com/travisvn/openai-edge-tts) 也是一个模拟 OpenAI API endpoint 的文本转语音服务，因此在可配置 OpenAI Speech endpoint URL 的场景下，可以直接替代原接口。

`openedai-speech` 功能更全面，支持多种模态，并可完全离线生成语音。

`openai-edge-tts` 则更轻量，它通过 Python 包 `edge-tts` 来生成音频。

</details>

## 前置要求

- 系统已安装 Docker
- Open WebUI 正在运行

## ⚡️ 快速开始

如果你想最快上手、无需额外配置，可直接运行下面命令：

```bash
docker run -d -p 5050:5050 travisvn/openai-edge-tts:latest
```

这会以默认配置在 5050 端口启动服务。

## 配置 Open WebUI 使用 `openai-edge-tts`

- 打开 Admin Panel 并进入 `Settings` -> `Audio`
- 按下图所示配置你的 TTS 设置
- *注意：你也可以在这里指定 TTS Voice*

![Screenshot of Open WebUI Admin Settings for Audio adding the correct endpoints for this project](https://utfs.io/f/MMMHiQ1TQaBobmOhsMkrO6Tl2kxX39dbuFiQ8cAoNzysIt7f)

:::info

默认 API key 是字符串 `your_api_key_here`。如果你不需要额外安全控制，可以不修改这个值。

:::

**到这里就已经能用了！**

## 如果你觉得 [OpenAI Edge TTS](https://github.com/travisvn/openai-edge-tts) 有用，请在 GitHub 上点个 ⭐️

<!-- markdownlint-disable-next-line MD033 -->
<details>
  <!-- markdownlint-disable-next-line MD033 -->
  <summary>使用 Python 运行</summary>

### 🐍 使用 Python 运行

如果你更喜欢直接用 Python 运行项目，请按以下步骤创建虚拟环境、安装依赖并启动服务。

#### 1. 克隆仓库

```bash
git clone https://github.com/travisvn/openai-edge-tts.git
cd openai-edge-tts
```

#### 2. 创建虚拟环境

创建并激活虚拟环境，以隔离依赖：

```bash

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. 安装依赖

使用 `pip` 安装 `requirements.txt` 中列出的依赖：

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

在项目根目录创建 `.env` 文件，并设置以下变量：

```plaintext
API_KEY=your_api_key_here
PORT=5050

DEFAULT_VOICE=en-US-AvaNeural
DEFAULT_RESPONSE_FORMAT=mp3
DEFAULT_SPEED=1.0

DEFAULT_LANGUAGE=en-US

REQUIRE_API_KEY=True
REMOVE_FILTER=False
EXPAND_API=True
```

#### 5. 启动服务

完成配置后，通过以下命令启动：

```bash
python app/server.py
```

服务会运行在 `http://localhost:5050`。

#### 6. 测试 API

现在你可以访问 `http://localhost:5050/v1/audio/speech` 以及其他可用 endpoint。请求示例可参考下方 Usage 部分。

</details>

<!-- markdownlint-disable-next-line MD033 -->
<details>
  <!-- markdownlint-disable-next-line MD033 -->
  <summary>使用详情</summary>

##### Endpoint：`/v1/audio/speech`（也可使用 `/audio/speech`）

该接口用于将输入文本转换为音频。支持以下参数：

**必填参数：**

- **input**（string）：要转换成语音的文本（最长 4096 字符）。

**可选参数：**

- **model**（string）：设置为 `tts-1` 或 `tts-1-hd`（默认：`"tts-1"`）。
- **voice**（string）：可使用 OpenAI 兼容语音（alloy、echo、fable、onyx、nova、shimmer），也可使用任意有效的 `edge-tts` 语音（默认：`"en-US-AvaNeural"`）。
- **response_format**（string）：音频格式，可选 `mp3`、`opus`、`aac`、`flac`、`wav`、`pcm`（默认：`mp3`）。
- **speed**（number）：播放速度（0.25 到 4.0，默认 `1.0`）。

:::tip

你可以在 [tts.travisvn.com](https://tts.travisvn.com) 浏览可用语音并试听示例。

:::

使用 `curl` 发送请求并保存为 mp3 文件的示例：

```bash
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "input": "Hello, I am your AI assistant! Just let me know how I can help bring your ideas to life.",
    "voice": "echo",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

或者使用更贴近 OpenAI API 参数形式的请求：

```bash
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "model": "tts-1",
    "input": "Hello, I am your AI assistant! Just let me know how I can help bring your ideas to life.",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

以下是非英语语言的示例：

```bash
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{
    "model": "tts-1",
    "input": "じゃあ、行く。電車の時間、調べておくよ。",
    "voice": "ja-JP-KeitaNeural"
  }' \
  --output speech.mp3
```

##### 其他 Endpoints

- **POST/GET /v1/models**：列出可用 TTS 模型。
- **POST/GET /v1/voices**：列出指定语言 / locale 下的 `edge-tts` 语音。
- **POST/GET /v1/voices/all**：列出全部 `edge-tts` 语音及其语言支持信息。

:::info

现在 `/v1` 前缀是可选的。

此外，项目还提供 **Azure AI Speech** 和 **ElevenLabs** 相关 endpoints，以便未来在 Open WebUI 支持这些自定义 API endpoint 时使用。

你也可以通过设置环境变量 `EXPAND_API=False` 来关闭这些扩展接口。

:::

</details>

## 🐳 Docker 快速配置

你也可以直接在运行命令中配置环境变量：

```bash
docker run -d -p 5050:5050 \
  -e API_KEY=your_api_key_here \
  -e PORT=5050 \
  -e DEFAULT_VOICE=en-US-AvaNeural \
  -e DEFAULT_RESPONSE_FORMAT=mp3 \
  -e DEFAULT_SPEED=1.0 \
  -e DEFAULT_LANGUAGE=en-US \
  -e REQUIRE_API_KEY=True \
  -e REMOVE_FILTER=False \
  -e EXPAND_API=True \
  travisvn/openai-edge-tts:latest
```

:::note

现在 Markdown 文本会经过一个过滤器，以提高可读性与支持效果。

如果你不需要它，可设置环境变量 `REMOVE_FILTER=True` 关闭。

:::

## 其他资源

如需了解更多 `openai-edge-tts` 信息，可查看其 [GitHub repo](https://github.com/travisvn/openai-edge-tts)。

如需直接支持，可访问 [Voice AI & TTS Discord](https://tts.travisvn.com/discord)。

## 🎙️ 语音样本

[播放语音样本并查看全部可用 Edge TTS 语音](https://tts.travisvn.com/)

## 故障排查

### 连接问题

#### Docker 中 `localhost` 不生效

如果 Open WebUI 运行在 Docker 中，且无法访问 `localhost:5050` 上的 TTS 服务：

**解决方案：**
- 使用 `host.docker.internal:5050` 代替 `localhost:5050`（Docker Desktop，Windows/Mac）
- Linux 上请使用宿主机 IP，或在 Docker run 命令中添加 `--network host`
- 如果两个服务都在 Docker Compose 中，使用容器名：`http://openai-edge-tts:5050/v1`

**同一网络下同时运行两个服务的 Docker Compose 示例：**

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_TTS_ENGINE=openai
      - AUDIO_TTS_OPENAI_API_BASE_URL=http://openai-edge-tts:5050/v1
      - AUDIO_TTS_OPENAI_API_KEY=your_api_key_here
    networks:
      - webui-network

  openai-edge-tts:
    image: travisvn/openai-edge-tts:latest
    ports:
      - "5050:5050"
    environment:
      - API_KEY=your_api_key_here
    networks:
      - webui-network

networks:
  webui-network:
    driver: bridge
```

#### 测试 TTS 服务

先单独验证 TTS 服务是否工作：

```bash
curl -X POST http://localhost:5050/v1/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key_here" \
  -d '{"input": "Test message", "voice": "alloy"}' \
  --output test.mp3
```

如果这个请求成功，但 Open WebUI 仍然连接失败，那么问题通常出在容器间网络。

### Open WebUI 中没有音频输出

1. 检查 API Base URL 是否以 `/v1` 结尾
2. 确认两个服务中的 API key 一致（或关闭其要求）
3. 查看 Open WebUI 容器日志：`docker logs open-webui`
4. 查看 openai-edge-tts 日志：`docker logs openai-edge-tts`（或你的容器名）

更多排查建议请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。
