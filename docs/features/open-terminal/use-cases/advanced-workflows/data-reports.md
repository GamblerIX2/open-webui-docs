---
sidebar_position: 1
title: "数据报告"
---

# 📊 将原始数据转化为精美报告

上传杂乱的数据，AI 会清洗、分析、建立图表，并生成可下载的 PDF 报告。

> **你：** $Data Report Generator <br/>
> *（拖挙 `survey_responses.csv` 到文件浏览器）* <br/>
> 分析这份问卷数据，为我们的团队会议制作一份报告。

## AI 的工作流程

1. 读取 CSV 并识别数据质量问题
2. 清理数据（修复格式、删除重复、处理缺失值）
3. 计算统计数据——回应率、均値、分布
4. 生成图表（条形图、饥形图、趋势线）
5. 将所有内容整合为带有封面、摘要、图表和数据表格的格式化 PDF
6. 将 PDF 保存到文件浏览器以供下载

{/* TODO: Screenshot — File browser showing three outputs: survey_cleaned.csv, charts/ folder with .png files, and survey_report.pdf. The PDF is previewed showing a professional title page. */}

{/* TODO: Screenshot — A page inside the generated PDF showing a bar chart, key findings, and a summary table. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: data-report-generator
description: Analyzes data files and creates professional PDF reports with charts and summaries
---

## Data Analysis & Reporting

When asked to analyze data:

1. **Profile the data first**: Read the file and report row count, column types, missing values, duplicates
2. **Clean the data**: Standardize formats, fill or flag missing values, remove exact duplicates. Save the cleaned version as a separate file
3. **Find the story**: Identify distributions, outliers, correlations, and trends. Focus on the 3-5 most interesting findings
4. **Create charts**: Use matplotlib with a consistent color palette. Label all axes clearly. Save each chart as a PNG in a /charts directory
5. **Build the PDF**: Use reportlab or weasyprint to create a report with:
   - Title page with report name and date
   - Executive summary (3-5 bullet points)
   - One section per major finding with chart and interpretation
   - Data tables in an appendix
6. **Save everything** to a /reports directory

Always explain findings in plain English, not statistical jargon.
```
