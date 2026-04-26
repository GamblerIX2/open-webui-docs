---
sidebar_position: 10
title: "Continue.dev"
---

# 将 Continue.dev VS Code 扩展与 Open WebUI 集成

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

## 下载扩展

您可以在 [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=Continue.continue) 下载 VS Code 扩展，或在 VS Code 的 `EXTENSION:MARKETPLACE` 中搜索 `continue` 直接安装。
安装完成后，您可以通过 VS Code 侧边栏中的 `continue` 选项卡访问该应用程序。

**VS Code 侧边栏图标：**

![continue.dev vscode icon](/images/tutorials/continue-dev/continue_dev_vscode_icon.png)

---

## 设置

点击主聊天输入框右侧的助手选择器，将鼠标悬停在 `Local Assistant` 上，然后点击设置图标（⚙️）。
这将在编辑器中打开 `config.yaml` 文件。在这里您可以更改 `Local Assistant` 的设置。

![continue.dev chat input](/images/tutorials/continue-dev/continue_dev_extension_input_field.png)

:::info

目前 `ollama` 提供商不支持身份验证，因此我们无法在 Open WebUI 中使用此提供商。
但是 Ollama 和 Open WebUI 都与 OpenAI API 规范兼容。请阅读 [Ollama 关于 OpenAI 兼容性的博客文章](https://ollama.com/blog/openai-compatibility)了解更多规范信息。
我们仍然可以将 continue.dev 设置为使用 openai 提供商，这样就可以使用 Open WebUI 的身份验证令牌。

:::

### 配置示例

以下是使用 Llama3 作为模型，配合本地 Open WebUI 设置的配置示例。

```yaml
name: Local Assistant
version: 1.0.0
schema: v1
models:
  - name: LLama3
    provider: openai
    model: Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
    env:
      useLegacyCompletionsEndpoint: false
    apiBase: http://localhost:3000/api
    apiKey: YOUR_OPEN_WEBUI_API_KEY
    roles:
      - chat
      - edit
context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase

```

---

### 其他配置设置

这些值是扩展正常运行所必需的。更多信息请参见[官方配置指南](https://docs.continue.dev/reference)。

```yaml
name: Local Assistant
version: 1.0.0
schema: v1
```

context 部分为模型提供额外信息。更多信息请参见[官方配置指南](https://docs.continue.dev/reference#context)和[上下文提供商指南](https://docs.continue.dev/customize/custom-providers)。

```yaml
context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase
```

---

### 模型

models 部分用于指定您要添加的所有模型。更多信息请参见[官方模型指南](https://docs.continue.dev/reference#models)。

```yaml
models:
  - ...
```

---

### 名称

设置您要使用的模型名称，该名称将显示在扩展的聊天输入框中。

```yaml
name: LLama3
```

![continue.dev chat input](/images/tutorials/continue-dev/continue_dev_extension_input_field.png)

---

### 提供商

指定与 API 通信的方式，本例中为 Open WebUI 提供的 OpenAI API 端点。

```yaml
provider: openai
```

---

### 模型

这是您在 Open WebUI 中模型的实际名称。导航至 `Admin Panel` > `Settings` > `Models`，然后点击您偏好的 LLM。
在用户指定的名称下方，您会找到实际的模型名称。

```yaml
model: Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

---

### 旧版 completions 端点

Open WebUI 不需要此设置，更多信息请参见[原始指南](https://platform.openai.com/docs/guides/completions/completions-api-legacy)。

```yaml
env:
  useLegacyCompletionsEndpoint: false
```

---

### APIBase

这是关键步骤：您需要将 continue.dev 扩展的请求指向您的 Open WebUI 实例。
如果实例托管在某处，请使用实际域名（例如 `https://example.com/api`），或使用本地设置（例如 `http://localhost:3000/api`）。
有关 URL 的更多信息，请参见 [API 端点指南](/reference/api-endpoints)。

```yaml
apiBase: http://localhost:3000/api
```

---

### API 密钥

要向 Open WebUI 实例进行身份验证，您需要生成一个 API 密钥。
请按照 [API 端点指南](/reference/api-endpoints)中的说明创建密钥。

```yaml
apiKey: YOUR_OPEN_WEBUI_API_KEY
```

---

### 角色

角色将允许您的模型在扩展中用于特定任务。初始可以选择 `chat` 和 `edit`。
有关角色的更多信息，请参见[官方角色指南](https://docs.continue.dev/customize/model-roles/intro)。

```yaml
roles:
  - chat
  - edit
```

设置现已完成，您可以通过聊天输入框与您的模型交互。有关 continue.dev 插件的功能和使用的更多信息，请参见[官方文档](https://docs.continue.dev/getting-started/overview)。
