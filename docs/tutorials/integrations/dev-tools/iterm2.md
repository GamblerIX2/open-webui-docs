---
title: "iTerm2"
---

# 在 iTerm2 中使用你的 Open WebUI 模型

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看[贡献教程](/contributing)。

:::

你可以在 iTerm2 AI 插件中直接调用 Open WebUI 模型。本指南将说明所需配置步骤。

## 为什么使用 iTerm2 AI 插件？

当你忘记命令，或需要快速生成重复任务的 bash 脚本时，通常会借助 AI。iTerm2 AI 插件可以把这条流程直接集成到终端中，让你将请求发送到指定 AI 提供商或 Open WebUI。

## 为什么连接到 Open WebUI 实例？

Open WebUI 通过 [API Endpoints](/reference/api-endpoints) 提供了简洁直接的 LLM 交互方式，尤其适合本地自托管模型。同时你还能复用已配置好的功能、监控与其他能力。

## 前置条件

### 1. 下载 iTerm2 AI 插件

如果你尚未安装 iTerm2 AI 插件，请先从[官方页面](https://iterm2.com/ai-plugin.html)下载。
解压后将应用移动到 **Applications** 文件夹。

### 2. 生成 Open WebUI API key

要与 Open WebUI 实例进行认证，你需要生成 API key。
请按 [API Endpoints 指南](/reference/api-endpoints)中的步骤创建。

## 配置

打开 iTerm2，进入 **iTerm2** 菜单中的 **Settings**（⌘,），然后选择 **AI** 标签页。

![iterm2 menu before setup](/images/tutorials/iterm2/iterm2_ai_plugin_before.png)

### 验证插件安装状态

安装完成后，请确认 **Plugin** 区域显示 `Plugin installed and working ✅`。

---

### 同意启用生成式 AI 功能

在 **Consent** 区域勾选 `Enable generative AI features`。

---

### 设置 API key

将前面创建的 Open WebUI API token 填入 **API Key** 字段。

---

### 可选：自定义提示词

如果你希望向 LLM 发送特定风格提示词，可编辑 `Prompt template`。

**原始提示词示例：**

```text
Return commands suitable for copy/pasting into \(shell) on \(uname). Do
NOT include commentary NOR Markdown triple-backtick code blocks as your
whole response will be copied into my terminal automatically.

The script should do this: \(ai.prompt)
```

关于 iTerm2 提示词可参阅 [iTerm2 文档](https://gitlab.com/gnachman/iterm2/-/wikis/AI-Prompt)。

---

### 选择你的 LLM

由于 iTerm2 AI 插件不会自动列出你的自定义模型，你需要手动添加。
在 Open WebUI 中进入 `Admin Panel` > `Settings` > `Models`，点击你要使用的 LLM。
在模型显示名下方可以找到实际模型名，填写到 iTerm2 中（例如：name 为 Gemma3，对应 model name 为 `/models/gemma3-27b-it-Q4_K_M.gguf`）。

---

### 调整 Token 数量

在这里设置你期望的 token 数量。通常推理工具本身也会有上限。

---

### 设置 URL

这是关键步骤：你需要将 iTerm2 AI 插件的请求指向 Open WebUI 实例。
如果实例部署在远端，请使用域名（例如 `https://example.com/api/chat/completions`）；如果是本地部署，可使用本地地址（例如 `http://localhost:8080/api/chat/completions`）。
URL 详情可参见 [API Endpoints 指南](/reference/api-endpoints)。

---

### Legacy Completions API

该设置在 Open WebUI 中通常不需要，如需了解可参考[原始文档](https://platform.openai.com/docs/guides/completions/completions-api-legacy)。

---

配置完成后，**AI** 区域大致如下：

![iterm2 menu after setup](/images/tutorials/iterm2/iterm2_ai_plugin_after.png)

## 使用方式

在终端会话中按 **command + y**（⌘y）打开提示词输入框。输入提示词后，点击 **OK** 或使用 **shift + enter**（⇧⌤）发送。

![iterm2 prompt window](/images/tutorials/iterm2/iterm2_ai_plugin_prompt_window.png)

---

发送后会回到终端，并在当前会话中出现一个附加窗口。查询结果会显示在该覆盖层中。若要将命令发送到终端，请将光标移动到目标行并按 **shift + enter**（⇧⌤）。

:::info

返回内容可能有多行。你可以使用方向键移动并按需编辑命令。

:::

![iterm2 prompt window](/images/tutorials/iterm2/iterm2_ai_plugin_result_window.png)
