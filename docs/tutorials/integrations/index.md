---
sidebar_position: 0
title: "集成"
---

# 🔌 集成教程

**将 Open WebUI 连接到 LLM 提供商、开发工具、监控平台与外部服务。**

这些由社区贡献的指南覆盖了具体集成场景，并提供分步说明。关于认证与 SSO 集成，请参阅 [认证与 SSO](../auth-sso)。

---

### LLM 提供商

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Azure OpenAI（Entra ID）](./llm-providers/azure-openai) | 通过 Entra ID 对 Azure OpenAI 实现无密钥认证 | 👤 管理员 · ⏱️ 30–60 分钟 |
| [DeepSeek R1 Dynamic](./llm-providers/deepseekr1-dynamic) | 通过 llama.cpp 运行完整 671B DeepSeek-R1 模型 | 👤 开发者 · ⏱️ 45 分钟 |
| [Intel GPU（IPEX-LLM）](./llm-providers/ipex_llm) | 在 Intel GPU 上使用 IPEX-LLM 加速 Ollama | 👤 开发者 · ⏱️ 20 分钟 |

---

### 监控与可观测性

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Helicone](./monitoring/helicone) | 记录并监控 LLM API 调用、成本与延迟 | 👤 管理员 · ⏱️ 15 分钟 |
| [Langfuse](./monitoring/langfuse) | 追踪 LLM 使用情况并评估提示词质量 | 👤 管理员 · ⏱️ 20 分钟 · ⚠️ 可能过时 |

---

### 开发工具

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Continue.dev](./dev-tools/continue-dev) | 将 Open WebUI 作为 Continue VS Code 扩展的后端 | 👤 开发者 · ⏱️ 15 分钟 |
| [Jupyter Notebooks](./dev-tools/jupyter) | 通过 Open WebUI 代码解释器运行代码并创建 Notebook | 👤 开发者 · ⏱️ 20 分钟 |
| [iTerm2](./dev-tools/iterm2) | 在 macOS 终端中调用 Open WebUI 模型 | 👤 开发者 · ⏱️ 10 分钟 |
| [Firefox Sidebar](./dev-tools/firefox-sidebar) | 将 Open WebUI 固定到 Firefox 内置 AI 侧栏 | 👤 用户 · ⏱️ 5 分钟 |
| [Browser Search Engine](./dev-tools/browser-search-engine) | 将 Open WebUI 添加为自定义浏览器搜索引擎 | 👤 用户 · ⏱️ 5 分钟 |

---

### 外部服务

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Notion（MCP）](./mcp-notion) | 通过 Model Context Protocol 连接 Notion | 👤 用户 · ⏱️ 5 分钟 |
| [OneDrive 与 SharePoint](./onedrive-sharepoint) | 将 Microsoft 365 文档接入 Open WebUI | 👤 管理员 · ⏱️ 30 分钟 |
| [LibreTranslate](./libre-translate) | 增加自托管翻译能力 | 👤 管理员 · ⏱️ 15 分钟 |
