---
sidebar_position: 3
title: "构建和预览网站"
---

# 构建和预览网站

Open Terminal 最令人印象深刻的功能之一：AI 构建网站、启动服务器，你**在预览面板中实时查看**——所有这些都在 Open WebUI 内完成。然后你告诉它要修改什么，预观实时更新。

---

## 工作原理

1. 你要求 AI 创建网站（或网应用、著陆页或任何基于 Web 的内容）
2. AI 创建文件并启动 Web 服务器
3. Open Terminal **自动检测**到运行中的服务器
4. Open WebUI 中出现**预览面板**，显示实时页面
5. 你说出修改要求 → AI 编辑文件 → 预览更新

![AI 创建著陆页，文件浏览器显示已创建的文件](/images/open-terminal-ai-web-dev.png)

---

## “给我做一个著陆页”

> **你：** 为我的摄影业务创建一个著陆页。包含相册、关于我的部分和联系表单。

AI 创建 HTML、CSS 和 JavaScript 文件，启动 Web 服务器，预览自动出现。页面专业精致——不是简单的线框居。

![File browser showing the created HTML files](/images/open-terminal-ai-web-dev-files.png)

---

## “修改颜色和布局”

页面上线后，继续对话即可迭代修改：

> **你：** 改成深色背景，使用更暖调的配色方案。将相册移到关于我的部分上方。

AI 编辑 CSS 和 HTML 文件，预览立即更新。

---

## “给我做一个交互式应用”

AI 能创建交互式网应用，不仅仅是静态页面：

> **你：** 做一个可在浏览器里运行的简单计算器。

![AI 创建并运行交互式应用的代码](/images/open-terminal-ai-code-execution.png)

---

## “帮我修复我的网站”

已有网站出问题或需要修改？上传文件并说明情况：

> **你：** *（通过文件浏览器上传 HTML/CSS 文件）* <br/>
> 联系表单无法提交。能修复吗？

AI 读取你的代码，找到问题，修复它，你在预览中验证。

![AI 定位并修复代码错误](/images/open-terminal-ai-debug-fix.png)

---

## 端口检测原理

预览出现不需要任何特殊操作。幕后的工作原理：

1. AI 启动 Web 服务器（如 `python -m http.server 3000` 或其他服务器）
2. Open Terminal 监控新的网络端口
3. 检测到服务器运行后，向 Open WebUI 报告端口
4. Open WebUI 通过自身的连接代理流量，展示预览面板

这意味着**不需要开放额外端口**或更改防火墙设置。直接使用即可。

:::tip 多个预览
如果 AI 启动了多个服务器（例如前端在端口 3000，后端 API 在端口 5000），你可以在端口区域中切换它们。
:::

## More things to try

- **[Run code from chat →](./code-execution)** — the AI writes, runs, and debugs code
- **[Analyze documents & data →](./file-analysis)** — spreadsheets, PDFs, Word docs, emails
- **[Automate tasks →](./system-automation)** — file management, backups, batch operations
