#!/usr/bin/env python3
"""Batch translation script for Open WebUI docs"""
import os
import re

BASE = 'd:/Github/open-webui-docs/docs'

def translate_file(filepath, replacements):
    """Apply a list of (old, new) replacements to a file."""
    try:
        content = open(filepath, encoding='utf-8').read()
    except FileNotFoundError:
        print(f'SKIP (not found): {filepath}')
        return
    
    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new, 1)
            changed = True
        else:
            # Check if already translated (new is in content)
            pass
    
    if changed:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print(f'TRANSLATED: {filepath}')
    else:
        print(f'UNCHANGED: {filepath}')


# ============================================================
# pipelines/index.mdx
# ============================================================
translate_file(f'{BASE}/features/extensibility/pipelines/index.mdx', [
    ('sidebar_position: 1\ntitle: "Pipelines"', 'sidebar_position: 1\ntitle: "Pipelines"'),  # keep
    ('# Pipelines: UI-Agnostic OpenAI API Plugin Framework',
     '# Pipelines：与 UI 无关的 OpenAI API 插件框架'),
    (':::warning\n\n**DO NOT USE PIPELINES IF!**\n\nIf your goal is simply to add support for additional providers like Anthropic or basic filters, you likely don\u2019t need Pipelines . For those cases, Open WebUI Functions are a better fit\u2014it\u2019s built-in, much more convenient, and easier to configure. Pipelines, however, comes into play when you\u2019re dealing with computationally heavy tasks (e.g., running large models or complex logic) that you want to offload from your main Open WebUI instance for better performance and scalability.\n\n:::',
     ':::warning\n\n**以下情况请勿使用 Pipelines！**\n\n如果你的目标只是添加对 Anthropic 等其他提供商或基本过滤器的支持，你很可能不需要 Pipelines。对于这些场景，Open WebUI Functions 是更好的选择——它内置于系统中，更方便，也更容易配置。Pipelines 适用于你需要将计算密集型任务（例如运行大型模型或复杂逻辑）从主 Open WebUI 实例卸载，以获得更好性能和可扩展性的场景。\n\n:::'),
    ('Welcome to **Pipelines**, an [Open WebUI](https://github.com/open-webui) initiative. Pipelines bring modular, customizable workflows to any UI client supporting OpenAI API specs \u2013 and much more! Easily extend functionalities, integrate unique logic, and create dynamic workflows with just a few lines of code.',
     '欢迎使用 **Pipelines**，这是 [Open WebUI](https://github.com/open-webui) 的一项计划。Pipelines 为任何支持 OpenAI API 规范的 UI 客户端带来模块化、可定制的工作流——以及更多功能！只需几行代码，即可轻松扩展功能、集成独特逻辑并创建动态工作流。'),
    ('## \U0001f680 Why Choose Pipelines?',
     '## 🚀 为什么选择 Pipelines？'),
    ('- **Flexible Extensibility:** Easily add custom logic and integrate Python libraries, from AI agents to home automation APIs.',
     '- **灵活的可扩展性：** 轻松添加自定义逻辑并集成 Python 库，从 AI 代理到智能家居 API。'),
    ('- **Seamless Integration:** Compatible with any UI/client supporting OpenAI API specs. (Only pipe-type pipelines are supported; filter types require clients with Pipelines support.)',
     '- **无缝集成：** 与任何支持 OpenAI API 规范的 UI/客户端兼容。（仅支持 pipe 类型的 Pipeline；filter 类型需要具有 Pipelines 支持的客户端。）'),
    ('- **Custom Hooks:** Build and integrate custom pipelines.',
     '- **自定义钩子：** 构建并集成自定义 Pipeline。'),
    ('### Examples of What You Can Achieve:',
     '### 你可以实现的示例：'),
    ('- [**Function Calling Pipeline**](https://github.com/open-webui/pipelines/blob/main/examples/filters/function_calling_filter_pipeline.py): Easily handle function calls and enhance your applications with custom logic.',
     '- [**函数调用 Pipeline**](https://github.com/open-webui/pipelines/blob/main/examples/filters/function_calling_filter_pipeline.py)：轻松处理函数调用，用自定义逻辑增强你的应用程序。'),
    ('- [**Custom RAG Pipeline**](https://github.com/open-webui/pipelines/blob/main/examples/pipelines/rag/llamaindex_pipeline.py): Implement sophisticated Retrieval-Augmented Generation pipelines tailored to your needs.',
     '- [**自定义 RAG Pipeline**](https://github.com/open-webui/pipelines/blob/main/examples/pipelines/rag/llamaindex_pipeline.py)：实现根据你的需求定制的复杂检索增强生成 Pipeline。'),
    ('- [**Message Monitoring Using Langfuse**](https://github.com/open-webui/pipelines/blob/main/examples/filters/langfuse_filter_pipeline.py): Monitor and analyze message interactions in real-time using Langfuse.',
     '- [**使用 Langfuse 进行消息监控**](https://github.com/open-webui/pipelines/blob/main/examples/filters/langfuse_filter_pipeline.py)：使用 Langfuse 实时监控和分析消息交互。'),
    ('- [**Rate Limit Filter**](https://github.com/open-webui/pipelines/blob/main/examples/filters/rate_limit_filter_pipeline.py): Control the flow of requests to prevent exceeding rate limits.',
     '- [**速率限制过滤器**](https://github.com/open-webui/pipelines/blob/main/examples/filters/rate_limit_filter_pipeline.py)：控制请求流量，防止超出速率限制。'),
    ('- [**Real-Time Translation Filter with LibreTranslate**](https://github.com/open-webui/pipelines/blob/main/examples/filters/libretranslate_filter_pipeline.py): Seamlessly integrate real-time translations into your LLM interactions.',
     '- [**使用 LibreTranslate 的实时翻译过滤器**](https://github.com/open-webui/pipelines/blob/main/examples/filters/libretranslate_filter_pipeline.py)：将实时翻译无缝集成到你的 LLM 交互中。'),
    ('- [**Toxic Message Filter**](https://github.com/open-webui/pipelines/blob/main/examples/filters/detoxify_filter_pipeline.py): Implement filters to detect and handle toxic messages effectively.',
     '- [**有毒消息过滤器**](https://github.com/open-webui/pipelines/blob/main/examples/filters/detoxify_filter_pipeline.py)：实现过滤器以有效检测和处理有毒消息。'),
    ('- **And Much More!**: The sky is the limit for what you can accomplish with Pipelines and Python. [Check out our scaffolds](https://github.com/open-webui/pipelines/blob/main/examples/scaffolds) to get a head start on your projects and see how you can streamline your development process!',
     '- **以及更多！** 使用 Pipelines 和 Python 可以实现的功能没有上限。[查看我们的脚手架](https://github.com/open-webui/pipelines/blob/main/examples/scaffolds)，为你的项目抢先一步，了解如何简化开发流程！'),
    ('## \U0001f527 How It Works',
     '## 🔧 工作原理'),
    ('Integrating Pipelines with any OpenAI API-compatible UI client is simple. Launch your Pipelines instance and set the OpenAI URL on your client to the Pipelines URL. That\u2019s it! You\u2019re ready to leverage any Python library for your needs.',
     '将 Pipelines 与任何 OpenAI API 兼容的 UI 客户端集成非常简单。启动你的 Pipelines 实例，并将客户端的 OpenAI URL 设置为 Pipelines URL。就这样！你已准备好利用任何 Python 库满足你的需求。'),
    ('## \u26a1 Quick Start with Docker',
     '## ⚡ 使用 Docker 快速开始'),
    (':::danger \u26a0\ufe0f Security Warning\n\nPipelines are a plugin system with arbitrary code execution \u2014 **don\u2019t fetch random pipelines from sources you don\u2019t trust**. A malicious Pipeline could access your file system, exfiltrate data, mine cryptocurrency, or compromise your system. Always review Pipeline source code before installing. See the [Security Policy](/security) for more details.\n\n:::',
     ':::danger ⚠️ 安全警告\n\nPipelines 是一个具有任意代码执行能力的插件系统——**不要从你不信任的来源获取随机 Pipeline**。恶意 Pipeline 可能访问你的文件系统、泄露数据、挖取加密货币或危害你的系统。安装前请务必审查 Pipeline 源代码。详情参见[安全政策](/security)。\n\n:::'),
    ('For a streamlined setup using Docker:', '使用 Docker 进行简化设置：'),
    ('1. **Run the Pipelines container:**', '1. **运行 Pipelines 容器：**'),
    ('2. **Connect to Open WebUI:**', '2. **连接到 Open WebUI：**'),
    ('   - Navigate to the **Admin Panel > Settings > Connections** section in Open WebUI.',
     '   - 在 Open WebUI 中导航到**管理面板 > 设置 > 连接**部分。'),
    ('   - When you\u2019re on this page, you can press the `+` button to add another connection.',
     '   - 在此页面上，你可以按 `+` 按钮添加另一个连接。'),
    ('   - Set the API URL to `http://localhost:9099` and the API key to `0p3n-w3bu!`.',
     '   - 将 API URL 设置为 `http://localhost:9099`，API 密钥设置为 `0p3n-w3bu!`。'),
    ('   - Once you\u2019ve added your pipelines connection and verified it, you will see an icon appear within the API Base URL field for the added connection. When hovered over, the icon itself will be labeled `Pipelines`. Your pipelines should now be active.',
     '   - 添加并验证 Pipeline 连接后，你将看到一个图标出现在已添加连接的 API Base URL 字段中。悬停时，该图标将显示为 `Pipelines`。你的 Pipeline 现在应已激活。'),
    (':::info\n\nIf your Open WebUI is running in a Docker container, replace `localhost` with `host.docker.internal` in the API URL.\n\n:::',
     ':::info\n\n如果你的 Open WebUI 运行在 Docker 容器中，请将 API URL 中的 `localhost` 替换为 `host.docker.internal`。\n\n:::'),
    ('3. **Manage Configurations:**', '3. **管理配置：**'),
    ('   - In the admin panel, go to **Admin Panel > Settings > Pipelines** tab.',
     '   - 在管理面板中，转到**管理面板 > 设置 > Pipelines** 标签页。'),
    ('   - Select your desired pipeline and modify the valve values directly from the WebUI.',
     '   - 选择所需的 Pipeline，直接从 WebUI 修改 Valve 值。'),
    (':::tip\n\nIf you are unable to connect, it is most likely a Docker networking issue. We encourage you to troubleshoot on your own and share your methods and solutions in the discussions forum.\n\n:::',
     ':::tip\n\n如果无法连接，很可能是 Docker 网络问题。我们鼓励你自行排查，并在讨论论坛中分享你的方法和解决方案。\n\n:::'),
    ('If you need to install a custom pipeline with additional dependencies:',
     '如果你需要安装具有额外依赖项的自定义 Pipeline：'),
    ('- **Run the following command:**', '- **运行以下命令：**'),
    ('Alternatively, you can directly install pipelines from the admin settings by copying and pasting the pipeline URL, provided it doesn\u2019t have additional dependencies.',
     '或者，你可以通过复制粘贴 Pipeline URL 直接从管理设置安装 Pipeline，前提是它没有额外依赖项。'),
])

