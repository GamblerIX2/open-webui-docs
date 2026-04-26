---
sidebar_position: 3
title: "Open Terminal"
---

# ⚡ Open Terminal

**给你的 AI 一台真正的计算机来工作。**

Open Terminal 将真实的计算环境连接到 Open WebUI。AI 可以编写代码、执行代码、读取输出、修复错误并反复迭代，全程无需离开聊天界面。它能处理文件、安装软件包、运行服务器，并将结果直接返回给你。在 Docker 容器中运行可获得隔离保护，也可在裸机上运行以直接访问你的机器。

这里是想法变成可运行软件的地方。提一个问题，得到一段运行中的脚本；描述一个网站，看它实时渲染；指向一个数据集，得到一份完整的报告。

![带有 Open Terminal、文件浏览器侧边栏和聊天的 Open WebUI](/images/open-terminal-file-browser.png)

---

## 功能概览

### 数据分析与报告

上传电子表格、CSV 或数据库文件。AI 读取数据、运行分析脚本并生成图表或报告。

![AI 分析电子表格数据](/images/open-terminal-ai-csv-analysis.png)

### 文档检索与内容提取

将 AI 指向包含 PDF、Word 文档或电子邮件的文件夹。它会逐一读取，并返回结构化结果：摘要、提取字段或交叉引用。

{/* TODO: Screenshot — A chat where the user asks about the Johnson contract. The AI lists the files it found in a folder (contract_v2.docx, notes.pdf, invoice.xlsx) and provides a consolidated summary of relevant information from each. */}

### Web 开发与实时预览

AI 构建 HTML/CSS/JS 项目、启动预览服务器，并在 Open WebUI 内部渲染结果。通过聊天描述修改内容，预览随即更新。

{/* TODO: Screenshot — A chat on the left side of the screen. On the right, a live website preview panel shows a clean event landing page with a banner, date, and registration button. */}

### 软件开发

通过自然语言克隆仓库、运行测试套件、调试失败、重构代码，以及与 Git 交互。

### 文件与系统自动化

批量重命名、排序、去重、转换、压缩和整理文件。管理磁盘空间、定时备份、处理日志。

{/* TODO: Screenshot — A chat where the user asks "rename all the photos to include the date". The AI responds confirming "Renamed 43 files" with a before/after example: IMG_4521.jpg → 2025-03-15_IMG_4521.jpg. */}

---

## 核心特性

| | |
| :--- | :--- |
| 🖥️ **代码执行** | 运行真实命令并返回输出 |
| 📁 **文件浏览器** | 在侧边栏浏览、上传、下载和编辑文件 |
| 📄 **文档阅读** | 支持 PDF、Word、Excel、PowerPoint、RTF、EPUB、电子邮件 |
| 🌐 **网站预览** | 在 Open WebUI 内实时预览 Web 项目 |
| 🔒 **可选隔离** | 在 Docker 容器中运行以沙箱隔离，或在裸机上运行以获得完整访问权限 |

---

## 快速开始

**[安装 →](./setup/installation)** · **[连接到 Open WebUI →](./setup/connecting)**

:::info 模型要求
Open Terminal 需要支持**原生函数调用**的模型。前沿模型（GPT-5.4、Claude Sonnet 4.6、Gemini 3.1 Pro）能很好地处理复杂的多步骤任务。较小的模型可以处理简单命令，但在较长的工作流中可能表现欠佳。请在你的模型上[启用原生函数调用](./setup/connecting#8-enable-native-function-calling)。
:::

---

## 使用场景

- **[代码执行](./use-cases/code-execution)** — 编写、运行和调试脚本
- **[软件开发](./use-cases/software-development)** — 仓库、测试、调试、重构、Git
- **[文档与数据分析](./use-cases/file-analysis)** — 电子表格、PDF、Word 文档、电子邮件
- **[Web 开发](./use-cases/web-development)** — 构建和预览网站
- **[系统自动化](./use-cases/system-automation)** — 文件管理、备份、批量操作
- **[高级工作流](./use-cases/advanced-workflows)** — 数据报告、研究、代码审查等技能
- **[文件浏览器](./file-browser)** — 上传、预览、编辑文件

---

## Enterprise Multi-User

Need isolated, per-user terminal containers for your team? **[Terminals](./terminals/)** provisions a dedicated Open Terminal instance for every user with automatic lifecycle management, resource controls, and policy-based environments.
