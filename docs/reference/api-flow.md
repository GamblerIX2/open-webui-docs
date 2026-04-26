---
sidebar_position: 40
title: "后端控制的 API 流程"
---

---

# 后端控制、兼容前端的 API 流程

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

- A **user message** must list its assistant reply IDs in `childrenIds`
- An **assistant message** typically has `childrenIds: []` (empty) unless there are follow-up messages

### The `currentId` Field

The `history` object must use `currentId` (**camelCase**, not `current_id`). This tells the frontend which message is at the end of the active conversation thread.

## Implementation Guide

### Critical Step: Enrich Chat Response with Assistant Message

The assistant message needs to exist in the chat data as a critical prerequisite **before** triggering the completion. This step is essential because the Open WebUI frontend expects assistant messages to exist in a specific structure.

The assistant message must appear in both locations:

- `chat.messages[]` — The main message array (used for legacy compatibility)
- `chat.history.messages[<assistantId>]` — The indexed message history (used by the frontend to render the tree)

**Expected structure of the assistant message:**

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

Without this enrichment, the assistant's response will not appear in the frontend interface, even if the completion is successful.

## Step-by-Step Implementation

### Step 1: Create Chat with User and Assistant Messages

This creates the chat with **both** the user message and an empty assistant placeholder in a single request. The response returns a `chatId` (in the `id` field) that will be used in subsequent requests.

:::tip

You can combine chat creation and assistant enrichment into this single step. The key is to include both the user message and an empty assistant message in the initial payload, with proper `parentId`, `childrenIds`, and `currentId` fields.

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

**Save the `id` field from the response** — this is your `chatId` for all subsequent steps.

:::note

The `messages[]` array at the top level is a flat list used for legacy compatibility. The `history.messages{}` object is the authoritative structure — it is a dictionary keyed by message ID that the frontend uses to build the conversation tree via `parentId` and `childrenIds`.

:::

### Step 2: Trigger Assistant Completion

Generate the actual AI response using the completion endpoint. Use the `chatId` from Step 1:

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

The `session_id` should be a unique UUID that you generate for this session. It helps maintain conversation context and is also used for WebSocket event routing if the frontend is open.

:::

#### Step 2.1: Trigger Assistant Completion with Knowledge Integration (RAG)

For advanced use cases involving knowledge bases or document collections, include knowledge files in the completion request:

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

### Step 3: Wait for Assistant Response Completion

Assistant responses can be handled in two ways depending on your implementation needs:

#### Option A: Stream Processing (Recommended)

If using `stream: true` in the completion request, you can process the streamed response in real-time and wait for the stream to complete. This is the approach used by the OpenWebUI web interface and provides immediate feedback.

#### Option B: Polling Approach

For implementations that cannot handle streaming, poll the chat endpoint until the response is ready. Use a retry mechanism with exponential backoff:

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

### Step 4: Fetch Final Chat

Retrieve the completed conversation:

```bash
curl -X GET https://<host>/api/v1/chats/<chatId> \
  -H "Authorization: Bearer <token>"
```

## Additional API Endpoints

### Fetch Knowledge Collection

Retrieve knowledge base information for RAG integration:

```bash
curl -X GET https://<host>/api/v1/knowledge/<knowledge-id> \
  -H "Authorization: Bearer <token>"
```

### Fetch Model Information

Get details about a specific model:

```bash
curl -X GET https://<host>/api/v1/models/model?id=<model-name> \
  -H "Authorization: Bearer <token>"
```

### Send Additional Messages to an Existing Chat

For multi-turn conversations, you can add new messages to an existing chat. You must include the full updated message tree with proper `parentId` and `childrenIds` linkage:

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

## Response Processing

### Parsing Assistant Responses

Assistant responses may be wrapped in markdown code blocks. Here's how to clean them:

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

