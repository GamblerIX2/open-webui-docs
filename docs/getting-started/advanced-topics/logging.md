---
sidebar_position: 5
title: "Open WebUI 日志"
---

# Open WebUI 日志

**控制 Open WebUI 记录什么、输出到哪里、采用什么格式——从快速调试到生产日志管道都适用。**

Open WebUI 有两个日志面：前端调试用的**浏览器控制台**，以及服务端事件用的 **Python 后端日志**。大多数配置都发生在后端：你可以通过一个环境变量调整详细程度，也可以切换到结构化 JSON 输出，以对接 Loki、Datadog、CloudWatch 等日志聚合器。

---

## 前端日志

前端使用标准浏览器 `console.log()` 调用。打开浏览器开发者工具（**F12**，或 macOS 上的 **Cmd+Option+I**），切换到 **Console** 标签页，即可看到客户端应用输出的信息、警告与错误。

各浏览器文档：

- [Chrome/Chromium DevTools](https://developer.chrome.com/docs/devtools/)
- [Firefox Developer Tools](https://firefox-source-docs.mozilla.org/devtools-user/)
- [Safari Developer Tools](https://developer.apple.com/safari/tools/)

---

## 后端日志

后端使用 Python 内置的 `logging` 模块。默认情况下，日志以 `INFO` 级别输出到 **stdout**，因此你可以直接在终端或容器日志中看到它们。

### 日志级别

| 级别 | 数值 | 适用场景 |
|---|---|---|
| `CRITICAL` | 50 | 灾难性故障；应用可能终止 |
| `ERROR` | 40 | 操作失败；应用继续运行，但已有功能出错 |
| `WARNING` | 30 | 值得调查的异常情况：弃用提示、资源压力等 |
| `INFO` | 20 | 正常运行流程：启动、关键事件、请求处理 **（默认）** |
| `DEBUG` | 10 | 详细诊断输出：函数调用、变量值、执行步骤 |

---

### 设置全局日志级别

设置 `GLOBAL_LOG_LEVEL` 即可调整整个后端的日志详细程度。它会通过 `logging.basicConfig(force=True)` 配置 Python 根 logger，从而影响所有 Open WebUI logger 以及大多数第三方库。

**Docker：**

```bash
--env GLOBAL_LOG_LEVEL="DEBUG"
```

**Docker Compose：**

```yaml
environment:
  - GLOBAL_LOG_LEVEL=DEBUG
```

:::tip
`DEBUG` 适合开发和故障排查。生产环境建议保持在 `INFO` 或 `WARNING`，以免日志量过大。
:::

---

### 结构化 JSON 日志 {#structured-json-logging}

如果生产环境使用日志聚合器，可设置 `LOG_FORMAT=json`，让所有 stdout 输出都变为单行 JSON 对象。

**Docker：**

```bash
--env LOG_FORMAT="json"
```

**Docker Compose：**

```yaml
environment:
  - LOG_FORMAT=json
```

**JSON 字段：**

| 字段 | 说明 |
|---|---|
| `ts` | ISO 8601 时间戳 |
| `level` | 日志级别（`debug`、`info`、`warn`、`error`、`fatal`） |
| `msg` | 日志消息 |
| `caller` | 源代码位置（`module:function:line`） |
| `extra` | 额外上下文数据（如有） |
| `error` | 错误详情（如适用） |
| `stacktrace` | 堆栈跟踪（如适用） |

**示例输出：**

```json
{"ts": "2026-02-22T20:14:53.386+00:00", "level": "info", "msg": "GLOBAL_LOG_LEVEL: INFO", "caller": "open_webui.env"}
{"ts": "2026-02-22T20:15:02.245+00:00", "level": "info", "msg": "Context impl SQLiteImpl.", "caller": "alembic.runtime.migration"}
```

:::note
- 默认行为（未设置 `LOG_FORMAT`）保持不变：仍为纯文本输出
- 设置 `LOG_FORMAT=json` 后会隐藏 ASCII banner，以保证日志流便于解析
- JSON 日志覆盖早期启动日志（stdlib `logging`）和运行期日志（Loguru）
:::
