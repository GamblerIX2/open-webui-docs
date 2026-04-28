---
sidebar_position: 8
title: "竞争对比"
---

# 🌐 竞争对比分析

抓取竞争对手定价页面并建立对比分析。

> **你：** $Competitive Analyst <br/>
> 检查这 5 个竞争对手网站，将它们的定价方案与我们进行对比。

## AI 的工作流程

1. 获取每个竞争对手的定价页面
2. 解析 HTML 提取方案名称、价格和功能列表
3. 标准化定价（按月/按年）
4. 建立对比电子表格并高亮主要差异
5. 撰写战略观察

<!-- TODO: 截图——文件浏览器中预览 competitor_pricing.csv 的表格：行是功能，列是竞争对手，并带有价格和 ✓/✗ 标记。 -->

<!-- TODO: 截图——摘要：“关键发现：竞争对手 A 有免费套餐，竞争对手 C 的 Pro 方案便宜 30%，但只有我们包含 24/7 支持。” -->

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: competitive-analyst
description: Scrapes competitor websites and builds pricing/feature comparison tables
---

## Competitive Analysis

When analyzing competitors:

1. **Use curl** to fetch pages. Set a user-agent header, handle redirects
2. **Parse HTML** with beautifulsoup4 to extract:
   - Plan names and prices
   - Feature lists
   - Promotional offers (free trials, discounts)
3. **Normalize data**: Convert annual to monthly prices where needed
4. **Create a comparison CSV** with competitors as columns and features as rows
5. **Write strategic observations**: Where are we cheaper/more expensive? What features do competitors have that we don't?
6. **Note the date** (pricing changes frequently)

Present findings as actionable insights, not just raw data.
```
