---
sidebar_position: 2
title: "连接到 Open WebUI"
---

# 将 Open Terminal 连接到 Open WebUI

Open Terminal 已[安装并运行](./installation)。本指南介绍如何将其连接到 Open WebUI。

---

## 推荐方式：管理面板

适用于所有部署场景，包括单用户场景。管理面板可将 API Key 保存在服务端。

### 1. 打开管理面板

点击左侧边栏底部的**你的名字**，打开用户菜单，然后点击**管理面板**。

![显示管理面板选项的用户菜单](/images/open-terminal-user-menu.png)

### 2. 进入 Settings → Integrations

在管理面板中，点击顶部导航栏的 **Settings**，再点击 **Integrations**。

![管理面板 — Settings → Integrations](/images/open-terminal-integrations-page.png)

### 3. 找到 "Open Terminal" 区域

向下滚动，直到看到 **Open Terminal** 区域。

![Integrations 下的 Open Terminal 区域](/images/open-terminal-connected.png)

:::warning 不要与 "Tools" 混淆
Open Terminal 在 Integrations 下有**独立的区域**——不要将它添加到 "External Tools" 或 "Tool Servers" 下。使用专属区域才能获得内置的文件浏览器和终端侧边栏。
:::

### 4. 点击 + 并填写详情

| 字段 | 填写内容 |
| :--- | :--- |
| **URL** | `http://localhost:8000`（使用 Docker Compose 时为 `http://open-terminal:8000`） |
| **API Key** | 安装时设置的密码 |
| **Auth Type** | 保持默认的 `Bearer` |

![填写了 URL 和 API Key 的连接表单](/images/open-terminal-connection-form.png)

### 5. 保存

点击**保存**。绿色的"Connected"指示器确认连接成功。

![带有绿色指示器的已连接状态](/images/open-terminal-connected.png)

### 6.（可选）限制特定组的访问

通过访问控制按钮，将终端访问限制到特定用户组。

{/* TODO: Screenshot — The Access Grants dropdown showing available user groups with checkboxes. */}

### 7. 在聊天中选择终端

在聊天输入区域，点击**终端按钮**（云图标 ☁）。管理员配置的终端会显示在 **System** 下方。选择一个以在当前对话中启用它。

![终端下拉菜单，显示 System 下的 Docs Terminal](/images/open-terminal-chat-dropdown.png)

所选终端名称会显示在云图标旁边。AI 现在可以通过它执行命令、读取文件和运行代码。

### 8. 启用原生函数调用

为使 AI 能可靠地使用终端工具，你需要在模型上启用**原生函数调用**：

1. 进入 **Workspace → Models**
2. 点击你正在使用的模型的编辑按钮
3. 在 **Capabilities** 下，启用 **Native Function Calling**（也称"tool use"）
4. 保存

![显示内置工具已启用的模型能力页面](/images/open-terminal-model-capabilities.png)

:::warning 不启用此功能，工具可能无法使用
原生函数调用让模型使用提供商内置的工具调用格式直接调用工具。若不启用，Open WebUI 会回退到基于提示词的工具调用，可靠性较差，且可能根本无法触发终端命令。
:::

:::tip 性能取决于所用模型
并非所有模型在工具使用方面都同样出色。前沿模型（GPT-5.4、Claude Sonnet 4.6、Gemini 3.1 Pro）能很好地处理多步骤终端工作流。较小或较旧的模型可能难以应对复杂任务、无法调用工具或产生格式错误的工具调用。如果效果不佳，请尝试更强大的模型。
:::

### 9. 测试一下

向 AI 提问，例如：

> "你运行的是什么操作系统？"

AI 应该会使用 Open Terminal 运行一条命令，然后告诉你答案。

![AI 使用 run_command 检查操作系统](/images/open-terminal-ai-os-query.png)


:::tip 通过环境变量预配置
对于 Docker 部署，可以使用 `TERMINAL_SERVER_CONNECTIONS` 环境变量自动配置终端连接——适用于希望在启动时就完成全部配置而无需手动操作的场景。
:::

---

## 个人设置（仅用于测试）

:::caution 不建议日常使用
通过个人设置添加终端连接会将 API Key 发送到你的浏览器，并直接从浏览器路由请求。这对于**快速测试**来说没问题，但除此之外，请使用管理员设置——它更安全，且对所有用户自动生效。
:::

如果需要在没有管理员权限的情况下测试连接，可以从 **Settings → Integrations → Open Terminal** 添加。URL 和 API Key 字段相同。

---

## 故障排除

### "连接失败"或超时

这几乎总是意味着 Open WebUI 无法通过网络访问 Open Terminal。使用哪个 URL 取决于你的配置：

| 你的配置 | 使用的 URL |
| :--- | :--- |
| Docker Compose（推荐） | `http://open-terminal:8000` |
| 独立 Docker 容器 | `http://host.docker.internal:8000` |
| 同一机器，无 Docker | `http://localhost:8000` |
| Open Terminal 在另一台机器上 | `http://那台机器的IP:8000` |

{/* TODO: Screenshot — A simple diagram showing Open WebUI and Open Terminal as two boxes, with an arrow between them labeled with the URL. Shows correct URLs for Docker Compose (service name) vs separate containers (host.docker.internal). */}

:::tip 快速检查
运行以下命令查看 Open WebUI 是否能访问 Open Terminal：

```bash
docker exec open-webui curl -s http://open-terminal:8000/health
```

如果输出 `{"status": "ok"}`，说明连接正常。如果报错，说明两个容器之间无法互相访问。
:::

### 终端显示了但 AI 不使用它

请确认：
- 连接旁边的开关**已打开**
- 添加连接后已**刷新页面**
- 你的模型支持工具调用（大多数现代模型都支持）

### API Key 错误

如果看到"unauthorized"或"invalid key"：
- 仔细核对密钥是否与安装时设置的一致
- 如果忘记了，运行 `docker logs open-terminal` 并查找 `API key:` 那一行

## 后续步骤

- **[代码执行](../use-cases/code-execution)**
- **[文档与数据分析](../use-cases/file-analysis)**
- **[软件开发](../use-cases/software-development)**
- **[文件浏览器](../file-browser)**
