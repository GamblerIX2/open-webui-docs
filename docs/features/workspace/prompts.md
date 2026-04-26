---
sidebar_position: 3
title: "提示词"
---

# 📝 提示词

**可复用的斜杠命令，将复杂指令转变为一键表单。**

提示词让您将常用指令保存为斜杠命令。在任何对话中输入 `/summarize`，完整提示词立即触发。添加自定义输入变量，用户在发送提示词前会看到一个弹出表单，包含下拉菜单、日期选择器和文本字段。无需记住确切的措辞或结构。

每次更改都通过完整的版本历史记录跟踪。回滚到之前的版本、比较更改，并通过访问控制与团队共享提示词。

---

## 为什么使用提示词？

### 停止重复输入相同的指令

保存一次提示词，用 `/command` 使用它。Bug 报告模板、会议记录、代码审查、内容简报：任何您输入超过两次的内容都应该成为提示词。

### 将提示词转变为交互式表单

添加类型化输入变量（下拉菜单、日期选择器、数字字段、复选框），用户会看到一个清晰的表单而不是编辑原始文本。非技术用户无需理解语法就能运行复杂的提示词。

### 带回滚的版本历史

每次更改都创建一个新版本。并排比较版本、将之前的版本恢复为生产版本、跟踪谁做了什么更改。

### 受控共享

与特定用户或用户组共享提示词。公开提示词出现在所有人的 `/` 建议中。私有提示词留在您自己的工作区中。

---

## 主要功能

| | |
| :--- | :--- |
| ⚡ **斜杠命令** | 输入 `/command` 插入完整提示词 |
| 📋 **输入变量表单** | 类型化字段（文本、下拉菜单、日期、数字、复选框等）生成弹出表单 |
| 🕑 **版本历史** | 带提交信息的完整变更跟踪、回滚和生产版本固定 |
| 🔄 **系统变量** | `{{CURRENT_DATE}}`、`{{USER_NAME}}`、`{{CLIPBOARD}}` 在运行时自动替换 |
| 🔒 **访问控制** | 与特定用户、用户组共享或设为公开 |
| 🔀 **启用/禁用切换** | 无需删除即可停用提示词 |
| 🏷️ **标签** | 组织和过滤您的提示词库 |

---

## 创建提示词

导航到**工作区 > 提示词**，点击 **+ 新建提示词**。

| 字段 | 说明 |
| :--- | :--- |
| **名称** | 用于标识的描述性标题 |
| **标签** | 用于过滤的分类 |
| **访问权限** | 控制谁可以查看和使用该提示词 |
| **命令** | 斜杠命令触发器（例如 `/summarize`） |
| **提示词内容** | 发送给模型的实际文本，包含变量 |
| **提交信息** | 可选的版本跟踪变更描述 |

使用清晰的变量名（`{{your_name}}` 而非 `{{var1}}`），添加描述性的 `placeholder` 文本，在合理的地方提供 `default` 值，只将真正必要的字段标记为 `:required`。公开提示词出现在每个用户的 `/` 建议中，因此应谨慎选择公开内容。使用启用/禁用切换将不活跃的提示词从建议中隐藏。

---

## 变量

### 系统变量

在运行时自动替换为对应的值：

| 变量 | 说明 |
| :--- | :--- |
| `{{CLIPBOARD}}` | 剪贴板中的内容（需要剪贴板权限） |
| `{{CURRENT_DATE}}` | 当前日期 |
| `{{CURRENT_DATETIME}}` | 当前日期和时间 |
| `{{CURRENT_TIME}}` | 当前时间 |
| `{{CURRENT_TIMEZONE}}` | 当前时区 |
| `{{CURRENT_WEEKDAY}}` | 当前星期几 |
| `{{USER_NAME}}` | 您的显示名称 |
| `{{USER_EMAIL}}` | 您的邮箱地址 |
| `{{USER_BIO}}` | 设置 > 账户 > 用户资料中的个人简介（未设置则不替换） |
| `{{USER_GENDER}}` | 设置 > 账户 > 用户资料中的性别（未设置则不替换） |
| `{{USER_BIRTH_DATE}}` | 设置 > 账户 > 用户资料中的出生日期（未设置则不替换） |
| `{{USER_AGE}}` | 根据出生日期计算的年龄（未设置则不替换） |
| `{{USER_LANGUAGE}}` | 您选择的语言 |
| `{{USER_LOCATION}}` | 您的位置（需要 HTTPS + 设置 > 界面开关） |

