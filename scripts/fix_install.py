content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()

old = ('## How to Install & Manage Workspace Tools\n\n'
       '\U0001f4e6 Workspace Tools are the most common way to extend your instance with community features.\n\n'
       '1. Go to [Community Tool Library](https://openwebui.com/search)\n'
       "2. Choose a Tool, then click the **Get** button.\n"
       "3. Enter your Open WebUI instance's URL (e.g. `http://localhost:3000`).\n"
       "4. Click **Import to WebUI**.\n\n"
       ":::warning Safety Tip\n"
       "Never import a Tool you don't recognize or trust. These are Python scripts and might run unsafe code on your host system. **Crucially, ensure you only grant \"Tool\" permissions to trusted users**, as the ability to create or import tools is equivalent to the ability to run arbitrary code on the server.\n"
       ":::")

new = ('## 如何安装和管理 Workspace Tools\n\n'
       '📦 Workspace Tools 是用社区功能扩展实例最常见的方式。\n\n'
       '1. 前往[社区工具库](https://openwebui.com/search)\n'
       '2. 选择一个 Tool，然后点击 **Get** 按钮。\n'
       '3. 输入你的 Open WebUI 实例 URL（如 `http://localhost:3000`）。\n'
       '4. 点击 **Import to WebUI**。\n\n'
       ':::warning 安全提示\n'
       '切勿导入你不认识或不信任的 Tool。这些是 Python 脚本，可能在你的主机系统上运行不安全代码。**至关重要的是，只向受信任的用户授予"Tool"权限**，'
       '因为创建或导入工具的能力等同于在服务器上运行任意代码的能力。\n'
       ':::')

if old in content:
    content = content.replace(old, new, 1)
    print('REPLACED')
else:
    print('NOT FOUND - debugging...')
    idx = content.find('## How to Install')
    if idx >= 0:
        file_seg = content[idx:idx+len(old)]
        for i, (a, b) in enumerate(zip(old, file_seg)):
            if a != b:
                print(f'Diff at {i}: expected {repr(a)} got {repr(b)}')
                break

open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', 'w', encoding='utf-8', newline='').write(content)
print('Saved')
