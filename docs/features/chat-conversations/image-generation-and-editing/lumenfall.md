---
sidebar_position: 7
title: "Lumenfall"
---

:::warning
本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。
:::

Open WebUI 还支持通过 [Lumenfall](https://lumenfall.ai) 进行图像生成。Lumenfall 是一个 AI 媒体网关，可将多个提供商上的主流图像模型统一为兼容 OpenAI 的 API，并提供免费模型可用。

## 初始设置

1. 在 [lumenfall.ai](https://lumenfall.ai) 注册一个免费账号
2. 在你的 [仪表盘](https://lumenfall.ai/app/api_keys) 中生成 API 密钥

## 配置图像生成

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `图像生成引擎` 设置为 `Open AI`（Lumenfall 使用与 OpenAI 相同的语法）
3. 将 API 端点 URL 改为 `https://api.lumenfall.ai/openai/v1`
4. 输入你的 Lumenfall API 密钥
5. API 版本可留空
6. 输入你想使用的模型，例如：`gemini-3-pro-image`、`gpt-image-1.5` 或 `flux.2-max`。完整模型列表请参阅 [lumenfall.ai/models](https://lumenfall.ai/models)
7. 设置图像尺寸（例如 `1024x1024`）。支持的尺寸取决于模型；如果不确定，`1024x1024` 对大多数模型都可用

![已使用 Lumenfall 配置好的 Open WebUI 图像设置页面截图。](/images/image-generation-and-editing/lumenfall-settings.png)

## 配置图像编辑

Lumenfall 也通过同一套 API 支持图像编辑：

1. 在同一 **Images** 设置页中，向下滚动到 **Edit Image** 部分
2. 打开 **图像编辑** 开关
3. 将 `图像编辑引擎` 设置为 `Open AI`
4. 输入相同的 API 端点 URL：`https://api.lumenfall.ai/openai/v1`
5. 输入你的 Lumenfall API 密钥
6. 选择一个支持编辑的模型（例如 `gpt-image-1.5`）

更多说明请参阅 [Lumenfall 文档](https://docs.lumenfall.ai/integrations/openwebui)。