### 自定义输入变量

在提示词内容中添加变量，用户使用斜杠命令时会看到弹出表单。

**简单输入**创建单行文本字段：
```
{{variable_name}}
```

**类型化输入**创建具有配置属性的特定字段类型：
```
{{variable_name | type:property="value"}}
```

所有自定义变量**默认为可选**。添加 `:required` 使字段为必填：
```
{{title | text:required}}
{{notes | textarea:placeholder="附加上下文（可选）"}}
```

### 可用输入类型

| 类型 | 说明 | 示例 |
| :--- | :--- | :--- |
| **text** | 单行文本（默认） | `{{name \| text:placeholder="输入名称":required}}` |
| **textarea** | 多行文本 | `{{description \| textarea:required}}` |
| **select** | 下拉菜单 | `{{priority \| select:options=["高","中","低"]:required}}` |
| **number** | 数字输入 | `{{count \| number:min=1:max=100:default=5}}` |
| **checkbox** | 布尔开关 | `{{include_details \| checkbox:label="包含分析"}}` |
| **date** | 日期选择器 | `{{start_date \| date:required}}` |
| **datetime-local** | 日期和时间选择器 | `{{appointment \| datetime-local}}` |
| **color** | 颜色选择器 | `{{brand_color \| color:default="#FFFFFF"}}` |
| **email** | 带验证的邮箱字段 | `{{email \| email:required}}` |
| **range** | 滑块 | `{{rating \| range:min=1:max=10}}` |
| **tel** | 电话号码 | `{{phone \| tel}}` |
| **time** | 时间选择器 | `{{meeting_time \| time}}` |
| **url** | 带验证的 URL | `{{website \| url:required}}` |
| **month** | 月份和年份（仅 Chrome/Edge，Firefox/Safari 降级为文本） | `{{billing_month \| month}}` |
| **map** | 用于坐标的交互式地图（实验性） | `{{location \| map}}` |

---

## 消息和提示词修饰符

这些修饰符对任务模型提示词特别有用（标题生成、标签生成、后续建议），其中对话包含粘贴的文档或代码等长消息。

### 提示词截断

`{{prompt}}` 变量支持基于字符的截断：

| 修饰符 | 功能 |
| :--- | :--- |
| `{{prompt:start:N}}` | 前 N 个字符 |
| `{{prompt:end:N}}` | 后 N 个字符 |
| `{{prompt:middletruncate:N}}` | 前半部分 + 后半部分，共 N 个字符 |

### 消息选择器与管道过滤器

`{{MESSAGES}}` 变量有两种不同的修饰符类型，在不同层面工作：

**消息选择器**（冒号 `:`）控制**包含多少条消息**：

| 选择器 | 功能 | 示例 |
| :--- | :--- | :--- |
| `START:N` | 前 N 条消息 | `{{MESSAGES:START:5}}` |
| `END:N` | 后 N 条消息 | `{{MESSAGES:END:5}}` |
| `MIDDLETRUNCATE:N` | 前 N/2 + 后 N/2 条消息 | `{{MESSAGES:MIDDLETRUNCATE:6}}` |

有 20 条消息时，`{{MESSAGES:MIDDLETRUNCATE:6}}` 保留消息 1-3 和 18-20，跳过中间的 14 条。

**管道过滤器**（管道 `|`）将**每条消息的内容**截断到字符限制：

| 过滤器 | 功能 | 示例 |
| :--- | :--- | :--- |
| `\|start:N` | 每条消息的前 N 个字符 | `\{\{MESSAGES\|start:300\}\}` |
| `\|end:N` | 每条消息的后 N 个字符 | `\{\{MESSAGES\|end:300\}\}` |
| `\|middletruncate:N` | 每条消息的前半 + 后半部分 | `\{\{MESSAGES\|middletruncate:500\}\}` |

