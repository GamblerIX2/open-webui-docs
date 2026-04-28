---
sidebar_position: 18
title: "Yacy"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [环境配置文档](/reference/env-configuration#web-search)。

:::

:::tip 故障排查

如果你在 web search 上遇到问题，请查看 [Web Search 故障排查指南](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## Yacy API

### 设置

1. 前往：`Admin Panel` -> `Settings` -> `Web Search`
2. 打开 `Enable Web Search`
3. 将 `Web Search Engine` 从下拉框中设为 `yacy`
4. 将 `Yacy Instance URL` 设为以下示例之一：

    - `http://yacy:8090`（使用容器名和暴露端口，适合 Docker 部署）
    - `http://host.docker.internal:8090`（使用 `host.docker.internal` 和宿主机端口，适合 Docker 部署）
    - `https://<yacy.local>:8443`（使用本地域名，适合局域网访问）
    - `https://yacy.example.com`（使用自定义域名，适合公网或私有 Yacy 实例）
    - `https://yacy.example.com:8443`（通过 Yacy 默认 HTTPS 端口访问）

5. 如果你的 Yacy 实例需要鉴权，可选填写 Yacy 用户名和密码；若两者都留空，则会跳过 digest authentication
6. 点击保存

![Open WebUI 管理面板中的 Yacy 配置](/images/tutorial_yacy.png)
