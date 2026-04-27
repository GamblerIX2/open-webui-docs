#!/usr/bin/env python3
"""Translate plugin-related docs"""
import os
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1] / "docs"

def r(filepath, old, new):
    content = open(filepath, encoding='utf-8').read()
    if old in content:
        content = content.replace(old, new, 1)
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        return True
    return False

def translate(filepath, pairs):
    content = open(filepath, encoding='utf-8').read()
    changed = False
    not_found = []
    for old, new in pairs:
        if old in content:
            content = content.replace(old, new, 1)
            changed = True
        else:
            not_found.append(old[:60])
    if changed:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print(f'TRANSLATED: {os.path.basename(filepath)}')
    else:
        print(f'UNCHANGED: {os.path.basename(filepath)}')
    for s in not_found:
        print(f'  NOT FOUND: {s}')

# ============================================================
# plugin/migration/index.mdx
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/migration/index.mdx', [
    ('title: "Migration Guides"', 'title: "迁移指南"'),
    ('# \U0001f69a Plugin Migration Guides\n\nOpen WebUI occasionally ships releases that require updates to existing Tools, Functions, Pipes, Filters, and Actions. This section collects the per-version migration guides for plugin authors.\n\nPick the guide that matches the version you are upgrading **from**. If you are crossing multiple major versions, work through the guides in order.',
     '# 🚚 插件迁移指南\n\nOpen WebUI 偶尔会发布需要更新现有 Tools、Functions、Pipes、Filters 和 Actions 的版本。本节为插件作者收集了各版本的迁移指南。\n\n选择与你**从**中升级的版本匹配的指南。如果你跨越多个主要版本，请按顺序阅读各指南。'),
    ('## Available Guides', '## 可用指南'),
    ('- **[Migrating to 0.5.0](/features/extensibility/plugin/migration/to-0.5.0)** \u2014 the `apps` \u2192 `routers` restructure, unified `chat_completion` endpoint, and the new `__request__` parameter in function signatures.',
     '- **[迁移到 0.5.0](/features/extensibility/plugin/migration/to-0.5.0)** — `apps` → `routers` 重构、统一的 `chat_completion` 端点以及函数签名中新增的 `__request__` 参数。'),
    ('- **[Migrating to 0.9.0](/features/extensibility/plugin/migration/to-0.9.0)** \u2014 the backend-wide sync \u2192 async refactor. Database model methods and most `open_webui.*` helpers now return coroutines and must be awaited.',
     '- **[迁移到 0.9.0](/features/extensibility/plugin/migration/to-0.9.0)** — 后端全面从同步改为异步。数据库模型方法和大多数 `open_webui.*` 辅助函数现在返回协程，必须使用 `await`。'),
    ('\U0001f4ac **Questions or Feedback?**\nIf you run into issues upgrading a plugin, open a [GitHub issue](https://github.com/open-webui/open-webui) or ask in the community forums.',
     '💬 **问题或反馈？**\n如果在升级插件时遇到问题，请提交 [GitHub issue](https://github.com/open-webui/open-webui) 或在社区论坛中提问。'),
])

