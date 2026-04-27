---
sidebar_position: 3
title: "Chatterbox TTS —— 声音克隆"
---

# Chatterbox TTS —— 声音克隆

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 什么是 `Chatterbox TTS API`？

[Chatterbox TTS API](https://github.com/travisvn/chatterbox-tts-api) 是一个 API 封装层，支持声音克隆与文本转语音，可直接替代 OpenAI Speech API endpoint。

[![Link to Resemble AI voice samples](https://img.shields.io/badge/listen-demo_samples-blue)](https://resemble-ai.github.io/chatterbox_demopage/)

## 主要特性

- 零样本声音克隆 —— 只需约 10 秒语音样本
- [表现优于 ElevenLabs](https://podonos.com/resembleai/chatterbox)
- 输出带水印，便于负责任地使用声音克隆
- 0.5B Llama backbone
- 自定义 Voice Library 管理
- 支持流式输出，生成更快
- 具备高级内存管理与自动清理
- 可选前端界面，便于管理和使用

### 硬件建议

- 内存：至少 4GB，推荐 8GB+
- GPU：CUDA（Nvidia）或 Apple M 系列（MPS）
- CPU：也能运行，但更慢 —— 生产环境推荐使用 GPU

:::info

Chatterbox 可能会占用较多内存，其硬件要求也可能高于你熟悉的其他本地 TTS 方案。如果你的机器难以满足要求，可以考虑 [OpenAI Edge TTS](https://docs.openwebui.com/tutorials/text-to-speech/openai-edge-tts-integration) 或 [Kokoro-FastAPI](https://docs.openwebui.com/tutorials/text-to-speech/Kokoro-FastAPI-integration) 作为替代方案。

:::

## ⚡️ 快速开始

### 🐍 使用 Python

#### 方案 A：使用 uv（推荐 —— 更快、依赖处理更好）

```bash

# 克隆仓库
git clone https://github.com/travisvn/chatterbox-tts-api
cd chatterbox-tts-api

# 如果还没安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 用 uv 安装依赖（会自动创建 venv）
uv sync

# 复制并自定义环境变量
cp .env.example .env

# 使用 FastAPI 启动 API
uv run uvicorn app.main:app --host 0.0.0.0 --port 4123

# 或使用主脚本
uv run main.py
```

> 💡 **为什么选 uv？** 用户普遍反馈它对 `chatterbox-tts` 兼容性更好、安装速度提升 25-40%，并且依赖解析更稳定。[查看迁移指南 →](https://github.com/travisvn/chatterbox-tts-api/blob/main/docs/UV_MIGRATION.md)

#### 方案 B：使用 pip（传统方式）

```bash

# 克隆仓库
git clone https://github.com/travisvn/chatterbox-tts-api
cd chatterbox-tts-api

# 配置环境 —— 使用 Python 3.11
python -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制并自定义环境变量
cp .env.example .env

# 添加你的语音样本（或使用项目自带样本）

# cp your-voice.mp3 voice-sample.mp3

# 使用 FastAPI 启动 API
uvicorn app.main:app --host 0.0.0.0 --port 4123

# 或使用主脚本
python main.py
```

> 遇到问题？请查看 [troubleshooting section](https://github.com/travisvn/chatterbox-tts-api?tab=readme-ov-file#common-issues)

### 🐳 Docker（推荐）

```bash

# 克隆并用 Docker Compose 启动
git clone https://github.com/travisvn/chatterbox-tts-api
cd chatterbox-tts-api

# 使用针对 Docker 优化的环境变量
cp .env.example.docker .env  # Docker 专用路径，可直接使用

# 或：cp .env.example .env    # 本地开发路径，需要自行修改

# 选择部署方式：

# 仅 API（默认）
docker compose -f docker/docker-compose.yml up -d             # 标准版（基于 pip）
docker compose -f docker/docker-compose.uv.yml up -d          # uv 优化版（构建更快）
docker compose -f docker/docker-compose.gpu.yml up -d         # 标准版 + GPU
docker compose -f docker/docker-compose.uv.gpu.yml up -d      # uv + GPU（GPU 用户推荐）
docker compose -f docker/docker-compose.cpu.yml up -d         # 仅 CPU

# API + Frontend（在以上任一命令后加 --profile frontend）
docker compose -f docker/docker-compose.yml --profile frontend up -d             # 标准版 + Frontend
docker compose -f docker/docker-compose.gpu.yml --profile frontend up -d         # GPU + Frontend
docker compose -f docker/docker-compose.uv.gpu.yml --profile frontend up -d      # uv + GPU + Frontend

# 查看初始化日志（第一次使用 TTS 最慢）
docker logs chatterbox-tts-api -f

# 测试 API
curl -X POST http://localhost:4123/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello from Chatterbox TTS!"}' \
  --output test.wav
```

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>**🚀 使用前端界面运行**</summary>

该项目包含一个可选的 React Web UI。你可以通过 Docker Compose profile 方便地选择是否启用前端：

### 使用 Docker Compose Profiles

```bash

# 仅 API（默认行为）
docker compose -f docker/docker-compose.yml up -d

# API + Frontend + Web UI（添加 --profile frontend）
docker compose -f docker/docker-compose.yml --profile frontend up -d

# 或者使用辅助脚本启动完整栈：
python start.py fullstack

# 其他部署变体同理：
docker compose -f docker/docker-compose.gpu.yml --profile frontend up -d    # GPU + Frontend
docker compose -f docker/docker-compose.uv.yml --profile frontend up -d     # uv + Frontend
docker compose -f docker/docker-compose.cpu.yml --profile frontend up -d    # CPU + Frontend
```

### 本地开发

本地开发时，你可以分别运行 API 和前端：

```bash

# 先启动 API（按前文说明）

# 然后启动前端：
cd frontend && npm install && npm run dev
```

> **注意：** 如果遇到依赖问题，可尝试使用 `npm install --force` 代替普通 `npm install`。

根据 Vite 输出的链接打开 Web UI 即可。

### 生产构建

为生产部署构建前端：

```bash
cd frontend && npm install && npm run build
```

> **注意：** 如果构建因依赖冲突失败，也可以尝试 `npm install --force`。

构建完成后可直接通过本地文件系统中的 `/dist/index.html` 访问。

### 端口说明

- **仅 API**：通过 `http://localhost:4123` 访问
- **带 Frontend**：Web UI 位于 `http://localhost:4321`，API 请求通过反向代理转发

因此，当使用 `--profile frontend` 运行时，Web 界面位于 `http://localhost:4321`，而 API 则在代理后端运行。

</details>

## 配置 Open WebUI 使用 `Chatterbox TTS API`

我们建议你先带前端界面运行，这样可以先上传想克隆的声音文件，再去配置 Open WebUI。如果已按上文正确启动，可访问 `http://localhost:4321` 打开前端。

让 Open WebUI 使用 Chatterbox TTS API 的步骤如下：

- 打开 Admin Panel 并进入 `Settings` -> `Audio`
- 将 TTS 设置为：
- - Text-to-Speech Engine: OpenAI
  - API Base URL: `http://localhost:4123/v1` # 也可尝试 `http://host.docker.internal:4123/v1`
  - API Key: `none`
  - TTS Model: `tts-1` 或 `tts-1-hd`
  - TTS Voice: 你克隆出来的语音名称（也可使用前端中定义的别名）
  - Response splitting: `Paragraphs`

:::info

默认 API key 为字符串 `none`（无需真实 API key）

:::

![Screenshot of Open WebUI Admin Settings for Audio adding the correct endpoints for this project](https://lm17s1uz51.ufs.sh/f/EsgO8cDHBTOUjUe3QjHytHQ0xqn2CishmXgGfeJ4o983TUMO)

## 如果觉得这个项目有帮助，请为 [repo on GitHub](https://github.com/travisvn/chatterbox-tts-api) 点个 ⭐️

## 需要帮助？

Chatterbox 初次启动时可能比较折腾，如果某种安装方式不顺利，你可以尝试切换到其他安装路径。

如需了解更多 `chatterbox-tts-api` 信息，请访问其 [GitHub repo](https://github.com/travisvn/chatterbox-tts-api)。

- 📖 **文档**：参见 [API Documentation](https://github.com/travisvn/chatterbox-tts-api/blob/main/docs/API_README.md) 和 [Docker Guide](https://github.com/travisvn/chatterbox-tts-api/blob/main/docs/DOCKER_README.md)
- 💬 **Discord**：可加入该项目的 [Discord](http://chatterboxtts.com/discord)

## 故障排查

### 内存要求

Chatterbox 的内存要求高于其他 TTS 方案：
- **最低：** 4GB RAM
- **推荐：** 8GB+ RAM
- **GPU：** 推荐使用 NVIDIA CUDA 或 Apple M 系列（MPS）

如果你有内存问题，可考虑改用更轻量的方案，例如 [OpenAI Edge TTS](/features/chat-conversations/audio/text-to-speech/openai-edge-tts-integration) 或 [Kokoro-FastAPI](/features/chat-conversations/audio/text-to-speech/Kokoro-FastAPI-integration)。

### Docker 网络

如果 Open WebUI 无法连接 Chatterbox：

- **Docker Desktop：** 使用 `http://host.docker.internal:4123/v1`
- **Docker Compose：** 使用 `http://chatterbox-tts-api:4123/v1`
- **Linux：** 使用宿主机 IP 地址

### 首次启动

第一次 TTS 请求通常会更慢，因为模型需要先加载。可使用以下命令查看日志：

```bash
docker logs chatterbox-tts-api -f
```

更多排查建议请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。
