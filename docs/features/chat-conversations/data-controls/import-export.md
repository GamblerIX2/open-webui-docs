---
sidebar_position: 4
title: "💾 导入与导出"
---

Open WebUI 提供工具让你备份聊天历史、稍后恢复，或从其他平台迁移对话。

## 进入导入与导出

1. 点击侧边栏左下角的**用户名**或头像
2. 在菜单中选择 **Settings**
3. 进入 **Data Controls** 标签
4. 使用 **Import Chats** 或 **Export Chats** 按钮

## 导出聊天

点击 **Export Chats** 按钮后，系统会将你的所有对话导出为一个 JSON 文件。该备份包含：

- 所有聊天消息及其元数据
- 每段对话所使用的模型信息
- 时间戳与对话结构

:::tip 定期备份
建议你定期导出聊天，尤其是在进行重大更新或迁移之前。
:::

## 导入聊天

点击 **Import Chats** 按钮并选择一个 JSON 文件，即可恢复对话。Open WebUI 支持导入以下来源：

- **Open WebUI 导出文件**：来自此前导出的原生 JSON 格式
- **ChatGPT 导出文件**：来自 OpenAI ChatGPT 的导出对话（会自动识别并转换）
- **自定义 JSON 文件**：任何遵循下文预期结构的 JSON 文件

### 导入行为

- 导入的聊天会追加到现有对话中（不会覆盖已有数据）
- 每个导入聊天都会分配新的唯一 ID，因此重复导入同一文件会产生重复聊天
- 如果是 ChatGPT 导出文件，系统会自动检测格式并完成转换

## 聊天导入 JSON Schema

导入文件必须是一个**JSON 数组**，其中每个元素都是聊天对象。系统接受两种格式：**标准格式**（Open WebUI 导出使用）与**旧格式**。

Open WebUI 提供工具让你备份聊天历史、稍后恢复，或从其他平台迁移对话。

数组中的每个对象都应包含一个 `chat` 键，用于承载对话数据：

```json
[
  {
    "chat": {
      "title": "My Conversation",
      "models": ["llama3.2"],
      "history": {
        "currentId": "message-id-2",
        "messages": {
            "childrenIds": ["message-id-2"],
            "role": "user",
            "content": "Hello, how are you?",
            "timestamp": 1700000000
          },
          "message-id-2": {
            "id": "message-id-2",
            "parentId": "message-id-1",
            "childrenIds": [],
            "done": true,
            "timestamp": 1700000005
          }
    "meta": {
      "tags": ["greeting"]
    },
    "pinned": false,
    "folder_id": null,
    "created_at": 1700000000,
    "updated_at": 1700000005
  }
]
```

### 旧格式

如果数组中的对象**没有** `chat` 键，那么整个对象会被直接视为聊天数据本身（也就是系统会自动将其包装为 `{ "chat": <object> }`）：

```json
[
  {
    "title": "My Conversation",
    "models": ["llama3.2"],
    "history": {
      "currentId": "message-id-2",
      "messages": {
        "message-id-1": {
          "id": "message-id-1",
          "parentId": null,
          "childrenIds": ["message-id-2"],
          "role": "user",
          "content": "Hello!"
        },
        "message-id-2": {
          "id": "message-id-2",
          "parentId": "message-id-1",
          "childrenIds": [],
          "role": "assistant",
          "content": "Hi there!",
          "model": "llama3.2",
          "done": true
        }
      }
    }
  }
]
```

### 字段说明

#### 顶层聊天对象（标准格式）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `chat` | object | ✅ | 对话数据（见下方 Chat Data） |
| `meta` | object | ❌ | 元数据，如 `tags`（字符串数组）。默认 `{}` |
| `pinned` | boolean | ❌ | 聊天是否置顶。默认 `false` |
| `folder_id` | string \| null | ❌ | 聊天应放入的文件夹 ID。默认 `null` |
| `created_at` | integer \| null | ❌ | 聊天创建时间的 Unix 时间戳（秒） |
| `updated_at` | integer \| null | ❌ | 聊天最后更新时间的 Unix 时间戳（秒） |

#### Chat Data 对象

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | ❌ | 对话标题。默认 `"New Chat"` |
| `models` | string[] | ❌ | 该对话使用的模型标识符列表 |
| `history` | object | ✅ | 包含消息树（见下方 History） |
| `options` | object | ❌ | 聊天级选项 / 参数 |

#### History 对象

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `currentId` | string | ✅ | 当前活动对话分支中最后一条消息的 ID |
| `messages` | object | ✅ | 消息 ID → 消息对象的映射（见下方 Message） |

#### Message 对象

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | ✅ | 消息唯一标识符 |
| `parentId` | string \| null | ✅ | 父消息 ID；第一条消息则为 `null` |
| `childrenIds` | string[] | ✅ | 子消息 ID 数组；最后一条消息为空数组 `[]` |
| `role` | string | ✅ | 只能是 `"user"` 或 `"assistant"` |
| `content` | string | ✅ | 消息文本（支持 Markdown） |
| `model` | string | ❌ | 模型标识符（主要用于 assistant 消息） |
| `done` | boolean | ❌ | 响应是否已完成 |
| `timestamp` | integer | ❌ | 消息时间戳（Unix 秒） |
| `context` | string \| null | ❌ | 消息的附加上下文 |

:::info 消息树结构
消息采用的是**树形结构**，而非扁平列表。每条消息通过 `parentId` 指向父消息，通过 `childrenIds` 指向子消息。这让 Open WebUI 能支持分支式对话（例如编辑一条消息后得到不同回复）。`history.currentId` 字段指向当前活动分支中的最后一条消息。
:::

### ChatGPT 导出格式

当数组中的第一个对象包含 `mapping` 键时，系统会自动识别其为 ChatGPT 导出格式。你无需手动转换 ChatGPT 导出文件——直接导入即可，Open WebUI 会自动完成转换。

### 最小可用示例

最小有效导入文件如下：

```json
[
  {
    "title": "Quick Chat",
    "history": {
      "currentId": "msg-1",
      "messages": {
        "msg-1": {
          "id": "msg-1",
          "parentId": null,
          "childrenIds": [],
          "role": "user",
          "content": "Hello!"
        }
      }
    }
  }
]
```

它使用的是旧格式（没有 `chat` 包装），并且只包含一条用户消息。

## FAQ

**Q：导入聊天会覆盖现有对话吗？**  
**A：** 不会。导入的聊天会与现有对话并列存在。

**Q：我可以导入 Claude、Gemini 或其他平台的聊天吗？**  
**A：** 目前没有内置这些平台的转换器。你需要先把导出文件转换为本文说明的 JSON 结构。关键在于正确构建消息树，以及 `parentId` / `childrenIds` 的关系。

**Q：导入有大小限制吗？**  
**A：** 没有硬编码上限，但非常大的文件会需要更长处理时间。实际限制取决于你的服务器配置与可用内存。

**Q：如果我重复导入同一个文件会怎样？**  
**A：** 每次导入都会创建新的聊天并分配新的 ID，因此最终会出现重复对话。

**Q：支持哪些消息角色？**  
**A：** 导入功能支持 `"user"` 和 `"assistant"` 角色。System message 通常通过模型配置设置，而不是直接存储在聊天历史中。
