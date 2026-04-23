---
sidebar_position: 15
title: "共享 Open WebUI"
---

# 共享 Open WebUI

**部署一次，让整个团队都能访问。**

Open WebUI 天生就适合共享。一套实例可以服务整个组织。用户只需打开浏览器即可开始聊天，无需按座位单独安装、无需客户端依赖，也不会把数据割裂在不同机器上。

---

## 为团队而生

### 顺畅接入

终端用户无需安装任何东西、管理 Docker 或操作终端。只要打开浏览器，访问你的实例 URL 并登录即可。

### 协作式智能

共享实例意味着共享知识。

| | |
| :--- | :--- |
| **[Channels](/features/channels)** | 团队与 AI 模型实时协作的持久化空间 |
| **共享聊天** | 将完整对话快照发送给同事 |
| **全局 Prompts 与 Knowledge** | 构建专用 Agent，并立即提供给所有人使用 |

### 共享算力

如果运行的是本地模型，一台强大的服务器（或集群）就能为整个团队提供能力，而不需要每张桌面都配备足够强的硬件。

### 集中式管理

在一个地方统一管理所有内容：控制用户可访问的模型、配置 [**基于角色的访问控制（RBAC）**](/features/authentication-access/rbac)、查看审计日志，并按需限制功能。

---

## 将实例开放给团队

要共享实例，你需要让它能够通过网络访问。常见做法有三种：从简单的局域网访问，到面向生产的公网域名。

### 1. 零配置局域网访问

如果团队成员位于同一局域网或 VPN 中，他们可以通过你的机器本地 IP 和端口访问 Open WebUI。

> `http://192.168.1.100:3000`

### 2. 安全的私有网络（推荐）

适合无需暴露到公共互联网的远程团队。叠加网络和安全隧道可以在不开放防火墙端口的情况下提供加密访问。

| | |
| :--- | :--- |
| **[Tailscale](/reference/https/tailscale)** | 带 MagicDNS 的私有 mesh 网络（`https://open-webui.tailnet-name.ts.net`） |
| **[Cloudflare Tunnels](/reference/https/cloudflare-tunnel)** | 通过 Cloudflare 边缘暴露，并由 Cloudflare Access（Zero Trust）保护 |
| **[ngrok](/reference/https/ngrok)** | 适合开发或测试时的临时快速共享 |

### 3. 公网 HTTPS（反向代理）

对于生产部署，请将 Open WebUI 放在反向代理之后，在你自己的域名上完成 SSL/TLS 终止（例如 `ai.yourcompany.com`）。

| | |
| :--- | :--- |
| **[Nginx](/reference/https/nginx)** | 行业标准 Web 服务器与反向代理 |
| **[Caddy](/reference/https/caddy)** | 配置简洁，自动启用 HTTPS |
| **[HAProxy](/reference/https/haproxy)** | 高性能负载均衡与代理 |

---

## 团队接入方式

当实例可以通过网络访问后，你还需要管理用户如何创建账号并登录。

### Pending 队列

第一个注册的用户会成为**管理员**。之后所有新注册账号都会进入 **Pending** 状态，只有管理员在 Admin Panel 中批准后，才能访问模型并使用平台。

### 企业级单点登录（SSO）

对于手动审批无法扩展的组织，Open WebUI 可以与现有身份提供商集成。

| | |
| :--- | :--- |
| **OAuth / OIDC** | 通过 **Google**、**Microsoft**、**Okta** 或 **Keycloak** 认证 |
| **组映射** | 将 IdP 组直接映射到 Open WebUI 组 |
| **[SCIM 2.0](/features/authentication-access/auth/scim)** | 自动完成用户和组的开通与回收 |

[**了解如何设置 SSO →**](/features/authentication-access/auth/sso)
