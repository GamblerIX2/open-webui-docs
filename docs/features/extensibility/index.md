---
sidebar_position: 0
title: "可扩展性"
---

# 🔌 可扩展性

**用 Python、HTTP 或一键安装的社区插件，让 Open WebUI 做任何事情。**

Open WebUI 内置了强大的默认功能，但你的工作流并不是"默认"的。可扩展性就是弥补这一差距的方式：为模型提供实时数据、强制执行合规规则、添加新的 AI 提供商，或连接到任意外部服务。写几行 Python、指向一个 OpenAPI 端点，或浏览社区库，平台适应你，而不是反过来。

系统分为三层，大多数团队最终会用到其中至少两层：

- **进程内 Python**（Tools & Functions）直接在 Open WebUI 内部运行，无需额外基础设施，可即时迭代。
- **外部 HTTP**（OpenAPI & MCP 服务器）连接到任意位置运行的服务，从 sidecar 容器到第三方 SaaS。
- **Pipeline 工作进程**（Pipelines）将繁重或敏感的处理卸载到独立容器，保持主实例高效、轻量。

---

## 为什么需要可扩展性？

### 赋予模型真实世界的能力

开箱即用的 LLM 只能处理训练数据和当前对话中的内容。Tools 让它能够向外延伸：查看天气、查询数据库、调用 API、执行计算。模型根据对话上下文决定何时使用某个工具，你只需提供该能力即可。

### 连接任意外部服务

拥有内部 API？有 OpenAPI 规范的第三方 SaaS？堆栈中已有 MCP 服务器？将规范指向 Open WebUI，它就会自动发现端点并将其暴露为模型可调用的工具，无需胶水代码，无需包装层。

### 控制每条消息

Functions 允许你在消息到达模型之前（输入过滤器）或到达用户之前（输出过滤器）拦截并转换消息。帮助脱敏 PII、强制格式化规则、记录到可观测平台、动态注入系统指令，这一切都无需修改模型配置。

### 卸载繁重处理

当插件需要 GPU 访问、大型依赖或隔离执行时，将其作为 Pipeline 在另一台机器上运行。Open WebUI 通过标准 API 与之通信，主实例保持精简。

### 从社区导入

从 Open WebUI 社区站点浏览数百个社区构建的 Tools 和 Functions，找到你需要的，点击**导入**即可上线。无需 `pip install`，无需重启。

---

## 核心功能

| | |
| :--- | :--- |
| 🐍 **Tools** | 赋予模型新能力的 Python 脚本：网络搜索、API 调用、代码执行 |
| ⚙️ **Functions** | 添加模型提供商（Pipes）、消息处理（Filters）或 UI 操作（Actions）的平台扩展 |
| 🔗 **MCP 支持** | 对 Model Context Protocol 服务器的原生 Streamable HTTP 支持 |
| 🌐 **OpenAPI 服务器** | 从任意 OpenAPI 兼容端点自动发现并暴露工具 |
| 🔧 **Pipelines** | 在独立工作进程上运行的模块化插件框架，适用于繁重或敏感处理 |
| 📝 **Skills** | 教导模型如何处理特定任务的 Markdown 指令集 |
| ⚡ **Prompts** | 带有类型化输入变量和版本控制的斜杠命令模板 |
| 🏪 **社区库** | 一键导入社区构建的 Tools 和 Functions |

---

## 架构概览

了解应使用哪一层可节省大量时间：

| 层 | 运行位置 | 最适合 | 权衡 |
|-------|-----------|----------|-----------|
| **Tools & Functions** | Open WebUI 进程内 | 实时数据、过滤器、UI 操作、新提供商 | 与主服务器共享资源 |
| **OpenAPI / MCP** | 任意 HTTP 端点 | 连接现有服务、第三方 API | 需要运行中的外部服务器 |
| **Pipelines** | 独立 Docker 容器 | GPU 工作负载、大型依赖、沙箱执行 | 需要额外管理基础设施 |

大多数用户从 **Tools & Functions** 开始。它们无需额外配置，内置代码编辑器，可覆盖绝大多数使用场景。

---

## 使用场景

### 实时数据丰富

销售团队构建一个查询 CRM API 的 Tool。当销售代表问"Acme 这个项目最新进展如何？"时，模型调用该工具，检索管道阶段、最后活动和交易金额，并综合出一份基于实时数据（而非陈旧训练知识）的简报。

### 企业合规过滤器

一家医疗机构部署了一个 Filter Function，用于扫描出站消息中的 PHI 模式（SSN、MRN、出生日期）。匹配项在响应到达用户之前被脱敏，原始内容被记录到其 SIEM 系统中。无需更改模型配置，过滤器在每次对话中透明运行。*（这是一个说明性示例，基于正则表达式的过滤可能无法捕获所有敏感数据模式。有合规要求的组织应独立验证过滤覆盖范围。）*

### 多提供商模型路由

工程团队使用 Pipe Functions 将 Anthropic、Google Vertex AI 和自托管的 vLLM 实例添加到现有的 Ollama 模型旁边。用户在单一模型选择器中看到所有提供商，无需单独登录，无需管理 API 密钥。

### 重计算 Pipeline

研究团队运行一个检索增强生成 Pipeline，使用需要 GPU 的交叉编码器模型进行重排序。他们将其部署为专用 GPU 节点上的 Pipeline，Open WebUI 自动将相关查询路由到该 Pipeline，同时主实例保持在普通硬件上运行。

---

## 限制

### 安全性

Tools、Functions 和 Pipelines 在服务器上执行**任意 Python 代码**。请只安装来自可信来源的扩展，导入前审查代码，并将工作区访问权限限制给管理员。详情参见[安全政策](/security)。

### 资源共享

进程内的 Tools 和 Functions 与 Open WebUI 共享 CPU 和内存。计算密集型插件应移至 Pipelines 或外部服务。

### MCP 传输

原生 MCP 支持仅限 **Streamable HTTP**。对于基于 stdio 或 SSE 的 MCP 服务器，请使用 [mcpo](https://github.com/open-webui/mcpo) 作为转换代理。

---

## 深入了解

| 主题 | 你将学到什么 |
|-------|-------------------|
| [**Tools & Functions**](plugin) | 编写 Python Tools、Functions（Pipes、Filters、Actions）及开发 API |
| [**MCP**](mcp) | 连接 Model Context Protocol 服务器、OAuth 设置、故障排查 |
| [**Pipelines**](pipelines) | 部署 Pipeline 工作进程、构建自定义 Pipeline、目录结构 |
