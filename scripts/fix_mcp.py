#!/usr/bin/env python3
content = open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', encoding='utf-8').read()

pairs = [
    (
        '*   **None**: Use this for **local MCP servers** or internal networks where no token is required.\n'
        '    *   **\u26a0\ufe0f Important**: Default to "None" unless your server strictly requires a token. Selecting "Bearer" without providing a key sends an empty Authorization header (`Authorization: Bearer`), which causes many servers to reject the connection immediately.\n'
        '*   **Bearer**: Use this **only** if your MCP server requires a specific API token. You **must** populate the "Key" field.\n'
        '*   **OAuth 2.1**: Uses Dynamic Client Registration (DCR). Best when your MCP server supports registering OAuth clients automatically.\n'
        '*   **OAuth 2.1 (Static)**: Uses a pre-created client ID/client secret. Best when your provider does not support DCR, or when your security team requires manually managed credentials.',
        '*   **None**\uff1a\u9002\u7528\u4e8e**\u672c\u5730 MCP \u670d\u52a1\u5668**\u6216\u4e0d\u9700\u8981\u4ee4\u724c\u7684\u5185\u7f51\u3002\n'
        '    *   **\u26a0\ufe0f \u91cd\u8981**\uff1a\u9664\u975e\u670d\u52a1\u5668\u4e25\u683c\u8981\u6c42\u4ee4\u724c\uff0c\u5426\u5219\u9ed8\u8ba4\u9009\u62e9 "None"\u3002\u5728\u672a\u63d0\u4f9b\u5bc6\u9470\u7684\u60c5\u51b5\u4e0b\u9009\u62e9 "Bearer" \u4f1a\u53d1\u9001\u7a7a\u7684 Authorization \u6807\u5934\uff08`Authorization: Bearer`\uff09\uff0c\u5bfc\u81f4\u8bb8\u591a\u670d\u52a1\u5668\u7acb\u5373\u62d2\u7edd\u8fde\u63a5\u3002\n'
        '*   **Bearer**\uff1a**\u4ec5**\u5728\u4f60\u7684 MCP \u670d\u52a1\u5668\u9700\u8981\u7279\u5b9a API \u4ee4\u724c\u65f6\u4f7f\u7528\u3002**\u5fc5\u987b**\u586b\u5199 "Key" \u5b57\u6bb5\u3002\n'
        '*   **OAuth 2.1**\uff1a\u4f7f\u7528\u52a8\u6001\u5ba2\u6237\u7aef\u6ce8\u518c\uff08DCR\uff09\u3002\u6700\u9002\u5408\u4f60\u7684 MCP \u670d\u52a1\u5668\u652f\u6301\u81ea\u52a8\u6ce8\u518c OAuth \u5ba2\u6237\u7aef\u7684\u60c5\u51b5\u3002\n'
        '*   **OAuth 2.1\uff08\u9759\u6001\uff09**\uff1a\u4f7f\u7528\u9884\u5148\u521b\u5efa\u7684\u5ba2\u6237\u7aef ID/\u5ba2\u6237\u7aef\u5bc6\u9470\u3002\u6700\u9002\u5408\u4f60\u7684\u63d0\u4f9b\u5546\u4e0d\u652f\u6301 DCR\uff0c\u6216\u4f60\u7684\u5b89\u5168\u56e2\u961f\u8981\u6c42\u624b\u52a8\u7ba1\u7406\u51ed\u636e\u7684\u60c5\u51b5\u3002'
    ),
    (
        '### Connection URLs\n\nIf you are running Open WebUI in **Docker** and your MCP server is on the **host machine**:\n'
        '*   Use `http://host.docker.internal:<port>` (e.g., `http://host.docker.internal:3000/sse`) instead of `localhost`.',
        '### \u8fde\u63a5 URL\n\n\u5982\u679c\u4f60\u5728 **Docker** \u4e2d\u8fd0\u884c Open WebUI\uff0c\u800c MCP \u670d\u52a1\u5668\u5728**\u5bbf\u4e3b\u673a**\u4e0a\uff1a\n'
        '*   \u4f7f\u7528 `http://host.docker.internal:<port>`\uff08\u5982 `http://host.docker.internal:3000/sse`\uff09\u800c\u4e0d\u662f `localhost`\u3002'
    ),
    (
        '### Function Name Filter List\n\nThis field restricts which tools are exposed to the LLM.\n'
        '*   **Default**: Leave empty to expose all tools (in most cases).\n'
        '*   **Workaround**: If you encounter connection errors with an empty list, try adding a single comma (`,`) to this field. This forces the system to treat it as a valid (but empty) filter, potentially bypassing some parsing issues.',
        '### \u51fd\u6570\u540d\u79f0\u8fc7\u6ee4\u5217\u8868\n\n\u6b64\u5b57\u6bb5\u9650\u5236\u54ea\u4e9b\u5de5\u5177\u66b4\u9732\u7ed9 LLM\u3002\n'
        '*   **\u9ed8\u8ba4**\uff1a\u5927\u591a\u6570\u60c5\u51b5\u4e0b\u7559\u7a7a\u4ee5\u66b4\u9732\u6240\u6709\u5de5\u5177\u3002\n'
        '*   **\u89e3\u51b3\u65b9\u6cd5**\uff1a\u5982\u679c\u5217\u8868\u4e3a\u7a7a\u65f6\u9047\u5230\u8fde\u63a5\u9519\u8bef\uff0c\u5c1d\u8bd5\u5728\u6b64\u5b57\u6bb5\u6dfb\u52a0\u4e00\u4e2a\u9017\u53f7\uff08`,`\uff09\u3002\u8fd9\u4f1a\u5f3a\u5236\u7cfb\u7edf\u5c06\u5176\u89c6\u4e3a\u6709\u6548\uff08\u4f46\u4e3a\u7a7a\uff09\u7684\u8fc7\u6ee4\u5668\uff0c\u53ef\u80fd\u7ed5\u8fc7\u67d0\u4e9b\u89e3\u6790\u95ee\u9898\u3002'
    ),
    (
        '### "Failed to connect to MCP server"\n\n**Symptom**: \nThe chat shows "Failed to connect to MCP server" when using a tool, even if the **Verify Connection** button in settings says "Connected".\n\n**Solutions**:\n'
        '1.  **Check Authentication**: Ensure you haven\u2019t selected `Bearer` without a key. Switch to `None` if no token is needed.\n'
        '2.  **Filter List Bug**: If the "Function Name Filter List" is empty, try adding a comma (`,`) to it.\n'
        '3.  **OAuth 2.1 Default Tool**: If the failing tool uses OAuth 2.1 and is set as a default tool on the model, this is a known limitation. Remove it from the model\u2019s default tools and have users enable it manually per-chat.',
        '### "Failed to connect to MCP server"\n\n**\u73b0\u8c61**\uff1a\n\u4f7f\u7528\u5de5\u5177\u65f6\u5bf9\u8bdd\u663e\u793a\u201cFailed to connect to MCP server\u201d\uff0c\u5373\u4f7f\u8bbe\u7f6e\u4e2d\u7684**\u9a8c\u8bc1\u8fde\u63a5**\u6309\u9215\u663e\u793a\u201c\u5df2\u8fde\u63a5\u201d\u3002\n\n**\u89e3\u51b3\u65b9\u6848**\uff1a\n'
        '1.  **\u68c0\u67e5\u8eab\u4efd\u9a8c\u8bc1**\uff1a\u786e\u4fdd\u6ca1\u6709\u5728\u6ca1\u6709\u5bc6\u9470\u7684\u60c5\u51b5\u4e0b\u9009\u62e9 `Bearer`\u3002\u5982\u679c\u4e0d\u9700\u8981\u4ee4\u724c\uff0c\u5207\u6362\u5230 `None`\u3002\n'
        '2.  **\u8fc7\u6ee4\u5217\u8868 Bug**\uff1a\u5982\u679c\u201c\u51fd\u6570\u540d\u79f0\u8fc7\u6ee4\u5217\u8868\u201d\u4e3a\u7a7a\uff0c\u5c1d\u8bd5\u5411\u5176\u6dfb\u52a0\u9017\u53f7\uff08`,`\uff09\u3002\n'
        '3.  **OAuth 2.1 \u9ed8\u8ba4\u5de5\u5177**\uff1a\u5982\u679c\u5931\u8d25\u7684\u5de5\u5177\u4f7f\u7528 OAuth 2.1 \u5e76\u88ab\u8bbe\u7f6e\u4e3a\u6a21\u578b\u7684\u9ed8\u8ba4\u5de5\u5177\uff0c\u8fd9\u662f\u5df2\u77e5\u9650\u5236\u3002\u4ece\u6a21\u578b\u7684\u9ed8\u8ba4\u5de5\u5177\u4e2d\u5220\u9664\u5b83\uff0c\u8ba9\u7528\u6237\u6bcf\u6b21\u5bf9\u8bdd\u624b\u52a8\u542f\u7528\u3002'
    ),
    (
        '### Infinite loading screen after adding External Tool\n\n**Symptom**: \n'
        'After adding an External Tool connection, the frontend gets stuck on a loading spinner. The browser console shows an error like `Cannot convert undefined or null to object at Object.entries`.\n\n'
        '**Cause**: \nYou likely configured an **MCP server** using the **OpenAPI** connection type, or entered MCP-style JSON (containing `mcpServers`) into an OpenAPI connection.\n\n'
        '**Solution**:\n'
        '1.  Open **Admin Settings \u2192 External Tools** (the sidebar still loads)\n'
        '2.  **Disable** or **delete** the problematic tool connection\n'
        '3.  Refresh the page (Ctrl+F5)\n'
        '4.  Re-add the connection with the correct **Type** set to **MCP (Streamable HTTP)**',
        '### \u6dfb\u52a0\u5916\u90e8\u5de5\u5177\u540e\u51fa\u73b0\u65e0\u9650\u52a0\u8f7d\u754c\u9762\n\n**\u73b0\u8c61**\uff1a\n'
        '\u6dfb\u52a0\u5916\u90e8\u5de5\u5177\u8fde\u63a5\u540e\uff0c\u524d\u7aef\u505c\u7559\u5728\u52a0\u8f7d\u65cb\u8f6c\u56fe\u6807\u4e0a\u3002\u6d4f\u89c8\u5668\u63a7\u5236\u53f0\u663e\u793a\u7c7b\u4f3c `Cannot convert undefined or null to object at Object.entries` \u7684\u9519\u8bef\u3002\n\n'
        '**\u539f\u56e0**\uff1a\n\u4f60\u53ef\u80fd\u4f7f\u7528 **OpenAPI** \u8fde\u63a5\u7c7b\u578b\u914d\u7f6e\u4e86 **MCP \u670d\u52a1\u5668**\uff0c\u6216\u8005\u5c06\u5305\u542b `mcpServers` \u7684 MCP \u98ce\u683c JSON \u8f93\u5165\u5230\u4e86 OpenAPI \u8fde\u63a5\u4e2d\u3002\n\n'
        '**\u89e3\u51b3\u65b9\u6848**\uff1a\n'
        '1.  \u6253\u5f00**\u7ba1\u7406\u5458\u8bbe\u7f6e \u2192 \u5916\u90e8\u5de5\u5177**\uff08\u4fa7\u8fb9\u680f\u4ecd\u53ef\u52a0\u8f7d\uff09\n'
        '2.  **\u7981\u7528**\u6216**\u5220\u9664**\u6709\u95ee\u9898\u7684\u5de5\u5177\u8fde\u63a5\n'
        '3.  \u5237\u65b0\u9875\u9762\uff08Ctrl+F5\uff09\n'
        '4.  \u4f7f\u7528\u6b63\u786e\u7684**\u7c7b\u578b**\uff08\u8bbe\u7f6e\u4e3a **MCP\uff08Streamable HTTP\uff09**\uff09\u91cd\u65b0\u6dfb\u52a0\u8fde\u63a5'
    ),
]

changed = False
for old, new in pairs:
    if old in content:
        content = content.replace(old, new, 1)
        changed = True
        print('OK:', old[:50])
    else:
        print('NOT FOUND:', repr(old[:60]))

if changed:
    open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', 'w', encoding='utf-8', newline='').write(content)
    print('mcp.mdx saved')