- Removal of ````json` prefix
- Removal of ```` suffix
- Trimming whitespace
- JSON validation

## API Reference

### DTO Structures

#### Chat DTO (Complete Structure)

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

### Response Examples

#### Create Chat Response

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

#### Final Chat Response (After Completion)

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

#### OWUIKnowledge DTO (Knowledge Collection)

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

#### Model Information Response

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

### Field Reference Guide

#### Required vs Optional Fields

**Chat Creation - Required Fields:**

- `title` — Chat title (string)
- `models` — Array of model names (string[])
- `messages` — Initial message array
- `history` — Message tree with `currentId` and `messages` map

**Chat Creation - Optional Fields:**

- `files` — Knowledge files for RAG (defaults to empty array)
- `tags` — Chat tags (defaults to empty array)
- `params` — Model parameters (defaults to empty object)

**Message Structure - User Message:**

- **Required:** `id`, `role`, `content`, `timestamp`, `models`, `childrenIds`
- **Optional:** `parentId` (for threading; omit for the first message in a chat)

**Message Structure - Assistant Message:**

- **Required:** `id`, `role`, `content`, `parentId`, `childrenIds`, `model`, `modelName`, `modelIdx`, `timestamp`
- **Optional:** `done` (boolean, defaults to false), additional metadata fields

**ChatCompletionsRequest - Required Fields:**

- `chat_id` — Target chat ID
- `id` — Assistant message ID
- `messages` — Array of ChatCompletionMessage
- `model` — Model identifier
- `session_id` — Session identifier (caller-generated UUID)

**ChatCompletionsRequest - Optional Fields:**

- `stream` — Enable streaming (defaults to false)
- `background_tasks` — Control automatic tasks
- `features` — Enable/disable features
- `variables` — Template variables
- `filter_ids` — Pipeline filters
- `files` — Knowledge collections for RAG

#### Field Constraints

**Timestamps:**

- Format: Unix timestamp in **seconds** (not milliseconds) for message timestamps in `history.messages`
- The top-level chat `timestamp` field uses milliseconds
- Example: `1720000000` (July 3, 2024)

**UUIDs:**

- All ID fields (`id`, `parentId`, `session_id`) should use valid UUID v4 format
- Example: `550e8400-e29b-41d4-a716-446655440000`
- IDs are **generated by the caller**, not assigned by the server

**Model Names:**

- Must match available models in your Open WebUI instance
- Common examples: `gpt-4o`, `gpt-3.5-turbo`, `claude-3-sonnet`

**Session IDs:**

- Can be any unique string identifier
- Recommendation: Use UUID format for consistency

**Knowledge File Status:**

- Valid values: `"processed"`, `"processing"`, `"error"`
- Only use `"processed"` files for completions

## Important Notes

- This workflow is compatible with Open WebUI + backend orchestration scenarios
- **Critical: Use `currentId` (camelCase)** in the history object, not `current_id` (snake_case)
- **Critical: Include `childrenIds`** on every message — the frontend uses this to build the message tree
- No frontend code changes are required for this approach
- The `stream: true` parameter allows for real-time response streaming if needed
- `outlet()` filters run inline during `/api/chat/completions` when `chat_id` and `id` (message ID) are present in the request body. Pure API callers that omit these fields will have outlet silently skipped — see [Filter Functions: Enabling Outlet for Pure API Callers](/features/extensibility/plugin/functions/filter#enabling-outlet-for-pure-api-callers) for a workaround. The separate `/api/chat/completed` endpoint is deprecated and no longer needed
- Background tasks like title generation can be controlled via the `background_tasks` object
- Session IDs help maintain conversation context across requests
- **Knowledge Integration:** Use the `files` array to include knowledge collections for RAG capabilities
- **Response Parsing:** Handle JSON responses that may be wrapped in markdown code blocks
- **Error Handling:** Implement proper retry mechanisms for network timeouts and server errors

## Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Chat created but messages don't appear in UI | Missing `childrenIds` on messages | Add `childrenIds` array linking parent → child messages |
| Chat shows "How can I help you today?" | Using `current_id` instead of `currentId` | Use camelCase `currentId` in the history object |
| Completion works but response only appears as notification | Assistant message not in chat history before triggering completion | Include empty assistant placeholder in Step 1 |
| Messages exist in DB but frontend shows empty chat | Missing `parentId` or broken tree linkage | Ensure every message has correct `parentId` and parent's `childrenIds` includes the child |

## Summary

Use the Open WebUI backend APIs to:

1. **Start a chat with messages** — Create the conversation with user input and an empty assistant placeholder (including proper `childrenIds` and `currentId`)
2. **Trigger a reply** — Generate the AI response (with optional knowledge integration)
3. **Monitor completion** — Wait for the assistant response using streaming or polling
4. **Fetch the final chat** — Retrieve and parse the completed conversation

**Enhanced Capabilities:**

- **RAG Integration** — Include knowledge collections for context-aware responses
- **Asynchronous Processing** — Handle long-running AI operations with streaming or polling
- **Response Parsing** — Clean and validate JSON responses from the assistant
- **Session Management** — Maintain conversation context across requests

This enables backend-controlled workflows that still appear properly in the Web UI frontend chat interface, providing seamless integration between programmatic control and user experience.

The key advantage of this approach is that it maintains full compatibility with the Open WebUI frontend while allowing complete backend orchestration of the conversation flow, including advanced features like knowledge integration and asynchronous response handling.

## Testing

You can test your implementation by following the step-by-step CURL examples provided above. Make sure to replace placeholder values with your actual:

- Host URL
- Authentication token
- Chat IDs (from the create chat response)
- Message IDs (UUIDs you generate)
- Model names (matching your configured models)

:::tip

Start with a simple user message and gradually add complexity like knowledge integration and advanced features once the basic flow is working.

:::
