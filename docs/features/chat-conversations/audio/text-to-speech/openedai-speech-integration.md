---
sidebar_position: 2
title: "使用 Docker 部署 Openedai-speech"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 通过 Docker 将 `openedai-speech` 集成到 Open WebUI

## 什么是 `openedai-speech`？

:::info

[openedai-speech](https://github.com/matatonic/openedai-speech) 是一个兼容 OpenAI audio/speech API 的文本转语音服务器。

它提供 `/v1/audio/speech` endpoint，可带来免费、私有且支持自定义声音克隆的文本转语音体验。该服务与 OpenAI 没有任何官方关联，也不需要 OpenAI API key。

:::

## 前置要求

- 系统已安装 Docker
- Open WebUI 正在 Docker 容器中运行
- 对 Docker 和 Docker Compose 有基本了解

## 方案 1：使用 Docker Compose

## 步骤 1：为 `openedai-speech` 服务创建新目录

创建一个新目录，例如 `openedai-speech-service`，用于存放 `docker-compose.yml` 和 `speech.env` 文件。

## 步骤 2：从 GitHub 克隆 `openedai-speech` 仓库

```bash
git clone https://github.com/matatonic/openedai-speech.git
```

这样会把 `openedai-speech` 仓库下载到本地，其中包含 Docker Compose 文件（`docker-compose.yml`、`docker-compose.min.yml`、`docker-compose.rocm.yml`）以及其他必要文件。

## 步骤 3：将 `sample.env` 改为 `speech.env`（可按需自定义）

在 `openedai-speech` 仓库目录中，创建一个名为 `speech.env` 的新文件，内容如下：

```yaml
TTS_HOME=voices
HF_HOME=voices

#PRELOAD_MODEL=xtts

#PRELOAD_MODEL=xtts_v2.0.2

#PRELOAD_MODEL=parler-tts/parler_tts_mini_v0.1

#EXTRA_ARGS=--log-level DEBUG --unload-timer 300

#USE_ROCM=1
```

## 步骤 4：选择 Docker Compose 文件

你可以使用下列任意一个 Docker Compose 文件：

- [docker-compose.yml](https://github.com/matatonic/openedai-speech/blob/main/docker-compose.yml)：使用 `ghcr.io/matatonic/openedai-speech` 镜像，并基于 [Dockerfile](https://github.com/matatonic/openedai-speech/blob/main/Dockerfile) 构建。
- [docker-compose.min.yml](https://github.com/matatonic/openedai-speech/blob/main/docker-compose.min.yml)：使用 `ghcr.io/matatonic/openedai-speech-min` 镜像，并基于 [Dockerfile.min](https://github.com/matatonic/openedai-speech/blob/main/Dockerfile.min) 构建。  
  这是一个最小版本，仅包含 Piper 支持，无需 GPU。
- [docker-compose.rocm.yml](https://github.com/matatonic/openedai-speech/blob/main/docker-compose.rocm.yml)：使用 `ghcr.io/matatonic/openedai-speech-rocm` 镜像，并基于 [Dockerfile](https://github.com/matatonic/openedai-speech/blob/main/Dockerfile) 在 ROCm 支持下构建。

## 步骤 4：构建所选 Docker 镜像

在运行 Docker Compose 文件之前，你需要先构建镜像：

- **Nvidia GPU（CUDA 支持）**：

```bash
docker build -t ghcr.io/matatonic/openedai-speech .
```

- **AMD GPU（ROCm 支持）**：

```bash
docker build -f Dockerfile --build-arg USE_ROCM=1 -t ghcr.io/matatonic/openedai-speech-rocm .
```

- **纯 CPU，无 GPU（仅 Piper）**：

```bash
docker build -f Dockerfile.min -t ghcr.io/matatonic/openedai-speech-min .
```

## 步骤 5：执行正确的 `docker compose up -d` 命令

- **Nvidia GPU（CUDA 支持）**：使用以下命令以 detached 模式启动 `openedai-speech`：

```bash
docker compose up -d
```

- **AMD GPU（ROCm 支持）**：使用以下命令以 detached 模式启动：

```bash
docker compose -f docker-compose.rocm.yml up -d
```

- **ARM64（Apple M 系列、树莓派）**：XTTS 在这里仅支持 CPU，速度会非常慢。你可以使用 Nvidia 镜像在 CPU 上跑 XTTS（仍然较慢），或使用仅 Piper 镜像（推荐）：

```bash
docker compose -f docker-compose.min.yml up -d
```

- **纯 CPU，无 GPU（仅 Piper）**：若你想使用更小的镜像（< 1GB，而不是 8GB）：

```bash
docker compose -f docker-compose.min.yml up -d
```

这会以 detached 模式启动 `openedai-speech` 服务。

## 方案 2：使用 Docker Run 命令

你也可以使用下列 Docker run 命令以 detached 模式启动 `openedai-speech`：

- **Nvidia GPU（CUDA）**：构建并启动服务：

```bash
docker build -t ghcr.io/matatonic/openedai-speech .
docker run -d --gpus=all -p 8000:8000 -v voices:/app/voices -v config:/app/config --name openedai-speech ghcr.io/matatonic/openedai-speech
```

- **ROCm（AMD GPU）**：构建并启动服务：

> 若要启用 ROCm 支持，请取消 `speech.env` 中 `#USE_ROCM=1` 这一行的注释。

```bash
docker build -f Dockerfile --build-arg USE_ROCM=1 -t ghcr.io/matatonic/openedai-speech-rocm .
docker run -d --privileged --init --name openedai-speech -p 8000:8000 -v voices:/app/voices -v config:/app/config ghcr.io/matatonic/openedai-speech-rocm
```

- **纯 CPU，无 GPU（仅 Piper）**：构建并启动服务：

```bash
docker build -f Dockerfile.min -t ghcr.io/matatonic/openedai-speech-min .
docker run -d -p 8000:8000 -v voices:/app/voices -v config:/app/config --name openedai-speech ghcr.io/matatonic/openedai-speech-min
```

## 步骤 6：配置 Open WebUI 使用 `openedai-speech` 进行 TTS

![openedai-tts](https://github.com/silentoplayz/docs/assets/50341825/ea08494f-2ebf-41a2-bb0f-9b48dd3ace79)

打开 Open WebUI 设置，进入 **Admin Panel > Settings > Audio** 下的 TTS 设置，并填写：

- **API Base URL**：`http://host.docker.internal:8000/v1`
- **API Key**：`sk-111111111`（这是一个占位 key，因为 `openedai-speech` 实际上不需要 API key。此字段只要填了任意值即可。）

## 步骤 7：选择语音

在同一音频设置菜单中的 `TTS Voice` 下，你可以为 `TTS Model` 选择 `openedai-speech` 支持的声音。以下声音主要针对英文优化：

- `tts-1` 或 `tts-1-hd`：`alloy`、`echo`、`echo-alt`、`fable`、`onyx`、`nova`、`shimmer`（`tts-1-hd` 可配置，默认使用 OpenAI 采样）

## 步骤 8：点击 `Save` 应用设置并开始使用自然语音

点击 `Save` 让设置生效。刷新页面后效果会完全应用，你就可以在 Open WebUI 中通过 `openedai-speech` 集成来朗读文本回复，获得更自然的 TTS 体验。

## 模型说明

`openedai-speech` 支持多种文本转语音模型，每种模型都有各自的特点和运行要求：

- **Piper TTS**（非常快，可在 CPU 上运行）：你可以通过 `voice_to_speaker.yaml` 配置文件接入自己的 [Piper voices](https://rhasspy.github.io/piper-samples/)。适合低延迟和高性能场景，并支持[多语言](https://github.com/matatonic/openedai-speech#multilingual)语音。
- **Coqui AI/TTS XTTS v2**（速度较快，但需要约 4GB GPU 显存和支持 CUDA 的 Nvidia GPU）：使用 Coqui AI 的 XTTS v2 声音克隆技术生成高质量语音。尽管需要更强 GPU，但音质与性能都很优秀，也支持[多语言](https://github.com/matatonic/openedai-speech#multilingual)语音。
- **Beta Parler-TTS Support**（实验性，较慢）：基于 Parler-TTS 生成语音。虽然目前仍处于 beta，但可以用文字描述说话者的基础特征。每次生成的声音会略有差异，但通常会接近描述内容。你可以参考 [Text Description to Speech](https://www.text-description-to-speech.com/) 获取灵感。

## 故障排查

如果你在将 `openedai-speech` 集成到 Open WebUI 时遇到问题，请尝试以下排查步骤：

- **确认 `openedai-speech` 服务已运行**：检查服务是否正在运行，以及 `docker-compose.yml` 中指定的端口是否已暴露。
- **检查 `host.docker.internal` 是否可访问**：确认 Open WebUI 容器内部能够解析 `host.docker.internal`。因为 `openedai-speech` 暴露在你电脑的 `localhost` 上，而 `open-webui` 容器默认无法直接访问宿主机 `localhost`。必要时可在 `docker-compose.yml` 中添加卷挂载，或调整网络方式。
- **检查 API key 配置**：确认 API key 已填为任意占位值，或确保没有因未填写而被拒绝。
- **检查语音配置**：确认你要使用的 TTS 语音确实存在于 `voice_to_speaker.yaml` 中，且对应文件（如 voice XML）位于正确目录。
- **确认语音模型路径正确**：如果语音模型加载失败，请再次核对 `voice_to_speaker.yaml` 中的路径是否与实际文件位置一致。

## 额外排查建议

- 查看 openedai-speech 日志中的报错或警告
- 核对 `docker-compose.yml` 是否适合你的环境
- 若仍有问题，可尝试重启 `openedai-speech` 服务或整个 Docker 环境
- 如果问题持续存在，请查看 `openedai-speech` GitHub 仓库或相关社区论坛

### GPU 内存问题（XTTS）

如果 XTTS 加载失败或出现 OOM：
- XTTS 大约需要 4GB GPU 显存
- 可改用仅 Piper 的最小镜像（`docker-compose.min.yml`），在 CPU 上运行
- 启动容器前先减少其他 GPU 占用

### AMD GPU（ROCm）说明

使用 AMD GPU 时：
1. 取消 `speech.env` 中 `USE_ROCM=1` 的注释
2. 使用 `docker-compose.rocm.yml`
3. 确保宿主机已正确安装 ROCm 驱动

### ARM64 / Apple Silicon

- XTTS 在 ARM64 上仅支持 CPU，**会非常慢**
- 对 ARM 设备建议使用 Piper-only 镜像（`docker-compose.min.yml`）
- Apple M 系列可用，但更适合使用最小镜像

### 容器网络

如果你使用 Docker 网络：
```yaml
# Add to your Docker Compose
networks:
  webui-network:
    driver: bridge
```

然后使用 `http://openedai-speech:8000/v1`，而不是 `localhost`。

更多排查建议请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。

## FAQ

**如何控制生成语音的情绪表现？**

目前没有直接的方法控制输出语音的情绪。某些因素（例如大写、语法）可能会影响结果，但内部测试显示效果并不稳定。

**语音文件存在哪里？配置文件呢？**

定义可用语音及其属性的配置文件存放在 config volume 中。默认语音配置定义在 `voice_to_speaker.default.yaml`。

## 其他资源

如需了解更多 Open WebUI 与 `openedai-speech` 的配置方式（包括环境变量），请参阅 [Open WebUI documentation](https://docs.openwebui.com/reference/env-configuration#text-to-speech)。

如需了解更多 `openedai-speech` 本身的信息，请访问其 [GitHub repository](https://github.com/matatonic/openedai-speech)。

**如何为 openedai-speech 添加更多声音：**
[Custom-Voices-HowTo](https://github.com/matatonic/openedai-speech?tab=readme-ov-file#custom-voices-howto)

:::note

你可以把 `docker-compose.yml` 中的端口改成任意空闲可用端口，但别忘了同步更新 Open WebUI Admin Audio 设置里的 **API Base URL**。

:::
