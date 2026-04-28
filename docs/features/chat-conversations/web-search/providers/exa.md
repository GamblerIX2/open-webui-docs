---
sidebar_position: 5
title: "Exa AI"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [Environment Configuration documentation](/reference/env-configuration#web-search)。

:::

:::tip Troubleshooting

如果你在 web search 上遇到问题，请查看 [Web Search Troubleshooting Guide](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

# Exa AI Web Search 集成

本指南说明如何将 [Exa AI](https://exa.ai/)——一个现代化、AI 驱动的搜索引擎——集成到 Open WebUI 中，以提供 web search 能力。

## 概览

Exa AI 是一个面向 AI 应用设计的搜索引擎，它通过 API 提供一整套能力，包括网页搜索、网站抓取与深度研究等。将 Exa AI 集成到 Open WebUI 后，你就可以直接在聊天界面中利用其强大的搜索能力。

## 计费模式

Exa AI 采用按 credit 计费、按量付费模式。它不是永久免费服务，但会为新用户提供试用额度以便评估 API。

- **初始免费额度：** 新用户会获得价值 10 美元的初始 credits，用于测试 API
- **按量付费：** 初始 credits 用完后，你需要升级到付费计划才能继续使用。免费额度仅用于评估，不包含固定的每月免费配额

有关最新且详细的价格信息，请参阅 [Exa AI pricing page](https://exa.ai/pricing)。

## 配置步骤

### 1. 获取 Exa AI API Key

首先，你需要注册一个 Exa AI 账号并获取 API key。

1.  **注册：** 前往 [Exa AI website](https://exa.ai/) 并创建一个新账号
2.  **进入 API Keys 页面：** 注册并登录后，在用户 dashboard 中进入 **API Keys** 页面
3.  **复制你的 API Key：** 在 API Keys 页面中，你会看到自己的专属 API key。复制它，稍后配置 Open WebUI 时会用到

### 2. 配置 Open WebUI

接下来，在 Open WebUI 的管理员设置中配置 Exa AI 集成。

1.  **使用管理员账号登录：** 进入你的 Open WebUI 实例，并以管理员账号登录
2.  **进入 Web Search 设置：** 前往 **Admin Panel**，然后点击 **Settings** > **Web Search**
3.  **将搜索引擎设为 Exa：** 在 “Web Search Engine” 下拉菜单中选择 **Exa**
4.  **填写 API Key：** 在出现的 **Exa API Key** 输入框中，粘贴你从 Exa AI dashboard 复制的 API key
5.  **保存更改：** 向下滚动并点击 **Save**

### 3.（可选）使用环境变量配置

你也可以使用环境变量配置 Exa AI 集成。这在 Docker 部署中尤其方便。

为你的 Open WebUI 实例设置以下环境变量：

- `EXA_API_KEY`：你的 Exa AI API key

设置后，管理员设置中的 “Exa API Key” 字段会自动填充。

**示例 Docker `run` 命令：**

```bash
docker run -d \\
  -p 3000:8080 \\
  -e EXA_API_KEY="your-exa-api-key-here" \\
  --name open-webui \\
  ghcr.io/open-webui/open-webui:main
```

## 验证集成

配置好 API key 后，你可以在聊天中启用 web search，并提出一个需要最新网页信息的问题来测试。如果集成成功，Open WebUI 就会使用 Exa AI 获取搜索结果，并据此返回更有依据的回答。
