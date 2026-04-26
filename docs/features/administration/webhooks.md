---
sidebar_position: 17
title: "Webhook 集成"
---

## 概述

Open WebUI 提供三种不同的 Webhook 集成，帮助您随时了解实例内发生的事件，并支持外部服务集成。这些 Webhook 允许您在 Discord、Slack 或任何支持传入 Webhook 的应用程序等外部服务中接收自动通知，也可以让外部服务向 Open WebUI 频道发送消息。

共有三种类型的 Webhook：

1.  **管理员 Webhook：** 当新用户注册时通知管理员的系统级 Webhook。
2.  **用户 Webhook：** 当对话响应就绪时通知单个用户的个人 Webhook，对于长时间运行的任务特别有用。
3.  **频道 Webhooks：** 允许外部服务向特定频道发送消息的传入 Webhook。

## 1. 管理员 Webhook：新用户通知

此 Webhook 专为管理员设计，用于监控 Open WebUI 实例上的新用户注册情况。

### 使用场景

- **用户注册跟踪：** 每当有新用户创建账户时，在专用的 Slack 或 Discord 频道中接收实时通知。这有助于您跟踪用户群并欢迎新成员。

### 配置

您可以通过两种方式配置管理员 Webhook：

#### 方式一：通过管理面板

1.  以管理员身份登录。
2.  导航到 **管理面板 > 设置 > 通用**。
3.  找到 **"Webhook URL"** 字段。
4.  输入您的外部服务（例如 Discord、Slack）提供的 Webhook URL。
5.  点击 **"保存"**。

#### 方式二：通过环境变量

