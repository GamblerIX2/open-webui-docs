---
sidebar_position: 9
title: "Mojeek"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [Environment Configuration documentation](/reference/env-configuration#web-search)。

:::

:::tip Troubleshooting

如果你在 web search 上遇到问题，请查看 [Web Search Troubleshooting Guide](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## Mojeek Search API

### 设置

1. 访问 [Mojeek Search API page](https://www.mojeek.com/services/search/web-search-api/) 获取 `API key`
2. 拿到 `API key` 后，打开 `Open WebUI Admin panel`，点击 `Settings`，再进入 `Web Search`
3. 启用 `Web search`，并将 `Web Search Engine` 设为 `mojeek`
4. 在 `Mojeek Search API Key` 中填写该 `API key`
5. 点击 `Save`

### Docker Compose 设置

将以下环境变量加入你的 Open WebUI `docker-compose.yaml`：

```yaml
services:
  open-webui:
    environment:
      ENABLE_WEB_SEARCH: True
      WEB_SEARCH_ENGINE: "mojeek"
      MOJEEK_SEARCH_API_KEY: "YOUR_MOJEEK_API_KEY"
      WEB_SEARCH_RESULT_COUNT: 3
      WEB_SEARCH_CONCURRENT_REQUESTS: 1
```
