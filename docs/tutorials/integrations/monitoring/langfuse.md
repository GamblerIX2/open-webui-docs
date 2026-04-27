---
sidebar_position: 20
title: "Langfuse ⚠️"
---

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看贡献教程。

:::

:::danger

该教程已被标记为 **已过时（OUTDATED）**。
在较新版本的 Open WebUI 或 Langfuse 中可能无法正常工作。

欢迎通过提交 PR 帮助更新本教程：[https://github.com/open-webui/docs](https://github.com/open-webui/docs)

:::

## 在 Open WebUI 中集成 Langfuse

[Langfuse](https://langfuse.com/)（[GitHub](https://github.com/langfuse/langfuse)）为 Open WebUI 提供开源可观测性与评估能力。启用 Langfuse 集成后，你可以追踪应用数据，用于开发、监控和优化 Open WebUI 的使用效果，包括：

- 应用[追踪（traces）](https://langfuse.com/docs/tracing)
- 使用模式
- 按用户和模型统计的成本数据
- 会话回放用于问题排查
- [评估（Evaluations）](https://langfuse.com/docs/scores/overview)

## 如何将 Langfuse 集成到 Open WebUI

![Langfuse Integration](https://langfuse.com/images/docs/openwebui-integration.gif)
*Langfuse 集成步骤*

Open WebUI 的 [Pipelines](https://github.com/open-webui/pipelines/) 是一个与 UI 无关的 OpenAI API 插件框架。它支持注入插件来拦截、处理并转发用户提示词到最终 LLM，从而增强对提示词处理流程的控制与定制能力。

要通过 Langfuse 追踪应用数据，你可以使用 [Langfuse pipeline](https://github.com/open-webui/pipelines/blob/039f9c54f8e9f9bcbabde02c2c853e80d25c79e4/examples/filters/langfuse_v3_filter_pipeline.py)，它可实现对消息交互的实时监控与分析。

## 快速开始

### 第 1 步：准备 Open WebUI

请先确保 Open WebUI 已在运行。可参考 [Open WebUI 文档](https://docs.openwebui.com/)。

### 第 2 步：部署 Pipelines

使用 Docker 启动 [Pipelines](https://github.com/open-webui/pipelines/)。可执行以下命令：

```bash
docker run -p 9099:9099 --add-host=host.docker.internal:host-gateway -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main
```

### 第 3 步：连接 Open WebUI 与 Pipelines

在 *Admin Settings* 中，新建并保存一个 OpenAI API 类型连接，参数如下：

- **URL:** `http://host.docker.internal:9099`（即前面启动的 Docker 容器地址）。
- **Password:** 0p3n-w3bu!（默认密码）

![Open WebUI Settings](https://langfuse.com/images/docs/openwebui-setup-settings.png)

### 第 4 步：添加 Langfuse 过滤 Pipeline

然后进入 *Admin Settings*->*Pipelines* 并添加 Langfuse Filter Pipeline。将 Pipelines 监听地址设为 `http://host.docker.internal:9099`（与前文一致），并通过 *Install from Github URL* 使用下方 URL 安装 [Langfuse Filter Pipeline](https://github.com/open-webui/pipelines/blob/039f9c54f8e9f9bcbabde02c2c853e80d25c79e4/examples/filters/langfuse_v3_filter_pipeline.py)：

```txt
https://github.com/open-webui/pipelines/blob/main/examples/filters/langfuse_v3_filter_pipeline.py
```

接着填入你的 Langfuse API key。若你尚未注册 Langfuse，可在[这里](https://cloud.langfuse.com)创建账号并获取 API key。

![Open WebUI add Langfuse Pipeline](https://langfuse.com//images/docs/openwebui-add-pipeline.png)

:::note

***说明：** 如果启用了流式输出，想统计 OpenAI 模型的使用量（token 计数），你需要进入 Open WebUI 的模型设置，在 *Capabilities* 下勾选 "Usage" [选项](https://github.com/open-webui/open-webui/discussions/5770#discussioncomment-10778586)。*

:::

### 第 5 步：在 Langfuse 中查看追踪

现在你可以与 Open WebUI 交互，并在 Langfuse 中看到追踪数据。

Langfuse UI 中的[追踪示例](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/904a8c1f-4974-4f8f-8a2f-129ae78d99c5?observation=fe5b127b-e71c-45ab-8ee5-439d4c0edc28)：

![Open WebUI Example Trace in Langfuse](https://langfuse.com/images/docs/openwebui-example-trace.png)

## 了解更多

如需更完整的 Open WebUI Pipelines 指南，可阅读[这篇文章](https://ikasten.io/2024/06/03/getting-started-with-openwebui-pipelines/)。
