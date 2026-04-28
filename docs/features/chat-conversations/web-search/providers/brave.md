---
sidebar_position: 3
title: "Brave"
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

## Brave API

### Docker Compose 设置

将以下环境变量加入你的 Open WebUI `docker-compose.yaml`：

```yaml
services:
  open-webui:
    environment:
      ENABLE_WEB_SEARCH: True
      WEB_SEARCH_ENGINE: "brave"
      BRAVE_SEARCH_API_KEY: "YOUR_API_KEY"
      WEB_SEARCH_RESULT_COUNT: 3
      WEB_SEARCH_CONCURRENT_REQUESTS: 1
```

### 限速说明（免费层）

Brave 的免费 API 层有严格限制：**每秒仅允许 1 次请求**。如果你的 LLM 生成了多条搜索查询（这很常见），你可能会遇到 HTTP 429 “Too Many Requests” 错误。

**给免费层用户的推荐配置：**

- 在管理面板 > 设置 > 网页搜索 中，将 “并发请求数” 设为 `1`；或者直接使用环境变量
- 将 `WEB_SEARCH_CONCURRENT_REQUESTS: 1`，确保请求按顺序执行而不是并行发送

**自动重试机制：**

Open WebUI 会自动处理 Brave API 返回的 429 限流响应。当系统检测到 rate limit 错误时，会：

1. 等待 1 秒（以遵守 Brave 的限速规则）
2. 自动重试一次请求
3. 只有在重试仍失败时才会真正报错

这意味着即使你的连接速度足够快，以至于在一秒内连续发起多次顺序请求，自动重试机制通常也能在无需人工干预的情况下平稳恢复。

:::tip
如果你使用的是 Brave 的付费层，并且拥有更高限额，可以提高 `WEB_SEARCH_CONCURRENT_REQUESTS` 来获得更快的并行搜索速度。
:::

:::info 理解并发与限速

`WEB_SEARCH_CONCURRENT_REQUESTS` 控制的是**单次搜索请求内部**的并发度，而不是整个应用全局的总并发。

- **何时不是问题**：对于单用户实例，或低流量环境中用户很少在同一秒同时按下 Enter，通常将并发设为 `1` 就足以满足免费层（1 req/sec）限制
- **何时会成为问题**：如果多个用户在同一时刻同时触发网页搜索（例如 3 个用户在同一秒搜索），Open WebUI 会并行处理这些请求。每个用户请求会建立自己的连接池，这意味着 3 个请求会同时被发往 API，从而在免费层下触发限流

**注意：** 如果你运行的是一个有多个并发用户同时使用网页搜索的环境，强烈建议升级到付费 API 层。免费层并不是为多用户吞吐量设计的。
:::
