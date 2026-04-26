---
sidebar_position: 50
title: "Tailscale"
---

# Tailscale 集成

**从任何设备私密加密地访问 Open WebUI，无需开放端口，无需管理证书。**

[Tailscale](https://tailscale.com) 在您的设备之间创建基于 WireGuard 的网状 VPN（"tailnet"）。每台设备都会获得一个稳定的主机名，例如 `my-server.tail1234.ts.net`，Tailscale 还可以自动配置受信任的 HTTPS 证书。您的 Open WebUI 实例保持完全私密，只有 tailnet 上的设备才能访问。

:::tip 何时使用 Tailscale
当您希望在不将 Open WebUI 暴露到公共互联网的情况下实现**跨设备私密、认证访问**时，Tailscale 是理想选择。非常适合个人用户、小团队，或者在外出时通过手机或笔记本访问家庭服务器。
:::

---

## 前提条件

| 要求 | 详情 |
| :--- | :--- |
| **Open WebUI** | 在本地端口 `8080`（默认值）上运行 |
| **Tailscale 账户** | 个人使用免费，注册地址 [tailscale.com](https://tailscale.com) |
| **已安装 Tailscale** | 在运行 Open WebUI 的服务器和所有客户端设备上均需安装 |

---

## 快速开始

### 1. 安装 Tailscale

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="mac" label="macOS" default>

从 [Mac App Store](https://apps.apple.com/app/tailscale/id1475387142) 下载，或运行：

```bash
brew install tailscale
```

  </TabItem>
  <TabItem value="linux" label="Linux">

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

  </TabItem>
  <TabItem value="windows" label="Windows">

从 [tailscale.com/download](https://tailscale.com/download/windows) 下载。

  </TabItem>
</Tabs>

### 2. 连接服务器

在运行 Open WebUI 的机器上：

```bash
sudo tailscale up
```

您的机器将获得类似 `my-server.tail1234.ts.net` 的 tailnet 主机名。通过以下命令查看：

```bash
tailscale status
```

### 3. 访问 Open WebUI

在同一 tailnet 上的任意设备，打开：

```
http://my-server.tail1234.ts.net:8080
```

该连接已由 WireGuard 进行端对端加密。如需使用语音通话等需要 HTTPS 的浏览器功能，请继续阅读下一节。

---

## 使用 Tailscale 启用 HTTPS

Tailscale 可以为您的 tailnet 主机名配置受信任的 Let's Encrypt 证书，无需反向代理。

有关完整的 HTTPS 配置步骤（证书生成、`tailscale serve`、配置 `WEBUI_URL`），请参阅专用参考指南：

👉 [**使用 Tailscale 启用 HTTPS**](/reference/https/tailscale)

简要版本：

```bash
# 将 HTTPS 流量直接代理到 Open WebUI
sudo tailscale serve https / http://localhost:8080
```

您的实例现在可通过 `https://my-server.tail1234.ts.net` 访问，并具有有效的 TLS 证书。

---

## Authentication via Tailscale (SSO)

[Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) can act as an authenticating reverse proxy. When a request passes through `tailscale serve`, Tailscale automatically sets the `Tailscale-User-Login` header with the email address of the authenticated user. Open WebUI can trust this header as a single sign-on mechanism. Users on your tailnet are automatically logged in without needing a separate Open WebUI password.

### How it works

1. A Tailscale sidecar container runs alongside Open WebUI
2. Tailscale Serve proxies HTTPS traffic to Open WebUI and injects identity headers
3. Open WebUI reads `Tailscale-User-Login` and `Tailscale-User-Name` to identify the user
4. Users are auto-registered and logged in on first visit

### Docker Compose Setup

Create a `tailscale/serve.json` file that configures Tailscale Serve to proxy to Open WebUI:

```json title="tailscale/serve.json"
{
    "TCP": {
        "443": {
            "HTTPS": true
        }
    },
    "Web": {
        "${TS_CERT_DOMAIN}:443": {
            "Handlers": {
                "/": {
                    "Proxy": "http://open-webui:8080"
                }
            }
        }
    }
}
```

Then set up the Docker Compose file with a Tailscale sidecar:

```yaml title="docker-compose.yaml"
---
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui:/app/backend/data
    environment:
      - WEBUI_AUTH_TRUSTED_EMAIL_HEADER=Tailscale-User-Login
      - WEBUI_AUTH_TRUSTED_NAME_HEADER=Tailscale-User-Name
    restart: unless-stopped
  tailscale:
    image: tailscale/tailscale:latest
    environment:
      - TS_AUTH_ONCE=true
      - TS_AUTHKEY=${TS_AUTHKEY}
      - TS_EXTRA_ARGS=--advertise-tags=tag:open-webui
      - TS_SERVE_CONFIG=/config/serve.json
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_HOSTNAME=open-webui
    volumes:
      - tailscale:/var/lib/tailscale
      - ./tailscale:/config
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - net_admin
      - sys_module
    restart: unless-stopped

volumes:
  open-webui: {}
  tailscale: {}
```

You will need to create an [OAuth client](https://tailscale.com/kb/1215/oauth-clients) with **device write** permission in the Tailscale admin console and pass the key as `TS_AUTHKEY`.

Your instance will be reachable at `https://open-webui.TAILNET_NAME.ts.net`.

:::warning Restrict direct access with ACLs
If you run Tailscale in the same network context as Open WebUI, users could bypass the Serve proxy and reach Open WebUI directly, skipping the trusted header authentication. Use [Tailscale ACLs](https://tailscale.com/kb/1018/acls) to restrict access to only port 443.
:::

For more details on trusted header authentication, see the [SSO documentation](/features/authentication-access/auth/sso#tailscale-serve).

---

## Tailscale Funnel (Optional Public Access)

If you want to share Open WebUI publicly without requiring Tailscale on the client, [Tailscale Funnel](https://tailscale.com/kb/1223/funnel) exposes your `tailscale serve` endpoint to the internet:

```bash
sudo tailscale funnel https / http://localhost:8080
```

Your Open WebUI is now publicly accessible at `https://my-server.tail1234.ts.net` with a valid TLS certificate. Funnel routes traffic through Tailscale's infrastructure, similar to Cloudflare Tunnel.

:::warning
Funnel makes your Open WebUI accessible to **anyone on the internet**. Make sure you have authentication configured in Open WebUI before enabling it.
:::

---

## Quick Reference

| What | Command / Value |
| :--- | :--- |
| Connect to tailnet | `sudo tailscale up` |
| Check hostname | `tailscale status` |
| Serve over HTTPS | `sudo tailscale serve https / http://localhost:8080` |
| Public access (Funnel) | `sudo tailscale funnel https / http://localhost:8080` |
| Generate cert manually | `sudo tailscale cert my-server.tail1234.ts.net` |
| Admin console | [login.tailscale.com/admin](https://login.tailscale.com/admin) |
| Set CORS origin | `CORS_ALLOW_ORIGIN=https://my-server.tail1234.ts.net` |
| Trusted email header | `WEBUI_AUTH_TRUSTED_EMAIL_HEADER=Tailscale-User-Login` |
| Trusted name header | `WEBUI_AUTH_TRUSTED_NAME_HEADER=Tailscale-User-Name` |

---

## Related Pages

- [HTTPS using Tailscale](/reference/https/tailscale) - focused HTTPS/TLS reference
- [SSO (Trusted Header)](/features/authentication-access/auth/sso#tailscale-serve) - generic trusted header configuration
- [Sharing Open WebUI](/getting-started/sharing) - overview of all sharing approaches
