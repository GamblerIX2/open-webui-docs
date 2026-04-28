---
sidebar_position: 2
title: "数据库分析"
---

# 🗄️ 连接数据库并进行分析

直接连接你的 PostgreSQL、MySQL 或 SQLite 数据库，让 AI 探索数据库结构、运行查询并产出洞察——无需自己编写 SQL。

> **你：** $Database Analyst <br/>
> 连接到 `db.example.com` 的 PostgreSQL 数据库，分析 `orders` 表。本季度我们销售最好的产品是什么？有什么趋势需要特别关注？

## AI 的工作流程

1. 如需安装数据库驱动（`pip install psycopg2-binary` 或 `pymysql`）
2. 使用你的凭据连接数据库
3. 探索数据库结构——列出表、列、关系
4. 编写并运行 SQL 查询回答你的问题
5. 将结果加载到 pandas 进行分析
6. 生成图表（收入趋势、爆款产品、地区分布）
7. 将所有内容保存为报告

<!-- TODO: 截图——聊天界面显示 AI 正在连接 PostgreSQL 数据库、列出表并随后执行查询。结果展示一个格式化表格，包含产品名称、销量和收入。 -->

<!-- TODO: 截图——由数据库查询生成的图表：按收入排名前 10 的产品柱状图、展示月度订单趋势的折线图，以及按地区划分销售额的饼图。 -->

:::tip 安全凭据
通过在启动 Open Terminal 时以环境变量传入数据库凭据，或将其存储在容器中的 `.env` 文件中。切勿在对话中直接粘贴密码——它们会被保存到聊天历史记录中。示例：

```bash
docker run -d --name open-terminal \
  -e DB_HOST=db.example.com \
  -e DB_USER=analyst \
  -e DB_PASS=your-password \
  -e DB_NAME=production \
  ghcr.io/open-webui/open-terminal
```

然后在技能中设置从环境变量读取凭据。
:::

## 支持的数据库

| 数据库 | Python 驱动 | 安装命令 |
| :--- | :--- | :--- |
| PostgreSQL | psycopg2 | `pip install psycopg2-binary` |
| MySQL / MariaDB | pymysql | `pip install pymysql` |
| SQLite | sqlite3 | 内置（无需安装） |
| Microsoft SQL Server | pymssql | `pip install pymssql` |
| MongoDB | pymongo | `pip install pymongo` |

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: database-analyst
description: Connects to SQL databases, explores schemas, runs queries, and creates analysis reports
---

## Database Analysis

When asked to analyze a database:

1. **Connect safely**: Read credentials from environment variables (DB_HOST, DB_USER, DB_PASS, DB_NAME). Never hardcode passwords. Use `psycopg2` for PostgreSQL, `pymysql` for MySQL, `sqlite3` for SQLite
2. **Explore the schema first**:
   - List all tables and their row counts
   - Show column names, types, and sample values for relevant tables
   - Identify primary keys and foreign key relationships
   - Present the schema summary before running analysis queries
3. **Write efficient SQL**:
   - Use appropriate JOINs (not subqueries) where possible
   - Add LIMIT clauses to prevent accidentally pulling millions of rows
   - Use aggregate functions (COUNT, SUM, AVG, GROUP BY) for summaries
   - Always include ORDER BY for readability
4. **Analyze results in Python**:
   - Load query results into a pandas DataFrame
   - Compute additional metrics: growth rates, percentages, rankings
   - Identify trends, anomalies, and notable patterns
5. **Create visualizations**:
   - Use matplotlib with clear labels and consistent styling
   - Time series → line charts
   - Rankings → horizontal bar charts
   - Proportions → pie or donut charts
   - Save each chart as a PNG
6. **Produce a report** with:
   - Schema overview (what tables exist and how they relate)
   - Key findings with supporting data
   - Charts embedded in context
   - The actual SQL queries used (so the user can re-run them)
7. **Close the connection** when done

Always show the SQL query before showing results so the user can verify it's correct.
```
