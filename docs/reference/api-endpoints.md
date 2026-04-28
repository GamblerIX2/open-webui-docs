---
sidebar_position: 400
title: "API 接口"
---

本指南提供了有效使用 API 接口所需的关键信息，帮助你实现与模型的无缝集成和自动化。请注意，该配置目前处于实验阶段，未来可能会有更新和改进。

## 认证

为确保 API 的安全访问，需要进行身份认证 🛡️。你可以使用 Bearer Token 机制对 API 请求进行认证。在 Open WebUI 的**设置 > 账户**中获取你的 API Key，或者使用 JWT（JSON Web Token）进行认证。有关启用和生成 API Key 的完整说明（包括管理员开关和非管理员用户所需的群组权限），请参阅 [API 密钥](/features/authentication-access/api-keys)。

## Swagger 文档链接

:::important

请确保将 `ENV` 环境变量设置为 `dev`，以访问这些服务的 Swagger 文档。没有此配置，文档将不可用。

:::

访问 Open WebUI 提供的各服务的详细 API 文档：

| 应用 | 文档路径 |
|-------------|-------------------------|
| 主应用 | `/docs` |

## 主要 API 接口

### 📜 获取所有模型

- **接口**：`GET /api/models`
- **说明**：获取通过 Open WebUI 创建或添加的所有模型。
- **示例**：

  ```bash
  curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:3000/api/models
  ```

### 💬 聊天补全

- **接口**：`POST /api/chat/completions`
- **说明**：作为兼容 OpenAI API 的聊天补全接口，支持 Open WebUI 上的所有模型，包括 Ollama 模型、OpenAI 模型和 Open WebUI Function 模型。

- **Curl 示例**：

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "llama3.1",
        "messages": [
          {
            "role": "user",
            "content": "Why is the sky blue?"
          }
        ]
      }'
  ```

- **Python 示例**：

  ```python
  import requests

  def chat_with_model(token):
      url = 'http://localhost:3000/api/chat/completions'
      headers = {
          'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json'
      }
      data = {
        "model": "granite3.1-dense:8b",
        "messages": [
          {
            "role": "user",
            "content": "Why is the sky blue?"
          }
        ]
      }
      response = requests.post(url, headers=headers, json=data)
      return response.json()
  ```

### 🔮 Anthropic 消息 API

Open WebUI 提供兼容 Anthropic 消息 API 的接口。这允许为 Anthropic API 构建的工具、SDK 和应用程序直接与 Open WebUI 配合工作——通过所有已配置的模型、过滤器和流水线路由请求。

在内部，该接口将 Anthropic 请求格式转换为 OpenAI 聊天补全格式，通过现有的聊天补全流水线路由，并将响应转换回 Anthropic 格式。支持流式和非流式请求。

- **接口**：`POST /api/message`，`POST /api/v1/messages`
- **认证**：支持 `Authorization: Bearer YOUR_API_KEY` 和 Anthropic 的 `x-api-key: YOUR_API_KEY` 头

- **Curl 示例**（非流式）：

  ```bash
  curl -X POST http://localhost:3000/api/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4o",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": "Why is the sky blue?"
          }
        ]
      }'
  ```

- **Curl 示例**（流式）：

  ```bash
  curl -X POST http://localhost:3000/api/v1/messages \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4o",
        "max_tokens": 1024,
        "stream": true,
        "messages": [
          {
            "role": "user",
            "content": "Why is the sky blue?"
          }
        ]
      }'
  ```

- **Python 示例**（使用 Anthropic SDK）：

  ```python
  from anthropic import Anthropic

  client = Anthropic(
      api_key="YOUR_OPEN_WEBUI_API_KEY",
      base_url="http://localhost:3000/api",
  )

  message = client.messages.create(
      model="gpt-4o",
      max_tokens=1024,
      messages=[
          {"role": "user", "content": "Why is the sky blue?"}
      ],
  )
  print(message.content[0].text)
  ```

  :::warning
  `base_url` 必须是 `http://localhost:3000/api`（而非 `/api/v1`）。Anthropic SDK 会自动将 `/v1/messages` 附加到 base URL 后面。
  :::