您也可以使用 `WEBHOOK_URL` 环境变量设置 Webhook URL。更多详情请参阅[环境变量配置](https://docs.openwebui.com/reference/env-configuration/#webhook_url)文档。

### 负载格式

当新用户注册时，Open WebUI 将向配置的 URL 发送包含新用户详情的 JSON `POST` 请求。

**负载示例：**

```json
{
  "event": "new_user",
  "user": {
    "email": "tim@example.com",
    "name": "Tim"
  }
}
```

## 2. 用户 Webhook：对话响应通知

此 Webhook 允许单个用户在模型完成响应时收到通知。对于可能需要数分钟处理的长时间运行任务特别有用，即使您已离开 Open WebUI 标签页也能收到通知。

### 使用场景

- **长时间任务提醒：** 如果您提交了需要数分钟处理的复杂提示词，可以关闭浏览器标签页，仍会在响应就绪时立即收到通知。这让您可以处理其他任务，无需不断查看 Open WebUI 界面。

### 工作原理

仅当您**未主动使用 WebUI** 时才会发送通知。如果您已打开并聚焦该标签页，则不会触发 Webhook，避免不必要的通知。

### 启用/禁用用户 Webhook

用户 Webhook 默认禁用。管理员可以在需要时为所有用户启用此功能，也可以保持禁用以防止外部请求。

可通过两种方式操作：

1.  **直接在管理面板中：**
    - 转到 **管理面板 > 设置 > 通用 > 功能**。
    - 切换 **"用户 Webhook"** 开关。

2.  **使用环境变量：**
    - 在后端配置中将环境变量 `ENABLE_USER_WEBHOOKS` 设置为 `False`。这将全局禁用该功能并从用户个人资料中隐藏该设置。

### 配置

1.  点击左下角的个人头像打开设置菜单。
2.  导航到 **设置 > 账户**。
3.  找到 **"通知 Webhook"** 字段。
4.  输入您的个人 Webhook URL。
5.  点击 **"保存"**。

### 负载格式

当对话响应就绪且您处于非活跃状态时，Open WebUI 将向您的 Webhook URL 发送包含对话详情的 JSON `POST` 请求。

**负载示例：**

```json
{
  "event": "chat_response",
  "chat": {
    "id": "abc-123-def-456",
    "title": "我的精彩对话",
    "last_message": "这是我提交的提示词内容。"
  }
}
```

## 3. 频道 Webhooks：外部消息集成

频道 Webhooks 允许外部服务、自动化工具或脚本直接向 Open WebUI 频道发送消息。这支持与监控系统、CI/CD 流水线、通知服务或任何自定义自动化工具的无缝集成。

### 使用场景

- **系统监控：** 将监控工具（Prometheus、Grafana、Nagios）的告警直接发送到团队频道。
- **CI/CD 集成：** 将来自 GitHub Actions、GitLab CI 或 Jenkins 的构建状态通知发送到开发频道。
- **自定义自动化：** 与 n8n、Zapier 或自定义脚本集成，自动化消息发送。
- **外部通知：** 将外部服务的通知转发到您的 Open WebUI 工作空间。

### 工作原理

每个频道可以有多个 Webhook。每个 Webhook 具有：
- 外部服务可向其 `POST` 的唯一 **Webhook URL**
- 显示为消息作者的**显示名称**
- 可选的**头像图片**，用于直观识别 Webhook 来源
- **最后使用时间戳**，用于跟踪 Webhook 活动

通过 Webhook 发送的消息会以 Webhook 的身份显示在频道中，清楚表明它来自外部来源而非用户。

### 管理频道 Webhooks

只有**频道管理员**和**系统管理员**才能为频道创建和管理 Webhook。

#### 创建 Webhook

1.  导航到要添加 Webhook 的频道。
2.  点击频道菜单（⋮）并选择 **编辑频道**。
3.  在频道设置模态框中，找到 **Webhooks** 部分。
4.  点击 **管理** 打开 Webhooks 模态框。
5.  点击 **新建 Webhook** 创建新 Webhook。
6.  配置 Webhook：
    - **名称：** 将显示为消息作者的显示名称
    - **头像图片：** （可选）上传图片以代表此 Webhook
7.  点击 **保存** 创建 Webhook。
8.  使用 **复制 URL** 按钮复制生成的 Webhook URL。

#### Webhook URL 格式

```
{WEBUI_API_BASE_URL}/channels/webhooks/{webhook_id}/{token}
```

此 URL 是唯一的，包含身份验证令牌。任何拥有此 URL 的人都可以向频道发送消息，请妥善保管。

#### 更新 Webhook

1.  从频道设置中打开 **Webhooks** 模态框。
2.  点击要编辑的 Webhook 展开它。
3.  根据需要修改**名称**或**头像图片**。
4.  点击 **保存** 应用更改。

更新名称或图片时，Webhook URL 保持不变。更新后发送的消息将显示新名称/图片，但已有消息保留发送时的 Webhook 身份。

#### 删除 Webhook

1.  从频道设置中打开 **Webhooks** 模态框。
2.  点击要删除的 Webhook 展开它。
3.  点击 **删除**（垃圾桶）图标。
4.  确认删除。

删除后，Webhook URL 立即停止工作。此前由该 Webhook 发送的消息仍保留在频道中，但作者显示为"已删除的 Webhook"。

### 通过 Webhook 发送消息

要从外部服务发送消息，请向 Webhook URL 发送包含 JSON 负载的 `POST` 请求。

#### 请求格式

**端点：** `POST {webhook_url}`
**请求头：** `Content-Type: application/json`
**请求体：**

```json
{
  "content": "您的消息内容"
}
```

#### 示例：使用 cURL

```bash
curl -X POST "https://your-instance.com/api/channels/webhooks/{webhook_id}/{token}" \
  -H "Content-Type: application/json" \
  -d '{"content": "生产环境部署成功完成！🚀"}'
```

#### 示例：使用 Python

```python
import requests

webhook_url = "https://your-instance.com/api/channels/webhooks/{webhook_id}/{token}"
message = {
    "content": "构建 #1234 失败：单元测试未通过。"
}

response = requests.post(webhook_url, json=message)
print(response.json())
```

#### 响应格式

成功时，Webhook 将返回：

```json
{
  "success": true,
  "message_id": "abc-123-def-456"
}
```

### 安全注意事项

-   **URL 保护：** Webhook URL 包含身份验证令牌，请妥善保管，不要在公共仓库或日志中暴露。
-   **频道访问：** 任何拥有 Webhook URL 的人都可以向频道发送消息。仅与可信服务共享 URL。
-   **消息内容：** 在发送端验证和过滤消息内容，防止注入攻击。
-   **重新生成：** 如果 Webhook URL 泄露，请删除该 Webhook 并创建新的。

### Webhook 身份

通过 Webhook 发送的消息具有特殊的身份系统：
- 消息以 Webhook 的**名称**和**头像图片**显示
- 用户角色标记为 **"webhook"**，以区别于普通用户
- 如果 Webhook 被删除，其消息仍然可见，但显示"已删除的 Webhook"，当前 Webhook 名称不再显示
- 每条消息在其元数据中存储 Webhook ID，即使 Webhook 后来被修改或删除，也能正确归因

## 故障排查

如果您没有收到 Webhook 通知，请检查以下几点：

-   **验证 URL：** 确保 Webhook URL 正确并已正确粘贴到设置字段中。
-   **服务配置：** 仔细检查 Webhook 是否在外部服务（例如 Discord、Slack）中正确设置。
-   **防火墙/代理：** 确保您的网络或防火墙没有阻止来自 Open WebUI 服务器的传出请求。
-   **Open WebUI 日志：** 检查 Open WebUI 服务器日志中与 Webhook 失败相关的错误消息。

:::note

Open WebUI 中的 Webhook 功能正在持续改进。请关注未来更新中的更多事件类型和自定义选项。

:::