**两者结合**，控制包含哪些消息及每条消息的长度：

| 语法 | 功能 |
| :--- | :--- |
| `\{\{MESSAGES:END:2\|middletruncate:500\}\}` | 最后 2 条消息，每条最多 500 字符 |
| `\{\{MESSAGES:START:5\|start:200\}\}` | 前 5 条消息，每条最多 200 字符 |
| `\{\{MESSAGES:MIDDLETRUNCATE:10\|middletruncate:50\}\}` | 前 5 + 后 5 条消息，每条最多 50 字符 |

:::warning 选择器计数消息而非字符
`{{MESSAGES:MIDDLETRUNCATE:500}}` 选择 **500 条消息**。要限制每条消息的字符数，请使用管道过滤器：`\{\{MESSAGES\|middletruncate:500\}\}`。没有管道过滤器，一个粘贴的文档可能会占满整个上下文窗口。
:::

---

## 版本历史

每次保存都会创建一个新版本。编辑提示词时，**历史侧边栏**显示所有版本，包括提交信息、作者、时间戳，以及当前生产版本上的"使用中"标识。

**预览**任何版本只需点击它。**设为生产版本**可将其恢复为活跃版本。从菜单**删除**旧版本（当前生产版本不能删除）。

:::note 迁移说明
版本控制更新之前创建的提示词已自动迁移，内容保留为初始"使用中"版本。URL 结构从基于命令改为基于 ID，因此现有书签可能需要更新。从 v0.5.0 起，所有变量默认为可选。
:::

---

## 示例

### Bug 报告生成器（`/bug_report`）

带有必填摘要、优先级下拉菜单和重现步骤的结构化表单，以及可选上下文字段：

```txt
请根据以下信息生成一份 Bug 报告：

**摘要：** {{summary | text:placeholder="问题的简要摘要":required}}
**优先级：** {{priority | select:options=["严重","高","中","低"]:default="中":required}}
**重现步骤：**
{{steps | textarea:placeholder="1. 进入...\n2. 点击...\n3. 出现错误...":required}}

**附加上下文：** {{additional_context | textarea:placeholder="浏览器版本、操作系统、截图等"}}
**解决方案：** {{workaround | textarea:placeholder="找到的任何临时解决方案"}}

请将以上内容格式化为清晰完整的 Bug 报告文档。
```

### 会议记录（`/meeting_minutes`）

日期和时间选择器、必填参与者和议程、可选决定和行动项：

```txt
# 会议记录

**日期：** {{meeting_date | date:required}}
**时间：** {{meeting_time | time:required}}
**标题：** {{title | text:placeholder="例如：每周团队同步":required}}
**参与者：** {{attendees | text:placeholder="逗号分隔的姓名列表":required}}

## 议程/主要讨论点
{{agenda_items | textarea:placeholder="粘贴议程或列出讨论的主要主题。":required}}

## 做出的决定
{{decisions | textarea:placeholder="关键决定和结果"}}

## 行动项
{{action_items | textarea:placeholder="每项行动的负责人和截止日期。"}}

## 下次会议
**日期：** {{next_meeting | date}}
**主题：** {{next_topics | text:placeholder="下次讨论的内容"}}

请将以上内容格式化为清晰专业的会议摘要。
```

### 标题生成（任务模型模板）

使用消息选择器 + 管道过滤器保持上下文小：

```txt
对话历史：
<chat_history>
{{MESSAGES:END:2|middletruncate:500}}
</chat_history>

为这段对话生成一个简短标题。
```

发送最后 2 条消息，每条最多 500 字符。

---

## 局限性

### 斜杠命令命名空间

公开提示词出现在每个用户的 `/` 建议中。过多公开提示词会使菜单杂乱。使用启用/禁用切换将不活跃的提示词从建议中排除。

### 默认为可选

所有自定义输入变量除非标记为 `:required`，否则默认为可选。如果您的提示词依赖某个字段，请明确添加 `:required`。