# ============================================================
# plugin/migration/to-0.5.0.mdx
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/migration/to-0.5.0.mdx', [
    ('title: "Migrating to 0.5.0"', 'title: "迁移到 0.5.0"'),
    ('# \U0001f69a Migration Guide: Open WebUI 0.4 to 0.5\n\nWelcome to the Open WebUI 0.5 migration guide! If you\'re working on existing projects or building new ones, this guide will walk you through the key changes from **version 0.4 to 0.5** and provide an easy-to-follow roadmap for upgrading your Functions. Let\'s make this transition as smooth as possible! \U0001f60a',
     '# 🚚 迁移指南：Open WebUI 0.4 升级到 0.5\n\n欢迎使用 Open WebUI 0.5 迁移指南！无论你是在处理现有项目还是构建新项目，本指南都将引导你了解**从 0.4 到 0.5 版本**的关键变更，并提供升级 Functions 的易于遵循的路线图。让这次过渡尽可能顺畅！😊'),
    ('## \U0001f9d0 What Has Changed and Why?', '## 🧐 发生了什么变化，为什么？'),
    ('With Open WebUI 0.5, we\'ve overhauled the architecture to make the project **simpler, more unified, and scalable**. Here\'s the big picture:',
     '在 Open WebUI 0.5 中，我们对架构进行了全面改造，使项目**更简单、更统一、更具可扩展性**。以下是整体概况：'),
    ('- **Old Architecture:** \U0001f3af Previously, Open WebUI was built on a **sub-app architecture** where each app (e.g., `ollama`, `openai`) was a separate FastAPI application. This caused fragmentation and extra complexity when managing apps.',
     '- **旧架构：** 🎯 以前，Open WebUI 建立在**子应用架构**上，每个应用（如 `ollama`、`openai`）都是独立的 FastAPI 应用。这在管理应用时造成了碎片化和额外复杂性。'),
    ('- **New Architecture:** \U0001f680 With version 0.5, we have transitioned to a **single FastAPI app** with multiple **routers**. This means better organization, centralized flow, and reduced redundancy.',
     '- **新架构：** 🚀 在 0.5 版本中，我们过渡到了具有多个**路由器**的**单个 FastAPI 应用**。这意味着更好的组织结构、集中的流程和减少冗余。'),
    ('### Key Changes:', '### 关键变更：'),
    ("Here's an overview of what changed:", '以下是变更概述：'),
    ('1. **Apps have been moved to Routers.**\n   - Previous: `open_webui.apps`\n   - Now: `open_webui.routers`',
     '1. **应用已迁移到路由器。**\n   - 之前：`open_webui.apps`\n   - 现在：`open_webui.routers`'),
    ('2. **Main app structure simplified.**\n   - The old `open_webui.apps.webui` has been transformed into `open_webui.main`, making it the central entry point for the project.',
     '2. **主应用结构简化。**\n   - 旧的 `open_webui.apps.webui` 已转换为 `open_webui.main`，使其成为项目的中央入口点。'),
    ('3. **Unified API Endpoint**\n   - Open WebUI 0.5 introduces a **unified function**, `chat_completion`, in `open_webui.main`, replacing separate functions for models like `ollama` and `openai`. This offers a consistent and streamlined API experience. However, the **direct successor** of these individual functions is `generate_chat_completion` from `open_webui.utils.chat`. If you prefer a lightweight POST request without handling additional parsing (e.g., files, tools, or misc), this utility function is likely what you want.',
     '3. **统一 API 端点**\n   - Open WebUI 0.5 在 `open_webui.main` 中引入了一个**统一函数** `chat_completion`，取代了 `ollama` 和 `openai` 等模型的独立函数。这提供了一致且简化的 API 体验。但是，这些独立函数的**直接继任者**是 `open_webui.utils.chat` 中的 `generate_chat_completion`。如果你希望进行轻量级 POST 请求而无需处理额外解析（如文件、工具或杂项），这个工具函数可能正是你所需要的。'),
    ('4. **Updated Function Signatures.**\n   - Function signatures now adhere to a new format, requiring a `request` object.\n   - The `request` object can be obtained using the `__request__` parameter in the function signature. Below is an example:',
     '4. **更新函数签名。**\n   - 函数签名现在遵循新格式，需要一个 `request` 对象。\n   - `request` 对象可以通过函数签名中的 `__request__` 参数获取。以下是示例：'),
    ('\U0001f4cc **Why did we make these changes?**\n- To simplify the codebase, making it easier to extend and maintain.\n- To unify APIs for a more streamlined developer experience.\n- To enhance performance by consolidating redundant elements.',
     '📌 **为什么进行这些变更？**\n- 为了简化代码库，使其更易于扩展和维护。\n- 为了统一 API，提供更简化的开发者体验。\n- 为了通过整合冗余元素来增强性能。'),
    ('## \u2705 Step-by-Step Migration Guide\n\nFollow this guide to smoothly update your project.',
     '## ✅ 逐步迁移指南\n\n按照本指南顺利更新你的项目。'),
    ('### \U0001f504 1. Shifting from `apps` to `routers`\n\nAll apps have been renamed and relocated under `open_webui.routers`. This affects imports in your codebase.\n\nQuick changes for import paths:',
     '### 🔄 1. 从 `apps` 迁移到 `routers`\n\n所有应用已重命名并迁移到 `open_webui.routers` 下。这会影响代码库中的导入语句。\n\n导入路径的快速变更：'),
])

