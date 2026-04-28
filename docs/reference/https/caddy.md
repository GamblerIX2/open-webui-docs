---
sidebar_position: 202
title: "使用 Caddy 的 HTTPS"
---


## 使用 Caddy 的 HTTPS {#https-using-caddy}

确保用户与 Open WebUI 之间的通信安全至关重要。HTTPS（HyperText Transfer Protocol Secure）会对传输中的数据进行加密，防止窃听和篡改。通过将 Caddy 配置为反向代理，你可以轻松为 Open WebUI 部署添加 HTTPS，同时提升安全性和可信度。

本指南提供一个简单的实操流程，帮助你在 Ubuntu 服务器上使用 Caddy 作为 Open WebUI 的反向代理，并借助自动证书管理启用 HTTPS。

接下来我们将按以下步骤完成配置：

- [使用 Caddy 的 HTTPS](#https-using-caddy)
- [Docker](#docker)
  - [安装 Docker](#installing-docker)
- [Open WebUI](#openwebui)
  - [安装 Open WebUI](#installing-openwebui)
- [Caddy](#caddy)
  - [安装 Caddy](#installing-caddy)
  - [配置 Caddy](#configure-caddy)
- [测试 HTTPS](#testing-https)
- [更新 Open WebUI](#updating-open-webui)
  - [停止 Open WebUI](#stopping-open-webui)
  - [拉取最新镜像](#pulling-the-latest-image)
  - [启动 Open WebUI](#starting-open-webui)

## Docker

按照 Docker 官方指南配置 apt 仓库：[Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

我在示例中也包含了 `docker-compose`，因为运行 `docker compose` 时会用到它。

### 安装 Docker {#installing-docker}

下面是我在 Ubuntu 上安装 Docker 时使用的命令：

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
```

## Open WebUI {#openwebui}

先为 Open WebUI 项目创建一个目录：

```bash
mkdir -p ~/open-webui
cd ~/open-webui
```

### 安装 Open WebUI {#installing-openwebui}

在 `~/open-webui` 目录中创建一个 `docker-compose.yml` 文件。示例里保留了一段注释，用于演示如何为 Qdrant 设置环境变量；如果你还需要配置其他[环境变量](https://docs.openwebui.com/reference/env-configuration)，也可以按同样方式添加。

```yaml
services:
    open-webui:
        image: ghcr.io/open-webui/open-webui:main
        container_name: open-webui
        ports:
            - "8080:8080"
        volumes:
            - ./data:/app/backend/data
        # environment:
        #     - "QDRANT_API_KEY=API_KEY_HERE"
        #     - "QDRANT_URI=https://example.com"
        restart: unless-stopped
```

## Caddy

Caddy 是一个强大的 Web 服务器，会自动替你管理 TLS 证书，因此非常适合通过 HTTPS 提供 Open WebUI 服务。

### 安装 Caddy {#installing-caddy}

请参考 [Caddy 在 Ubuntu 上的安装指南](https://caddyserver.com/docs/install#debian-ubuntu-raspbian)。

### 配置 Caddy {#configure-caddy}

接下来需要修改 `Caddyfile`，将其替换为你的域名。

编辑 `/etc/caddy/Caddyfile` 文件：

```bash
sudo nano /etc/caddy/Caddyfile
```

然后将配置更新为如下内容：

```caddyfile
your-domain.com {
  reverse_proxy localhost:8080
}
```

请务必将 `your-domain.com` 替换为你的真实域名。

## 测试 HTTPS {#testing-https}

假设你已经将 DNS 记录指向服务器 IP，现在可以在 `~/open-webui` 目录中运行 `docker compose up`，测试 Open WebUI 是否可以通过 HTTPS 访问。

```bash
cd ~/open-webui
docker compose up -d
```

现在你应该可以通过 `https://your-domain.com` 访问 Open WebUI。

## 更新 Open WebUI {#updating-open-webui}

再补充一条：如何在不丢失数据的情况下更新 Open WebUI。由于我们使用 volume 存储数据，因此只需拉取最新镜像并重启容器即可。

### 停止 Open WebUI {#stopping-open-webui}

首先停止并删除现有容器：

```bash
docker rm -f open-webui
```

### 拉取最新镜像 {#pulling-the-latest-image}

然后拉取最新镜像：

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

### 启动 Open WebUI {#starting-open-webui}

最后重新启动 Open WebUI 容器：

```bash
docker compose up -d
```
