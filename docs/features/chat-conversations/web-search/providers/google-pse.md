---
sidebar_position: 6
title: "Google PSE"
---

:::warning

**新的 Google PSE 项目已不再受支持。** Google 已将旧版 JSON API 限制为仅面向现有客户开放。新用户在使用 Google PSE 时会收到 `403 Forbidden` 错误。

:::

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [Environment Configuration documentation](/reference/env-configuration#web-search)。

:::

:::tip Troubleshooting

如果你在 web search 上遇到问题，请查看 [Web Search Troubleshooting Guide](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## Google PSE API

### 设置

1. 前往 Google Developers，使用 [Programmable Search Engine](https://developers.google.com/custom-search)，登录或创建账号
2. 前往 [control panel](https://programmablesearchengine.google.com/controlpanel/all)，点击 `Add`
3. 输入搜索引擎名称，根据需要设置其他属性，通过机器人验证后点击 `Create`
4. 生成 `API key` 并获取 `Search engine ID`（创建完成后可用）
5. 拿到 `API key` 与 `Search engine ID` 后，打开 `Open WebUI Admin panel`，点击 `Settings`，再进入 `Web Search`
6. 启用 `Web search`，并将 `Web Search Engine` 设为 `google_pse`
7. 将 `Google PSE API Key` 填为 `API key`，将 `Google PSE Engine Id` 填为第 4 步得到的值
8. 点击 `Save`

![Open WebUI Admin panel](/images/tutorial_google_pse1.png)

#### 注意

你还需要在提示词输入框中通过加号（`+`）按钮启用 `Web search`。
然后就可以开始搜索网页了 ;-)

![enable Web search](/images/tutorial_google_pse2.png)