# ============================================================
# plugin/migration/to-0.9.0.mdx
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/migration/to-0.9.0.mdx', [
    ('title: "Migrating to 0.9.0"', 'title: "迁移到 0.9.0"'),
    ('# \U0001f69a Migration Guide: Upgrading to Open WebUI 0.9.0\n\nThis guide covers breaking changes and required updates for Tools, Functions, Pipes, Filters, and Actions when upgrading to **Open WebUI 0.9.0**.',
     '# 🚚 迁移指南：升级到 Open WebUI 0.9.0\n\n本指南涵盖升级到 **Open WebUI 0.9.0** 时 Tools、Functions、Pipes、Filters 和 Actions 的破坏性变更和必要更新。'),
    ('## \U0001f9d0 What Has Changed and Why?', '## 🧐 发生了什么变化，为什么？'),
    ('Open WebUI 0.9.0 ships a large internal refactor: the backend data layer has moved from **synchronous** to **asynchronous** from top to bottom. Almost every database-backed method on every model class (Users, Chats, Files, Models, Functions, Tools, Knowledge, Memories, Groups, Folders, Messages, Feedback, \u2026) is now an `async def` and must be awaited.',
     'Open WebUI 0.9.0 进行了大规模内部重构：后端数据层从上到下从**同步**改为**异步**。每个模型类（Users、Chats、Files、Models、Functions、Tools、Knowledge、Memories、Groups、Folders、Messages、Feedback……）上的几乎每个数据库支持方法现在都是 `async def`，必须使用 `await`。'),
    ('At the storage layer, SQLAlchemy is now used in its async mode: sessions are `AsyncSession` instances, and queries are issued via `await db.execute(select(...))` instead of the legacy `db.query(...).first()` style. A sync engine still exists internally, but it is reserved for startup-only tasks (config loading, Alembic/peewee migrations, health checks) \u2014 **all runtime code, including plugins, must use the async engine**.',
     '在存储层，SQLAlchemy 现在以异步模式使用：会话是 `AsyncSession` 实例，查询通过 `await db.execute(select(...))` 发出，而不是旧式的 `db.query(...).first()`。同步引擎仍在内部存在，但仅用于启动任务（配置加载、Alembic/peewee 迁移、健康检查）——**所有运行时代码（包括插件）必须使用异步引擎**。'),
    ('\U0001f4cc **Why did we make this change?**\n- **Concurrency**: blocking DB calls on the event loop were the biggest bottleneck under load. Making the data layer async lets FastAPI handle many more concurrent chats without thread-pool saturation.\n- **Consistency**: request handlers were already async; the data layer being sync forced awkward `run_in_threadpool` wrappers throughout the codebase.\n- **Forward-looking**: SQLAlchemy 2.0\'s async API is the supported path going forward.',
     '📌 **为什么进行这次变更？**\n- **并发性**：事件循环上的阻塞 DB 调用是负载下最大的瓶颈。将数据层改为异步使 FastAPI 能够处理更多并发对话，而不会耗尽线程池。\n- **一致性**：请求处理器已经是异步的；数据层是同步的迫使整个代码库使用笨拙的 `run_in_threadpool` 包装器。\n- **面向未来**：SQLAlchemy 2.0 的异步 API 是未来的受支持路径。'),
    ('## \u26a0\ufe0f Breaking Changes', '## ⚠️ 破坏性变更'),
    ('If your plugin touches the Open WebUI database or models \u2014 **or calls any helper that eventually touches them** \u2014 you will need to update it. Because almost every utility in `open_webui.utils.*` and every router function ultimately reads or writes through a model, "async reach" extends well beyond obvious `Users.`/`Chats.` calls. Specifically:',
     '如果你的插件访问 Open WebUI 数据库或模型——**或调用最终访问它们的任何辅助函数**——你需要更新它。由于 `open_webui.utils.*` 中的几乎每个工具以及每个路由器函数最终都通过模型进行读写，"异步影响范围"远超明显的 `Users.`/`Chats.` 调用。具体来说：'),
    ('Plugin entrypoints themselves (the `pipe`, `inlet`, `outlet`, `stream`, `action`, and Tool methods) were already asynchronous in 0.5 and later, so the signatures you declare do not change \u2014 only the bodies do.',
     '插件入口点本身（`pipe`、`inlet`、`outlet`、`stream`、`action` 和 Tool 方法）在 0.5 及更高版本中已经是异步的，因此你声明的签名不会改变——只有函数体需要更新。'),
    ('## \u2705 Step-by-Step Migration', '## ✅ 逐步迁移'),
    ('### \U0001f504 1. Await every model method', '### 🔄 1. 对每个模型方法使用 await'),
    ('The most common change. Anywhere your plugin reads or writes through a model class, add `await`.',
     '最常见的变更。在你的插件通过模型类进行读写的任何地方，添加 `await`。'),
    ('#### Before (0.8.x):', '#### 之前（0.8.x）：'),
    ('#### After (0.9.0):', '#### 之后（0.9.0）：'),
    ('Note that the helper itself became `async def`. Its callers must now `await` it in turn \u2014 async propagates upward through your code.',
     '注意辅助函数本身变成了 `async def`。其调用者现在也必须依次使用 `await`——异步向上传播到你的代码中。'),
    ('### \U0001f5c4\ufe0f 2. Replace `get_db_context` with `get_async_db_context`',
     '### 🗄️ 2. 将 `get_db_context` 替换为 `get_async_db_context`'),
])

