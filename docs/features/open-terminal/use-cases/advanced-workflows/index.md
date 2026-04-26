---
sidebar_position: 0
title: "高级工作流"
---

# 使用技能的高级工作流

这些工作流将多种 Open Terminal 能力组合成强大的多步骤流水线。每个工作流都包含一个**技能（Skill）**——你在 Open WebUI 中创建的可复用指令集，它告诉 AI 如何处理特定类型的任务。

---

## 什么是技能？

**技能**是一组你保存在 Open WebUI 中的可复用 Markdown 指令。当你调用某个技能时，其指令会注入到该对话的 AI 系统提示中，使 AI 成为该特定任务的专家。

就像在让人做某件工作前给他一份详细的 SOP（标准操作流程）——只是 AI 可以在不同对话中始终如一地参考这份流程。

### 创建技能

1. 点击左侧边栏的**工作区**
2. 点击**技能**
3. 点击**创建**（+ 按钮）
4. 填写**名称**（例如"数据报告生成器"）和**描述**
5. 在**内容区域**用 Markdown 编写指令
6. 点击**保存并创建**

![Open WebUI 模型能力页面](/images/open-terminal-model-capabilities.png)

:::tip Frontmatter 快捷方式
如果技能指令以 YAML frontmatter 开头，名称和描述字段会自动填充：

```markdown
---
name: data-report-generator
description: Analyzes data files and creates professional PDF reports
---

## Instructions
When asked to analyze data:
1. First, read the file...
```
:::

### 使用技能

有两种方式使用技能：

**方式 1：在聊天中提及（`$`）**

在聊天输入框中输入 `$`，然后按名称搜索你的技能。选择后，AI 会在该对话中接收**完整指令**。这适合你想明确告诉 AI 现在遵循特定技能的情况。

![AI 使用技能和结构化工作流与数据交互](/images/open-terminal-ai-csv-analysis.png)

**方式 2：附加到模型（自动发现）**

这是更强大的选项。前往**工作区 → 模型 → 编辑**，在**技能**部分勾选相应技能。现在 AI 会**在相关时自动发现并使用它**——你完全不需要提及该技能。

幕后工作原理：

1. AI 接收一个清单，列出每个附加技能的**名称和描述**（而非完整指令——那样会浪费上下文）
2. 当你的请求与某技能描述匹配时，AI **自主调用内置的 `view_skill` 工具**加载完整指令
3. AI 然后按这些指令处理你的请求

这意味着你可以将"数据报告生成器"技能附加到你的模型上，每次你上传 CSV 并说"分析这个"时，AI 都会自动加载并按报告指令操作——无需你记住这个技能的存在。

![模型能力设置页面](/images/open-terminal-model-capabilities.png)

:::tip 附加多个技能打造瑞士军刀型模型
将多个技能附加到单个模型，使其成为多用途专家。上传电子表格 → 加载数据分析技能。说"调研电动汽车电池" → 加载研究技能。构建着陆页 → 加载 Web 开发技能。全部自动完成。
:::

### 分享技能

技能有访问控制。你可以：
- 保持**私有**（仅自己可用）
- 与**特定用户或群组**共享
- 设为**公开**（实例上所有人可用）

在技能编辑器中点击**访问**按钮，配置谁可以使用你的技能。

![AI 集成设置和访问控制](/images/open-terminal-integrations-page.png)

---

## 工作流库

以下每个页面都是一个完整工作流，包含可直接粘贴的技能：

| 工作流 | 功能说明 |
| :--- | :--- |
| **[数据报告](./data-reports)** | 将杂乱的 CSV 转化为带有图表的精美 PDF 报告 |
| **[数据库分析](./database-analysis)** | 连接 PostgreSQL/MySQL/SQLite，运行查询，产出洞察 |
| **[研究助手](./research-assistant)** | 收集网络资料并撰写结构化简报 |
| **[邮件处理](./email-processing)** | 从 .eml 文件中提取待办事项和截止日期 |
| **[文档比较](./document-comparison)** | 对合同或提案的两个版本进行差异对比 |
| **[财务仪表盘](./finance-dashboard)** | 分析银行账单并生成支出图表 |
| **[图像处理](./image-processing)** | 批量调整大小、添加水印和转换图片格式 |
| **[竞争分析](./competitive-analysis)** | 抓取竞争对手定价并建立比较 |
| **[应用构建器](./app-builder)** | 从描述中构建完整的 Web 应用 |
| **[代码审查](./code-review)** | 审查代码变更的安全性、性能和风格问题 |

---

## 编写优质技能的技巧

### 让指令具体
差：「分析数据」
好：「读取文件，统计行数，识别列，检查缺失值，然后按类别计算平均值」

### 对步骤编号
LLM 遵循编号指令比遵循散文段落更可靠。

### 包含输出预期
告诉技能最终交付物应该是什么样：「创建一个包含封面和 3 个部分的 PDF」比「做一份报告」更好。

### 测试并迭代
创建技能，在真实任务上试用，并根据 AI 做对做错的地方完善指令。

