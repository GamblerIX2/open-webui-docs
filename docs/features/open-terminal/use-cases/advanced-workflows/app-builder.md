---
sidebar_position: 9
title: "应用构建器"
---

# 🏗️ 构建完整应用

描述你想要的，获得一个具有前端、后端和数据库的完整工作应用。

> **你：** $App Builder <br/>
> 帮我做一个库存跟踪器。我需要加入带有名称、数量和价格属性的产品。显示总价値和库存预警。

## AI 的工作流程

1. 设计数据库结构
2. 使用 Flask 构建带有 CRUD 接口的 Python API
3. 创建带有仰表盘、图表和搜索功能的精美前端
4. 填充示例数据
5. 启动服务器并测试每个接口
6. 端口预览展示运行中的应用

{/* TODO: Screenshot — The port preview showing a polished dashboard: summary cards (Total Items: 156, Total Value: $24,350, Low Stock: 3), a bar chart by category, and a searchable product table. */}

{/* TODO: Screenshot — File browser showing the project structure: app.py, database.py, templates/, static/. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: app-builder
description: Builds complete web applications with frontend, backend, and database
---

## Full-Stack Application Builder

When building a web app:

1. **Clarify requirements**: What data is managed? What should the UI show?
2. **Design the database first**: Use SQLite with proper schema
3. **Build the API** with Flask or FastAPI: CRUD, search, filtering, error handling
4. **Build a polished frontend**:
   - Modern CSS (not a skeleton — make it look demo-ready)
   - Dashboard with key metrics and charts (Chart.js)
   - Responsive tables with search
   - Forms for data entry
5. **Seed with realistic sample data** so the demo looks good
6. **Start the server** and test every endpoint with curl
7. **Verify the full flow**: create, read, update, delete, search

Build something polished enough to demo, not a wireframe.
```