# ============================================================
# plugin/development/reserved-args.mdx
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/development/reserved-args.mdx', [
    ('title: "Reserved Arguments"', 'title: "保留参数"'),
    (':::warning\n\nThis tutorial is a community contribution and is not supported by the Open WebUI team. It serves only as a demonstration on how to customize Open WebUI for your specific use case. Want to contribute? Check out the contributing tutorial.\n\n:::',
     ':::warning\n\n本教程是社区贡献，不受 Open WebUI 团队官方支持。它仅作为如何为特定使用场景自定义 Open WebUI 的演示。想要贡献？请查看贡献教程。\n\n:::'),
    ('# \U0001fa84 Special Arguments\n\nWhen developping your own `Tools`, `Functions` (`Filters`, `Pipes` or `Actions`), `Pipelines` etc, you can use special arguments explore the full spectrum of what Open-WebUI has to offer.\n\nThis page aims to detail the type and structure of each special argument as well as provide an example.',
     '# 🪄 特殊参数\n\n在开发自己的 `Tools`、`Functions`（`Filters`、`Pipes` 或 `Actions`）、`Pipelines` 等时，你可以使用特殊参数探索 Open WebUI 提供的全部功能。\n\n本页面旨在详细说明每个特殊参数的类型和结构，并提供示例。'),
    ('### `body`\n\nA `dict` usually destined to go almost directly to the model. Although it is not strictly a special argument, it is included here for easier reference and because it contains itself some special arguments.',
     '### `body`\n\n一个 `dict`，通常几乎直接发送给模型。虽然它严格来说不是特殊参数，但为了便于参考而包含在此，因为它本身包含一些特殊参数。'),
    ('### `__user__`\n\nA `dict` with user information.\n\nNote that if the `UserValves` class is defined, its instance has to be accessed via `__user__["valves"]`. Otherwise, the `valves` keyvalue is missing entirely from `__user__`.',
     '### `__user__`\n\n包含用户信息的 `dict`。\n\n注意，如果定义了 `UserValves` 类，其实例必须通过 `__user__["valves"]` 访问。否则，`valves` 键值将完全从 `__user__` 中缺失。'),
])

