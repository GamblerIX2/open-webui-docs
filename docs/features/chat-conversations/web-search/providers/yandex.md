---
sidebar_position: 14
title: "Yandex"
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

## Yandex Search API

Yandex Web Search 通过 [Yandex Cloud Search API](https://yandex.cloud/en/docs/search-api/api-ref/WebSearch/search) 集成到 Open WebUI 中。

### Docker Compose 设置

将以下环境变量加入你的 Open WebUI `docker-compose.yaml`：

```yaml
services:
  open-webui:
    environment:
      ENABLE_WEB_SEARCH: True
      WEB_SEARCH_ENGINE: "yandex"
      YANDEX_WEB_SEARCH_API_KEY: "YOUR_YANDEX_CLOUD_API_KEY"
      # Optional: Override default search URL
      # YANDEX_WEB_SEARCH_URL: "https://searchapi.api.cloud.yandex.net/v2/web/search"
      # Optional: Custom JSON configuration for Yandex Search API
      # YANDEX_WEB_SEARCH_CONFIG: '{"query": {"searchType": "SEARCH_TYPE_RU"}}'
```

### 配置项说明

* **YANDEX_WEB_SEARCH_URL**：Yandex Search API 端点，默认值为 `https://searchapi.api.cloud.yandex.net/v2/web/search`
* **YANDEX_WEB_SEARCH_API_KEY**：你的 Yandex Cloud API Key
* **YANDEX_WEB_SEARCH_CONFIG**：一个可选的 JSON 字符串，用于自定义搜索请求。你可以通过它设置 Yandex Search API 支持的任意参数
