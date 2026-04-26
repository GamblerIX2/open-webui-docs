---
sidebar_position: 2
title: "软件开发"
---

# 软件开发

Open Terminal 让 AI 能够与真实代码库交互——克隆仓库、运行测试、读取错误、安装依赖，并不断迭代修复。

---

## 克隆并探索代码仓库

> **你：** 克隆 https://github.com/user/project 并给我一个代码库概述。架构是什么？入口点在哪里？

AI 会：
1. 运行 `git clone` 拉取仓库
2. 扫描目录结构，读取关键文件（`README`、`package.json`、`pyproject.toml` 等）
3. 识别技术栈、入口点和主要组件
4. 返回包含文件数量、依赖项和架构说明的结构化摘要

![AI 列出项目文件并描述结构](/images/open-terminal-ai-file-listing.png)

---

## 运行测试套件并修复失败

> **你：** 运行测试。如果有任何失败，找出原因并修复它。

AI 会：
1. 检测测试框架（`pytest`、`jest`、`go test` 等）
2. 如需要则安装依赖
3. 运行完整测试套件
4. 读取失败输出，追踪 bug，编辑源码
5. 重新运行失败的测试以确认修复

![AI 运行测试并迭代修复](/images/open-terminal-ai-test-suite.png)

:::tip 迭代调试
AI 看到的终端输出与开发者看到的完全相同——堆栈跟踪、断言错误、日志消息。多轮"运行 → 读取错误 → 修复 → 重新运行"自动进行。
:::

---

## 设置开发环境

> **你：** 设置这个项目，让我可以在上面开发。安装所有依赖、创建数据库并运行开发服务器。

AI 会：
1. 阅读设置文档（`README`、`Makefile`、`docker-compose.yml`）
2. 安装系统软件包和语言依赖
3. 创建配置文件、设置数据库、运行迁移
4. 启动开发服务器并确认正常运行
5. 报告你可以访问的 URL

![AI 安装依赖并运行项目](/images/open-terminal-ai-install-run.png)

---

## 自信地重构

> **你：** 将 `users.py` 中的数据库查询重构为使用 async/await。确保测试仍然通过。

AI 会：
1. 读取当前实现
2. 按你要求的修改重写代码
3. 运行测试套件验证没有破坏任何内容
4. 如果测试失败，调整重构代码直到通过
5. 显示修改内容的 `git diff`

![AI 自动调试和修复代码错误](/images/open-terminal-ai-debug-fix.png)

---

## Git 工作流

> **你：** 显示自上次发布标签以来的变更。总结提交记录。

AI 直接使用 Git 工作：

- `git log`、`git diff`、`git blame` 分析历史
- 创建分支、暂存修改、创建提交
- 从提交历史生成变更日志
- 使用 `git bisect` 查找 bug 引入时间
- 解决合并冲突

![AI 初始化 git 仓库并与 git 交互](/images/open-terminal-ai-git-workflow.png)

---

## 编写和运行测试

> **你：** 为 `orders.py` 中的 `calculate_shipping()` 函数编写单元测试。覆盖边缘情况。

AI 会：
1. 读取函数以理解其逻辑和参数
2. 识别边缘情况（零数量、负值、国际与国内、免运费阈值）
3. 使用项目现有测试框架编写测试用例
4. 运行它们以验证是否通过
5. 如果有失败，判断是测试 bug 还是代码 bug

![AI 使用 pytest 编写和运行单元测试](/images/open-terminal-ai-test-suite.png)

---

## 调试特定问题

> **你：** 用户反映登录接口有时返回 500。这是日志中的错误：`KeyError: 'session_token'`。找出并修复它。

AI 会：
1. 搜索代码库中 `session_token` 的使用位置
2. 读取周围代码理解流程
3. 识别 bug（例如：会话过期时缺少键检查）
4. 编写带有适当错误处理的修复方案
5. 为该边缘情况添加测试用例
6. 运行测试确认修复

![AI 在代码库中找到并修复 bug](/images/open-terminal-ai-debug-fix.png)

---

## 构建并验证 API

> **你：** 创建一个管理书店的 REST API。我需要书籍、作者和分类的 CRUD 功能。使用 FastAPI 和 SQLite。

AI 会：
1. 搭建项目结构
2. 定义数据库模型和模式
3. 实现所有带验证的接口
4. 创建种子数据
5. 启动服务器并用 `curl` 测试每个接口
6. 展示 Swagger 文档页面

![AI 创建并运行 Web 应用程序](/images/open-terminal-ai-web-dev.png)

---

## 支持哪些语言和工具？

Docker 镜像预装了常用开发工具：

| 类别 | 可用工具 |
| :--- | :--- |
| **语言** | Python、Node.js、Ruby、C/C++、Bash |
| **包管理器** | pip、npm、gem、apt |
| **版本控制** | Git |
| **编辑器** | nano、vim |
| **构建工具** | make、gcc、g++ |