# ============================================================
# plugin/development/events.mdx  (first section)
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/development/events.mdx', [
    ('title: "Events"', 'title: "事件"'),
    ('# \U0001f514 Events: Using `__event_emitter__` and `__event_call__` in Open WebUI\n\nOpen WebUI\'s plugin architecture is not just about processing input and producing output\u2014**it\'s about real-time, interactive communication with the UI and users**. To make your Tools, Functions, and Pipes more dynamic, Open WebUI provides a built-in event system via the `__event_emitter__` and `__event_call__` helpers.\n\nThis guide explains **what events are**, **how you can trigger them** from your code, and **the full catalog of event types** you can use (including much more than just `"input"`).',
     '# 🔔 事件：在 Open WebUI 中使用 `__event_emitter__` 和 `__event_call__`\n\nOpen WebUI 的插件架构不仅仅是处理输入和产生输出——**它还涉及与 UI 和用户的实时交互式通信**。为了使你的 Tools、Functions 和 Pipes 更具动态性，Open WebUI 通过 `__event_emitter__` 和 `__event_call__` 辅助函数提供了内置事件系统。\n\n本指南解释了**什么是事件**、**如何从代码中触发事件**以及**可以使用的完整事件类型目录**（包括远不止 `"input"` 的更多内容）。'),
    ('## \U0001f30a What Are Events?', '## 🌊 什么是事件？'),
    ('**Events** are real-time notifications or interactive requests sent from your backend code (Tool, or Function) to the web UI. They allow you to update the chat, display notifications, request confirmation, run UI flows, and more.\n\n- Events are sent using the `__event_emitter__` helper for one-way updates, or `__event_call__` when you need user input or a response (e.g., confirmation, input, etc.).\n\n**Metaphor:**\nThink of Events like push notifications and modal dialogs that your plugin can trigger, making the chat experience richer and more interactive.',
     '**事件**是从你的后端代码（Tool 或 Function）发送到 Web UI 的实时通知或交互式请求。它们允许你更新对话、显示通知、请求确认、运行 UI 流程等。\n\n- 事件使用 `__event_emitter__` 辅助函数发送单向更新，或在需要用户输入或响应时（如确认、输入等）使用 `__event_call__`。\n\n**比喻：**\n将事件想象成插件可以触发的推送通知和模态对话框，使对话体验更丰富、更具交互性。'),
    ('## \U0001f3c1 Availability', '## 🏁 可用性'),
    ('### Native Python Tools & Functions\n\nEvents are **fully available** for native Python Tools and Functions defined directly in Open WebUI using the `__event_emitter__` and `__event_call__` helpers.',
     '### 原生 Python Tools & Functions\n\n对于直接在 Open WebUI 中使用 `__event_emitter__` 和 `__event_call__` 辅助函数定义的原生 Python Tools 和 Functions，事件**完全可用**。'),
    ('### External Tools (OpenAPI & MCP)\n\nExternal tools can emit events via a **dedicated REST endpoint**. Open WebUI passes the following headers to all external tool requests when `ENABLE_FORWARD_USER_INFO_HEADERS=True` is set:',
     '### 外部工具（OpenAPI & MCP）\n\n外部工具可以通过**专用 REST 端点**发出事件。当设置 `ENABLE_FORWARD_USER_INFO_HEADERS=True` 时，Open WebUI 将以下标头传递给所有外部工具请求：'),
    ('Your external tool can use these headers to emit events back to the UI via:',
     '你的外部工具可以使用这些标头通过以下方式将事件发送回 UI：'),
    ('See [External Tool Events](#-external-tool-events) below for details.',
     '详情参见下方的[外部工具事件](#-外部工具事件)。'),
    ('## \U0001f9f0 Basic Usage', '## 🧰 基本用法'),
    ('### Sending an Event\n\nYou can trigger an event anywhere inside your Tool, or Function by calling:',
     '### 发送事件\n\n你可以通过调用以下代码在 Tool 或 Function 的任何位置触发事件：'),
    ('You **do not** need to manually add fields like `chat_id` or `message_id`\u2014these are handled automatically by Open WebUI.',
     '你**不需要**手动添加 `chat_id` 或 `message_id` 等字段——这些由 Open WebUI 自动处理。'),
    ('### Interactive Events\n\nWhen you need to pause execution until the user responds (e.g., confirm/cancel dialogs, code execution, or input), use `__event_call__`:',
     '### 交互式事件\n\n当你需要暂停执行直到用户响应时（如确认/取消对话框、代码执行或输入），使用 `__event_call__`：'),
])