# ============================================================
# pipelines/valves.md
# ============================================================
translate_file(f'{BASE}/features/extensibility/pipelines/valves.md', [
    ('sidebar_position: 4\ntitle: "Valves"', 'sidebar_position: 4\ntitle: "Valves"'),  # keep
    ('## Valves\n\n`Valves` (see the dedicated [Valves & UserValves](/features/extensibility/plugin/development/valves) page) can also be set for `Pipeline`. In short, `Valves` are input variables that are set per pipeline.',
     '## Valves\n\n`Valves`（参见专用的 [Valves & UserValves](/features/extensibility/plugin/development/valves) 页面）也可以为 `Pipeline` 设置。简而言之，`Valves` 是每个 Pipeline 单独设置的输入变量。'),
    ('`Valves` are set as a subclass of the `Pipeline` class, and initialized as part of the `__init__` method of the `Pipeline` class.',
     '`Valves` 作为 `Pipeline` 类的子类设置，并在 `Pipeline` 类的 `__init__` 方法中初始化。'),
    ('When adding valves to your pipeline, include a way to ensure that valves can be reconfigured by admins in the web UI. There are a few options for this:',
     '向 Pipeline 添加 Valve 时，请包含一种确保管理员可以在 Web UI 中重新配置 Valve 的方法。有以下几个选项：'),
    ('- Use `os.getenv()` to set an environment variable to use for the pipeline, and a default value to use if the environment variable isn\u2019t set. An example can be seen below:',
     '- 使用 `os.getenv()` 为 Pipeline 设置要使用的环境变量，以及在未设置环境变量时使用的默认值。示例如下：'),
    ('- Set the valve to the `Optional` type, which will allow the pipeline to load even if no value is set for the valve.',
     '- 将 Valve 设置为 `Optional` 类型，即使未为 Valve 设置值，也允许 Pipeline 加载。'),
    ("If you don't leave a way for valves to be updated in the web UI, you'll see the following error in the Pipelines server log after trying to add a pipeline to the web UI:\n`WARNING:root:No Pipeline class found in <pipeline name>`",
     '如果你不提供在 Web UI 中更新 Valve 的方法，在尝试将 Pipeline 添加到 Web UI 后，你会在 Pipelines 服务器日志中看到以下错误：\n`WARNING:root:No Pipeline class found in <pipeline name>`'),
])