- **Claude Code 配置**：

  要将 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 与 Open WebUI 作为代理一起使用，请将其配置为指向你的 Open WebUI 实例：

  ```bash
  # 设置 Claude Code 的环境变量
  export ANTHROPIC_BASE_URL="http://localhost:3000/api"
  export ANTHROPIC_API_KEY="YOUR_OPEN_WEBUI_API_KEY"

  # 然后正常运行 Claude Code
  claude
  ```

  或者，创建或编辑 `~/.claude/settings.json`：

  ```json
  {
    "env": {
      "ANTHROPIC_BASE_URL": "http://localhost:3000/api",
      "ANTHROPIC_AUTH_TOKEN": "YOUR_OPEN_WEBUI_API_KEY"
    }
  }
  ```

  这会将所有 Claude Code 请求通过 Open WebUI 的认证和访问控制层路由，让你可以使用任何已配置的模型（包括通过 Ollama 或 vLLM 的本地模型）与 Claude Code 的界面配合使用。

:::info
Open WebUI 中配置的所有模型都可以通过此接口访问——包括 Ollama 模型、OpenAI 模型和任何自定义 Function 模型。`model` 字段应使用模型在 Open WebUI 中显示的模型 ID。过滤器（inlet/stream）应用于这些请求，与兼容 OpenAI 的接口相同。

**工具使用：** Anthropic 消息接口支持工具使用（`tools` 和 `tool_choice` 参数）。来自上游模型的工具调用会被转换为流式和非流式响应中的 Anthropic 格式 `tool_use` 内容块。
:::

### 🔧 API 请求中的过滤器和 Function 行为

直接使用 API 接口时，过滤器（Functions）的行为与通过 Web 界面发出请求时有所不同。

:::info 认证说明
Open WebUI 同时接受 **API Key**（以 `sk-` 为前缀）和 **JWT Token** 进行 API 认证。这是有意为之的——Web 界面在内部对相同的 API 接口使用 JWT Token。两种认证方式提供同等的 API 访问权限。
:::

#### 过滤器执行

| 过滤器 Function | WebUI 请求 | 直接 API — 稳定版（`main`） | 直接 API — 预发布版（`dev`） |
|----------------|--------------|------------------------------|-----------------------------------|
| `inlet()` | ✅ 执行 | ✅ 执行 | ✅ 执行 |
| `stream()` | ✅ 执行 | ✅ 执行 | ✅ 执行 |
| `outlet()` | ✅ 执行 | ❌ `/api/chat/completions` 不调用——使用 `/api/chat/completed` | ⚠️ 仅在特定条件下内联执行（见下文） |

`inlet()` 函数始终执行，非常适合用于：
- **速率限制** - 追踪并限制每用户的请求数
- **请求日志** - 记录所有 API 使用情况以供监控
- **输入验证** - 在请求到达模型之前拒绝无效请求

:::danger 直接 API 调用的 Outlet 行为——请仔细阅读
本页面的早期版本称 `outlet()` 会在 `/api/chat/completions` 的 WebUI 和 API 请求中内联运行。这是错误的。以下是经后端源码验证的准确情况：

**标记发布版本 / `main`**：`outlet()` 根本**不会**被 `/api/chat/completions` 内联调用。只有当调用方向 `/api/chat/completed` 发送第二次 POST 请求时，它才会运行。目前，如果你的集成需要 `outlet()`，仍然必须发起那次第二步调用。

**`dev` / 预发布版本**：`outlet()` 可以在 `/api/chat/completions` 后内联运行，但仅当**以下所有条件都满足**时：

1. 请求体中**同时包含** `chat_id` **和** `id`（助手消息 ID）。如果缺少任一项，后端将没有 `event_emitter`，并静默跳过 outlet 块。
2. `chat_id` 是经认证用户已经**拥有的**对话，否则请求将在到达 outlet 路径之前返回 404。（或者，发送不带 `chat_id` 的 `parent_id: null`，以触发服务器端新对话的创建。）
3. 请求为**非流式**。满足条件 (1) 和 (2) 的流式请求会走一条专为 WebUI 设计的代码路径：服务器自行消费上游流并通过 WebSocket 将内容路由给用户，因此流式 API 调用者收到的 HTTP 响应实际上为空。Outlet 会运行，但你无法通过 HTTP 看到其效果。

