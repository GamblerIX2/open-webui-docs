---
sidebar_position: 50
title: "Tailscale"
---

# Tailscale 集成

**从任意设备私密、加密地访问 Open WebUI——无需开放端口，也无需手动管理证书。**

[Tailscale](https://tailscale.com) 会在你的设备之间建立一个基于 WireGuard 的 mesh VPN（即 “tailnet”）。每台设备都会获得一个稳定主机名，例如 `my-server.tail1234.ts.net`，并且 Tailscale 还能自动配置受信任的 HTTPS 证书。你的 Open WebUI 实例可以保持完全私有，只有 tailnet 中的设备才能访问。

:::tip 何时使用 Tailscale
如果你希望在**不把 Open WebUI 暴露到公网**的前提下，实现跨设备、私密且可认证的访问，Tailscale 是非常理想的选择。它尤其适合个人用户、小团队，或需要在外通过手机、笔记本访问家庭服务器的场景。
:::

---

## 前提条件

| 要求 | 详情 |
| :--- | :--- |
| **Open WebUI** | 已运行在本地端口 `8080`（默认值） |
| **Tailscale 账号** | 个人使用可免费注册，见 [tailscale.com](https://tailscale.com) |
| **已安装 Tailscale** | 运行 Open WebUI 的服务器以及所有客户端设备都需安装 |

---

## 快速开始

### 1. 安装 Tailscale

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="mac" label="macOS" default>

从 [Mac App Store](https://apps.apple.com/app/tailscale/id1475387142) 下载，或执行：

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

在运行 Open WebUI 的机器上执行：

```bash
sudo tailscale up
```

你的机器将获得一个类似 `my-server.tail1234.ts.net` 的 tailnet 主机名。可通过以下命令查看：

```bash
tailscale status
```

### 3. 访问 Open WebUI

在同一 tailnet 上的任意设备中打开：

```
http://my-server.tail1234.ts.net:8080
```

此连接已由 WireGuard 端到端加密。如果你还需要浏览器原生 HTTPS 能力（例如语音通话等），请继续阅读下一节。

---

## 使用 Tailscale 启用 HTTPS

Tailscale 可以为你的 tailnet 主机名自动配置受信任的 Let's Encrypt 证书，而无需反向代理。

完整 HTTPS 配置步骤（包括证书生成、`tailscale serve`、`WEBUI_URL` 配置等），请参阅专门的参考指南：

👉 [**使用 Tailscale 启用 HTTPS**](/reference/https/tailscale)

简要版本如下：

```bash
# 将 HTTPS 流量直接代理到 Open WebUI
sudo tailscale serve https / http://localhost:8080
```

此时你的实例就可以通过 `https://my-server.tail1234.ts.net` 访问，并带有有效 TLS 证书。

---

## 通过 Tailscale 实现认证（SSO）

[Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) 可以充当一个带认证能力的反向代理。当请求经过 `tailscale serve` 时，Tailscale 会自动写入 `Tailscale-User-Login` header，其值为当前已认证用户的邮箱地址。Open WebUI 可以把这个 header 作为单点登录信任来源，因此同一 tailnet 中的用户无需再单独输入 Open WebUI 密码即可登录。

### 工作原理

1. 一个 Tailscale sidecar container 与 Open WebUI 一起运行
2. Tailscale Serve 把 HTTPS 流量代理到 Open WebUI，并注入身份 headers
3. Open WebUI 读取 `Tailscale-User-Login` 和 `Tailscale-User-Name` 来识别用户
4. 用户首次访问时会被自动注册并自动登录

### Docker Compose 配置

先创建一个 `tailscale/serve.json` 文件，用于配置 Tailscale Serve 把流量代理到 Open WebUI：

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

然后在 Docker Compose 中增加 Tailscale sidecar：

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

你还需要在 Tailscale 管理后台创建一个拥有 **device write** 权限的 [OAuth client](https://tailscale.com/kb/1215/oauth-clients)，并把该 key 作为 `TS_AUTHKEY` 传入。

你的实例之后会通过 `https://open-webui.TAILNET_NAME.ts.net` 访问。

:::warning 使用 ACLs 限制绕过直连
如果 Tailscale 与 Open WebUI 运行在相同网络上下文中，用户可能绕过 Serve proxy，直接访问 Open WebUI，从而跳过 trusted header 认证。建议使用 [Tailscale ACLs](https://tailscale.com/kb/1018/acls) 将访问限制在 443 端口。
:::

若要进一步了解 trusted header 认证，请参阅 [SSO 文档](/features/authentication-access/auth/sso#tailscale-serve)。

---

## Tailscale Funnel（可选的公网访问）

如果你想在客户端**无需安装 Tailscale** 的情况下对外公开 Open WebUI，可使用 [Tailscale Funnel](https://tailscale.com/kb/1223/funnel) 将 `tailscale serve` 暴露到公网：

```bash
sudo tailscale funnel https / http://localhost:8080
```

此时你的 Open WebUI 将通过 `https://my-server.tail1234.ts.net` 对公网可访问，并带有有效 TLS 证书。Funnel 会通过 Tailscale 基础设施转发流量，类似于 Cloudflare Tunnel。

:::warning
Funnel 会让你的 Open WebUI 对**整个互联网**开放。启用前，请务必先在 Open WebUI 中完成认证配置。
:::

---

## 快速参考

| 操作 | 命令 / 值 |
| :--- | :--- |
| 加入 tailnet | `sudo tailscale up` |
| 查看主机名 | `tailscale status` |
| 通过 HTTPS 提供服务 | `sudo tailscale serve https / http://localhost:8080` |
| 公网访问（Funnel） | `sudo tailscale funnel https / http://localhost:8080` |
| 手动生成证书 | `sudo tailscale cert my-server.tail1234.ts.net` |
| 管理后台 | [login.tailscale.com/admin](https://login.tailscale.com/admin) |
| 设置 CORS origin | `CORS_ALLOW_ORIGIN=https://my-server.tail1234.ts.net` |
| 受信任邮箱 header | `WEBUI_AUTH_TRUSTED_EMAIL_HEADER=Tailscale-User-Login` |
| 受信任名称 header | `WEBUI_AUTH_TRUSTED_NAME_HEADER=Tailscale-User-Name` |

---

## 相关页面

- [HTTPS using Tailscale](/reference/https/tailscale) —— 专注于 HTTPS / TLS 的参考页
- [SSO (Trusted Header)](/features/authentication-access/auth/sso#tailscale-serve) —— 通用 trusted header 配置
- [Sharing Open WebUI](/getting-started/sharing) —— 所有共享方式的总览
