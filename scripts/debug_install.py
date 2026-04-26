content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()
idx = content.find('## How to Install')
if idx >= 0:
    print(repr(content[idx:idx+600]))
else:
    # Maybe already translated to Chinese title
    idx2 = content.find('如何安装')
    print('ALREADY TRANSLATED?', idx2)
    if idx2 >= 0:
        print(repr(content[idx2:idx2+200]))
