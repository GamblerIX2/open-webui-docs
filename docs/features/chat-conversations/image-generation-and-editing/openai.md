---
sidebar_position: 4
title: "OpenAI"
---

:::warning
本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。
:::

Open WebUI 也支持通过 **OpenAI APIs** 进行图像生成。该方案可在 DALL·E 2、DALL·E 3 与 GPT-Image-1 之间选择，不同模型支持的图像尺寸也不同。

### 初始设置

1. 从 OpenAI 获取一个 [API key](https://platform.openai.com/api-keys)

### 配置 Open WebUI

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `Image Generation Engine` 设置为 `Open AI`
3. 输入你的 OpenAI API key
4. 选择你要使用的模型。请注意，可用图像尺寸会随模型变化：
   - **DALL·E 2**：支持 `256x256`、`512x512` 或 `1024x1024`
   - **DALL·E 3**：支持 `1024x1024`、`1792x1024` 或 `1024x1792`
   - **GPT-Image-1**：支持 `auto`、`1024x1024`、`1536x1024` 或 `1024x1536`

![Screenshot of the Open WebUI Images settings page with Open AI selected and the API key, model, and image size fields highlighted.](/images/image-generation-and-editing/openai-settings.png)

### Azure OpenAI

Open WebUI 同样支持 Azure OpenAI（DALL·E 或 GPT-Image）图像生成。配置方法如下：

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `Image Generation Engine` 设置为 `Open AI`（Azure OpenAI 使用与 OpenAI 相同的语法）
3. 将 API endpoint URL 改为 `https://<instance-id>.cognitiveservices.azure.com/openai/deployments/<model>/`。其中实例 ID 和模型 ID 可在 Azure AI Foundry 设置中找到
4. 将 API version 设置为你在 Azure AI Foundry 设置中看到的值
5. 输入你的 Azure OpenAI API key

![Screenshot of the Open WebUI Images settings page with Open AI selected and the API endpoint URL, API version, and API key fields highlighted for Azure OpenAI configuration.](/images/image-generation-and-editing/azure-openai-settings.png)

:::tip Azure GPT-Image-1.5 配置
若要在 Azure OpenAI 中成功使用 **gpt-image-1.5**，请使用以下设置：
- **Model**：`gpt-image-1.5`
- **Image Size**：`1024x1024`
- **API Version**：`2025-04-01-preview`
- **API Endpoint URL**：`https://<your-resource-name>.openai.azure.com/openai/deployments/<your-deployment-name>/`（请确保末尾保留 `/`）

如果你遇到 `[ERROR: azure-openai error: Unknown parameter: 'response_format'.]` 报错，请再次确认 API Version 是否为 `2025-04-01-preview` 或更高版本。
:::

:::tip
另一种 API endpoint URL 写法是：`https://<endpoint name>.openai.azure.com/openai/deployments/<model name>/` —— 其中 endpoint name 可在 https://ai.azure.com/resource/overview 找到，model name 可在 https://ai.azure.com/resource/deployments 找到。
你也可以直接复制部署详情页中的 Target URI，但记得删除模型名称后面的多余字符串。
例如，如果你的 Target URI 是 `https://test.openai.azure.com/openai/deployments/gpt-image-1/images/generations?api-version=2025-04-01-preview`，那么 Open WebUI 中应填写的 API endpoint URL 为 `https://test.openai.azure.com/openai/deployments/gpt-image-1/`。
:::

### 使用 OpenAI Endpoint 的 LiteLLM Proxy

Open WebUI 支持通过使用 OpenAI endpoints 的 LiteLLM proxy 进行图像生成。配置方法如下：

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `Image Generation Engine` 设置为 `Open AI`
3. 将 API endpoint URL 改为 `https://<your-litellm-url>:<port>/v1`
4. 输入你的 LiteLLM API key
5. API version 可留空
6. 输入你在 LiteLLM 配置中使用的图像模型名称
7. 将图像尺寸设置为该模型支持的尺寸之一

:::tip

若要查看 LiteLLM 连接信息，请前往 **Admin Panel** > **Settings** > **Connections**。
你的连接信息会显示在 OpenAI API connection 下方。

:::
