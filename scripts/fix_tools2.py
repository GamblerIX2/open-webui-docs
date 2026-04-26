content = open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', encoding='utf-8').read()

pairs = [
    (
        "\u2699\ufe0f Tools are the various ways you can extend an LLM's capabilities beyond ssimple text generation. When enabled, they allow your chatbot to do amazing things \u2014 like search the web, scrape data, generate images, talk back using AI voices, and more.\n\nBecause there are several ways to integrate \u201cTools\u201d in Open WebUI, it\u2019s important to understand which type you are using.",
        '\u2699\ufe0f Tools \u662f\u4f60\u6269\u5c55 LLM \u80fd\u529b\u3001\u8d85\u8d8a\u7b80\u5355\u6587\u672c\u751f\u6210\u7684\u5404\u79cd\u65b9\u5f0f\u3002\u542f\u7528\u540e\uff0c\u5b83\u4eec\u5141\u8bb8\u4f60\u7684\u804a\u5929\u673a\u5668\u4eba\u505a\u60ca\u4eba\u7684\u4e8b\u60c5\u2014\u2014\u6bd4\u5982\u641c\u7d22\u7f51\u7edc\u3001\u6293\u53d6\u6570\u636e\u3001\u751f\u6210\u56fe\u50cf\u3001\u4f7f\u7528 AI \u8bed\u97f3\u56de\u5e94\u7b49\u3002\n\n\u7531\u4e8e\u5728 Open WebUI \u4e2d\u6709\u51e0\u79cd\u96c6\u6210\u201cTools\u201d\u7684\u65b9\u5f0f\uff0c\u4e86\u89e3\u4f60\u4f7f\u7528\u7684\u662f\u54ea\u79cd\u7c7b\u578b\u975e\u5e38\u91cd\u8981\u3002'
    ),
]
# Get exact bytes around "How to Install"
idx = content.find('## How to Install')
snippet = content[idx:idx+200]
print(repr(snippet))
idx2 = content.find("## How to Use Tools in Chat")
snippet2 = content[idx2:idx2+200]
print(repr(snippet2))

changed = False
for old, new in pairs:
    if old in content:
        content = content.replace(old, new, 1)
        changed = True
        print('REPLACED')
    else:
        print('NOT FOUND, checking char by char...')
        idx_old = content.find('\u2699\ufe0f Tools are the various')
        if idx_old >= 0:
            file_snippet = content[idx_old:idx_old+len(old)]
            for i, (a, b) in enumerate(zip(old, file_snippet)):
                if a != b:
                    print(f'  Diff at {i}: expected {repr(a)} got {repr(b)}')
                    break

if changed:
    open('d:/Github/open-webui-docs/docs/features/extensibility/plugin/tools/index.mdx', 'w', encoding='utf-8', newline='').write(content)
