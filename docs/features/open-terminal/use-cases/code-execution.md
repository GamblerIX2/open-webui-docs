---
sidebar_position: 1
title: "代码执行"
---

# 代码执行

Open Terminal 让 AI 能够实时编写、执行和调试代码。它处理完整的循环——编写脚本、运行它、读取错误，并不断迭代，直到得到正确结果。

---

## 数据可视化

> **你：** 创建一张展示全球人口最多的前 10 个国家的图表。

AI 编写 Python 脚本、执行它并保存输出。结果在文件浏览器中可用。

![AI 创建并运行带输出的 Python 脚本](/images/open-terminal-ai-code-execution.png)

---

## 下载和处理文件

> **你：** 从这个网页下载图片并按大小排序。

AI 安装所需软件包、编写脚本、下载文件并整理：

![AI 安装库并运行脚本](/images/open-terminal-ai-install-run.png)

:::tip 自动安装依赖
在 Docker 模式下，AI 可以按需安装软件包。如果一项任务需要未预装的库，它会在执行之前自动安装。
:::

---

## 自动纠错

代码失败时，AI 读取错误输出并进行调整：

> **你：** 抓取这个新闻网站的所有文章标题。

AI 编写一个爬虫程序，遇到意外的页面布局，读取 `AttributeError` 跟踪，调整 CSS 选择器，并成功重运行。

![AI 检测到错误、修复脚本并成功运行](/images/open-terminal-ai-debug-fix.png)

---

## 多步项目脆核

> **你：** 创建一个带 Web 界面和数据库的待办事应用。

AI：
1. 创建项目文件（HTML、CSS、JavaScript、Python 后端）
2. 安装依赖
3. 设置数据库
4. 启动服务器
5. 在 Web 预览中验证结果

![AI 列出文件并描述项目结构](/images/open-terminal-ai-file-listing.png)



---

## 系统查询

> **你：** 检查谁占用了最多的磁盘空间。

![AI 分析磁盘使用情况并定位大文件](/images/open-terminal-ai-disk-usage.png)

---

## 可用语言

| 语言 | 状态 |
| :--- | :--- |
| Python | 预装 |
| JavaScript (Node.js) | 预装 |
| Bash | 始终可用 |
| Ruby | 预装 |
| C / C++ | Compiler pre-installed |

Additional languages (Rust, Go, Java, etc.) can be installed on the fly.

## Related

- **[Software development →](./software-development)** — repos, tests, debugging, refactoring
- **[Document & data analysis →](./file-analysis)** — spreadsheets, PDFs, Word docs
- **[Web development →](./web-development)** — build and preview websites
- **[System automation →](./system-automation)** — file management, backups, batch operations
