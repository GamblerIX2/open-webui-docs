---
sidebar_position: 2
title: "Kokoro-FastAPI Using Docker"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 什么是 `Kokoro-FastAPI`？

[Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) 是 [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) 文本转语音模型的 Docker 化 FastAPI 封装，实现了 OpenAI API endpoint 规范，并提供高性能的文本转语音能力。

## 主要特性

- 兼容 OpenAI Speech endpoint，支持内联语音组合
- 支持 NVIDIA GPU 加速或 CPU ONNX 推理
- 支持流式输出与可变分块
- 支持多种音频格式（`.mp3`、`.wav`、`.opus`、`.flac`、`.aac`、`.pcm`）
- 集成 Web 界面，默认位于 localhost:8880/web（仓库中也提供了额外 gradio 容器）
- 提供音素转换与生成功能 endpoint

## Voices

- af
- af_bella
- af_irulan
- af_nicole
- af_sarah
- af_sky
- am_adam
- am_michael
- am_gurney
- bf_emma
- bf_isabella
- bm_george
- bm_lewis

## Languages

- en_us
- en_uk

## 前置要求

- 系统已安装 Docker
- Open WebUI 正在运行
- 若使用 GPU：需要支持 CUDA 12.3 的 NVIDIA GPU
- 若仅 CPU：无特殊要求

## ⚡️ 快速开始

### 你可以选择 GPU 或 CPU 版本

### GPU 版本（需要支持 CUDA 12.8 的 NVIDIA GPU）

使用 docker run：

```bash
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu
```

或者创建 `docker-compose.yml` 后用 docker compose 启动。例如：

```yaml
name: kokoro
services:
    kokoro-fastapi-gpu:
        ports:
            - 8880:8880
        image: ghcr.io/remsky/kokoro-fastapi-gpu:v0.2.1
        restart: always
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: all
                          capabilities:
                              - gpu
```

:::info

你可能需要先安装并配置 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

:::

### CPU 版本（ONNX 优化推理）

使用 docker run：

```bash
docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu
```

使用 docker compose：

```yaml
name: kokoro
services:
    kokoro-fastapi-cpu:
        ports:
            - 8880:8880
        image: ghcr.io/remsky/kokoro-fastapi-cpu
        restart: always
```

## 配置 Open WebUI 使用 `Kokoro-FastAPI`

按照以下步骤让 Open WebUI 使用 Kokoro-FastAPI：

- 打开 Admin Panel 并进入 `Settings` -> `Audio`
- 将 TTS 设置为：
- - Text-to-Speech Engine: OpenAI
  - API Base URL: `http://localhost:8880/v1` # 也可能需要改成 `host.docker.internal`
  - API Key: `not-needed`
  - TTS Voice: `af_bella` # 也接受现有 OAI voice 的映射值以保持兼容
  - TTS Model: `kokoro`

:::info

默认 API key 字符串是 `not-needed`。如果你不需要额外安全控制，可以保持不变。

:::

## 构建 Docker 容器

```bash
git clone https://github.com/remsky/Kokoro-FastAPI.git
cd Kokoro-FastAPI
cd docker/cpu # 或 docker/gpu
docker compose up --build
```

**就是这么简单！**

如需了解构建容器、修改端口等更多信息，请参阅 [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) 仓库。

## 故障排查

### 未检测到 NVIDIA GPU

如果 GPU 版本没有使用到你的显卡：

1. **安装 NVIDIA Container Toolkit：**
   ```bash
   # Ubuntu/Debian
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

2. **验证 GPU 可访问：**
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.2.0-base nvidia-smi
   ```

### 从 Open WebUI 连接失败

如果 Open WebUI 无法访问 Kokoro：

- 使用 `host.docker.internal:8880` 代替 `localhost:8880`（Docker Desktop）
- 如果两者都在 Docker Compose 中，使用 `http://kokoro-fastapi-gpu:8880/v1`
- 确认服务正在运行：`curl http://localhost:8880/health`

### CPU 版本性能

CPU 版本使用 ONNX 优化，对大多数场景已经够用。如果你仍然关心速度：

- 可升级到 GPU 版本
- 确保 CPU 上没有其他重负载进程
- 对于没有兼容 NVIDIA GPU 的系统，CPU 版仍是推荐选择

更多排查建议请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。
