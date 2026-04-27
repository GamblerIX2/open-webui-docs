---
sidebar_position: 150
title: "📖 参考文档"
---

# 参考文档

**每个旋钮、接口和配置选项背后的技术细节。**

Open WebUI 具有高度可配置性。本节是环境变量、API 接口、网络架构、反向代理配置和生产监控的权威参考来源。无论你是调整单项设置还是规划多节点部署，都可以从这里开始。

---

## ⚙️ 环境变量配置

**Open WebUI 在启动时读取的每个标志、路径和密钥，全部汇总于此。**

200 多个环境变量控制着认证、模型路由、存储、日志记录等。了解 `PersistentConfig` 行为，排查被忽略的设置，找到你所需的精确变量。

| | |
| :--- | :--- |
| 🔐 **认证与注册** | `ENABLE_SIGNUP`、`ENABLE_LOGIN_FORM`、`WEBUI_ADMIN_EMAIL`、OIDC/LDAP/SCIM |
| 🤖 **模型连接** | Ollama、OpenAI、直接流水线 URL、超时、负载均衡 |
| 💾 **存储与数据库** | SQLite、PostgreSQL、S3/GCS/Azure Blob、Redis |
| 📊 **日志与审计** | `GLOBAL_LOG_LEVEL`、JSON 日志、审计日志级别与路径 |
| 🧠 **RAG 与检索** | 分块大小、重叠、嵌入引擎、重排序、向量数据库选择 |

[**浏览所有环境变量 →**](/reference/env-configuration)

---

## 🔌 API 接口

**兼容 OpenAI 和 Anthropic 的 API，以及 RAG、文件管理和 Ollama 代理路由。**

Open WebUI 提供完整的 REST API，通过 Bearer Token 或 JWT 进行认证。使用与 Web UI 相同的接口来构建自动化工具、聊天机器人和自定义集成。

| | |
| :--- | :--- |
| 💬 **聊天补全** | `POST /api/chat/completions`，兼容 OpenAI |
| 🔮 **Anthropic 消息** | `POST /api/v1/messages`，兼容 Anthropic SDK 和 Claude Code |
| 🦙 **Ollama 代理** | `/ollama/api/*`，直通到原生 Ollama 接口 |
| 📄 **文件与知识库** | 上传文件、创建知识库集合、通过 RAG 查询 |
| 🔧 **过滤器（入口/流/出口）** | 每个请求的入口、流和出口钩子 |

[**探索 API →**](/reference/api-endpoints)

---

## 🔒 HTTPS 配置

**使用 Nginx、Caddy 或 HAProxy 在 Open WebUI 前端终止 TLS。**

逐步的反向代理配置指南，用于通过 HTTPS 保护你的部署。每个指南都包含证书处理、WebSocket 支持和生产级强化设置。

| | |
| :--- | :--- |
| 🟢 **Nginx** | 完整配置，包含 SSL 终止、WebSocket 代理和请求头 |
| ⚡ **Caddy** | 最简配置实现自动 HTTPS |
| 🔄 **HAProxy** | 企业级负载均衡与 TLS 卸载 |
| ☁️ **Cloudflare Tunnel** | 无需开放端口即可安全暴露 Open WebUI |
| 🔒 **Tailscale** | 跨设备私有加密访问，无需公开暴露 |
| 🧪 **ngrok** | 用于开发和测试的即时 HTTPS 隧道 |

[**配置 HTTPS →**](/reference/https)

---

## 🔑 API 密钥

**为脚本、机器人和集成提供对 Open WebUI 的程序化访问。**

生成个人访问令牌，让外部代码调用与 Web UI 相同的接口。每个密钥继承创建者的权限。

| | |
| :--- | :--- |
| 🔐 **Bearer Token 认证** | 标准 `Authorization: Bearer` 头，适用于任何 HTTP 客户端 |
| 🛡️ **用户范围** | 密钥继承你的角色和群组权限 |
| 🚫 **接口限制** | 可选择限制密钥可访问的 API 路由 |

[**配置 API 密钥 →**](/features/authentication-access/api-keys)

---

## 📊 监控

**使用 Uptime Kuma、OpenTelemetry、Prometheus 和 Grafana 观察你的部署。**

生产环境监控指南，涵盖健康检查、模型连通性验证、分布式追踪、指标和结构化日志。可与现有的可观测性堆栈集成，或从头建立新的监控体系。

| | |
| :--- | :--- |
| ✅ **健康检查** | 使用 Uptime Kuma 进行基础、模型连通性和深度健康检查 |
| 📡 **OpenTelemetry** | 将追踪、指标和日志输送到任何兼容 OTLP 的后端 |
| 📈 **仪表盘** | Prometheus + Grafana 实现实时系统和模型指标 |

[**配置监控 →**](/reference/monitoring)

---

## 🌐 网络架构图

**查看 Open WebUI、Ollama 和 Docker 在不同部署拓扑中的通信方式。**

可视化 C4 架构图，涵盖主机网络、Docker Compose 栈、独立网络以及平台特定差异。适用于调试连通性问题或规划架构。

| | |
| :--- | :--- |
| 🖥️ **macOS / Windows** | 主机 Ollama、Compose 栈、独立网络、主机网络的注意事项 |
| 🐧 **Linux** | 相同拓扑，包含 Linux 特定的网络行为 |

[**查看网络架构图 →**](/reference/network-diagrams)
