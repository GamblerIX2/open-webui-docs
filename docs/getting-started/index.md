---
sidebar_position: 100
title: "🚀 开始使用"
---

# 开始使用 Open WebUI

**从零开始，不到五分钟开启你的第一次 AI 对话。**

Open WebUI 几乎可以运行在任何环境中（Docker、Kubernetes、pip、裸机），并可开箱即用地连接 Ollama、兼容 OpenAI 的提供商以及 Open Responses 提供商。选择一种安装方式，连接一个提供商，然后直接开始聊天。

---

## ⏱️ 快速开始

**安装 Open WebUI，连接模型，立即开聊。**

这里汇集了搭建可用环境所需的一切内容。Docker 是最快的路径，Python 适合轻量部署，Kubernetes 适合生产编排。每份指南都包含如何连接你的第一个模型提供商。

| | |
| :--- | :--- |
| 🐳 **Docker** | 一条命令部署，官方推荐方案 |
| 📦 **Python (pip / uv)** | 适合低资源环境或手动部署的轻量安装方式 |
| ☸️ **Kubernetes (Helm)** | 适合扩展与编排的生产级方案 |
| 🖥️ **桌面应用** | 原生应用（实验性），无需 Docker |
| 🔌 **连接提供商** | Ollama、OpenAI、Anthropic、llama.cpp、vLLM 等 |
| ⚙️ **理解设置** | 了解管理员设置与用户设置如何协同工作 |

[**开始安装 →**](/getting-started/quick-start)

---

## ✨ 新用户必读

**已经安装并开始聊天了——接下来呢？**

五个简短部分，带你了解每位新用户最终都会想早点知道的事情：什么是插件、如何安装；为什么长对话最终会报错（以及如何用过滤器解决）；驱动标题与自动补全的“隐形” Task Model；如何开始基于自己文档做 RAG；以及如何启用原生工具调用。

| | |
| :--- | :--- |
| 🧩 **插件** | Tools、Pipes、Filters、Actions——完整扩展能力概览 |
| 🧠 **上下文管理** | 为什么长对话会撞墙，以及如何处理 |
| 🤖 **任务模型** | 让标题、标签和自动补全不再占用主模型 |
| 📚 **基础 RAG** | 与你自己的文档对话 |
| 🔧 **工具调用** | 原生模式 + 首批推荐安装的 Tools |

[**阅读必读内容 →**](/getting-started/essentials)

---

## 🤖 连接 Agent

**不止连接模型提供商。还可以连接自主 AI Agent。**

像 Hermes Agent 和 OpenClaw 这样的 AI Agent 自带终端、文件操作、网页搜索、记忆等工具，并把 Open WebUI 用作功能丰富的聊天前端。Agent 会自行决定何时使用工具、执行操作，并将结果流式返回给你。

| | |
| :--- | :--- |
| 🧠 **Hermes Agent** | Nous Research 的 Agent，支持终端、文件操作、网页搜索与技能 |
| 🐾 **OpenClaw** | 具备 shell 访问、网页浏览和频道机器人能力的自托管 Agent 框架 |

[**连接 Agent →**](/getting-started/quick-start/connect-an-agent)

---

## 共享 Open WebUI

**一次部署，让整个组织都能使用 AI。**

Open WebUI 不只是本地 AI 界面，更可以作为团队的集中式 AI 操作系统。只需部署一次，就能获得更顺畅的接入流程、协作式智能、资源复用与集中式安全控制。

| | |
| :--- | :--- |
| **局域网与隧道** | Tailscale、Cloudflare Tunnels 和本地 IP 访问 |
| **反向代理** | 使用 Nginx、Caddy 或 HAProxy 保护你的实例 |
| **团队接入** | 管理员审批流程与 Enterprise SSO 集成 |
| **共享上下文** | 频道、共享聊天和公共知识库 |

[**了解如何共享 Open WebUI →**](/getting-started/sharing)

---

## 🛠️ 高级主题

**扩展、观测并自定义你的部署。**

如果你需要超越基础配置，这里就是下一站。你可以配置环境变量、连接外部数据库、接入云存储、启用 OpenTelemetry，或借助 Redis 和多 worker 实现横向扩展。

| | |
| :--- | :--- |
| ⚖️ **扩展** | 多 worker、多节点、Redis 支持的会话 |
| 📊 **日志与可观测性** | OpenTelemetry 链路、指标和结构化日志 |
| 🧪 **开发环境** | 从源码运行，进行本地开发与测试 |

[**探索高级主题 →**](/getting-started/advanced-topics)

---

## 🔄 更新

**通过最新功能和安全修复保持版本最新。**

你可以手动用一条 Docker 或 pip 命令更新，也可以通过 Watchtower、WUD 或 Diun 自动化。还包含备份/恢复流程和生产环境版本固定建议。

| | |
| :--- | :--- |
| 🔄 **手动更新** | Docker 拉取并重建，或 pip 升级 |
| 🤖 **自动更新** | Watchtower、WUD 或 Diun |
| 📌 **版本固定** | 锁定到特定版本以保持稳定 |
| 💾 **备份与恢复** | 一条命令完成卷备份和恢复 |

[**更新指南 →**](/getting-started/updating)
