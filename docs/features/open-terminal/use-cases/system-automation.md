---
sidebar_position: 4
title: "自动化任务"
---

# 自动化任务

Open Terminal 不仅限于代码。AI 可以管理文件、整理文件夹、批量处理数据、处理备份并自动化重复性工作——所有这些都通过对话完成。

---

## “重命名和整理这些文件”

> **你：** /photos 文件夹里有 200 张图片，文件名格式为 IMG_4521.jpg。请将它们重命名为包含日期的名称，并按月份整理到各文件夹。

AI 读取文件日期，重命名所有文件，并创建按月分类的文件夹：

![AI 创建并重命名带日期前缀的文件](/images/open-terminal-ai-file-rename.png)

---

## “找出并删除重复文件”

> **你：** 我的文档文件夹里有重复文件吗？

AI 检查文件大小和内容找出完全相同的文件，然后询问你如何处理：

![AI 分析文件硬盘使用详情](/images/open-terminal-ai-disk-usage.png)

---

## “备份这个文件夹”

> **你：** 将 /projects 文件夹创建一个包含今天日期的 zip 备份文件。

![AI 执行系统自动化命令](/images/open-terminal-ai-file-rename.png)

---

## “转换这些文件”

> **你：** 将文件夹中所有 .png 截图转换为 .jpg 并缩小一半。

AI 使用图像工具（Docker 镜像预装）进行批量转换和缩放：

![AI 使用 run_command 进行批量文件操作](/images/open-terminal-ai-install-run.png)

---

## “检查系统状态”

> **你：** 磁盘还剩多少空间？有没有大文件可以清理一下？

![AI 检查磁盘使用情况并分析存储](/images/open-terminal-ai-disk-usage.png)

---

## “对文件夹里的每个文件执行这个操作”

> **你：** 对 /data 中的每个 CSV 文件，添加一行 “Name, Date, Amount” 表头并保存。

AI 编写脚本，处理每个文件，并报告结果：

![AI 读取并分析 CSV 数据](/images/open-terminal-ai-csv-analysis.png)

---

## 预装工具

Docker 镜像预装了常用工具，开箱即用：

| 你想要做的事 | 可用工具 |
| :--- | :--- |
| 从互联网下载文件 | curl、wget |
| 处理 JSON 数据 | jq |
| 压缩/解压文件 | zip、tar、gzip、7z |
| 处理图像 | ffmpeg、ImageMagick（如已安装） |
| 使用数据库 | sqlite3 |
| 在服务器间传输文件 | rsync、scp |

Open Terminal isn't just for code. The AI can manage files, organize folders, process data in bulk, handle backups, and automate repetitive work — all from a conversation.

---

## "Rename and organize these files"

> **You:** I have 200 photos in the /photos folder with names like IMG_4521.jpg. Rename them to include the date and sort them into folders by month.

The AI reads the file dates, renames everything, and creates monthly folders:

![AI creating and renaming files with date prefixes](/images/open-terminal-ai-file-rename.png)

---

## "Find and remove duplicates"

> **You:** Are there any duplicate files in my documents folder?

The AI checks file sizes and content to find exact duplicates, then asks you what to do:

![AI analyzing files with disk usage details](/images/open-terminal-ai-disk-usage.png)

---

## "Back up this folder"

> **You:** Create a zip backup of the /projects folder with today's date in the filename.

![AI executing system automation commands](/images/open-terminal-ai-file-rename.png)

---

## "Convert these files"

> **You:** Convert all the .png screenshots in this folder to .jpg and make them half the size.

The AI uses image tools (which come pre-installed in Docker) to batch-convert and resize:

![AI using run_command for batch file operations](/images/open-terminal-ai-install-run.png)

---

## "Check on the system"

> **You:** How much disk space is left? Are any big files I should clean up?

![AI checking disk usage and analyzing storage](/images/open-terminal-ai-disk-usage.png)

---

## "Do this to every file in the folder"

> **You:** For every CSV file in /data, add a header row with "Name, Date, Amount" and save it.

The AI writes a script, processes every file, and reports back:

![AI reading and analyzing CSV data](/images/open-terminal-ai-csv-analysis.png)

---

## Pre-installed tools

The Docker image comes with common tools ready to use:

| What you want to do | Tools available |
| :--- | :--- |
| Download files from the internet | curl, wget |
| Work with JSON data | jq |
| Compress / decompress files | zip, tar, gzip, 7z |
| Process images | ffmpeg, ImageMagick (if installed) |
| Work with databases | sqlite3 |
| Transfer files between servers | rsync, scp |

If a tool isn't installed, the AI can install it on the fly (`sudo apt install ...`).

## More things to try

- **[Run code from chat →](./code-execution)** — the AI writes, runs, and debugs code
- **[Analyze documents & data →](./file-analysis)** — spreadsheets, PDFs, Word docs, emails
- **[Build & preview websites →](./web-development)** — create and iterate on web pages
