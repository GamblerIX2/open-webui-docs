---
sidebar_position: 1
title: "HTTPS using Cloudflare Tunnel"
---

# 使用 Cloudflare Tunnel 的 HTTPS

**安全地将 Open WebUI 暴露到互联网。无需开放端口、无需证书、也无需反向代理。**

Cloudflare Tunnel（`cloudflared`）会从你的机器向 Cloudflare 边缘网络建立一条仅出站连接。流量通过 Cloudflare 基础设施转发，并自动获得 TLS、DDoS 防护和访问控制，而你的服务器无需暴露任何端口。

:::tip 何时使用 Cloudflare Tunnel
如果你希望在**无需自己管理 TLS 证书或防火墙规则**的情况下获得**生产级公网访问**，这是推荐方案。它适用于各种网络环境，包括 NAT 后面或受限防火墙环境。
:::

---

## 前提条件

| 要求 | 详情 |
| :--- | :--- |
| **Open WebUI** | 已在本地端口 `8080`（默认值）运行 |
| **Cloudflare 账号** | 可在 [cloudflare.com](https://dash.cloudflare.com/sign-up) 免费注册 |
| **Cloudflare 托管域名** | 你的域名 DNS 必须由 Cloudflare 管理 |

---

## 方案 A：Dashboard 配置（无需 CLI）

最简单的方式。全部通过 Cloudflare dashboard 完成。

### 1. 创建 tunnel

1. 前往 [**Zero Trust → Networks → Tunnels**](https://one.dash.cloudflare.com/networks/tunnels)
2. 点击 **Create a tunnel** → 选择 **Cloudflared**
3. 为 tunnel 命名（例如 `open-webui`）
4. 按页面说明在你的机器上安装并运行 connector

### 2. 添加公网主机名

在 tunnel 配置中添加一个 **Public Hostname**：

| 字段 | 值 |
| :--- | :--- |
| **Subdomain** | `chat`（或你喜欢的任意名称） |
| **Domain** | 选择你的 Cloudflare 域名 |
| **Service type** | `HTTP` |
| **URL** | `localhost:8080` |

保存后，Cloudflare 会自动创建对应 DNS 记录。

### 3. 访问 Open WebUI

打开 `https://chat.your-domain.com`。HTTPS 全部由 Cloudflare 处理。

---

## 方案 B：CLI 配置

适合自动化、基础设施即代码，或无头服务器场景。

### 1. 安装 cloudflared

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="mac" label="macOS" default>

```bash
brew install cloudflared
```

  </TabItem>
  <TabItem value="linux" label="Linux">

```bash
curl -sSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared
```

  </TabItem>
  <TabItem value="windows" label="Windows">

```powershell
winget install Cloudflare.cloudflared
```

  </TabItem>
</Tabs>

### 2. 完成认证

```bash
cloudflared tunnel login
```

该命令会打开浏览器，让你授权 `cloudflared` 访问你的 Cloudflare 账号。

### 3. 创建 tunnel

```bash
cloudflared tunnel create open-webui
```

请记下输出中的 **Tunnel ID**，后续配置时会用到。

### 4. 配置

创建 `~/.cloudflared/config.yml`：

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /home/YOUR_USER/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: chat.your-domain.com
    service: http://localhost:8080
  - service: http_status:404
```

### 5. 创建 DNS 记录

```bash
cloudflared tunnel route dns open-webui chat.your-domain.com
```

### 6. 启动 tunnel

```bash
cloudflared tunnel run open-webui
```

然后打开 `https://chat.your-domain.com`。

---

## 作为系统服务运行

若想让 tunnel 在系统重启后仍自动运行：

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

它会自动使用 `~/.cloudflared/config.yml` 中的配置。

---

## 配置 Open WebUI

设置 `WEBUI_URL`，确保 OAuth 回调和内部链接都能正确解析：

```bash
docker run -d \
  -p 8080:8080 \
  -e WEBUI_URL=https://chat.your-domain.com \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

---

## 在 Docker Compose 中集成 cloudflared

你也可以把 Open WebUI 与 tunnel connector 一起放进同一个 stack：

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    volumes:
      - open-webui:/app/backend/data
    environment:
      - WEBUI_URL=https://chat.your-domain.com
    restart: unless-stopped

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    command: tunnel --no-autoupdate run --token YOUR_TUNNEL_TOKEN
    restart: unless-stopped

volumes:
  open-webui:
```

你可以在 [Cloudflare dashboard](https://one.dash.cloudflare.com/networks/tunnels) 中获取 tunnel token：选择你的 tunnel → **Configure** → 从安装命令中复制 token。

:::tip
在这种部署方式中，`open-webui` 服务**不需要**暴露 `ports`。`cloudflared` 会通过 Docker 内部网络连接它。此时请把 tunnel config 中的 service URL 改成 `http://open-webui:8080`。
:::

---

## 添加访问控制（可选）

Cloudflare Zero Trust 可以在不改动 Open WebUI 的情况下，为你的实例加上一层认证保护：

1. 前往 [**Zero Trust → Access → Applications**](https://one.dash.cloudflare.com/access/apps)
2. 点击 **Add an application** → Self-hosted
3. 将域名设置为 `chat.your-domain.com`
4. 创建一条 **Access Policy**（例如只允许 `@your-company.com` 邮箱访问）

这样用户在进入 Open WebUI 前，会先看到 Cloudflare 登录页。

---

## 快速参考

| 操作 | 命令 / 值 |
| :--- | :--- |
| 创建 tunnel | `cloudflared tunnel create open-webui` |
| 启动 tunnel | `cloudflared tunnel run open-webui` |
| 添加 DNS | `cloudflared tunnel route dns open-webui chat.your-domain.com` |
| 安装为系统服务 | `sudo cloudflared service install` |
| Dashboard | [one.dash.cloudflare.com/networks/tunnels](https://one.dash.cloudflare.com/networks/tunnels) |
| 设置 CORS origin | `CORS_ALLOW_ORIGIN=https://chat.your-domain.com` |