# ============================================================
# pipelines/pipes.md  (partial - frontmatter + intro section)
# ============================================================
translate_file(f'{BASE}/features/extensibility/pipelines/pipes.md', [
    ('sidebar_position: 3\ntitle: "Pipes"', 'sidebar_position: 3\ntitle: "Pipes"'),  # keep
    ('## Pipes\n\nPipes are standalone functions that process inputs and generate responses, possibly by invoking one or more LLMs or external services before returning results to the user. Examples of potential actions you can take with Pipes are Retrieval Augmented Generation (RAG), sending requests to non-OpenAI LLM providers (such as Anthropic, Azure OpenAI, or Google), or executing functions right in your web UI. Pipes can be hosted as a Function or on a Pipelines server. A list of examples is maintained in the [Pipelines repo](https://github.com/open-webui/pipelines/tree/main/examples/pipelines). The general workflow can be seen in the image below.',
     '## Pipes\n\nPipes 是处理输入并生成响应的独立函数，在向用户返回结果之前，可能会调用一个或多个 LLM 或外部服务。使用 Pipes 可以进行的操作示例包括：检索增强生成（RAG）、向非 OpenAI LLM 提供商（如 Anthropic、Azure OpenAI 或 Google）发送请求，或直接在 Web UI 中执行函数。Pipes 可以作为 Function 托管，也可以托管在 Pipelines 服务器上。示例列表维护在 [Pipelines 仓库](https://github.com/open-webui/pipelines/tree/main/examples/pipelines)中。一般工作流如下图所示。'),
    ('Pipes that are defined in your WebUI show up as a new model with an "External" designation attached to them. An example of two Pipe models, `Database RAG Pipeline` and `DOOM`, can be seen below next to two self-hosted models:',
     '在 WebUI 中定义的 Pipes 显示为带有"External"标识的新模型。以下是两个 Pipe 模型 `Database RAG Pipeline` 和 `DOOM` 与两个自托管模型并排的示例：'),
    ('## Streaming response format',
     '## 流式响应格式'),
    ('Pipes can return either a single `str` or an iterator/generator. When streaming, each yielded item can be:',
     'Pipes 可以返回单个 `str` 或迭代器/生成器。流式传输时，每个 yield 的项可以是：'),
    ('- **A plain string** \u2014 treated as assistant-visible text content and appended to the message as it arrives. This is the simplest form and the one most agent pipelines should use for regular output.',
     '- **纯字符串** — 被视为助手可见的文本内容，随到随追加到消息中。这是最简单的形式，也是大多数代理 Pipeline 应用于常规输出的形式。'),
    ('- **An OpenAI-compatible SSE chunk dict** \u2014 same shape as the `/v1/chat/completions` streaming response, i.e.',
     '- **OpenAI 兼容的 SSE chunk 字典** — 与 `/v1/chat/completions` 流式响应形状相同，即：'),
    ('  Use this when you need to set fields other than `content` (for example `finish_reason` on the final chunk).',
     '  当你需要设置 `content` 以外的字段时使用（例如最终 chunk 上的 `finish_reason`）。'),
    ('For a self-contained stream, close it with a single terminating chunk:',
     '对于自包含流，使用单个终止 chunk 关闭它：'),
    ('`finish_reason` should appear **exactly once**, at the end, and for a pipeline that handles its own tool execution it should always be `"stop"` \u2014 not `"tool_calls"` (see the next section).',
     '`finish_reason` 应**恰好出现一次**，在末尾，对于自行处理工具执行的 Pipeline，它应始终为 `"stop"` — 而不是 `"tool_calls"`（参见下一节）。'),
    ('## Self-contained agents and `delta.tool_calls`',
     '## 自包含代理与 `delta.tool_calls`'),
    ('This is the single biggest gotcha when building an agent pipeline (LangChain, LlamaIndex, a custom planner, anything that executes its own tools and streams the result back).',
     '这是构建代理 Pipeline（LangChain、LlamaIndex、自定义规划器，任何执行自己工具并流式返回结果的东西）时最大的陷阱。'),
    ('`delta.tool_calls` in a chunk means **"please execute this tool call for me, client"**. When Open WebUI\u2019s middleware sees it, the tool executor picks up the call, runs it, appends a `role: "tool"` message, and fires a continuation request back at the same pipeline. It does this in a loop capped by `CHAT_RESPONSE_MAX_TOOL_CALL_RETRIES` (\u224830).',
     'chunk 中的 `delta.tool_calls` 意味着**"请帮我执行这个工具调用，客户端"**。当 Open WebUI 的中间件看到它时，工具执行器会接收调用、运行它、追加 `role: "tool"` 消息，并向同一 Pipeline 发送继续请求。这在由 `CHAT_RESPONSE_MAX_TOOL_CALL_RETRIES`（≈30）限制的循环中进行。'),
    ('If your pipeline already executed the tool internally, emitting `delta.tool_calls` makes Open WebUI try to execute it *again* \u2014 and since the pipeline keeps emitting the same call on every retry, you get 30 copies of the response stacked on top of each other before the retry cap trips. Same thing happens if you set `finish_reason: "tool_calls"` mid-stream.',
     '如果你的 Pipeline 已在内部执行了工具，发出 `delta.tool_calls` 会让 Open WebUI 再次尝试执行它——由于 Pipeline 在每次重试时都会发出相同的调用，在达到重试上限之前你会得到 30 份响应叠加在一起。如果你在流中途设置 `finish_reason: "tool_calls"` 也会发生同样的情况。'),
    ('**Rule of thumb:**\n\n- The model is calling a tool Open WebUI should run \u2192 emit `delta.tool_calls`, terminate with `finish_reason: "tool_calls"`, let the middleware call the tool and re-enter your pipeline.\n- The pipeline is running an agent that owns its own tools \u2192 **do not** emit `delta.tool_calls` at all. Render the tool execution as content using the `<details type="tool_calls">` block described below.',
     '**经验法则：**\n\n- 模型正在调用 Open WebUI 应该运行的工具 → 发出 `delta.tool_calls`，以 `finish_reason: "tool_calls"` 终止，让中间件调用工具并重新进入你的 Pipeline。\n- Pipeline 正在运行一个拥有自己工具的代理 → **不要**发出 `delta.tool_calls`。使用下面描述的 `<details type="tool_calls">` 块将工具执行渲染为内容。'),
    ('### Rendering tool execution as content',
     '### 将工具执行渲染为内容'),
    ("Open WebUI\u2019s own server-side tool path renders finished tool executions as `<details type=\"tool_calls\">` blocks in the message content. You can emit the same block from an agent pipeline to get the identical \"Called &lt;tool&gt;\" chip with an expandable arguments + result view:",
     'Open WebUI 自身的服务器端工具路径将已完成的工具执行渲染为消息内容中的 `<details type="tool_calls">` 块。你可以从代理 Pipeline 发出相同的块，以获得相同的"Called &lt;tool&gt;"芯片以及可展开的参数 + 结果视图：'),
    ('Yield `details_block` as content \u2014 either directly as a string (simplest on a Pipelines server) or inside a `delta.content` chunk:',
     '将 `details_block` 作为内容 yield——可以直接作为字符串（在 Pipelines 服务器上最简单），也可以放在 `delta.content` chunk 中：'),
    ('The final stream for a self-contained agent that ran one tool looks like this end-to-end:',
     '运行了一个工具的自包含代理的最终流从头到尾如下所示：'),
])

