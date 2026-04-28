---
sidebar_position: 40
title: "后端控制的 API 流程"
---

---

## 后端控制、兼容前端的 API 流程

:::warning

本教程为社区贡献内容，并不属于 Open WebUI 团队的官方支持。它仅用于展示如何根据你的具体需求定制 Open WebUI。想要贡献？请查看[贡献指南](/tutorials/contributing-tutorial)。

:::

本教程展示如何实现对 Open WebUI 对话的服务器端编排，并确保助手回复能在前端 UI 中正常显示。这种方法不需前端任何介入，并允许完全的后端控制聊天流程。
本教程已验证适用于 Open WebUI 版本 v0.6.15。未来版本可能会展开行为或 API 结构的变化。

## 前置条件

在实践本教程之前，请确保你有：

- 一个运行中的 Open WebUI 实例
- 有效的 API 认证令牌
- 能够访问 Open WebUI 后端 API
- 对 REST API 和 JSON 的基本了解
- 命令行工具：`curl`、`jq`（可选，用于 JSON 解析）

## 概述

本教程描述了一个包含 6 个步骤的完整流程，能够实现对 Open WebUI 对话的服务器端编排，同时确保助手回复能在前端 UI 中正常显示。

### 流程步骤

核心步骤如下：

1. **创建包含用户和助手消息的新对话** —— 使用用户输入和空助手占位符初始化对话
2. **触发助手补全** —— 生成实际的 AI 响应（可带知识集成）
3. **等待响应完成** —— 监控助手响应直到完全生成
4. **获取并处理最终对话** —— 获取并解析已完成的对话

这将实现服务器端编排，同时使回复在前端 UI 中显示，完全如同通过正常用户交互生成一样。

## 重要概念

### 消息 ID 由调用方生成

所有消息 ID（`user-msg-id`、`assistant-msg-id`）必须在**发起 API 调用之前**由**调用方以有效的 UUID 生成**。Open WebUI 不会为你分配消息 ID。使用任何 UUID v4 生成器即可。

示例（bash）：

```bash
USER_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")
ASSISTANT_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")
```

### `childrenIds` 字段

Open WebUI 前端将消息渲染为一个**树形结构**。每条消息必须包含 `childrenIds` 数组，列出其直接子消息的 ID。没有这个字段，前端无法遍历消息树，**消息将无法显示**，即使它们已存在于数据库中。

- **用户消息**必须在 `childrenIds` 中列出其对应的助手回复 ID
- **助手消息**通常使用 `childrenIds: []`（空数组），除非后面还有继续对话的消息

### `currentId` 字段

`history` 对象必须使用 `currentId`（**camelCase**，不是 `current_id`）。这个字段告诉前端当前活动对话线程最后一条消息是哪一条。

## 实现指南

### 关键步骤：在聊天响应中补充助手消息

在触发补全之前，助手消息必须作为关键前提先存在于聊天数据中。这个步骤至关重要，因为 Open WebUI 前端期望助手消息具有特定的结构。

助手消息必须同时出现在以下两个位置：

- `chat.messages[]` — 主要消息数组（用于旧版兼容）
- `chat.history.messages[<assistantId>]` — 按 ID 索引的消息历史（前端用它来渲染树状结构）

**助手消息的预期结构：**

```json
{
  "id": "<uuid>",
  "role": "assistant",
  "content": "",
  "parentId": "<user-msg-id>",
  "childrenIds": [],
  "model": "gpt-4o",
  "modelName": "gpt-4o",
  "modelIdx": 0,
  "done": false,
  "timestamp": 1720000001
}
```

如果不做这一步补充，即使补全成功，助手的回复也不会出现在前端界面中。

## 分步实现

### 第 1 步：创建包含用户和助手消息的对话

这一步会在一次请求中同时创建用户消息和一个空的助手占位符。响应会返回一个 `chatId`（位于 `id` 字段），后续请求会使用它。

:::tip

你可以把创建对话和补充助手消息合并到这一步。关键是在初始载荷中同时包含用户消息和空的助手消息，并正确设置 `parentId`、`childrenIds` 和 `currentId` 字段。

:::

