---
sidebar_position: 4
title: "邮件处理"
---

# 📧 处理一批邮件

上传一批 `.eml` 文件，获得一份包含待办事项和截止日期的结构化电子表格。

> **你：** $Email Processor <br/>
> 处理 /project-emails 文件夹，提取所有待办事项和截止日期。

## AI 的工作流程

1. 列出文件夹中所有 `.eml` 文件
2. 读取每封邮件：头部（发件人、收件人、主题、日期）和正文
3. 识别待办事项、截止日期、决策和待解答的问题
4. 创建带结构化列的 CSV
5. 标记过期项目
6. 撰写最关键邮件的摘要

{/* TODO: Screenshot — Chat showing the AI processing 45 email files and producing a summary. File browser previews email_actions.csv as a formatted table with Date, From, Subject, Action Item, Deadline, Status columns. */}

{/* TODO: Screenshot — The summary output listing the 5 most critical action items with their deadlines and which email they came from. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: email-processor
description: Reads .eml email files and extracts action items, deadlines, and key decisions
---

## Email Processing

When asked to process email files:

1. **List all .eml files** in the specified directory
2. **For each email, extract**:
   - Headers: From, To, CC, Date, Subject
   - Body: prefer plain text, strip HTML tags as fallback
   - Attachment filenames (if any)
3. **Analyze each body for**:
   - Action items (tasks assigned to someone)
   - Deadlines or due dates
   - Decisions made
   - Questions that need answers
4. **Create a CSV** with columns: Date, From, Subject, Action Items, Deadline, Priority
5. **Sort by date** and flag anything overdue
6. **Write a summary** highlighting the 5 most critical items

Preserve original email context so findings are traceable.
```