# ============================================================
# pipelines/filters.md
# ============================================================
translate_file(f'{BASE}/features/extensibility/pipelines/filters.md', [
    ('sidebar_position: 2\ntitle: "Filters"', 'sidebar_position: 2\ntitle: "Filters"'),  # keep
    ('## Filters\n\nFilters are used to perform actions against incoming user messages and outgoing assistant (LLM) messages. Potential actions that can be taken in a filter include sending messages to monitoring platforms (such as Langfuse or DataDog), modifying message contents, blocking toxic messages, translating messages to another language, or rate limiting messages from certain users. A list of examples is maintained in the [Pipelines repo](https://github.com/open-webui/pipelines/tree/main/examples/filters). Filters can be executed as a Function or on a Pipelines server. The general workflow can be seen in the image below.',
     '## Filters\n\nFilters 用于对传入的用户消息和传出的助手（LLM）消息执行操作。过滤器中可以执行的操作包括：将消息发送到监控平台（如 Langfuse 或 DataDog）、修改消息内容、屏蔽有毒消息、将消息翻译成另一种语言，或对特定用户的消息进行速率限制。示例列表维护在 [Pipelines 仓库](https://github.com/open-webui/pipelines/tree/main/examples/filters)中。Filters 可以作为 Function 执行，也可以在 Pipelines 服务器上执行。一般工作流如下图所示。'),
    ('When a filter pipeline is enabled on a model or pipe, the incoming message from the user (or "inlet") is passed to the filter for processing. The filter performs the desired action against the message before requesting the chat completion from the LLM model. Finally, the filter performs post-processing on the outgoing LLM message (or "outlet") before it is sent to the user.',
     '在模型或 Pipe 上启用过滤器 Pipeline 后，来自用户的传入消息（即"inlet"）会传递给过滤器进行处理。过滤器在向 LLM 模型请求对话完成之前对消息执行所需的操作。最后，过滤器在将传出的 LLM 消息（即"outlet"）发送给用户之前对其进行后处理。'),
])