```bash
USER_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")
ASSISTANT_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")
TIMESTAMP=$(date +%s)

curl -X POST https://<host>/api/v1/chats/new \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chat": {
      "title": "New Chat",
      "models": ["gpt-4o"],
      "messages": [
        {
          "id": "'"$USER_MSG_ID"'",
          "role": "user",
          "content": "Hi, what is the capital of France?",
          "timestamp": '"$TIMESTAMP"',
          "models": ["gpt-4o"],
          "childrenIds": ["'"$ASSISTANT_MSG_ID"'"]
        },
        {
          "id": "'"$ASSISTANT_MSG_ID"'",
          "role": "assistant",
          "content": "",
          "parentId": "'"$USER_MSG_ID"'",
          "childrenIds": [],
          "model": "gpt-4o",
          "modelName": "gpt-4o",
          "modelIdx": 0,
          "done": false,
          "timestamp": '"$((TIMESTAMP + 1))"'
        }
      ],
      "history": {
        "currentId": "'"$ASSISTANT_MSG_ID"'",
        "messages": {
          "'"$USER_MSG_ID"'": {
            "id": "'"$USER_MSG_ID"'",
            "role": "user",
            "content": "Hi, what is the capital of France?",
            "timestamp": '"$TIMESTAMP"',
            "models": ["gpt-4o"],
            "childrenIds": ["'"$ASSISTANT_MSG_ID"'"]
          },
          "'"$ASSISTANT_MSG_ID"'": {
            "id": "'"$ASSISTANT_MSG_ID"'",
            "role": "assistant",
            "content": "",
            "parentId": "'"$USER_MSG_ID"'",
            "childrenIds": [],
            "model": "gpt-4o",
            "modelName": "gpt-4o",
            "modelIdx": 0,
            "done": false,
            "timestamp": '"$((TIMESTAMP + 1))"'
          }
        }
      }
    }
  }'
```

**请保存响应中的 `id` 字段** —— 这就是后续步骤要用的 `chatId`。

:::note

顶层的 `messages[]` 数组是用于旧版兼容的扁平列表。`history.messages{}` 对象才是权威结构——它是一个以消息 ID 为键的字典，前端会通过 `parentId` 和 `childrenIds` 用它来构建对话树。

:::

### 第 2 步：触发助手补全

使用补全端点生成实际的 AI 响应。请使用第 1 步得到的 `chatId`：

```bash
curl -X POST https://<host>/api/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<chatId>",
    "id": "'"$ASSISTANT_MSG_ID"'",
    "messages": [
      {
        "role": "user",
        "content": "Hi, what is the capital of France?"
      }
    ],
    "model": "gpt-4o",
    "stream": true,
    "background_tasks": {
      "title_generation": true,
      "tags_generation": false,
      "follow_up_generation": false
    },
    "features": {
      "code_interpreter": false,
      "web_search": false,
      "image_generation": false,
      "memory": false
    },
    "variables": {
      "{{USER_NAME}}": "",
      "{{USER_LANGUAGE}}": "en-US",
      "{{CURRENT_DATETIME}}": "2025-07-14T12:00:00Z",
      "{{CURRENT_TIMEZONE}}": "Europe"
    },
    "session_id": "<session-uuid>"
  }'
```

:::note

`session_id` 应该是你为本次会话生成的唯一 UUID。它有助于保持对话上下文，如果前端处于打开状态，它也会用于 WebSocket 事件路由。

:::

#### 第 2.1 步：结合知识集成（RAG）触发助手补全

对于涉及知识库或文档集合的高级用例，可以在补全请求中包含知识文件：

```bash
curl -X POST https://<host>/api/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<chatId>",
    "id": "'"$ASSISTANT_MSG_ID"'",
    "messages": [
      {
        "role": "user",
        "content": "Hi, what is the capital of France?"
      }
    ],
    "model": "gpt-4o",
    "stream": true,
    "files": [
      {
        "id": "knowledge-collection-id",
        "type": "collection",
        "status": "processed"
      }
    ],
    "background_tasks": {
      "title_generation": true,
      "tags_generation": false,
      "follow_up_generation": false
    },
    "features": {
      "code_interpreter": false,
      "web_search": false,
      "image_generation": false,
      "memory": false
    },
    "variables": {
      "{{USER_NAME}}": "",
      "{{USER_LANGUAGE}}": "en-US",
      "{{CURRENT_DATETIME}}": "2025-07-14T12:00:00Z",
      "{{CURRENT_TIMEZONE}}": "Europe"
    },
    "session_id": "<session-uuid>"
  }'
```

### 第 3 步：等待助手响应完成

根据你的实现需求，助手响应可以通过两种方式处理：

#### 选项 A：流式处理（推荐）

如果在补全请求中使用 `stream: true`，你就可以实时处理流式响应，并等待流结束。这是 OpenWebUI Web 界面采用的方式，能提供即时反馈。

