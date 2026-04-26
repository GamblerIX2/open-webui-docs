---
sidebar_position: 3
title: "研究助手"
---

# 🔍 研究并总结任何主题

给 AI 一个问题，它就会从网络收集信息、整理并撰写结构化简报。

> **你：** $Research Assistant <br/>
> 固态电池目前的现状是什么？主要参与者有哪些？商业化的时间线是什么？

## AI 的工作流程

1. 使用 `curl` 从相关科技新闻网站、公司页面和文章中获取内容
2. 解析 HTML 提取有用文本
3. 对多个来源进行之客对比
4. 创建带有小标题、来源引用和对比表格的结构化 Markdown 简报
5. 保存为 Markdown 和 PDF 两种格式

{/* TODO: Screenshot — Chat showing the AI gathering information from 6+ sources and producing a structured briefing document. The file browser shows research_briefing.md being previewed with headers, bullet points, and a comparison table. */}

{/* TODO: Screenshot — The briefing document showing an executive summary, a comparison table of key companies and their technology approaches, and a source list with URLs. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: research-assistant
description: Researches topics from the web and creates structured briefing documents
---

## Research Assistant

When asked to research a topic:

1. **Plan first**: Identify 3-5 angles to investigate
2. **Gather information**: Use curl to fetch content from authoritative sources. Parse HTML with beautifulsoup4 to extract text
3. **For each source, note**:
   - Key claims and data points
   - Publication date
   - Source authority/reliability
4. **Organize into a document**:
   - Executive summary (3 sentences)
   - Findings by theme
   - Comparison tables where helpful
   - Source list with URLs
5. **Flag conflicts**: Note where sources disagree
6. **Save** as Markdown and optionally PDF

Clearly distinguish facts from sources vs. your own analysis.
```
