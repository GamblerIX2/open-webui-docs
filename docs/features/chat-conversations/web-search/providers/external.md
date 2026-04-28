---
sidebar_position: 19
title: "外部"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [环境配置文档](/reference/env-configuration#web-search)。

:::

:::tip 故障排查

如果你在 web search 上遇到问题，请查看 [Web Search 故障排查指南](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时、内容为空等常见问题。

:::

## 外部 Web Search API

这个选项允许你把 Open WebUI 连接到你自己托管的 web search API 端点。适用场景包括：

- 集成 Open WebUI 原生未支持的搜索引擎
- 实现自定义搜索逻辑、过滤规则或结果处理流程
- 使用私有或内部搜索索引

### Open WebUI 配置

1. 进入 Open WebUI `管理面板`
2. 打开 `设置` 标签，再进入 `网页搜索`
3. 将 `启用 Web Search` 切换为开启
4. 将 `网页搜索引擎` 从下拉菜单设为 `external`
5. 在 `External Search URL` 中填写你自定义搜索 API 的完整 URL（例如 `http://localhost:8000/search` 或 `https://my-search-api.example.com/api/search`）
6. 在 `External Search API Key` 中填写访问该搜索端点所需的密钥。如果你的端点不需要鉴权，也可以留空（但对于公网端点，不推荐）
7. 点击 `Save`

![Open WebUI 管理面板中的 External Search 配置](/images/tutorial_external_search.png)

### API 规范

Open WebUI 会按如下方式与你的 `External Search URL` 交互：

- **方法：** `POST`
- **请求头：**
  - `Content-Type: application/json`
  - `Authorization: Bearer <YOUR_EXTERNAL_SEARCH_API_KEY>`
- **请求体（JSON）：**

    ```json
    {
      "query": "The user's search query string",
      "count": 5 // The maximum number of search results requested
    }
    ```

  - `query`（string）：用户输入的搜索关键词
  - `count`（integer）：Open WebUI 希望获取的最大结果数。必要时，你的 API 也可以返回更少结果

- **期望的响应体（JSON）：**
    你的 API 端点 **必须**返回一个 JSON 数组，其中每个元素都是搜索结果对象，结构如下：

    ```json
    [
      {
        "link": "URL of the search result",
        "title": "Title of the search result page",
        "snippet": "A brief description or snippet from the search result page"
      },
      {
        "link": "...",
        "title": "...",
        "snippet": "..."
      }
      // ... potentially more results up to the requested count
    ]
    ```

  - `link`（string）：搜索结果的直接 URL
  - `title`（string）：网页标题
  - `snippet`（string）：页面内容中与查询相关的简要描述

    如果发生错误，或未找到结果，建议你的端点返回空数组 `[]`

### 示例实现（Python/FastAPI）

以下示例演示如何使用 Python + FastAPI + `duckduckgo-search` 库实现一个自托管搜索 API。

```python
import uvicorn
from fastapi import FastAPI, Header, Body, HTTPException
from pydantic import BaseModel
from duckduckgo_search import DDGS

EXPECTED_BEARER_TOKEN = "your_secret_token_here"

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    count: int

class SearchResult(BaseModel):
    link: str
    title: str | None
    snippet: str | None

@app.post("/search")
async def external_search(
    search_request: SearchRequest = Body(...),
    authorization: str | None = Header(None),
):
    expected_auth_header = f"Bearer {EXPECTED_BEARER_TOKEN}"
    if authorization != expected_auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    query, count = search_request.query, search_request.count

    results = []
    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query, safesearch="moderate", max_results=count, backend="lite"
            )

        results = [
            SearchResult(
                link=result["href"],
                title=result.get("title"),
                snippet=result.get("body"),
            )
            for result in search_results
        ]

    except Exception as e:
        print(f"Error during DuckDuckGo search: {e}")

    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888)
```
