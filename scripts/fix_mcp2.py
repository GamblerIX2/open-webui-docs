content = open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', encoding='utf-8').read()

old = ('### "Failed to connect to MCP server"\n\n'
       '**Symptom**: \n'
       'The chat shows "Failed to connect to MCP server" when using a tool, even if the **Verify Connection** button in settings says "Connected".\n\n'
       '**Solutions**:\n'
       "1.  **Check Authentication**: Ensure you haven't selected `Bearer` without a key. Switch to `None` if no token is needed.\n"
       '2.  **Filter List Bug**: If the "Function Name Filter List" is empty, try adding a comma (`,`) to it.\n'
       "3.  **OAuth 2.1 Default Tool**: If the failing tool uses OAuth 2.1 and is set as a default tool on the model, this is a known limitation. Remove it from the model's default tools and have users enable it manually per-chat.")

new = ('### "Failed to connect to MCP server"\n\n'
       '**现象**：\n'
       '使用工具时对话显示 "Failed to connect to MCP server"，即使设置中的**验证连接**按钮显示"已连接"。\n\n'
       '**解决方案**：\n'
       '1.  **检查身份验证**：确保没有在没有密钥的情况下选择 `Bearer`。如果不需要令牌，切换到 `None`。\n'
       '2.  **过滤列表 Bug**：如果"函数名称过滤列表"为空，尝试向其添加逗号（`,`）。\n'
       '3.  **OAuth 2.1 默认工具**：如果失败的工具使用 OAuth 2.1 并被设置为模型的默认工具，这是已知限制。从模型的默认工具中删除它，让用户每次对话手动启用。')

if old in content:
    content = content.replace(old, new, 1)
    open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', 'w', encoding='utf-8', newline='').write(content)
    print('OK')
else:
    print('NOT FOUND')
    # Debug: check char by char
    for i, (a, b) in enumerate(zip(old, content[3744:3744+len(old)])):
        if a != b:
            print(f'Diff at {i}: expected {repr(a)} got {repr(b)}')
            break