#### 选项 B：轮询方式

对于无法处理流式响应的实现，可以轮询聊天端点，直到响应准备好。请使用带指数退避的重试机制：

```bash

# Poll every few seconds until assistant content is populated
while true; do
  response=$(curl -s -X GET https://<host>/api/v1/chats/<chatId> \
    -H "Authorization: Bearer <token>")

  # Check if assistant message has content (response is ready)
  assistant_content=$(echo "$response" | jq -r ".chat.history.messages[\"$ASSISTANT_MSG_ID\"].content // empty")
  if [ -n "$assistant_content" ]; then
    echo "Assistant response is ready!"
    echo "$assistant_content"
    break
  fi

  echo "Waiting for assistant response..."
  sleep 2
done
```

### 第 4 步：获取最终对话

获取已完成的对话：

```bash
curl -X GET https://<host>/api/v1/chats/<chatId> \
  -H "Authorization: Bearer <token>"
```

## 其他 API 端点

### 获取知识集合

获取用于 RAG 集成的知识库信息：

```bash
curl -X GET https://<host>/api/v1/knowledge/<knowledge-id> \
  -H "Authorization: Bearer <token>"
```

### 获取模型信息

获取某个特定模型的详细信息：

```bash
curl -X GET https://<host>/api/v1/models/model?id=<model-name> \
  -H "Authorization: Bearer <token>"
```

### 向现有对话发送更多消息

对于多轮对话，你可以向现有聊天中追加新消息。你必须提供完整更新后的消息树，并正确维护 `parentId` 和 `childrenIds` 的关联：

```bash
NEW_USER_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")
NEW_ASSISTANT_MSG_ID=$(uuidgen || python3 -c "import uuid; print(uuid.uuid4())")

# First: update the chat to add the new user + assistant placeholder
# You need to link the previous assistant message to the new user message via childrenIds
curl -X POST https://<host>/api/v1/chats/<chatId> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chat": {
      "history": {
        "currentId": "'"$NEW_ASSISTANT_MSG_ID"'",
        "messages": {
          "'"$ASSISTANT_MSG_ID"'": {
            "childrenIds": ["'"$NEW_USER_MSG_ID"'"]
          },
          "'"$NEW_USER_MSG_ID"'": {
            "id": "'"$NEW_USER_MSG_ID"'",
            "role": "user",
            "content": "Can you tell me more about Paris?",
            "parentId": "'"$ASSISTANT_MSG_ID"'",
            "childrenIds": ["'"$NEW_ASSISTANT_MSG_ID"'"],
            "timestamp": '"$(date +%s)"',
            "models": ["gpt-4o"]
          },
          "'"$NEW_ASSISTANT_MSG_ID"'": {
            "id": "'"$NEW_ASSISTANT_MSG_ID"'",
            "role": "assistant",
            "content": "",
            "parentId": "'"$NEW_USER_MSG_ID"'",
            "childrenIds": [],
            "model": "gpt-4o",
            "modelName": "gpt-4o",
            "modelIdx": 0,
            "done": false,
            "timestamp": '"$(($(date +%s) + 1))"'
          }
        }
      }
    }
  }'

# Then: trigger completion for the new assistant message (same as Step 2)
curl -X POST https://<host>/api/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<chatId>",
    "id": "'"$NEW_ASSISTANT_MSG_ID"'",
    "messages": [
      { "role": "user", "content": "Hi, what is the capital of France?" },
      { "role": "assistant", "content": "The capital of France is Paris." },
      { "role": "user", "content": "Can you tell me more about Paris?" }
    ],
    "model": "gpt-4o",
    "stream": true,
    "session_id": "<session-uuid>"
  }'
```

:::note

When updating an existing chat via `POST /api/v1/chats/<chatId>`, the payload is **merged** with the existing chat data. You only need to include the fields you are changing. For `history.messages`, you can pass partial updates — existing messages that are not included in the update will be preserved.

:::

## 响应处理

### 解析助手回复

助手回复有时会被包裹在 Markdown 代码块中。可以按以下方式清理：

```bash

# Example raw response from assistant
raw_response='```json
{
  "result": "The capital of France is Paris.",
  "confidence": 0.99
}
```'

# Clean the response (remove markdown wrappers)
cleaned_response=$(echo "$raw_response" | sed 's/^```json//' | sed 's/```$//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