即使在非流式情况下，**`outlet()` 也不会重写 HTTP 响应体**。它会更新已持久化的聊天消息并发出 `chat:outlet` WebSocket 事件，但你的客户端收到的 JSON 是 outlet 处理前的内容。如果你需要 outlet 过滤后的文本，请从聊天记录中读取、订阅 WebSocket，或继续使用 `/api/chat/completed`。

**实用建议**：如果你是纯 API 消费者（Continue.dev、Claude Code、自定义脚本、Langfuse 流水线等），请将 `/api/chat/completed` 作为当前运行 `outlet()` 的受支持方式。`dev` 上的内联执行主要面向已在 WebSocket 上监听的 WebUI 形态客户端。
:::

#### 旧版/API 支持接口：`/api/chat/completed`

`POST /api/chat/completed` 是为直接 API 集成可靠运行 `outlet()` 的接口。在 `dev` 版本中，它被标记为已弃用，以支持内联执行，但如上所述，内联执行目前不会向纯 API 调用者返回过滤后的响应体——因此在实践中，`/api/chat/completed` 仍是当今大多数 API 集成的正确选择。

- **接口**：`POST /api/chat/completed`
- **说明**：对已完成的聊天载荷无条件运行 `outlet()` 过滤器（以及流水线 outlet 过滤器）。返回过滤后的载荷。

- **Curl 示例**：

  ```bash
  curl -X POST http://localhost:3000/api/chat/completed \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "llama3.1",
        "messages": [
          {"role": "user", "content": "Hello"},
          {"role": "assistant", "content": "Hi! How can I help you today?"}
        ],
        "chat_id": "optional-uuid",
        "session_id": "optional-session-id"
      }'
  ```

- **Python 示例**：

  ```python
  import requests

  def complete_chat_with_outlet(token, model, messages, chat_id=None):
      """
      第二步调用，为直接 API 调用者真正运行 outlet()。
      在标记版本中，/api/chat/completions 根本不会内联运行 outlet。
      在 dev 版本中，它仅在特定条件下内联运行且不重写
      HTTP 响应体，因此对于大多数需要通过 HTTP 获取 outlet 输出
      的 API 集成来说，这个接口仍然是正确的选择。
      """
      url = 'http://localhost:3000/api/chat/completed'
      headers = {
          'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json'
      }
      payload = {
          'model': model,
          'messages': messages  # 包含完整对话记录（含助手回复）
      }
      if chat_id:
          payload['chat_id'] = chat_id
      
      response = requests.post(url, headers=headers, json=payload)
      return response.json()
  ```

