---
sidebar_position: 7
title: "Jina"
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

# Jina Web Search 集成

本指南说明如何将 [Jina AI](https://jina.ai/) 这一强大的 AI 搜索基础设施集成到 Open WebUI 中。该集成使用 Jina 的 `DeepSearch` API 提供 web search 能力。

## 概览

Jina AI 的 `DeepSearch` 不只是一个简单搜索 API；它更像是一个自主 agent，能够结合网页搜索、阅读和推理来完成深入研究。与依赖预训练知识的标准 LLM，或仅执行单轮搜索的 RAG 系统不同，DeepSearch 会循环执行搜索、阅读与推理，并根据过程中发现的信息动态决定下一步动作。它可以通过多轮搜索与推理深入探索主题，并在返回结果前自我评估答案质量。

:::tip OpenAI API 兼容性
Jina DeepSearch API 与 OpenAI Chat API schema 完全兼容。这意味着你只需将 API endpoint 替换为 `https://deepsearch.jina.ai/v1/chat/completions`，并使用 `jina-deepsearch-v1` 作为模型名，就可以在任何兼容 OpenAI 的客户端中使用它。
:::

## 价格与 API Key

在 Open WebUI 中使用 Jina 的 `DeepSearch` API 需要 API key。Jina 为新用户提供免费层，其中包含 **1000 万 tokens** 可用于任意模型。你可以通过在 Jina AI 平台创建账号来获取免费 API key。

- **API Key：** 需要一个 Jina API key。你可以在 [Jina API Dashboard](https://jina.ai/api-dashboard) 登录后获取

## 配置步骤

### 1. 获取 Jina API Key

获取 API key 的步骤如下：

1. **访问 Jina API Dashboard：** 前往 [jina.ai/api-dashboard](https://jina.ai/api-dashboard)
2. **登录或注册：** 创建新账号，或登录现有账号
3. **获取 API Key：** 登录后，你的专属 API key 会显示在 dashboard 上，将其复制保存

### 2. 配置 Open WebUI

要在 Open WebUI 中启用 Jina 搜索集成，请按以下步骤操作：

1. **以管理员身份登录：** 进入你的 Open WebUI 实例，并使用管理员账号登录
2. **进入 Web Search 设置：** 打开 **Admin Panel**，然后点击 **Settings** > **Web Search**
3. **将搜索引擎设为 Jina：** 在 “Web Search Engine” 下拉框中选择 **Jina**
4. **输入 API Key：** 将你的 Jina API key 粘贴到 **Jina API Key** 输入框中
5. **（可选）填写 Jina API Base URL：** 如果你需要使用某个特定 endpoint（例如欧盟数据处理节点），可在 **Jina API Base URL** 中填写；默认值为 `https://s.jina.ai/`
6. **保存更改：** 向下滚动并点击 **Save**

### 3. 环境变量配置

对于基于 Docker 的部署，你也可以通过环境变量配置 Jina 集成。

为 Open WebUI 实例设置以下环境变量：

- `JINA_API_KEY`：你的 Jina API key
- `JINA_API_BASE_URL`：（可选）自定义 Jina API endpoint

**示例 Docker `run` 命令：**

```bash
docker run -d \\
  -p 3000:8080 \\
  -e JINA_API_KEY="your-jina-api-key-here" \\
  --name open-webui \\
  ghcr.io/open-webui/open-webui:main
```

## 高级配置（Jina API）

虽然 Open WebUI 提供了直接可用的集成方式，但 Jina DeepSearch API 本身还提供了丰富参数，用于更细致地调整行为。这些参数属于 Jina API 层，并不会直接暴露在 Open WebUI 设置中，但了解它们对高级用法很有帮助。

### 质量控制

你可以通过以下参数控制“结果质量”与“token 消耗”之间的平衡：

- **`reasoning_effort`**：一个预设项，会自动调整 `budget_tokens` 和 `max_attempts`。可选值为 `low`、`medium`、`high`。这是最简单的质量控制方式
- **`budget_tokens`**：设置 DeepSearch 整个过程允许使用的最大 token 数。预算越高，通常回答质量越好
- **`max_attempts`**：系统尝试解决问题的重试次数
- **`team_size`**：并行处理问题的 agent 数量，用于拓宽研究范围

### 来源控制

你还可以控制 DeepSearch 从哪些来源获取信息：

- **`no_direct_answer`**：即使问题很简单，也强制系统始终搜索网页
- **`boost_hostnames`**：优先级更高的域名列表
- **`bad_hostnames`**：必须严格排除的域名列表
- **`only_hostnames`**：只允许包含的域名列表

更多说明请参阅 [official Jina DeepSearch documentation](https://jina.ai/deepsearch/)。

## 验证集成

配置完成后，你可以在聊天中启用 web search 并提问测试。此时 Open WebUI 会使用 Jina 的 `DeepSearch` 来检索与处理网页内容，并据此回答你的问题。
