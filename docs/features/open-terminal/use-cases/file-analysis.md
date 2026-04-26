---
sidebar_position: 2
title: "分析文档和数据"
---

# 分析你的文档和数据

有一大堆电子表格、PDF、Word 文档或邮件需要整理？将它们拖入文件浏览器，让 AI 替你阅读。Open Terminal 可以打开并理解所有这些格式——无需任何特殊设置。

## 可以读取哪些文件类型？

| 类型 | 格式 |
| :--- | :--- |
| **电子表格** | Excel（.xlsx、.xls）、OpenDocument（.ods）、CSV |
| **文档** | Word（.docx）、OpenDocument（.odt）、RTF（.rtf）、PDF |
| **演示文稿** | PowerPoint（.pptx）、OpenDocument（.odp） |
| **其他** | 邮件（.eml）、电子书（.epub）、纯文本、HTML、Markdown、JSON、XML |

AI 可以直接读取所有这些格式——无需将其上传到外部服务。文件内容存储在你的服务器上并在本地处理。

---

## “将这份报告总结一下”

> **你：** *（拖挙一个 PDF 到文件浏览器）* <br/>
> 你能读一下这份季度报告并给我列出重点吗？

AI 打开 PDF，阅读全文，并给出简洁摘要——提取收入数据、重要决策、显著变化等关键信息。

![AI 读取并分析文件内容](/images/open-terminal-ai-csv-analysis.png)

---

## “处理所有这些发票”

> **你：** /invoices 文件夹里有大约 30 份发票。能否把它们都读一遍，并制作一个包含供应商名称、日期和金额的电子表格？

AI 打开文件夹中的每个文件——即使是 PDF 和 Word 文档混合——提取信息，并创建一个整洁的电子表格供你下载。

![AI 列出文件并提供结构化分析](/images/open-terminal-ai-file-listing.png)

---

## “这些邮件里提到了哪些截止日期？”

> **你：** *（上传几个 .eml 文件）* <br/>
> 读一下这些邮件，找出所有有关截止日期或到期日期的内容。

AI 读取邮件文件——包括发件人、日期、主题和正文——并提取相关信息。

![AI 读取文件并提取特定信息](/images/open-terminal-ai-file-listing.png)

---

## “分析这个数据并制作图表”

> **你：** *（拖入 sales_data.xlsx 到文件浏览器）* <br/>
> 按地区展示销售情况并制作饥形图。

AI 读取电子表格、处理数据、创建图表，并保存为可预览和下载的图片。

![AI 分析销售数据并按产品汇总](/images/open-terminal-ai-csv-analysis.png)

---

## “在所有文档中搜索”

> **你：** 搜索 /contracts 文件夹中所有文件，找出所有提到“终止条款”或“取消”的内容。

AI 搜索每个文件——PDF、Word 文档、电子表格，无论什么格式——并说明确切在哪里找到了匹配项。

![AI 在文件中搜索特定内容](/images/open-terminal-ai-file-listing.png)

:::tip 无需建索引
与传统搜索或 RAG 系统不同，AI 每次为你实时读取文件。这意味着它看到的是磁盘上的当前版本——无需重建索引、无同步延迟、无需管理数据库。
:::

---

## 处理大文件

如果文档非常长，AI 会智能地分段读取，而不是一次性全部读入。你也可以要求它只关注特定部分：

> “只读这份报告的执行摘要部分”

> “显示这个电子表格的第 500 到 600 行”

## 更多玩法

- **[在对话中运行代码 →](./code-execution)** —— AI 编写、运行和调试代码
- **[构建和预览网站 →](./web-development)** —— 创建并迭代网页
- **[浏览文件浏览器 →](../file-browser)** —— 上传、预览、下载和编辑文件

Got a pile of spreadsheets, PDFs, Word documents, or emails you need to make sense of? Drop them into the file browser and let the AI read them for you. Open Terminal can open and understand all of these formats — no special setup needed.

## What file types can it read?

| Type | Formats |
| :--- | :--- |
| **Spreadsheets** | Excel (.xlsx, .xls), OpenDocument (.ods), CSV |
| **Documents** | Word (.docx), OpenDocument (.odt), Rich Text (.rtf), PDF |
| **Presentations** | PowerPoint (.pptx), OpenDocument (.odp) |
| **Other** | Email (.eml), E-books (.epub), plain text, HTML, Markdown, JSON, XML |

The AI can read all of these directly — it doesn't need to upload them to any external service. File content stays on your server and is processed locally.

---

## "Summarize this report"

> **You:** *(drag-drop a PDF into the file browser)* <br/>
> Can you read this quarterly report and give me the key takeaways?

The AI opens the PDF, reads through it, and gives you a concise summary — pulling out revenue figures, key decisions, notable changes, whatever matters.

![AI reading and analyzing file contents](/images/open-terminal-ai-csv-analysis.png)

---

## "Go through all those invoices"

> **You:** There are about 30 invoices in the /invoices folder. Can you read them all and make a spreadsheet with the vendor name, date, and amount?

The AI opens every file in the folder — even if they're a mix of PDFs and Word documents — extracts the information, and creates a clean spreadsheet you can download.

![AI listing files and providing structured analysis](/images/open-terminal-ai-file-listing.png)

---

## "What do these emails say about the deadline?"

> **You:** *(upload several .eml files)* <br/>
> Read through these emails and find any mentions of deadlines or due dates.

The AI reads the email files — including sender, date, subject, and body — and pulls out the relevant information.

![AI reading files and extracting specific information](/images/open-terminal-ai-file-listing.png)

---

## "Analyze this data and make a chart"

> **You:** *(drop a sales_data.xlsx into the file browser)* <br/>
> Break down the sales by region and make a pie chart.

The AI reads the spreadsheet, processes the data, creates a chart, and saves it as an image you can preview and download.

![AI analyzing sales data and summarizing by product](/images/open-terminal-ai-csv-analysis.png)

---

## "Search across all these documents"

> **You:** Search through everything in the /contracts folder for any mention of "termination clause" or "cancellation".

The AI searches across every file — PDFs, Word docs, spreadsheets, whatever's there — and tells you exactly where it found matches.

![AI searching across files for specific content](/images/open-terminal-ai-file-listing.png)

:::tip No indexing required
Unlike traditional search or RAG systems, the AI reads files live every time you ask. That means it sees the current version on disk — no re-indexing, no sync delays, no database to manage.
:::

---

## Working with large files

If a document is very long, the AI is smart about reading it in sections rather than all at once. You can also ask it to focus on specific parts:

> "Read just the executive summary section of this report"

> "Show me rows 500 through 600 of this spreadsheet"

## More things to try

- **[Run code from chat →](./code-execution)** — the AI writes, runs, and debugs code
- **[Build & preview websites →](./web-development)** — create and iterate on web pages
- **[Explore the file browser →](../file-browser)** — upload, preview, download, and edit files
