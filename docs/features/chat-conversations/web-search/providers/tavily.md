---
sidebar_position: 17
title: "Tavily"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 [contributing tutorial](https://docs.openwebui.com/contributing)。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [Environment Configuration documentation](/reference/env-configuration#web-search)。

:::

:::tip Troubleshooting

如果你在 web search 上遇到问题，请查看 [Web Search Troubleshooting Guide](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## 概览

将 Tavily 集成到 Open WebUI 后，你的语言模型就可以执行实时网页搜索，从而获得最新、相关的信息。本教程将指导你把 Tavily 配置为 Open WebUI 的 web search provider。

Tavily 是一个针对 AI 应用优化的搜索 API，可返回经过整理和结构化的搜索结果。按照以下步骤配置后，Open WebUI 就能在聊天界面中利用 Tavily 执行网页搜索。

## 前提条件

请确保你具备：

- **已安装 Open WebUI**：一个可运行的 Open WebUI 实例（本地或 Docker）。参阅 [Getting Started guide](https://docs.openwebui.com/getting-started)
- **Tavily 账号**：以及来自 [Tavily](https://app.tavily.com/sign-in) 的 API key
- **管理员权限**：对 Open WebUI 实例具备管理权限
- **网络连接**：用于发起 Tavily API 请求
- **WEBUI_URL 环境变量**：已正确指向你的 Open WebUI 实例。参阅 [Environment Variable Configuration](https://docs.openwebui.com/environment)

## 分步配置

### 1. 获取 Tavily API Key

1. 在 [Tavily](https://app.tavily.com/sign-in) 注册或登录
2. 进入 **Dashboard** 或 **API Keys** 页面
3. 复制现有 key，或生成一个新的 API key，并妥善保存

> **注意：** 请在 [Tavily Pricing](https://tavily.com/#pricing) 页面查看你当前套餐的查询限制。

### 2. 配置 Open WebUI

1. 使用管理员账号登录 Open WebUI
2. 点击左下角 **user icon**，选择 **Settings**
3. 打开 **Web Search** 标签
4. 将 **Web Search** 切换为 **On**
5. 在 **Web Search Engine** 下拉框中选择 **tavily**
6. 将你的 Tavily API key 粘贴到 **Tavily API Key** 字段
7. （可选）按需调整最大搜索结果数等设置

> **提示：** 请确认 API key 正确无误，以避免配置错误。

### 3. 测试集成

1. 保存设置
2. 开启一段新的聊天
3. 点击提示词输入框中的 **plus (+)** 按钮以启用 web search
4. 输入一个查询（例如 `+latest AI news`），确认 Tavily 能返回实时结果

> **示例：** `+latest AI news` 会触发 Tavily 搜索，并将结果嵌入回复中。

## 可选配置

- **搜索参数**：更多高级选项（如域名过滤）请参阅 [Tavily API Documentation](https://docs.tavily.com/docs/introduction)
- **环境变量**：可在 `.env` 文件或 Docker 命令中设置 `TAVILY_API_KEY`：

  ```bash
  -e TAVILY_API_KEY="your_tavily_api_key"
  ```

  参阅 [Environment Variable Configuration](https://docs.openwebui.com/environment)
- **RAG 集成**：你可以将 Tavily 结果与本地数据结合，构建 Retrieval Augmented Generation 工作流。参阅 [RAG Documentation](https://docs.openwebui.com/features/chat-conversations/rag)

## 故障排查

- **API Key 无效**：确认复制的 key 没有多余空格
- **无搜索结果**：确认已启用 web search 开关（`+`）并且网络正常
- **额度耗尽**：在 [Tavily Pricing](https://tavily.com/#pricing) 查看套餐配额
- **设置未保存**：确认你有管理员权限，并且 `webui.db` 可写

若需进一步帮助，请访问 [Open WebUI Community](https://openwebui.com/search) 或 [Tavily Support](https://tavily.com/#contact)。

## 额外资源

- [Tavily API Documentation](https://docs.tavily.com/docs/introduction)：API 参考与高级选项
- [Open WebUI Features](https://docs.openwebui.com/features)：RAG 与 web search 说明
- [Contributing to Open WebUI](https://docs.openwebui.com/contributing)：提交改进或反馈问题

完成本教程后，你就成功在 Open WebUI 中启用了 Tavily web search，为 AI 提供实时网页数据。祝你搜索顺利！
