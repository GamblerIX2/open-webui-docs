---
sidebar_position: 2
title: "Kokoro Web - Open WebUI 的轻量 TTS 集成"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 什么是 `Kokoro Web`？

[Kokoro Web](https://github.com/eduardolat/kokoro-web) 为强大的 [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) 文本转语音模型提供了一个轻量、兼容 OpenAI 的 API，可与 Open WebUI 无缝集成，为 AI 对话带来自然流畅的语音。

## 🚀 两步完成集成

### 1. 部署 Kokoro Web API（一个命令）

```yaml
services:
  kokoro-web:
    image: ghcr.io/eduardolat/kokoro-web:latest
    ports:
      - "3000:3000"
    environment:
      # 改成你自己的任意密钥，作为 OpenAI 兼容 API key 使用
      - KW_SECRET_API_KEY=your-api-key
    volumes:
      - ./kokoro-cache:/kokoro/cache
    restart: unless-stopped
```

运行：`docker compose up -d`

### 2. 连接 OpenWebUI（30 秒）

1. 在 OpenWebUI 中进入 `Admin Panel` → `Settings` → `Audio`
2. 按如下方式配置：
   - Text-to-Speech Engine：`OpenAI`
   - API Base URL：`http://localhost:3000/api/v1`
     （如果使用 Docker：`http://host.docker.internal:3000/api/v1`）
   - API Key：`your-api-key`（来自步骤 1）
   - TTS Model：`model_q8f16`（体积 / 音质平衡最佳）
   - TTS Voice：`af_heart`（默认温暖自然的英文声音）。你也可以切换为 [Kokoro Web Demo](https://voice-generator.pages.dev) 中的其他语音或公式

**完成！你的 OpenWebUI 现在已经具备 AI 语音能力。**

## 🌍 支持的语言

Kokoro Web 支持 8 种语言，并为每种语言提供优化语音：

- 英语（美国）- en-us
- 英语（英国）- en-gb
- 日语 - ja
- 中文 - cmn
- 西班牙语 - es-419
- 印地语 - hi
- 意大利语 - it
- 葡萄牙语（巴西）- pt-br

每种语言都有专门语音，以获得更好的发音和自然度。完整语言专属语音列表请查看 [GitHub repository](https://github.com/eduardolat/kokoro-web)，或直接使用 [Kokoro Web Demo](https://voice-generator.pages.dev) 试听并创建自定义语音。

## 💾 针对不同硬件优化的模型

你可以根据硬件条件选择合适模型：

| Model ID | Optimization | Size | Ideal For |
|----------|-------------|------|-----------|
| model_q8f16 | 混合精度 | 86 MB | **推荐** - 平衡最佳 |
| model_quantized | 8-bit | 92.4 MB | CPU 表现较好 |
| model_uint8f16 | 混合精度 | 114 MB | 中端 CPU 上质量更好 |
| model_q4f16 | 4-bit 与 fp16 权重 | 154 MB | 音质更高，仍较高效 |
| model_fp16 | fp16 | 163 MB | 高品质 |
| model_uint8 | 8-bit 与混合 | 177 MB | 均衡方案 |
| model_q4 | 4-bit matmul | 305 MB | 高质量方案 |
| model | fp32 | 326 MB | 最高质量（更慢） |

## ✨ 安装前先试听

访问 [**Kokoro Web Demo**](https://voice-generator.pages.dev) 可立即试听全部语音。这个 Demo：

- **100% 在浏览器中运行** —— 无需服务器
- **免费使用** —— 无使用限制，无需注册
- **零安装** —— 打开网页即可开始
- **包含全部功能** —— 可立即测试任意语音或语言

## 还需要更多帮助？

如需更多选项、语音定制指南或高级设置，请访问 [GitHub repository](https://github.com/eduardolat/kokoro-web)。

## 故障排查

### 连接问题

如果 Open WebUI 无法访问 Kokoro Web：

- **Docker Desktop（Windows/Mac）：** 使用 `http://host.docker.internal:3000/api/v1`
- **Docker Compose（同一网络）：** 使用 `http://kokoro-web:3000/api/v1`
- **Linux Docker：** 使用宿主机 IP 地址

### 语音无法工作

1. 确认 Kokoro Web 配置和 Open WebUI 设置中的 secret API key 一致
2. 直接测试 API：
   ```bash
   curl -X POST http://localhost:3000/api/v1/audio/speech \
     -H "Authorization: Bearer your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"input": "Hello world", "voice": "af_heart"}'
   ```

更多排查建议请参阅 [Audio Troubleshooting Guide](/troubleshooting/audio)。

**祝你在 OpenWebUI 对话中享受自然的 AI 语音体验！**
