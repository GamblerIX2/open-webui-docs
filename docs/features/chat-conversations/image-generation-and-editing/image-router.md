---
sidebar_position: 6
title: "Image Router"
---

:::warning
本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。
:::

Open WebUI 也支持通过 **Image Router API** 进行图像生成。Image Router 是一个 [开源](https://github.com/DaWe35/image-router) 图像生成代理，可将大多数流行模型统一封装为单一 API。

## 初始设置

1. 从 Image Router 获取一个 [API 密钥](https://imagerouter.io/api-keys)

### 配置 Open WebUI

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `图像生成引擎` 设置为 `Open AI`（Image Router 使用与 OpenAI 相同的语法）
3. 将 API 端点 URL 改为 `https://api.imagerouter.io/v1/openai`
4. 输入你的 Image Router API 密钥
5. 输入你想使用的模型名称。**不要**使用下拉框选择模型，请直接手动输入模型名。更多信息请参阅 [查看全部模型](https://imagerouter.io/models)

![Open WebUI 图像设置页面截图，已选中 Open AI，并高亮显示 API 端点 URL、API 密钥和模型字段，用于 Image Router 配置。](/images/image-generation-and-editing/image-router-settings.png)