AI 可以即时安装额外工具——Rust、Go、Java、Docker CLI、数据库客户端，以及任何可通过 `apt` 或语言专属包管理器获取的内容。

> **You:** Clone https://github.com/user/project and give me an overview of the codebase. What's the architecture? Where are the entry points?

The AI:
1. Runs `git clone` to pull the repo
2. Scans the directory structure, reads key files (`README`, `package.json`, `pyproject.toml`, etc.)
3. Identifies the tech stack, entry points, and major components
4. Returns a structured summary with file counts, dependencies, and architecture notes

![AI listing project files and describing the structure](/images/open-terminal-ai-file-listing.png)

---

## Run the test suite and fix failures

> **You:** Run the tests. If anything fails, figure out why and fix it.

The AI:
1. Detects the test framework (`pytest`, `jest`, `go test`, etc.)
2. Installs dependencies if needed
3. Runs the full test suite
4. Reads failure output, traces the bug, edits the source code
5. Re-runs the failing tests to confirm the fix

![AI running tests and iterating on fixes](/images/open-terminal-ai-test-suite.png)

:::tip Iterative debugging
The AI sees the same terminal output a developer would — stack traces, assertion errors, log messages. Multiple rounds of "run → read error → fix → re-run" happen automatically.
:::

---

## Set up a development environment

> **You:** Set up this project so I can develop on it. Install all dependencies, create the database, and run the dev server.

The AI:
1. Reads setup docs (`README`, `Makefile`, `docker-compose.yml`)
2. Installs system packages and language dependencies
3. Creates config files, sets up databases, runs migrations
4. Starts the dev server and confirms it's working
5. Reports the URL where you can access it

![AI installing dependencies and running a project](/images/open-terminal-ai-install-run.png)

---

## Refactor with confidence

> **You:** Refactor the database queries in `users.py` to use async/await. Make sure the tests still pass.

The AI:
1. Reads the current implementation
2. Rewrites the code with your requested changes
3. Runs the test suite to verify nothing broke
4. If tests fail, adjusts the refactored code until they pass
5. Shows you a `git diff` of what changed

![AI debugging and fixing code errors automatically](/images/open-terminal-ai-debug-fix.png)

---

## Git workflows

> **You:** Show me what changed since the last release tag. Summarize the commits.

The AI works with Git directly:

- `git log`, `git diff`, `git blame` to analyze history
- Create branches, stage changes, make commits
- Generate changelogs from commit history
- Find when a bug was introduced with `git bisect`
- Resolve merge conflicts

![AI initializing a git repo and working with git](/images/open-terminal-ai-git-workflow.png)

---

## Write and run tests

> **You:** Write unit tests for the `calculate_shipping()` function in `orders.py`. Cover edge cases.

The AI:
1. Reads the function to understand its logic and parameters
2. Identifies edge cases (zero quantity, negative values, international vs domestic, free shipping threshold)
3. Writes test cases using the project's existing test framework
4. Runs them to verify they pass
5. If any fail, it determines whether it's a test bug or a code bug

![AI writing and running unit tests with pytest](/images/open-terminal-ai-test-suite.png)

---

## Debug a specific issue

> **You:** Users are reporting that the login endpoint returns 500 sometimes. Here's the error from the logs: `KeyError: 'session_token'`. Find and fix it.

The AI:
1. Searches the codebase for where `session_token` is used
2. Reads the surrounding code to understand the flow
3. Identifies the bug (e.g., missing key check when session expires)
4. Writes the fix with proper error handling
5. Adds a test case for the edge case
6. Runs the tests to confirm

![AI finding and fixing a bug in the codebase](/images/open-terminal-ai-debug-fix.png)

---

## Build and verify an API

> **You:** Create a REST API for managing a bookstore. I need CRUD for books, authors, and categories. Use FastAPI and SQLite.

The AI:
1. Scaffolds the project structure
2. Defines database models and schemas
3. Implements all endpoints with validation
4. Creates seed data
5. Starts the server and tests every endpoint with `curl`
6. Shows you the Swagger docs page

![AI creating and running a web application](/images/open-terminal-ai-web-dev.png)

---

## What languages and tools are available?

The Docker image comes with common development tools pre-installed:

| Category | Tools available |
| :--- | :--- |
| **Languages** | Python, Node.js, Ruby, C/C++, Bash |
| **Package managers** | pip, npm, gem, apt |
| **Version control** | Git |
| **Editors** | nano, vim |
| **Build tools** | make, gcc, g++ |

The AI can install additional tools on the fly — Rust, Go, Java, Docker CLI, database clients, and anything else available via `apt` or language-specific package managers.

## Related

- **[Code execution →](./code-execution)** — quick scripts and one-off tasks
- **[Web development →](./web-development)** — build and preview websites
- **[Advanced workflows →](./advanced-workflows)** — skills for code review, database analysis, and more
