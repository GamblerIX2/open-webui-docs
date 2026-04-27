---
sidebar_position: 13
title: "SerpApi"
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

## SerpApi API

[SerpApi](https://serpapi.com/) 提供快速、易用且完整的 Google 及其他搜索引擎抓取 API。任何当前或未来会返回 `organic_results` 的 SERP engine 都可被支持。默认 web search engine 是 `google`，但也可以改为 `bing`、`baidu`、`google_news`、`google_scholar`、`google_patents` 等。

### 设置

1. 前往 [SerpApi](https://serpapi.com/) 并登录或创建账号
2. 进入 `Dashboard`，复制 API key
3. 拿到 `API key` 后，打开 `Open WebUI Admin panel`，点击 `Settings`，再进入 `Web Search`
4. 启用 `Web search`，并将 `Web Search Engine` 设为 `serpapi`
5. 在 `SerpApi API Key` 中填写你在第 2 步从 [SerpApi](https://serpapi.com/) dashboard 复制的 `API key`
6. [可选] 输入你要查询的 `SerpApi engine` 名称，例如 `google`、`bing`、`baidu`、`google_news`、`google_videos`、`google_scholar`、`google_patents`。默认值为 `google`。更多选项请参阅 [SerpApi documentation](https://serpapi.com/dashboard)
7. 点击 `Save`

![Open WebUI Admin panel](/images/tutorial_serpapi_search.png)

#### 注意

你还需要在提示词输入框中启用 `Web search`，才能通过 [SerpApi](https://serpapi.com/) 引擎搜索网页。

![enable Web search](/images/enable_web_search.png)
