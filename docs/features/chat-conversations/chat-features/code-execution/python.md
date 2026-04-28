---
sidebar_position: 3
title: "Python 代码执行"
---

# 🐍 Python 代码执行

## 概览

Open WebUI 提供两种执行 Python 代码的方式：

1. **手动代码执行**：对 LLM 生成的 Python 代码块点击 “Run” 按钮，即可在浏览器中运行（基于 Pyodide / WebAssembly）
2. **Code Interpreter**：一种 AI 能力，允许模型在回复过程中自动编写并执行 Python 代码（基于 Pyodide 或 Jupyter）

这两种方式都支持像 matplotlib 图表这样的可视化输出，并可直接在聊天中内联显示。使用 Pyodide 引擎时，还会提供一个位于 `/mnt/uploads/` 的**持久化虚拟文件系统**——文件会在多次代码执行和页面刷新之间保留，并且附加到消息的文件会自动放入其中，供代码直接访问。

## Code Interpreter 能力

Code Interpreter 是一种模型能力，可让 LLM 在对话过程中自主编写并执行 Python 代码。启用后，模型可以：

- 执行计算与数据分析
- 生成可视化内容（图表、曲线、图形）
- 动态处理数据
- 执行多步骤计算任务

### 启用 Code Interpreter

**按模型配置（管理员）：**
1. 前往 **Admin Panel → Models**
2. 选择你要配置的模型
3. 在 **Capabilities** 下启用 **Code Interpreter**
4. 保存更改

**全局配置（Admin Panel）：**

这些设置可以在 **Admin Panel → Settings → Code Execution** 中配置：
- 全局启用 / 禁用 code interpreter
- 选择引擎：**Pyodide**（推荐）或 **Jupyter（旧版）**
- 配置 Jupyter 连接设置
- 设置被禁用模块

**全局配置（环境变量）：**

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_CODE_INTERPRETER` | `true` | 全局启用 / 禁用 code interpreter |
| `CODE_INTERPRETER_ENGINE` | `pyodide` | 使用的引擎：`pyodide`（浏览器，推荐）或 `jupyter`（服务器，旧版） |
| `CODE_INTERPRETER_PROMPT_TEMPLATE` | （内置） | 自定义 code interpreter 提示模板 |
| `CODE_INTERPRETER_BLACKLISTED_MODULES` | `""` | 用逗号分隔的被禁用 Python 模块列表 |

有关 Jupyter 配置，请参阅 [Jupyter Notebook Integration](/tutorials/integrations/dev-tools/jupyter) 教程。

:::note 文件系统提示注入
当选择 Pyodide 引擎时，Open WebUI 会自动在 code interpreter 指令后附加一段与文件系统相关的提示，告知模型 `/mnt/uploads/` 的存在以及如何发现用户上传的文件。使用 Jupyter 时，则不会附加这一段（因为 Jupyter 有自己的文件系统）。因此，你无需在自定义 `CODE_INTERPRETER_PROMPT_TEMPLATE` 中手动加入文件系统说明——系统会自动补上。
:::

### Native Function Calling（Native Mode）

当你在支持的模型上启用 **Native function calling mode**（例如 GPT-5、Claude 4.5、MiniMax M2.5）时，code interpreter 会以一个名为 `execute_code` 的内置工具形式提供。这会带来更自然的集成体验：

- **无需 XML 标签**：模型可以直接调用 `execute_code(code)`
- **图像处理方式相同**：输出中的 base64 图像 URL 会被替换为文件 URL；模型随后通过 markdown 嵌入

**使用要求：**
1. 必须在全局启用 `ENABLE_CODE_INTERPRETER`
2. 模型必须启用 `code_interpreter` capability
3. 模型必须使用 **Native** function calling mode（在模型高级参数中设置）

有关 builtin tools 和 native mode 的详细说明，请参阅 [Tool Development Guide](/features/extensibility/plugin/tools#built-in-system-tools-nativeagentic-mode)。

## 在聊天中内联显示图像（matplotlib 等）

使用 matplotlib 或其他可视化库时，图像可以直接显示在聊天中。要让这一机制正常工作，代码必须将图像输出为 **base64 data URL**。

### 推荐的 matplotlib 模式

```python
import matplotlib.pyplot as plt
import io
import base64

# Create your chart
plt.figure(figsize=(10, 6))
plt.bar(['A', 'B', 'C'], [4, 7, 5])
plt.title('Sample Chart')

