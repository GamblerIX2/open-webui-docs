---
sidebar_position: 1
title: "代码执行"
---

Open WebUI 直接在聊天界面中提供强大的代码执行能力，让你无需离开平台，就能把想法转化为可执行结果。

## 主要特性

- **代码解释器能力**：允许模型在回复过程中自主编写并执行 Python 代码。通过 Native（Agentic）Mode 下的 `execute_code` 工具运行——这是唯一受支持的工具调用模式。旧版 Default Mode 仍保留基于 XML 的历史集成，但已不再支持；新部署应使用 Native Mode。

- **Python 代码执行**：可在浏览器中通过 Pyodide，或在服务器上通过 Jupyter，直接运行 Python 脚本。支持 pandas、matplotlib 等常用库，几乎无需额外配置。

- **MermaidJS 渲染**：使用 MermaidJS 语法创建并可视化流程图、图表及其他视觉内容，系统会在聊天中自动渲染。

- **交互式 Artifacts**：可在对话中直接生成并交互 HTML 网站、SVG 图形、JavaScript 可视化等富内容。

- **Open Terminal**：将远程 shell 执行 API 作为工具接入，获得完整操作系统级访问——可在隔离 Docker 容器中执行任意命令、安装软件包和管理文件。

这些执行能力连接了“对话”和“实现”之间的鸿沟，让你可以在与 AI 模型聊天时无缝探索思路、分析数据并创建可视内容。

## 如何选择代码执行后端

Open WebUI 支持多种代码执行后端，适用于不同场景。选择哪一种，取决于你是需要轻量的浏览器端执行、完整 Python 环境，还是不受限制的 shell 访问。

### Pyodide（默认）

Pyodide 通过 WebAssembly 在浏览器中运行 Python。它具备沙箱隔离，适合多用户环境，但也存在一些限制：

- **持久化文件存储** —— `/mnt/uploads/` 虚拟文件系统由 IndexedDB（IDBFS）支持；同一会话中多次代码执行之间、甚至页面刷新后，文件仍然保留
- **内置文件浏览器** —— 启用 Code Interpreter 后，聊天控制侧边栏会出现文件浏览器面板。你可以浏览、预览、上传、下载和删除 Pyodide 文件系统中的文件，无需终端
- **用户文件访问** —— 附加到消息的文件会在执行前自动放入 `/mnt/uploads/`，因此模型和你的代码都可以直接读取
- **库支持有限** —— 仅有部分 Python 包可用。依赖 C 扩展或系统调用的库通常无法使用
- **无 shell 访问** —— 不能执行 shell 命令、安装软件包或直接与操作系统交互

:::tip
Pyodide 很适合 **文本分析、哈希计算、图表生成、文件处理** 等自包含任务。像 matplotlib 这样的图表库会输出 base64 编码图像，Open WebUI 会自动捕获它们、上传为文件，并将图像链接注入输出中——因此模型无需额外配置即可直接在聊天中显示图表。
:::

:::warning 仅适合基础分析
Pyodide 通过 WebAssembly 在浏览器内运行 Python。AI **无法安装额外库**，只能使用下方列出的固定小集合；任何导入不受支持包的代码都会失败。执行速度也**明显慢于原生 Python**，大数据集或高 CPU 负载任务可能会触发浏览器内存上限。Pyodide 最适合 **基础文件分析、简单计算、文本处理和图表生成**。若需要更重型的任务，请改用 **Open Terminal**，它能在 Docker 容器中提供原生性能和不受限制的软件包访问。

可用库包括：micropip、requests、beautifulsoup4、numpy、pandas、matplotlib、seaborn、scikit-learn、scipy、regex、sympy、tiktoken、pytz 以及 Python 标准库。**除此之外的库都不能在运行时安装。**
:::

:::note 与 Open Terminal 互斥
Code Interpreter 开关与 Open Terminal 开关不能同时启用。启用其中一个会自动关闭另一个——它们目的相近，但后端不同。
:::

### Jupyter（旧版）

:::caution 旧版引擎
Jupyter 现在被视为**旧版**代码执行引擎。大多数场景推荐使用 Pyodide；若需要完整服务端执行能力，则推荐 Open Terminal。未来版本中，Jupyter 支持可能会被弃用。
:::

Jupyter 提供完整 Python 环境，几乎能处理任何任务——创建文件、安装软件包、使用复杂库等。但在共享部署中，它也有明显缺点：

- **共享环境** —— 所有用户共享同一个 Python 运行时和文件系统
- **默认不隔离** —— 若未仔细配置，用户可能访问系统资源或读取其他用户数据
- **并非为多租户设计** —— Jupyter 最初是为单用户工作流构建的

:::warning
如果你运行的是多用户或组织级部署，**不推荐**使用 Jupyter 作为代码执行后端。Open WebUI 的 Jupyter 集成连接的是一个共享实例，没有按用户隔离。Jupyter 更适合**单用户、开发环境或可信用户环境**。
:::

### Open Terminal {#open-terminal}