echo "$cleaned_response" | jq '.'
```

This cleaning process handles:

- 移除 ````json` 前缀
- 移除结尾的 ``` 代码块标记
- 去除首尾空白字符
- 验证 JSON 格式

## API 参考

### DTO 结构

#### Chat DTO（完整结构）

```json
{
  "id": "chat-uuid-12345",
  "title": "New Chat",
  "models": ["gpt-4o"],
  "files": [],
  "tags": [],
  "params": {
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "timestamp": 1720000000,
  "messages": [
    {
      "id": "user-msg-id",
      "role": "user",
      "content": "Hi, what is the capital of France?",
      "timestamp": 1720000000,
      "models": ["gpt-4o"],
      "childrenIds": ["assistant-msg-id"]
    },
    {
      "id": "assistant-msg-id",
      "role": "assistant",
      "content": "",
      "parentId": "user-msg-id",
      "childrenIds": [],
      "model": "gpt-4o",
      "modelName": "gpt-4o",
      "modelIdx": 0,
      "done": false,
      "timestamp": 1720000001
    }
  ],
  "history": {
    "currentId": "assistant-msg-id",
    "messages": {
      "user-msg-id": {
        "id": "user-msg-id",
        "role": "user",
        "content": "Hi, what is the capital of France?",
        "timestamp": 1720000000,
        "models": ["gpt-4o"],
        "childrenIds": ["assistant-msg-id"]
      },
      "assistant-msg-id": {
        "id": "assistant-msg-id",
        "role": "assistant",
        "content": "",
        "parentId": "user-msg-id",
        "childrenIds": [],
        "model": "gpt-4o",
        "modelName": "gpt-4o",
        "modelIdx": 0,
        "done": false,
        "timestamp": 1720000001
      }
    }
  },
  "currentId": "assistant-msg-id"
}
```

#### ChatCompletionsRequest DTO

```json
{
  "chat_id": "chat-uuid-12345",
  "id": "assistant-msg-id",
  "messages": [
    {
      "role": "user",
      "content": "Hi, what is the capital of France?"
    }
  ],
  "model": "gpt-4o",
  "stream": true,
  "background_tasks": {
    "title_generation": true,
    "tags_generation": false,
    "follow_up_generation": false
  },
  "features": {
    "code_interpreter": false,
    "web_search": false,
    "image_generation": false,
    "memory": false
  },
  "variables": {
    "{{USER_NAME}}": "",
    "{{USER_LANGUAGE}}": "en-US",
    "{{CURRENT_DATETIME}}": "2025-07-14T12:00:00Z",
    "{{CURRENT_TIMEZONE}}": "Europe"
  },
  "session_id": "session-uuid-67890",
  "filter_ids": [],
  "files": [
    {
      "id": "knowledge-collection-id",
      "type": "collection",
      "status": "processed"
    }
  ]
}
```

#### ChatCompletionMessage DTO

```json
{
  "role": "user",
  "content": "Hi, what is the capital of France?"
}
```

#### History DTO

```json
{
  "currentId": "assistant-msg-id",
  "messages": {
    "user-msg-id": {
      "id": "user-msg-id",
      "role": "user",
      "content": "Hi, what is the capital of France?",
      "timestamp": 1720000000,
      "models": ["gpt-4o"],
      "childrenIds": ["assistant-msg-id"]
    },
    "assistant-msg-id": {
      "id": "assistant-msg-id",
      "role": "assistant",
      "content": "The capital of France is Paris.",
      "parentId": "user-msg-id",
      "childrenIds": [],
      "model": "gpt-4o",
      "modelName": "gpt-4o",
      "modelIdx": 0,
      "timestamp": 1720000001
    }
  }
}
```

#### Message DTO (Complete Structure)

**User message:**

```json
{
  "id": "user-msg-id",
  "role": "user",
  "content": "Hi, what is the capital of France?",
  "timestamp": 1720000000,
  "models": ["gpt-4o"],
  "childrenIds": ["assistant-msg-id"]
}
```

**Assistant message:**

```json
{
  "id": "assistant-msg-id",
  "role": "assistant",
  "content": "The capital of France is Paris.",
  "parentId": "user-msg-id",
  "childrenIds": [],
  "model": "gpt-4o",
  "modelName": "gpt-4o",
  "modelIdx": 0,
  "done": true,
  "timestamp": 1720000001
}
```

### 响应示例

#### 创建对话响应

```json
{
  "id": "chat-uuid-12345",
  "user_id": "user-uuid",
  "title": "New Chat",
  "chat": {
    "title": "New Chat",
    "models": ["gpt-4o"],
    "messages": [
      {
        "id": "user-msg-id",
        "role": "user",
        "content": "Hi, what is the capital of France?",
        "timestamp": 1720000000,
        "models": ["gpt-4o"],
        "childrenIds": ["assistant-msg-id"]
      },
      {
        "id": "assistant-msg-id",
        "role": "assistant",
        "content": "",
        "parentId": "user-msg-id",
        "childrenIds": [],
        "model": "gpt-4o",
        "modelName": "gpt-4o",
        "modelIdx": 0,
        "done": false,
        "timestamp": 1720000001
      }
    ],
    "history": {
      "currentId": "assistant-msg-id",
      "messages": {
        "user-msg-id": {
          "id": "user-msg-id",
          "role": "user",
          "content": "Hi, what is the capital of France?",
          "timestamp": 1720000000,
          "models": ["gpt-4o"],
          "childrenIds": ["assistant-msg-id"]
        },
        "assistant-msg-id": {
          "id": "assistant-msg-id",
          "role": "assistant",
          "content": "",
          "parentId": "user-msg-id",
          "childrenIds": [],
          "model": "gpt-4o",
          "modelName": "gpt-4o",
          "modelIdx": 0,
          "done": false,
          "timestamp": 1720000001
        }
      }
    },
    "currentId": "assistant-msg-id"
  },
  "updated_at": 1720000000,
  "created_at": 1720000000
}
```

#### 最终对话响应（完成后）

```json
{
  "id": "chat-uuid-12345",
  "title": "Capital of France Discussion",
  "chat": {
    "models": ["gpt-4o"],
    "history": {
      "currentId": "assistant-msg-id",
      "messages": {
        "user-msg-id": {
          "id": "user-msg-id",
          "role": "user",
          "content": "Hi, what is the capital of France?",
          "timestamp": 1720000000,
          "models": ["gpt-4o"],
          "childrenIds": ["assistant-msg-id"]
        },
        "assistant-msg-id": {
          "id": "assistant-msg-id",
          "role": "assistant",
          "content": "The capital of France is Paris. Paris is not only the capital but also the most populous city in France, known for its iconic landmarks such as the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral.",
          "parentId": "user-msg-id",
          "childrenIds": [],
          "model": "gpt-4o",
          "modelName": "gpt-4o",
          "modelIdx": 0,
          "done": true,
          "timestamp": 1720000001
        }
      }
    },
    "currentId": "assistant-msg-id"
  }
}
```

#### OWUIKnowledge DTO（知识集合）

```json
{
  "id": "knowledge-collection-id",
  "type": "collection",
  "status": "processed",
  "name": "Geography Knowledge Base",
  "description": "Contains information about world geography and capitals",
  "created_at": 1720000000,
  "updated_at": 1720000001
}
```

#### 模型信息响应

```json
{
  "id": "gpt-4o",
  "name": "GPT-4 Optimized",
  "model": "gpt-4o",
  "base_model_id": "gpt-4o",
  "meta": {
    "description": "Most advanced GPT-4 model optimized for performance",
    "capabilities": ["text", "vision", "function_calling"],
    "context_length": 128000,
    "max_output_tokens": 4096
  },
  "params": {
    "temperature": 0.7,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  },
  "created_at": 1720000000,
  "updated_at": 1720000001
}
```

### 字段参考

#### 必填与可选字段

**创建对话 - 必填字段：**

- `title` — Chat title (string)
- `models` — Array of model names (string[])
- `messages` — Initial message array
- `history` — Message tree with `currentId` and `messages` map

**创建对话 - 可选字段：**

- `files` — Knowledge files for RAG (defaults to empty array)
- `tags` — Chat tags (defaults to empty array)
- `params` — Model parameters (defaults to empty object)

**消息结构 - 用户消息：**

- **Required:** `id`, `role`, `content`, `timestamp`, `models`, `childrenIds`
- **Optional:** `parentId` (for threading; omit for the first message in a chat)

**消息结构 - 助手消息：**

- **Required:** `id`, `role`, `content`, `parentId`, `childrenIds`, `model`, `modelName`, `modelIdx`, `timestamp`
- **Optional:** `done` (boolean, defaults to false), additional metadata fields

**ChatCompletionsRequest - 必填字段：**

- `chat_id` — Target chat ID
- `id` — Assistant message ID
- `messages` — Array of ChatCompletionMessage
- `model` — Model identifier
- `session_id` — Session identifier (caller-generated UUID)

**ChatCompletionsRequest - 可选字段：**

- `stream` — Enable streaming (defaults to false)
- `background_tasks` — Control automatic tasks
- `features` — Enable/disable features
- `variables` — Template variables
- `filter_ids` — Pipeline filters
- `files` — Knowledge collections for RAG

#### 字段约束

**时间戳：**

- Format: Unix timestamp in **seconds** (not milliseconds) for message timestamps in `history.messages`
- The top-level chat `timestamp` field uses milliseconds
- Example: `1720000000` (July 3, 2024)

**UUID：**

- All ID fields (`id`, `parentId`, `session_id`) should use valid UUID v4 format
- Example: `550e8400-e29b-41d4-a716-446655440000`
- IDs are **generated by the caller**, not assigned by the server

**模型名称：**

- Must match available models in your Open WebUI instance
- Common examples: `gpt-4o`, `gpt-3.5-turbo`, `claude-3-sonnet`

**会话 ID：**

- Can be any unique string identifier
- Recommendation: Use UUID format for consistency

**知识文件状态：**

- Valid values: `"processed"`, `"processing"`, `"error"`
- Only use `"processed"` files for completions

## 重要说明

- This workflow is compatible with Open WebUI + backend orchestration scenarios
- **Critical: Use `currentId` (camelCase)** in the history object, not `current_id` (snake_case)
- **Critical: Include `childrenIds`** on every message — the frontend uses this to build the message tree
- No frontend code changes are required for this approach
- `stream: true` 参数可在需要时提供实时流式响应
- 当请求体中同时包含 `chat_id` 和 `id`（消息 ID）时，`outlet()` 过滤器会在 `/api/chat/completions` 中同步执行。纯 API 调用如果省略这些字段，outlet 会被静默跳过——相关行为细节请参见 [过滤函数：可切换过滤器 vs. 始终启用过滤器](/features/extensibility/plugin/functions/filter#toggleable-filters-vs-always-on-filters)。单独的 `/api/chat/completed` 端点已弃用，不再需要
- 标题生成等后台任务可以通过 `background_tasks` 对象控制
- 会话 ID 有助于在多个请求之间保持对话上下文
- **知识集成：** 使用 `files` 数组包含知识集合，以支持 RAG 能力
- **响应解析：** 处理可能被 Markdown 代码块包裹的 JSON 响应
- **错误处理：** 为网络超时和服务器错误实现合适的重试机制

## 常见问题

| 现象 | 原因 | 解决办法 |
| --- | --- | --- |
| 已创建对话但消息没有显示在 UI 中 | 消息缺少 `childrenIds` | 添加 `childrenIds` 数组，把父消息和子消息连接起来 |
| 对话显示“今天我能帮你做什么？” | 使用了 `current_id`，而不是 `currentId` | 在 history 对象中使用 camelCase 的 `currentId` |
| 补全成功但回复只以通知形式出现 | 触发补全前，助手消息没有先写入聊天历史 | 在第 1 步中包含空的助手占位符 |
| 数据库里有消息，但前端显示空对话 | 缺少 `parentId` 或树状关联断裂 | 确保每条消息都有正确的 `parentId`，且父消息的 `childrenIds` 包含该子消息 |

## 总结

使用 Open WebUI 后端 API 来：

1. **用消息创建对话** — 使用用户输入和空的助手占位符创建对话（包含正确的 `childrenIds` 和 `currentId`）
2. **触发回复** — 生成 AI 响应（可选地结合知识集成）
3. **监控完成状态** — 使用流式或轮询方式等待助手回复
4. **获取最终对话** — 获取并解析已完成的对话

**增强能力：**

- **RAG 集成** — 通过知识集合提供上下文感知回复
- **异步处理** — 使用流式或轮询处理耗时较长的 AI 操作
- **响应解析** — 清理并验证助手返回的 JSON 响应
- **会话管理** — 在多个请求之间保持对话上下文

这样即可实现由后端控制的工作流，同时在 Web UI 前端聊天界面中正常呈现，兼顾程序化控制与用户体验。

这种方案的关键优势在于，它在允许后端完全编排对话流程的同时，仍与 Open WebUI 前端保持完整兼容，并支持知识集成、异步响应处理等高级能力。

## 测试

你可以按照上面提供的分步 `curl` 示例测试实现。请务必把占位符替换成你自己的实际值：

- 主机 URL
- 认证令牌
- 对话 ID（来自创建对话响应）
- 消息 ID（你生成的 UUID）
- 模型名称（与你配置的模型一致）

:::tip

先从一个简单的用户消息开始，确认基础流程正常后，再逐步加入知识集成和高级功能。

:::