# Output as base64 data URL (triggers automatic upload)
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
print(f"data:image/png;base64,{img_base64}")
plt.close()
```

### 图像显示机制

1. 代码执行后，将 `data:image/png;base64,...` 打印到 stdout
2. Open WebUI 的中间层检测到输出中的 base64 图像数据
3. 图像会被自动上传并保存为文件
4. base64 字符串会被**替换为文件 URL**（例如 `/api/v1/files/{id}/content`）
5. 模型会在代码输出中看到这个 URL，并可在回复中引用它
6. 图像最终在聊天中内联渲染

:::info 理解整个流程
模型编写的代码应打印 base64 data URL。Open WebUI 会拦截该输出，并将其转换为永久文件 URL。模型随后应在回复中使用这个**转换后的 URL**，例如以 markdown 形式写成 `![Chart](/api/v1/files/abc123/content)`——而**不是**直接把原始 base64 字符串粘贴到回复文本里。

如果你在聊天回复中看到原始 base64 文本，说明模型错误地回显了 base64，而不是使用代码输出中转换后的 URL。
:::

### 示例提示词

> Create a bar chart showing quarterly sales: Q1: 150, Q2: 230, Q3: 180, Q4: 310.

**期望的模型行为：**
1. 模型使用上面的 base64 模式编写 Python 代码
2. 代码执行并输出 `data:image/png;base64,...`
3. Open WebUI 将其转换为输出中的文件 URL（例如 `![Output Image](/api/v1/files/abc123/content)`）
4. 模型在回复中引用该 URL，从而显示图表

### 常见问题

| Issue | Cause | Solution |
|-------|-------|----------|
| 聊天中出现原始 base64 文本 | 模型在回复文本中直接输出了 base64 | 提示模型仅在代码中打印 base64，不要在回复里重复它 |
| 图像没有显示 | 代码仅用了 `plt.show()`，没有输出 base64 | 改用上面的 base64 模式 |
| “Analyzing...” 一直转圈 | 代码执行超时或出错 | 检查后端日志中的错误 |

## 手动代码执行（Pyodide）

Open WebUI 内置了基于 [Pyodide](https://pyodide.org/)（WebAssembly）的浏览器端 Python 环境。这允许你无需服务端配置，就直接在浏览器里运行 Python 脚本。

Pyodide worker 是**持久化**的——它只会创建一次，并在后续多次代码执行中复用。这意味着，同一会话中执行之间，变量、已导入模块以及写入虚拟文件系统的文件都会被保留。

### 手动运行代码

1. 让 LLM 为你生成 Python 代码
2. 代码块中会出现一个 **Run** 按钮
3. 点击后即可通过 Pyodide 执行
4. 输出会显示在代码块下方

### 支持的库

Pyodide 预装以下包，系统会根据 import 语句自动检测并按需加载：

| Package | Use case |
|---------|----------|
| micropip | 包安装器（内部使用） |
| requests | HTTP 请求 |
| beautifulsoup4 | HTML/XML 解析 |
| numpy | 数值计算 |
| pandas | 数据分析与处理 |
| matplotlib | 图表与绘图 |
| seaborn | 统计数据可视化 |
| scikit-learn | 机器学习 |
| scipy | 科学计算 |
| regex | 高级正则表达式 |
| sympy | 符号数学 |
| tiktoken | LLM token 计数 |
| pytz | 时区处理 |

Python 标准库也完整可用（json、csv、math、datetime、os、io 等）。

:::warning 无法在运行时安装新库
AI **不能安装**上述列表之外的库。任何导入不受支持包的代码都会触发 import error。依赖 C 扩展、系统调用或本地二进制的包（如 torch、tensorflow、opencv、psycopg2）都**不可用**，也无法在 Pyodide 中启用。Pyodide 最适合 **基础文件分析、简单计算、文本处理和图表生成**。如果你需要完整 Python 包访问，请改用 **[Open Terminal](/features/chat-conversations/chat-features/code-execution#open-terminal)**。
:::

## 持久化文件系统

使用 Pyodide 引擎时，会在 `/mnt/uploads/` 挂载一个持久化虚拟文件系统。它由浏览器的 IndexedDB 和 [IDBFS](https://emscripten.org/docs/api_reference/Filesystem-API.html#filesystem-api-idbfs) 提供支持，并具备以下能力：

- **跨执行持久化** —— 一次代码执行写入的文件，在后续执行中仍可访问
- **跨刷新持久化** —— 页面刷新后文件仍然保留（存储在 IndexedDB 中）
- **自动挂载上传文件** —— 附件会在执行前从服务器拉取，并放入 `/mnt/uploads/`，因此模型能直接读取
- **文件浏览器面板** —— 启用 Code Interpreter 后，聊天控制侧边栏中会显示文件浏览器。你可浏览、预览、上传、下载和删除文件，无需终端

### 在代码中操作文件

```python
import os

