content = open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', encoding='utf-8').read()

# Find section
idx = content.find('### \u201cFailed to connect')
if idx < 0:
    idx = content.find('### "Failed to connect')
print('section at:', idx)
print(repr(content[idx:idx+700]))
