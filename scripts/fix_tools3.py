import re
content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()

# Find the exact text to replace using a more flexible approach
old_start = '⚙️ Tools are the various ways'
old_end = 'understand which type you are using.'
idx_start = content.find(old_start)
idx_end = content.find(old_end)
if idx_start >= 0 and idx_end >= 0:
    old = content[idx_start:idx_end+len(old_end)]
    print('FOUND, length:', len(old))
    new = 'Tools 是你扩展 LLM 能力、超越简单文本生成的各种方式。启用后，它们允许你的聊天机器人做惊人的事情——比如搜索网络、抓取数据、生成图像、使用 AI 语音回应等。\n\n由于在 Open WebUI 中有几种集成"Tools"的方式，了解你使用的是哪种类型非常重要。'
    content = content.replace(old, new, 1)
    print('REPLACED')
else:
    print('NOT FOUND', idx_start, idx_end)

# Handle "How to Install" section
old2_start = '## How to Install & Manage Workspace Tools'
old2_end = ':::warning Safety Tip\nNever import a Tool you don'
idx2 = content.find(old2_start)
if idx2 >= 0:
    end_marker = 'as the ability to run arbitrary code on the server.\n:::'
    idx2_end = content.find(end_marker)
    if idx2_end >= 0:
        old2 = content[idx2:idx2_end+len(end_marker)]
        new2 = ('## 如何安装和管理 Workspace Tools\n\n'
                '📦 Workspace Tools 是用社区功能扩展实例最常见的方式。\n\n'
                '1. 前往[社区工具库](https://openwebui.com/search)\n'
                '2. 选择一个 Tool，然后点击 **Get** 按钮。\n'
                '3. 输入你的 Open WebUI 实例 URL（如 `http://localhost:3000`）。\n'
                '4. 点击 **Import to WebUI**。\n\n'
                ':::warning 安全提示\n'
                '切勿导入你不认识或不信任的 Tool。这些是 Python 脚本，可能在你的主机系统上运行不安全代码。**至关重要的是，只向受信任的用户授予"Tool"权限**，'
                '因为创建或导入工具的能力等同于在服务器上运行任意代码的能力。\n:::'
               )
        content = content.replace(old2, new2, 1)
        print('REPLACED How to Install section')
    else:
        print('Could not find end of How to Install section')
else:
    print('ALREADY TRANSLATED: How to Install')

# Handle "How to Use Tools in Chat"
old3_start = "## How to Use Tools in Chat"
idx3 = content.find(old3_start)
if idx3 >= 0:
    old3_end = 'is the recommended way to let the model auto-select tools.'
    idx3_end = content.find(old3_end)
    if idx3_end >= 0:
        old3 = content[idx3:idx3_end+len(old3_end)]
        print('USE TOOLS snippet:', repr(old3[:100]))
        # Make replacement
        new3 = ('## 如何在对话中使用 Tools\n\n'
                '🔧 安装或连接后，以下是为对话启用它们的方法：\n\n'
                '### 选项 1：即时启用（特定对话）\n'
                '聊天时，点击输入区域中的 **➕（加号）** 图标。你将看到可用 Tools 列表——你可以专门为该会话启用它们。\n\n'
                '### 选项 2：默认启用（全局/模型级别）\n'
                '1. 前往 **Workspace ➡️ 模型**。\n'
                '2. 选择你使用的模型并点击 ✏️ 编辑图标。\n'
                '3. 滚动到 **Tools** 部分。\n'
                '4. ✅ 勾选你希望此模型默认始终访问的 Tools。\n'
                '5. 点击**保存**。\n\n'
                '对于支持的模型，**原生工具调用模式**（见下方[工具调用模式](#tool-calling-modes-default-vs-native)）让模型自己决定每轮调用哪些附加工具。这取代了旧的基于提示注入的"auto-tool"过滤方法，是让模型自动选择工具的推荐方式。'
               )
        content = content.replace(old3, new3, 1)
        print('REPLACED How to Use Tools section')
    else:
        print('Could not find end of How to Use section')
else:
    print('ALREADY TRANSLATED: How to Use Tools')

open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', 'w', encoding='utf-8', newline='').write(content)
print('Saved')