:::tip
如果你今天需要通过 HTTP 获取 `outlet()` 的输出，请先调用 `/api/chat/completions`，再调用 `/api/chat/completed`。`dev` 版本上的内联执行主要面向从 WebSocket 读取数据的 WebUI 形态客户端。有关过滤器行为的更多详情，请参阅[过滤器 Function 文档](/features/extensibility/plugin/functions/filter#-filter-behavior-with-api-requests)。
:::

### 🦙 Ollama API 代理支持

如果你想直接与 Ollama 模型交互——包括生成嵌入向量或原始提示词流式传输——Open WebUI 通过代理路由提供对原生 Ollama API 的透明直通。

- **基础 URL**：`/ollama/<api>`
- **参考**：[Ollama API 文档](https://github.com/ollama/ollama/blob/main/docs/api.md)

#### 🔁 生成补全（流式）

```bash
curl http://localhost:3000/ollama/api/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'
```

#### 📦 列出可用模型

```bash
curl http://localhost:3000/ollama/api/tags \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 🧠 生成嵌入向量

```bash
curl -X POST http://localhost:3000/ollama/api/embed \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "llama3.2",
  "input": ["Open WebUI is great!", "Let'\''s generate embeddings."]
}'
```

:::info
使用 Ollama 代理接口时，POST 请求**必须**包含 `Content-Type: application/json` 头部，否则 API 可能无法解析请求体。如果实例已配置安全认证，还需要包含授权头部。
:::

#### 🔮 Responses API（兼容 OpenAI）

Ollama 支持 OpenAI Responses API 格式。Open WebUI 通过 Ollama 路由器代理路由，使用与聊天补全相同的模型解析、访问控制和前缀处理。

```bash
curl -X POST http://localhost:3000/ollama/v1/responses \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "llama3.2",
  "input": "Why is the sky blue?"
}'
```

这允许 API 消费者（Codex、Claude Code 等）直接将 Responses API 与 Ollama 托管模型配合使用，无需配置单独的兼容 OpenAI 连接。

这非常适合使用 Ollama 模型在 Open WebUI 后端构建搜索索引、检索系统或自定义流水线。

<a id="-retrieval-augmented-generation-rag"></a>
### 🧩 检索增强生成（RAG）

检索增强生成（RAG）功能允许你将外部数据源内容融入到响应中。以下介绍如何通过 API 管理文件和知识库集合，以及如何在聊天补全中有效使用它们。

#### 上传文件

要在 RAG 响应中使用外部数据，首先需要上传文件。上传文件的内容会自动提取并存储到向量数据库中。

- **接口**：`POST /api/v1/files/`
- **查询参数**：
  - `process`（布尔型，默认：`true`）：是否提取内容并计算嵌入向量
  - `process_in_background`（布尔型，默认：`true`）：是否异步处理
- **Curl 示例**：

  ```bash
  curl -X POST -H "Authorization: Bearer YOUR_API_KEY" -H "Accept: application/json" \
  -F "file=@/path/to/your/file" http://localhost:3000/api/v1/files/
  ```

- **Python 示例**:
  ```python
  url = 'http://localhost:3000/api/v1/files/'
  headers = {
      'Authorization': f'Bearer {token}',
      'Accept': 'application/json'
  }
  files = {'file': open(file_path, 'rb')}
  response = requests.post(url, headers=headers, files=files)
  return response.json()
  ```

:::warning 异步处理与竞争条件

默认情况下，文件上传为**异步处理**。上传接口会立即返回文件 ID，内容提取和嵌入向量计算在后台继续进行。

如果在处理完成之前尝试将文件添加到知识库，你会收到 `400` 错误：

```
The content provided is empty. Please ensure that there is text or data present before proceeding.
```

**在将文件添加到知识库之前，必须等待文件处理完成。** 详见下方[检查文件处理状态](#checking-file-processing-status)部分。

:::

#### 检查文件处理状态 {#checking-file-processing-status}

将文件添加到知识库之前，请通过状态接口验证处理已完成。

- **接口**：`GET /api/v1/files/{id}/process/status`
- **查询参数**：
  - `stream`（布尔型，默认：`false`）：如果为 `true`，则返回服务器发送事件（SSE）流

**状态値：**
| 状态 | 说明 |
|--------|-------------|
| `pending` | 文件仍在处理中 |
| `completed` | 处理成功完成 |
| `failed` | 处理失败（查看 `error` 字段了解详情） |

- **Python 示例**（轮询）：

  ```python
  import requests
  import time

  def wait_for_file_processing(token, file_id, timeout=300, poll_interval=2):
      """
      Wait for a file to finish processing.
      
      Returns:
          dict: Final status with 'status' key ('completed' or 'failed')
      
      Raises:
          TimeoutError: If processing doesn't complete within timeout
      """
      url = f'http://localhost:3000/api/v1/files/{file_id}/process/status'
      headers = {'Authorization': f'Bearer {token}'}
      
      start_time = time.time()
      while time.time() - start_time < timeout:
          response = requests.get(url, headers=headers)
          result = response.json()
          status = result.get('status')
          
          if status == 'completed':
              return result
          elif status == 'failed':
              raise Exception(f"File processing failed: {result.get('error')}")
          
          time.sleep(poll_interval)
      
      raise TimeoutError(f"File processing did not complete within {timeout} seconds")
  ```

- **Python 示例**（SSE 流式）：

  ```python
  import requests
  import json

  def wait_for_file_processing_stream(token, file_id):
      """
      Wait for file processing using Server-Sent Events stream.
      More efficient than polling for long-running operations.
      """
      url = f'http://localhost:3000/api/v1/files/{file_id}/process/status?stream=true'
      headers = {'Authorization': f'Bearer {token}'}
      
      with requests.get(url, headers=headers, stream=True) as response:
          for line in response.iter_lines():
              if line:
                  line = line.decode('utf-8')
                  if line.startswith('data: '):
                      data = json.loads(line[6:])
                      status = data.get('status')
                      
                      if status == 'completed':
                          return data
                      elif status == 'failed':
                          raise Exception(f"File processing failed: {data.get('error')}")
      
      raise Exception("Stream ended unexpectedly")
  ```

#### 将文件添加到知识库集合

上传完成后，你可以将文件分组到知识库集合中，或在聊天中单独引用。

:::important
**将文件添加到知识库之前，必须等待文件处理完成。** 仍在处理中的文件内容为空，会导致 `400` 错误。使用上方的状态接口验证文件状态为 `completed`。
:::

- **接口**：`POST /api/v1/knowledge/{id}/file/add`
- **Curl 示例**：

  ```bash
  curl -X POST http://localhost:3000/api/v1/knowledge/{knowledge_id}/file/add \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "your-file-id-here"}'
  ```

- **Python 示例**:

  ```python
  import requests

  def add_file_to_knowledge(token, knowledge_id, file_id):
      url = f'http://localhost:3000/api/v1/knowledge/{knowledge_id}/file/add'
      headers = {
          'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json'
      }
      data = {'file_id': file_id}
      response = requests.post(url, headers=headers, json=data)
      return response.json()
  ```


#### 将网页 URL 处理入知识库集合

使用此接口获取网页、提取内容，并将生成的块存入知识库集合中。

- **接口**：`POST /api/v1/retrieval/process/web`
- **查询参数**：
  - `process`（布尔型，默认：`true`）：如果为 `false`，仅获取并返回提取的内容而不保存向量
  - `overwrite`（布尔型，默认：`true`）：是否在保存新块之前替换目标集合中现有的向量，即清空给定集合并用给定 URL 的内容替换它
- **请求体**：
  - `url`（字符串，必需）：要获取和解析的网页 URL
  - `collection_name`（字符串，可选）：目标集合名称。如果省略， Open WebUI 会根据 URL 自动生成

**`overwrite` 行为：**
| 値 | 结果 |
|-------|--------|
| `true`（默认） | 插入新 URL 块之前，目标集合中现有的向量被替换 |
| `false` | 保留现有向量，新 URL 块被添加到同一集合中 |

- **Curl 示例**（保留现有向量）：

  ```bash
  curl -X POST 'http://localhost:3000/api/v1/retrieval/process/web?process=true&overwrite=false' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
        "url": "https://example.com/docs",
        "collection_name": "testkb"
      }'
  ```

- **Python 示例**：

  ```python
  import requests

  def process_web_url(token, url, collection_name="testkb", overwrite=False):
      response = requests.post(
          'http://localhost:3000/api/v1/retrieval/process/web',
          headers={
              'Authorization': f'Bearer {token}',
              'Content-Type': 'application/json'
          },
          params={
              'process': 'true',
              'overwrite': str(overwrite).lower()
          },
          json={
              'url': url,
              'collection_name': collection_name
          }
      )
      return response.json()
  ```

:::tip
如果启用了 `ENV=dev`，此接口的 schema（包括 `overwrite` 等查询参数）也可在 Swagger 的 `/docs` 中查看。
:::

#### 完整工作流程示例

以下是一个完整示例，展示如何上传文件、等待处理并将其添加到知识库：

```python
import requests
import time

