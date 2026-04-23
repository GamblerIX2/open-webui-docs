---
sidebar_position: 90
title: "自定义 CA 证书库"
---

:::warning

本教程来自社区贡献，不属于 Open WebUI 官方支持范围。它仅演示如何根据你的具体场景自定义 Open WebUI。想参与贡献？请查看贡献教程。

:::

如果你在运行 OI 时遇到 `[SSL: CERTIFICATE_VERIFY_FAILED]` 错误，通常说明你所在的网络会拦截 HTTPS 流量（例如企业内网）。

要解决这个问题，你需要把新的证书添加到 OI 的 truststore 中。

**对于预构建 Docker 镜像：**

1. 在 `docker run` 中通过 `--volume=/etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro`，把宿主机的证书库挂载到容器内
2. 设置 `SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt`，强制 Python 使用系统 truststore（参见 https://docs.docker.com/reference/cli/docker/container/run/#env）

来自 [@KizzyCode](https://github.com/open-webui/open-webui/issues/1398#issuecomment-2258463210) 的 `compose.yaml` 示例：

```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - /var/containers/openwebui:/app/backend/data:rw
      - /etc/containers/openwebui/compusrv.crt:/etc/ssl/certs/ca-certificates.crt:ro
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    environment:
      - WEBUI_NAME=compusrv
      - ENABLE_SIGNUP=False
      - ENABLE_COMMUNITY_SHARING=False
      - WEBUI_SESSION_COOKIE_SAME_SITE=strict
      - WEBUI_SESSION_COOKIE_SECURE=True
      - ENABLE_OLLAMA_API=False
      - SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

`ro` 标志会以只读方式挂载 CA 证书库，避免意外修改宿主机上的 CA 数据。

**对于本地开发：**

你也可以通过修改 `Dockerfile`，在构建过程中加入证书。如果你想顺便修改 UI，这种方式会更方便。
由于构建采用的是[多阶段构建](https://docs.docker.com/build/building/multi-stage/)，所以前后端阶段都需要添加证书。

1. 前端（`build` 阶段）：

```dockerfile
COPY package.json package-lock.json <YourRootCert>.crt ./
ENV NODE_EXTRA_CA_CERTS=/app/<YourRootCert>.crt
RUN npm ci
```

2. 后端（`base` 阶段）：

```dockerfile
COPY <CorporateSSL.crt> /usr/local/share/ca-certificates/
RUN update-ca-certificates
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt     REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```
