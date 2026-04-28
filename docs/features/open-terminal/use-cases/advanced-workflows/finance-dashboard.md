---
sidebar_position: 6
title: "财务仪表盘"
---

# 💰 个人财务仪表盘

上传银行对账单，获得带图表的支出分析报告。

> **你：** $Finance Analyzer <br/>
> *（拖入 3 个 CSV 银行对账单到文件浏览器）* <br/>
> 分析我这 3 个月的支出情况。我的钱主要花在哪里？

## AI 的工作流程

1. 读取所有 CSV 文件并标准化不同格式
2. 对交易分类：食材、餐饮、订阅服务、交通等
3. 识别定期费用并标记异常项目
4. 创建包含月度趋势、类别分布和主要商家的仪表盘
5. 标记异常项目：异常大额费用、新增订阅、可能的重复费用

<!-- TODO: 截图——文件浏览器中预览生成的 spending_dashboard.html：包含支出类别饼图、月度趋势柱状图和主要商家表格。 -->

<!-- TODO: 截图——异常报告：“需要检查的 3 项：2 月 15 日向 'TECHSTORE' 收取 450 美元（异常偏高）、新增每月 14.99 美元的 'StreamPlus' 订阅、3 月 3 日和 5 日可能存在重复的 89.00 美元扣费。” -->

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: finance-analyzer
description: Analyzes bank statements and creates spending reports with charts
---

## Financial Analysis

When analyzing bank statements:

1. **Read all files** and normalize columns (date, description, amount, type). Handle different CSV formats (detect delimiters, date formats, debit/credit conventions)
2. **Categorize transactions** using keyword matching:
   - Groceries: walmart, costco, trader joe, whole foods
   - Dining: restaurant, cafe, doordash, uber eats
   - Subscriptions: netflix, spotify, recurring monthly charges
   - Transport: gas, uber, lyft, parking
   - (Add more categories as needed)
3. **Generate charts**:
   - Monthly spending trend (line chart)
   - Category breakdown (pie chart)
   - Top 10 merchants (bar chart)
4. **Detect anomalies**: charges >2x average for that merchant, new recurring charges, possible duplicates (same amount within 3 days)
5. **Create an HTML dashboard** viewable in the file browser

Use proper currency formatting and round to 2 decimal places.
```