WEBUI_URL = 'http://localhost:3000'
TOKEN = 'your-api-key-here'

def upload_and_add_to_knowledge(file_path, knowledge_id, timeout=300):
    """
    上传文件并将其添加到知识库。
    在添加之前正确等待处理完成。
    """
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/json'
    }
    
    # 第一步：上传文件
    with open(file_path, 'rb') as f:
        response = requests.post(
            f'{WEBUI_URL}/api/v1/files/',
            headers=headers,
            files={'file': f}
        )
    
    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.text}")
    
    file_data = response.json()
    file_id = file_data['id']
    print(f"File uploaded with ID: {file_id}")
    
    # 第二步：等待处理完成
    print("正在等待文件处理...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status_response = requests.get(
            f'{WEBUI_URL}/api/v1/files/{file_id}/process/status',
            headers=headers
        )
        status_data = status_response.json()
        status = status_data.get('status')
        
        if status == 'completed':
            print("文件处理完成！")
            break
        elif status == 'failed':
            raise Exception(f"Processing failed: {status_data.get('error')}")
        
        time.sleep(2)  # Poll every 2 seconds
    else:
        raise TimeoutError("文件处理超时")
    
    # 第三步：添加到知识库
    add_response = requests.post(
        f'{WEBUI_URL}/api/v1/knowledge/{knowledge_id}/file/add',
        headers={**headers, 'Content-Type': 'application/json'},
        json={'file_id': file_id}
    )
    
    if add_response.status_code != 200:
        raise Exception(f"Failed to add to knowledge: {add_response.text}")
    
    print(f"文件成功添加到知识库！")
    return add_response.json()

