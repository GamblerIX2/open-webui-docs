content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()
idx = content.find('## How to Install')
if idx >= 0:
    print(repr(content[idx:idx+900]))