### 与 Open Terminal 能力结合
真正的力量来自于将技能与 Open Terminal 的工具结合：文件读取、代码执行、网页预览和文件浏览器。指令中写「读取电子表格，用 Python 生成图表，并保存为 PNG」可以充分发挥所有这些功能。

These workflows combine multiple Open Terminal capabilities into powerful multi-step pipelines. Each one includes a **Skill** — a reusable set of instructions you create in Open WebUI that tells the AI exactly how to approach a specific type of task.

---

## What are Skills?

A **Skill** is a reusable set of markdown instructions that you save in Open WebUI. When you invoke a skill, its instructions are injected into the AI's system prompt for that conversation, making the AI an expert at that specific task.

Think of it like giving someone a detailed SOP (standard operating procedure) before asking them to do a job — except the AI can reference it consistently across conversations.

### Creating a Skill

1. Go to **Workspace** in the left sidebar
2. Click **Skills**
3. Click **Create** (+ button)
4. Give it a **name** (e.g., "Data Report Generator") and a **description**
5. Write the instructions in markdown in the **content area**
6. Click **Save & Create**

![Open WebUI model capabilities page](/images/open-terminal-model-capabilities.png)

:::tip Frontmatter shortcut
If your skill instructions start with YAML frontmatter, the name and description fields auto-populate:

```markdown
---
name: data-report-generator
description: Analyzes data files and creates professional PDF reports
---

## Instructions
When asked to analyze data:
1. First, read the file...
```
:::

### Using a Skill

There are two ways to use a skill:

**Option 1: Mention it in chat (`$`)**

Type `$` in the chat input, then search for your skill by name. Select it, and the AI receives the **full instructions** for that conversation. This is best when you want to explicitly tell the AI to follow a specific skill right now.

![AI interacting with data using skills and structured workflows](/images/open-terminal-ai-csv-analysis.png)

**Option 2: Attach it to a Model (auto-discovery)**

This is the more powerful option. Go to **Workspace → Models → Edit** and check the skill under the **Skills** section. Now the AI **automatically discovers and uses it when relevant** — you don't need to mention the skill at all.

Here's how it works behind the scenes:

1. The AI receives a manifest listing each attached skill's **name and description** (not the full instructions — that would waste context)
2. When your request matches a skill's description, the AI **autonomously calls a built-in `view_skill` tool** to load the full instructions
3. The AI then follows those instructions to handle your request

This means you can attach a "Data Report Generator" skill to your model, and any time you drop a CSV and say "analyze this," the AI will automatically load and follow the reporting instructions — without you needing to remember the skill exists.

![Model capabilities settings page](/images/open-terminal-model-capabilities.png)

:::tip Attach multiple skills for a Swiss-army-knife model
Attach several skills to a single model and it becomes a multi-purpose expert. Drop a spreadsheet → it loads the data analysis skill. Ask "research EV batteries" → it loads the research skill. Build a landing page → it loads the web dev skill. All automatically.
:::

### Sharing Skills

Skills have access controls. You can:
- Keep them **private** (only you can use them)
- Share with **specific users or groups**
- Make them **public** (available to everyone on your instance)

Click the **Access** button in the skill editor to configure who can use your skill.

![AI integration settings and access controls](/images/open-terminal-integrations-page.png)

---

## Workflow Library

Each page below is a complete workflow with a copy-pasteable skill:

| Workflow | What it does |
| :--- | :--- |
| **[Data Reports](./data-reports)** | Turn messy CSVs into polished PDF reports with charts |
| **[Database Analysis](./database-analysis)** | Connect to PostgreSQL/MySQL/SQLite, run queries, produce insights |
| **[Research Assistant](./research-assistant)** | Gather web sources and write structured briefings |
| **[Email Processing](./email-processing)** | Extract action items and deadlines from .eml files |
| **[Document Comparison](./document-comparison)** | Diff two versions of a contract or proposal |
| **[Finance Dashboard](./finance-dashboard)** | Analyze bank statements and chart spending |
| **[Image Processing](./image-processing)** | Batch resize, watermark, and convert images |
| **[Competitive Analysis](./competitive-analysis)** | Scrape competitor pricing and build comparisons |
| **[App Builder](./app-builder)** | Build a complete web app from a description |
| **[Code Review](./code-review)** | Review code changes for security, performance, and style issues |

---

## Tips for Writing Great Skills

### Keep instructions specific
Bad: "Analyze the data"
Good: "Read the file, count rows, identify columns, check for missing values, then compute averages per category"

### Number your steps
LLMs follow numbered instructions more reliably than prose paragraphs.

### Include output expectations
Tell the skill what the final deliverable should look like: "Create a PDF with a title page and 3 sections" is better than "make a report."

### Test and iterate
Create the skill, try it on a real task, and refine the instructions based on what the AI gets right or wrong.

### Combine with Open Terminal capabilities
The real power comes from combining skills with Open Terminal's tools: file reading, code execution, web preview, and the file browser. A skill that says "read the spreadsheet, generate a chart with Python, and save it as a PNG" leverages all of these.
