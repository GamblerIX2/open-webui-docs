---
sidebar_position: 5
title: "文档对比"
---

# 📑 对比文档的两个版本

上传合同或方案的两个版本，获得清晰的变更摘要。

> **你：** $Document Comparator <br/>
> *（上传 contract_v1.docx 和 contract_v2.docx）* <br/>
> 对比这两个版本。重点关注付款条款和责任变更。

## AI 的工作流程

1. 读取两个文档（Open Terminal 原生支持 .docx）
2. 在段落/句子级别计算文本差异
3. 将变更分类：仅格式、小幅改词、实质性变更
4. 高亮你指定的具体内容（付款条款、责任条款）
5. 创建包含重要变更对比视图的对比报告

{/* TODO: Screenshot — Chat showing the AI's analysis: "Found 14 changes. 3 substantive:" followed by a highlighted comparison showing a payment term change ("Net 30" → "Net 60") with surrounding context. */}

{/* TODO: Screenshot — A generated diff report showing additions in green and removals in red, with change categories labeled. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: document-comparator
description: Compares two document versions and highlights meaningful changes
---

## Document Comparison

When asked to compare documents:

1. **Read both versions** and extract full text
2. **Compute differences** at the paragraph or sentence level using Python's difflib
3. **Categorize each change**:
   - Formatting only (spacing, capitalization)
   - Minor wording (synonyms, clarifications)
   - Substantive (numbers, dates, terms, obligations, new/removed clauses)
4. **If the user mentions areas of interest** (e.g., "payment terms"), search both documents for those sections and present a focused comparison
5. **Create a report** with:
   - Summary of changes by category
   - Substantive changes with full surrounding context
   - Side-by-side view of key sections
6. **Save** as Markdown and HTML

Always flag changes affecting financial terms, legal obligations, or deadlines.
```