[Open Terminal](https://github.com/open-webui/open-terminal) 是一个轻量级 API，用于在 Docker 容器中远程执行 shell 命令。它提供完整的操作系统级访问——任意语言、任意工具、任意 shell 命令——并通过容器实现隔离。

- **完整 shell 访问** —— 模型可安装软件包、运行任意语言脚本、使用 ffmpeg、git、curl 等系统工具
- **容器级隔离** —— 运行在独立 Docker 容器中，与 Open WebUI 和其他服务分离
- **预装丰富工具集** —— 镜像默认包含 Python 3.12、数据科学库、构建工具、网络工具等
- **内置文件浏览器** —— 可直接从聊天控制面板中浏览、预览、创建、删除、上传和下载文件
- **内置多用户模式** —— 单个容器可服务多个用户，并通过 Linux 账号实现按用户隔离（适合小团队，不适合大规模部署）

完整文档请参阅 [Open Terminal 集成指南](/features/open-terminal)。

### Terminals（多租户编排器）

[Terminals](https://github.com/open-webui/terminals) 是一个多租户编排层，可为**每个用户**动态创建并管理独立的 Open Terminal 容器。Open Terminal 是单实例工具，而 Terminals 则是其上层扩展，负责完整生命周期：创建、路由、空闲清理和销毁。它需要 [企业许可证](/enterprise)。

- **每用户一个容器** —— 每个用户都有独立的 Open Terminal 容器，拥有自己的文件系统、进程和资源；用户之间不共享 kernel 或进程空间
- **自动生命周期管理** —— 首次请求时自动创建容器，空闲超时后自动停止，并自动清理
- **支持多种后端** —— Docker（每用户一个容器）、Kubernetes（每用户一个 Pod + PVC + Service）、Kubernetes Operator（基于 CRD）、local（开发用 subprocess）或 static（代理到单一实例）
- **透明路由** —— 所有 Open Terminal API endpoint 都可通过 `/terminals/` 访问；Terminals 会根据 `X-User-Id` 将请求路由到对应用户容器
- **企业就绪** —— 支持使用 PostgreSQL 存储租户状态、对接 Open WebUI 的 JWT 身份验证、审计日志、SIEM webhook 集成和加密 API key 存储
- **管理员面板** —— 内置前端用于管理租户和监控实例

:::warning Alpha 软件
Terminals 仍在积极开发中，尚未准备好用于生产环境。API、配置和功能都可能随时变更。
:::

:::note 许可证
Terminals 使用 [Open WebUI 企业许可证](/enterprise) 授权，而不是 MIT。
:::

### 对比

| 考量项 | Pyodide | Jupyter（旧版） | Open Terminal | Terminals |
| :--- | :--- | :--- | :--- | :--- |
| **运行位置** | 浏览器（WebAssembly） | 服务器（Python kernel） | 服务器（Docker 容器） | 服务器（编排容器） |
| **库支持** | 有限子集 | 完整 Python 生态 | 完整 OS —— 任意语言、任意工具 | 完整 OS —— 任意语言、任意工具 |
| **Shell 访问** | ❌ 无 | ⚠️ 有限 | ✅ 完整 shell | ✅ 完整 shell |
| **文件持久性** | ✅ IDBFS（跨执行与刷新持久） | ✅ 共享文件系统 | ✅ 容器文件系统（直到被移除） | ✅ 每用户持久卷 |
| **文件浏览器** | ✅ 内置侧边栏面板 | ❌ 无 | ✅ 内置侧边栏面板 | ✅ 内置侧边栏面板 |
| **用户文件访问** | ✅ 附件自动放入 `/mnt/uploads/` | ❌ 手动 | ✅ 可直接访问附件文件 | ✅ 可直接访问附件文件 |
| **隔离性** | ✅ 浏览器沙箱 | ❌ 共享环境 | ✅ 容器级隔离（Docker） | ✅ 完整每用户容器隔离 |
| **多用户安全性** | ✅ 天然按用户隔离 | ⚠️ 无隔离 | ℹ️ 内置多用户模式（适合小团队） | ✅ 每用户容器并带生命周期管理 |
| **文件生成** | ✅ 写入 `/mnt/uploads/`，通过文件浏览器下载 | ✅ 完整支持 | ✅ 完整支持上传 / 下载 | ✅ 完整支持上传 / 下载 |
| **设置方式** | 无（内置） | 管理员全局配置 | 通过 “设置 → 集成” 原生集成 | 独立服务 + Docker socket 或 K8s 集群 |
| **组织推荐** | ✅ 安全默认值 | ❌ 无隔离时不推荐 | ℹ️ 适合小团队 | ✅ 为多租户组织设计 |
| **企业级扩展性** | ✅ 客户端运行，无服务器负载 | ❌ 单一共享实例 | ℹ️ 单容器，共享资源 | ✅ 横向扩展（Docker 或 Kubernetes） |
| **空闲管理** | N/A | N/A | N/A（始终运行） | ✅ 可配置超时后自动停止 |
| **许可证** | MIT | MIT | MIT | [Enterprise](/enterprise) |