# ============================================================
# plugin/development/rich-ui.mdx  (first section)
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/development/rich-ui.mdx', [
    ('title: "Rich UI Embedding"', 'title: "富 UI 嵌入"'),
    ('# Rich UI Element Embedding\n\nTools and Actions both support rich UI element embedding, allowing them to return HTML content and interactive iframes that display directly within chat conversations. This feature enables sophisticated visual interfaces, interactive widgets, charts, dashboards, and other rich web content \u2014 regardless of whether the function was triggered by the model (Tool) or by the user (Action).\n\nWhen a function returns an `HTMLResponse` with the appropriate headers, the content will be embedded as an interactive iframe in the chat interface rather than displayed as plain text.',
     '# 富 UI 元素嵌入\n\nTools 和 Actions 都支持富 UI 元素嵌入，允许它们返回直接显示在对话中的 HTML 内容和交互式 iframe。此功能支持复杂的视觉界面、交互式小部件、图表、仪表板和其他富 Web 内容——无论函数是由模型（Tool）还是用户（Action）触发的。\n\n当函数返回带有适当标头的 `HTMLResponse` 时，内容将作为交互式 iframe 嵌入到对话界面中，而不是显示为纯文本。'),
    ('## Tool Usage\n\nTo embed HTML content, your tool should return an `HTMLResponse` with the `Content-Disposition: inline` header:',
     '## Tool 用法\n\n要嵌入 HTML 内容，你的工具应返回带有 `Content-Disposition: inline` 标头的 `HTMLResponse`：'),
    ('### Custom Result Context\n\nBy default, when a tool returns an `HTMLResponse`, the LLM receives a generic message: `"<tool_name>: Embedded UI result is active and visible to the user."` This gives the model no information about *what* was actually generated.\n\nTo provide the LLM with actionable context about the embed, return a **tuple** of `(HTMLResponse, context)` where the second element is a `str`, `dict`, or `list`:',
     '### 自定义结果上下文\n\n默认情况下，当工具返回 `HTMLResponse` 时，LLM 会收到一条通用消息：`"<tool_name>: Embedded UI result is active and visible to the user."`。这不会向模型提供关于*实际生成了什么*的信息。\n\n要为 LLM 提供关于嵌入的可操作上下文，请返回 `(HTMLResponse, context)` 的**元组**，其中第二个元素是 `str`、`dict` 或 `list`：'),
    ('The context can be:\n- A **string** \u2014 sent as-is to the LLM (e.g., `"Generated a bar chart with 5 categories"`)\n- A **dict** \u2014 serialized as JSON for structured context\n- A **list** \u2014 serialized as JSON for multiple items\n\nIf the second element is missing or not one of these types, the generic fallback message is used.',
     '上下文可以是：\n- **字符串** — 原样发送给 LLM（如 `"Generated a bar chart with 5 categories"`）\n- **dict** — 序列化为 JSON 提供结构化上下文\n- **list** — 序列化为 JSON 提供多个项目\n\n如果第二个元素缺失或不是这些类型之一，则使用通用回退消息。'),
    (':::tip When to use this\nThis is particularly useful when your tool generates dynamic content and the LLM needs to reference what was generated in follow-up conversation \u2014 for example, telling the LLM which parameters were used, what data is being displayed, or what actions the user can take next.\n:::',
     ':::tip 何时使用\n当你的工具生成动态内容，且 LLM 需要在后续对话中引用所生成内容时，这尤为有用——例如，告诉 LLM 使用了哪些参数、显示了哪些数据，或用户接下来可以执行什么操作。\n:::'),
    ('## Action Usage\n\nActions work exactly the same way. The rich UI embed is delivered to the chat via the event emitter:',
     '## Action 用法\n\nActions 的工作方式完全相同。富 UI 嵌入通过事件发射器传递到对话：'),
])

# ============================================================
# plugin/development/valves.mdx
# ============================================================
translate(f'{BASE}/features/extensibility/plugin/development/valves.mdx', [
    ('title: "Valves"', 'title: "Valves"'),  # keep
    ('## Valves\n\nValves and UserValves are used to allow users to provide dynamic details such as an API key or a configuration option. These will create a fillable field or a bool switch in the GUI menu for the given function. They are always optional, but HIGHLY encouraged.\n\nHence, Valves and UserValves class can be defined in either a `Pipe`, `Pipeline`, `Filter` or `Tools` class.\n\nValves are configurable by admins alone via the Tools or Functions menus. On the other hand UserValves are configurable by any users directly from a chat session.',
     '## Valves\n\nValves 和 UserValves 用于允许用户提供动态详情，如 API 密钥或配置选项。这些将在给定函数的 GUI 菜单中创建可填写字段或布尔开关。它们始终是可选的，但**强烈建议**使用。\n\n因此，Valves 和 UserValves 类可以在 `Pipe`、`Pipeline`、`Filter` 或 `Tools` 类中定义。\n\nValves 只能由管理员通过 Tools 或 Functions 菜单进行配置。而 UserValves 可以由任何用户直接从对话会话中配置。'),
    ('## Input Types', '## 输入类型'),
])

print('\nDone!')