# List uploaded files
print(os.listdir('/mnt/uploads'))

# Read a user-uploaded CSV
import pandas as pd
df = pd.read_csv('/mnt/uploads/data.csv')
print(df.head())

# Write output to the persistent filesystem (downloadable via file browser)
df.to_csv('/mnt/uploads/result.csv', index=False)
print('Saved result.csv to /mnt/uploads/')
```

:::tip
文件浏览器面板允许你下载模型生成的任意文件。你只需让模型把输出保存到 `/mnt/uploads/`，它就会出现在文件浏览器中供你下载。
:::

:::note Jupyter 引擎
持久化文件系统提示和 `/mnt/uploads/` 集成**仅适用于 Pyodide**。使用 Jupyter 时，文件通过 Jupyter 自身文件系统管理，文件浏览器面板也不会显示。
:::

## 示例：创建一个图表

**提示词：**
> "Create a bar chart with matplotlib showing: Acuity 4.1, Signify 7.2, Hubbell 5.6, Legrand 8.9. Output the chart as a base64 data URL so it displays inline."

**期望代码输出：**
```python
import matplotlib.pyplot as plt
import io
import base64

companies = ['Acuity', 'Signify', 'Hubbell', 'Legrand']
values = [4.1, 7.2, 5.6, 8.9]

plt.figure(figsize=(10, 6))
bars = plt.bar(companies, values, color=['#3498db', '#2ecc71', '#e74c3c', '#9b59b6'])

for bar, value in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
             str(value), ha='center', va='bottom', fontsize=12)

plt.title('Company Values', fontsize=16, fontweight='bold')
plt.xlabel('Company', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.tight_layout()

buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
print(f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}")
plt.close()
```

图像会被自动上传，并直接显示在聊天中。

## 浏览器兼容性

### Microsoft Edge：Pyodide 崩溃

如果基于 Pyodide 的代码执行导致 Microsoft Edge 出现 `STATUS_ACCESS_VIOLATION` 崩溃，这通常是由 Edge 的增强安全模式引起的。

**症状：** 运行 Python 代码时，浏览器标签页甚至整个浏览器直接崩溃，且没有有用的错误提示。

**原因：** Edge 的 “Enhance your security on the web” 设置（位于 `edge://settings/privacy/security`）会启用更严格的安全缓解机制，而这与 Pyodide 这类基于 WebAssembly 的运行时不兼容。

**解决方案：**

1. **关闭 Edge 增强安全模式：**
   - 前往 `edge://settings/privacy/security`
   - 关闭 **"Enhance your security on the web"**

2. **使用其他浏览器：**
   - Chrome 和 Firefox 不存在这个问题

3. **改用 Jupyter 后端：**
   - 将 `CODE_INTERPRETER_ENGINE` 切换为 `jupyter`，完全绕过浏览器端执行

:::note
这是 Edge 增强安全模式与 WebAssembly 之间一个已知兼容性问题。在启用该设置时，官方 [Pyodide console](https://pyodide.org/en/stable/console.html) 也会出现同样崩溃。
:::

## 获得更好结果的小技巧

- **明确说明运行环境**：告诉 LLM 它运行在 “Pyodide environment” 或 “code interpreter” 中，有助于生成更准确代码
- **明确输出形式**：如果想显示图像，请明确要求 “base64 data URL output”
- **使用 print 语句**：结果必须打印出来，才能显示在输出中
- **先检查库支持**：确认你需要的库在 Pyodide 中是否可用

## 延伸阅读

- [Pyodide Documentation](https://pyodide.org/en/stable/)
- [Jupyter Notebook Integration](/tutorials/integrations/dev-tools/jupyter)
- [Environment Configuration](/reference/env-configuration)（搜索 `CODE_INTERPRETER`）
