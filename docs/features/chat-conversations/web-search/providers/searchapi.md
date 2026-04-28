---
sidebar_position: 11
title: "SearchApi"
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

## SearchApi API

[SearchApi](https://searchapi.io) 提供一组实时 SERP API。任何当前或未来会返回 `organic_results` 的 SERP 引擎都可被支持。默认 web search engine 是 `google`，但你也可以改成 `bing`、`baidu`、`google_news`、`bing_news`、`google_scholar`、`google_patents` 等。

### 设置

1. 前往 [SearchApi](https://searchapi.io) 并登录或创建新账号
2. 进入 `Dashboard`（控制台），复制 API key
3. 拿到 `API key` 后，打开 `Open WebUI 管理面板`，点击 `Settings`，再进入 `Web Search`
4. 启用 `Web search`，并将 `Web Search Engine` 设为 `searchapi`
5. 在 `SearchApi API Key` 中填写你在第 2 步从 [SearchApi](https://www.searchapi.io/) 控制台复制的 `API key`
6. [可选] 填写你想查询的 `SearchApi engine` 名称，例如 `google`、`bing`、`baidu`、`google_news`、`bing_news`、`google_videos`、`google_scholar`、`google_patents`。默认值为 `google`
7. 点击 `Save`

![Open WebUI 管理面板](/images/tutorial_searchapi_search.png)

#### 注意

你还需要在提示词输入框中通过加号（`+`）按钮启用 `Web search`，才能使用 [SearchApi](https://www.searchapi.io/) 引擎进行网页搜索。

![启用 Web search](/images/enable_web_search.png)