# 使用方式
result = upload_and_add_to_knowledge('/path/to/document.pdf', 'your-knowledge-id')
```

#### 在聊天补全中使用文件和集合

你可以在 RAG 查询中引用单个文件或整个集合，以丰富响应内容。

##### 在聊天补全中使用单个文件

当你希望肊天模型的响应聚焦在特定文件的内容上时，此方法非常适用。

- **接口**：`POST /api/chat/completions`
- **Curl 示例**：

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4-turbo",
        "messages": [
          {"role": "user", "content": "Explain the concepts in this document."}
        ],
        "files": [
          {"type": "file", "id": "your-file-id-here"}
        ]
      }'
  ```

- **Python 示例**：

  ```python
  import requests

  def chat_with_file(token, model, query, file_id):
      url = 'http://localhost:3000/api/chat/completions'
      headers = {
          'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json'
      }
      payload = {
          'model': model,
          'messages': [{'role': 'user', 'content': query}],
          'files': [{'type': 'file', 'id': file_id}]
      }
      response = requests.post(url, headers=headers, json=payload)
      return response.json()
  ```

##### 在聊天补全中使用知识库集合

当查询可能需要更广泛的上下文或多个文档时，利用知识库集合来增强响应。

- **接口**：`POST /api/chat/completions`
- **Curl 示例**：

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "gpt-4-turbo",
        "messages": [
          {"role": "user", "content": "Provide insights on the historical perspectives covered in the collection."}
        ],
        "files": [
          {"type": "collection", "id": "your-collection-id-here"}
        ]
      }'
  ```

- **Python 示例**:

  ```python
  import requests

  def chat_with_collection(token, model, query, collection_id):
      url = 'http://localhost:3000/api/chat/completions'
      headers = {
          'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json'
      }
      payload = {
          'model': model,
          'messages': [{'role': 'user', 'content': query}],
          'files': [{'type': 'collection', 'id': collection_id}]
      }
      response = requests.post(url, headers=headers, json=payload)
      return response.json()
  ```

这些方法可以通过上传的文件和粿展的知识库集合有效利用外部知识，增强聊天应用的能力。无论是单独使用文件还是将其纳入集合，你都可以根据具体需要自定义集成方式。

## 将 Open WebUI 作为统一 LLM 提供商的优势

Open WebUI 提供了许多优势，使其成为开发者和企业的重要工具：

- **统一界面**：通过单一的集成平台，简化与不同 LLM 的交互。
- **实现简便**：配合全面的文档和社区支持，快速开始集成。

按照这些指南，你可以迅速集成并开始使用 Open WebUI API。如果遇到任何问题，请透过我们的 Discord 社区进行反馈，或查阅 FAQ。祝编程愉快！🌟