# ============================================================
# pipelines/tutorials.md
# ============================================================
translate_file(f'{BASE}/features/extensibility/pipelines/tutorials.md', [
    ('sidebar_position: 5\ntitle: "Tutorials"', 'sidebar_position: 5\ntitle: "Tutorials"'),  # keep
    ('## Pipeline Tutorials\n\n## Tutorials Welcome\n\nAre you a content creator with a blog post or YouTube video about your pipeline setup? Get in touch\nwith us, as we\u2019d love to feature it here!',
     '## Pipeline 教程\n\n## 欢迎投稿教程\n\n你是有关于 Pipeline 设置的博客文章或 YouTube 视频的内容创作者吗？请与我们联系，我们很乐意在这里展示！'),
    ('## Featured Tutorials', '## 精选教程'),
    ('[Monitoring Open WebUI with Filters](https://medium.com/@0xthresh/monitor-open-webui-with-datadog-llm-observability-620ef3a598c6) (Medium article by @0xthresh)\n\n- A detailed guide to monitoring the Open WebUI using DataDog LLM observability.',
     '[使用 Filters 监控 Open WebUI](https://medium.com/@0xthresh/monitor-open-webui-with-datadog-llm-observability-620ef3a598c6)（@0xthresh 的 Medium 文章）\n\n- 使用 DataDog LLM 可观测性监控 Open WebUI 的详细指南。'),
    ('[Building Customized Text-To-SQL Pipelines](https://www.youtube.com/watch?v=y7frgUWrcT4) (YouTube video by Jordan Nanos)\n\n- Learn how to develop tailored text-to-sql pipelines, unlocking the power of data analysis and extraction.',
     '[构建自定义文本转 SQL Pipeline](https://www.youtube.com/watch?v=y7frgUWrcT4)（Jordan Nanos 的 YouTube 视频）\n\n- 了解如何开发定制的文本转 SQL Pipeline，释放数据分析和提取的力量。'),
    ('[Demo and Code Review for Text-To-SQL with Open-WebUI](https://www.youtube.com/watch?v=iLVyEgxGbg4) (YouTube video by Jordan Nanos)\n\n- A hands-on demonstration and code review on utilizing text-to-sql tools powered by the Open WebUI.',
     '[Open-WebUI 文本转 SQL 演示和代码审查](https://www.youtube.com/watch?v=iLVyEgxGbg4)（Jordan Nanos 的 YouTube 视频）\n\n- 关于利用 Open WebUI 支持的文本转 SQL 工具的实操演示和代码审查。'),
    ('[Deploying custom Document RAG pipeline with Open-WebUI](https://github.com/Sebulba46/document-RAG-pipeline) (GitHub guide by Sebulba46)\n\n- Step by step guide to deploy Open-WebUI and pipelines containers and creating your own document RAG with local LLM API.',
     '[使用 Open-WebUI 部署自定义文档 RAG Pipeline](https://github.com/Sebulba46/document-RAG-pipeline)（Sebulba46 的 GitHub 指南）\n\n- 逐步指南，部署 Open-WebUI 和 Pipeline 容器，并使用本地 LLM API 创建自己的文档 RAG。'),
])

print('\nAll done!')
