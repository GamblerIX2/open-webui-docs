---
sidebar_position: 22
title: "You.com"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 [贡献教程](https://docs.openwebui.com/contributing)。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [环境配置文档](/reference/env-configuration#web-search)。

:::

:::tip 故障排查

如果你在 web search 上遇到问题，请查看 [Web Search 故障排查指南](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## You.com YDC Index API

[You.com](https://you.com/) 提供 YDC Index API，这是一套会返回结构化搜索结果的 web search API，包括标题、URL、描述和 snippets。

### 前提条件

- 拥有来自 [You.com API](https://you.com/api) 的 You.com API key

### Docker Compose 设置

将以下环境变量加入你的 Open WebUI `docker-compose.yaml`：

```yaml
services:
  open-webui:
    environment:
      ENABLE_WEB_SEARCH: True
      WEB_SEARCH_ENGINE: "youcom"
      YOUCOM_API_KEY: "YOUR_API_KEY"
      WEB_SEARCH_RESULT_COUNT: 3
      WEB_SEARCH_CONCURRENT_REQUESTS: 10
```

### Admin Panel 设置

1. 使用管理员账号登录 Open WebUI
2. 前往 **Admin Panel** → **Settings** → **Web Search**
3. 将 **Web Search** 切换为 **On**
4. 在 **Web Search Engine** 下拉框中选择 **youcom**
5. 将你的 You.com API key 粘贴到 **You.com API Key** 字段
6. （可选）按需调整返回结果数量与并发设置
