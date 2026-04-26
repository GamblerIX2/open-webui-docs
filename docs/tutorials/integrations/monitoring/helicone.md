---
title: "Helicone"
sidebar_position: 10
---

# 在 Open WebUI 中集成 Helicone

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看贡献教程。

:::

Helicone 是一个开源 LLM 可观测性平台，帮助开发者监控、调试并优化**生产就绪**应用，包括你的 Open WebUI 部署。

启用 Helicone 后，你可以记录 LLM 请求、评估和实验提示词，并快速获得洞察，帮助你更有信心地将变更推向生产环境。

- **跨模型类型统一实时监控**：在单一界面同时监控本地 Ollama 模型与云端 API
- **请求可视化与回放**：查看 Open WebUI 向各模型发送的提示词及 LLM 生成输出，便于评估
- **本地 LLM 性能跟踪**：衡量自托管模型的响应时间与吞吐量
- **按模型的使用分析**：对比 Open WebUI 中不同模型的使用模式
- **用户分析**：了解交互行为模式
- **调试能力**：排查模型响应问题
- **成本跟踪**：统计跨提供商的 LLM 使用成本

## 如何将 Helicone 集成到 OpenWebUI

<iframe
  width="560"
  height="315"
  src="https://www.youtube-nocookie.com/embed/8iVHOkUrpSA?si=Jt1GVqA0wY4UI7sF"
  title="YouTube video player"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen>
</iframe>

### 第 1 步：创建 Helicone 账号并生成 API key

创建 [Helicone 账号](https://www.helicone.ai/)并登录，生成 [API key](https://us.helicone.ai/settings/api-keys)。

*— 请务必生成 [write only API key](https://docs.helicone.ai/helicone-headers/helicone-auth)。这样可只允许写入日志数据到 Helicone，而不会授予读取你私有数据的权限。*

### 第 2 步：创建 OpenAI 账号并生成 API key

 创建 OpenAI 账号，并登录 [OpenAI Developer Portal](https://platform.openai.com/account/api-keys) 生成 API key。

### 第 3 步：使用 Helicone 的 base URL 运行 Open WebUI

首次启动 Open WebUI 时，可参考 [Open WebUI 文档](https://docs.openwebui.com/)中的命令，并加入 Helicone 的 API BASE URL，以便自动接入查询与监控。

```bash
  # 设置环境变量
   export HELICONE_API_KEY=<YOUR_API_KEY>
   export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

  # 启动集成 Helicone 的 Open WebUI
   docker run -d -p 3000:8080 \
     -e OPENAI_API_BASE_URL="https://oai.helicone.ai/v1/$HELICONE_API_KEY" \
     -e OPENAI_API_KEY="$OPENAI_API_KEY" \
     --name open-webui \
     ghcr.io/open-webui/open-webui
```

如果你已部署 Open WebUI，可进入 `Admin Panel` > `Settings` > `Connections`，点击 “Managing OpenAI API Connections” 的 `+` 号，并更新以下字段：

- `API Base URL` 设置为 ``https://oai.helicone.ai/v1/<YOUR_HELICONE_API_KEY>``
- `API KEY` 设置为你的 OpenAI API key。

![Open WebUI Helicone Setup](https://res.cloudinary.com/dacofvu8m/image/upload/v1745272273/openwebui-helicone-setup_y4ssca.gif)

### 第 4 步：确认监控正常工作

为确认集成成功，请登录 Helicone 控制台并查看 “Requests” 标签页。

你应能看到通过 Open WebUI 发起的请求已经记录在 Helicone 中。

![Example Helicone Trace](https://res.cloudinary.com/dacofvu8m/image/upload/v1745272747/CleanShot_2025-04-21_at_17.57.46_2x_wpkpyf.png)

## 了解更多

如需更完整的 Helicone 指南，可参考 [Helicone 官方文档](https://docs.helicone.ai/getting-started/quick-start)。
