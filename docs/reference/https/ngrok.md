---
sidebar_position: 2
title: "HTTPS using ngrok"
---

# 使用 ngrok 的 HTTPS

**为本地 Open WebUI 立刻获得公网 HTTPS。零配置、零开放端口。**

ngrok 会从公网 URL 向你的本地机器建立一条安全隧道。它是让本地 Open WebUI 快速支持 HTTPS 的最快方式，尤其适用于开发、演示或测试那些需要安全上下文的功能（例如 Voice Calls）。

:::tip 何时使用 ngrok
ngrok 非常适合**开发与测试**。对于生产部署，请优先选择反向代理方案，例如 [Nginx](/reference/https/nginx)、[Caddy](/reference/https/caddy)，或使用 [Cloudflare Tunnel](/reference/https/cloudflare-tunnel) 获得 zero-trust 访问。
:::

---

## 前提条件

| 要求 | 详情 |
| :--- | :--- |
| **Open WebUI** | 已在本地端口 `8080`（默认值）运行 |
| **ngrok 账号** | 可在 [ngrok.com](https://ngrok.com) 免费注册，并获得稳定的 authtoken |

---

## 1. 安装 ngrok

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="mac" label="macOS" default>

```bash
brew install ngrok
```

  </TabItem>
  <TabItem value="linux" label="Linux">

```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok-v3-stable-linux-amd64.tgz \
  | sudo tar xz -C /usr/local/bin
```

  </TabItem>
  <TabItem value="windows" label="Windows">

```powershell
choco install ngrok
```

或直接从 [ngrok.com/download](https://ngrok.com/download) 下载。

  </TabItem>
</Tabs>

## 2. 完成认证

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

你的 authtoken 可在 [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) 获取。

## 3. 启动隧道

```bash
ngrok http 8080
```

ngrok 会输出类似下面的公网地址：

```
Forwarding  https://a1b2-203-0-113-42.ngrok-free.app → http://localhost:8080
```

直接在浏览器中打开这个 `https://` URL 即可。

---

## 配置 Open WebUI

设置 `WEBUI_URL`，确保 OAuth 回调与内部链接都能正确解析：

```bash
docker run -d \
  -p 8080:8080 \
  -e WEBUI_URL=https://a1b2-203-0-113-42.ngrok-free.app \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

:::warning
ngrok 免费层的 URL 会在每次重启 tunnel 后变化。请相应更新 `WEBUI_URL`，或者使用 [ngrok custom domain](https://ngrok.com/docs/guides/how-to-set-up-a-custom-domain/)（付费）来获得固定 URL。
:::

---

## 自定义域名（可选）

在付费 ngrok 计划中，你可以申请固定子域名，使 URL 不再变化：

```bash
ngrok http 8080 --url=your-name.ngrok-free.app
```

这样你就能在 `WEBUI_URL` 中一次性配置固定地址，无需频繁更新。

---

## 快速参考

| 操作 | 命令 / 值 |
| :--- | :--- |
| 启动 tunnel | `ngrok http 8080` |
| 自定义域名 | `ngrok http 8080 --url=your-name.ngrok-free.app` |
| Dashboard | [dashboard.ngrok.com](https://dashboard.ngrok.com) |
| 查看请求流量 | `http://localhost:4040`（ngrok 本地调试面板） |
| 设置 CORS origin | `CORS_ALLOW_ORIGIN=https://your-name.ngrok-free.app` |

---

## 限制

| 问题 | 说明 |
| :--- | :--- |
| **免费层 URL 会轮换** | 每次重启 tunnel 后 URL 都会变化，除非你使用自定义域名 |
| **首次访问拦截页** | 免费层首次访问会显示 ngrok splash page |
| **不适合生产环境** | ngrok 会增加额外延迟，并且本身是单点依赖；生产环境请改用反向代理或 Cloudflare Tunnel |
| **速率限制** | 免费层有限速；付费计划可移除这类限制 |
