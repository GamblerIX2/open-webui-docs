---
sidebar_position: 40
title: "Firefox 侧栏"
---

## 🦊 Firefox AI 聊天机器人侧栏

# 在 Mozilla Firefox 中将 Open WebUI 集成为本地 AI 浏览器助手

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看贡献教程。

:::

## 前置条件

在 Firefox 中把 Open WebUI 集成为 AI 聊天机器人助手前，请先确认：

- 已准备 Open WebUI 实例 URL（本地或域名均可）
- 已安装 Firefox 浏览器

## 在 Firefox 中启用 AI Chatbot

1. 点击右上角汉堡菜单按钮（三条横线，位于 `X` 按钮下方）
2. 打开 Firefox 设置
3. 进入 `Firefox Labs`
4. 打开 `AI Chatbot` 开关

你也可以通过 `about:config` 页面启用 AI Chatbot（见下节）。

## 配置 about:config 选项

1. 在 Firefox 地址栏输入 `about:config`
2. 点击 `Accept the Risk and Continue`
3. 搜索 `browser.ml.chat.enabled`，若未在 Firefox Labs 启用则将其设为 `true`
4. 搜索 `browser.ml.chat.hideLocalhost` 并设为 `false`

### browser.ml.chat.prompts.{#}

如需添加自定义提示词，请按以下步骤操作：

1. 搜索 `browser.ml.chat.prompts.{#}`（将 `{#}` 替换为数字，如 `0`、`1`、`2`）
2. 点击 `+` 新增提示词
3. 填写提示词 label、value 和 ID（例如 `{"id":"My Prompt", "value": "This is my custom prompt.", "label": "My Prompt"}`）
4. 按需重复以上步骤添加更多提示词

### browser.ml.chat.provider

1. Search for `browser.ml.chat.provider`
2. 填入你的 Open WebUI 实例 URL，并可附带可选参数（例如 `https://my-open-webui-instance.com/?model=browser-productivity-assistant&temporary-chat=true&tools=jina_web_scrape`）

## Open WebUI URL 参数

你可以使用以下 URL 参数来自定义 Open WebUI：

### 模型与模型选择

- `models`：为会话指定多个模型（逗号分隔），例如 `/?models=model1,model2`
- `model`：为会话指定单个模型，例如 `/?model=model1`

### YouTube 转录

- `youtube`：提供 YouTube 视频 ID，在聊天中转录该视频（例如 `/?youtube=VIDEO_ID`）

### Web Search

- `web-search`：将此参数设为 `true` 以启用网页搜索（例如 `/?web-search=true`）

### 工具选择

- `tools` 或 `tool-ids`：指定要在聊天中启用的工具 ID 列表（逗号分隔），例如 `/?tools=tool1,tool2` 或 `/?tool-ids=tool1,tool2`

### 通话叠加层

- `call`：将此参数设为 `true` 可在聊天界面启用视频/通话叠加层（例如 `/?call=true`）

### 初始查询

- `q`：设置聊天初始问题或提示词（例如 `/?q=Hello%20there`）

### 临时聊天会话

- `temporary-chat`：将此参数设为 `true` 可标记为临时会话（例如 `/?temporary-chat=true`）
  - *注意：临时聊天中的文档处理仅在前端执行。需要后端解析的复杂文件可能无法工作。*

更多 URL 参数及用法请见 https://docs.openwebui.com/features/chat-conversations/chat-features/url-params 。

## 其他 about:config 设置

以下 `about:config` 项可进一步自定义：

- `browser.ml.chat.shortcuts`：启用 AI Chatbot 侧栏自定义快捷键
- `browser.ml.chat.shortcuts.custom`：启用 AI Chatbot 侧栏自定义按键
- `browser.ml.chat.shortcuts.longPress`：设置快捷键长按延迟
- `browser.ml.chat.sidebar`：启用 AI Chatbot 侧栏
- `browser.ml.checkForMemory`：加载模型前检查可用内存
- `browser.ml.defaultModelMemoryUsage`：设置模型默认内存占用
- `browser.ml.enable`：启用 Firefox 机器学习功能
- `browser.ml.logLevel`：设置机器学习功能日志级别
- `browser.ml.maximumMemoryPressure`：设置最大内存压力阈值
- `browser.ml.minimumPhysicalMemory`：设置最小物理内存要求
- `browser.ml.modelCacheMaxSize`：设置模型缓存最大容量
- `browser.ml.modelCacheTimeout`：设置模型缓存超时时间
- `browser.ml.modelHubRootUrl`：设置模型仓库根 URL
- `browser.ml.modelHubUrlTemplate`：设置模型仓库 URL 模板
- `browser.ml.queueWaitInterval`：设置队列等待间隔
- `browser.ml.queueWaitTimeout`：设置队列等待超时

## 打开 AI Chatbot 侧栏

可使用以下方式打开 AI Chatbot 侧栏：

- 按 `CTRL+B` 打开书签侧栏后切换到 AI Chatbot
- 按 `CTRL+Alt+X` 直接打开 AI Chatbot 侧栏
