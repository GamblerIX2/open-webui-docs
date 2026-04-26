---
sidebar_position: 10
title: "文件浏览器"
---

# 文件浏览器

当 Open Terminal 连接后，聊天的侧边栏中会出现一个**文件浏览器**。它的使用方式就像你电脑上的文件资源管理器——可以浏览文件夹、打开文件、上传内容和下载结果。AI 创建的所有内容都会自动显示在这里。

![带有文件浏览器侧边栏的聊天界面](/images/open-terminal-file-browser.png)

---

## 浏览文件

点击文件夹进行导航，点击文件预览内容。顶部的面包屑导航栏会显示你当前所在的位置。

![带有面包屑导航的项目目录浏览](/images/open-terminal-file-browser-project.png)

---

## 预览文件

点击任意文件即可查看预览。不同文件类型的显示方式各不相同：

### 文本与代码
源代码和文本文件会以语法高亮和行号的形式呈现。

![带有语法高亮和行号的 Python 代码](/images/open-terminal-preview-code.png)

### PDF
PDF 文档可直接在浏览器中渲染——无需下载即可阅读。

![带有渲染 Markdown 预览的文件浏览器](/images/open-terminal-preview-markdown.png)

### 电子表格（CSV、TSV）
数据文件以**格式化表格**的形式呈现，包含标题和整洁的行——比原始逗号分隔文本更易阅读。

![CSV 数据渲染为整洁表格](/images/open-terminal-preview-csv.png)

### Markdown
Markdown 文件会显示**渲染预览**（包含格式化的标题、链接、加粗文本），并提供切换到原始源码的开关。

![带有标题、列表和格式化文本的渲染 Markdown](/images/open-terminal-preview-markdown.png)

### 图片
图片以合适的大小内联显示。

![显示图片预览的文件浏览器](/images/open-terminal-file-browser-home.png)

---

## 上传文件

直接将文件从你的电脑**拖放**到文件浏览器中即可上传。这是与 AI 共享数据的方式——拖入电子表格、PDF、图片或任何你希望 AI 处理的文件。

![显示已上传文件名称和大小的文件浏览器](/images/open-terminal-file-browser-home.png)

:::tip 上传到任意文件夹
先导航到你想要的文件夹，然后再拖放。文件会上传到你当前正在浏览的目录。
:::

---

## 下载文件

点击任意文件上的**下载按钮**即可将其保存到你的电脑。这是获取结果的方式：AI 生成图表、创建电子表格、处理图片或撰写报告后，直接下载即可。

![带有下载和操作按钮的文件浏览器](/images/open-terminal-file-browser-project.png)

---

## 编辑文件

点击任意文本文件上的**编辑图标**，即可在编辑器中打开并进行修改，保存即可生效。这对于快速修改非常方便——编辑配置值、纠正错别字，或调整 AI 生成的内容。

![在文件浏览器中直接编辑文件](/images/open-terminal-preview-code.png)

---

## Creating and deleting

You can create new files and folders, or delete things you don't need anymore, directly from the file browser.

![File browser action bar with New File, New Folder options](/images/open-terminal-file-browser-home.png)

---

## Good to know

:::tip Files update automatically
When the AI creates or changes files, the file browser refreshes automatically. You don't need to manually reload.
:::

:::tip Remembers where you were
The file browser remembers which folder you were in, even when you switch between chats or terminals.
:::

:::tip Multiple terminals
If you have more than one terminal connected, switching between them in the dropdown updates the file browser to show that terminal's files.
:::

## More things to try

- **[Analyze documents & data →](./use-cases/file-analysis)** — drag in a spreadsheet or PDF and ask about it
- **[Run code from chat →](./use-cases/code-execution)** — the AI creates files you can see here
- **[Build & preview websites →](./use-cases/web-development)** — the files the AI creates appear in the browser
