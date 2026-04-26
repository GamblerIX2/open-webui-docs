content = open('d:/Github/open-webui-docs/docs/features/extensibility/mcp.mdx', encoding='utf-8').read()
idx = content.find('Symptom')
if idx >= 0:
    print(repr(content[idx-30:idx+250]))
else:
    print('Symptom not found')
idx2 = content.find('Troubleshooting')
print(repr(content[idx2:idx2+500]))
