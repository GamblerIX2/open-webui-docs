content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()
idx = content.find('Tools are the various')
print('idx:', idx)
if idx >= 0:
    snippet = content[idx-5:idx+250]
    print(repr(snippet))

# also check if already translated
idx2 = content.find('如何安装和管理')
print('already translated check:', idx2)
idx3 = content.find('LLM\u80fd\u529b')
print('already translated check2:', idx3)
