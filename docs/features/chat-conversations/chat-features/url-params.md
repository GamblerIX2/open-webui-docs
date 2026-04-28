---
sidebar_position: 7
title: "URL 参数"
---

在 Open WebUI 中，你可以通过多种 URL 参数来自定义聊天会话。这些参数允许你按聊天粒度设置特定配置、启用功能并定义模型设置，从而直接通过 URL 为单个聊天会话提供更强的灵活性与控制力。

## URL 参数概览

下表列出了可用 URL 参数、其作用和示例用法。

|**参数**|**说明**|**示例**|
|---|---|---|
|`models`|指定要使用的模型列表，多个模型以逗号分隔|`/?models=model1,model2`|
|`model`|为该聊天会话指定单个模型|`/?model=model1`|
|`youtube`|指定要在聊天中转录的 YouTube 视频 ID|`/?youtube=VIDEO_ID`|
|`load-url`|指定要抓取并作为文档上传到聊天中的网站 URL|`/?load-url=https://google.com`|
|`web-search`|若设为 `true`，则启用网络搜索功能|`/?web-search=true`|
|`tools` or `tool-ids`|指定要在聊天中启用的工具 ID 列表，多个以逗号分隔|`/?tools=tool1,tool2`|
|`call`|若设为 `true`，则启用通话叠层|`/?call=true`|
|`q`|为聊天设置初始查询或提示词|`/?q=Hello%20there`|
|`temporary-chat`|若设为 `true`，则将聊天标记为临时会话|`/?temporary-chat=true`|
|`code-interpreter`|若设为 `true`，则启用代码解释器功能|`/?code-interpreter=true`|
|`image-generation`|若设为 `true`，则启用图像生成功能|`/?image-generation=true`|

### 1. **模型与模型选择**

- **说明**：`models` 和 `model` 参数可让你指定某个聊天会话使用哪些[语言模型](/features/workspace/models)
- **如何设置**：多个模型用 `models`，单个模型用 `model`
- **示例**：
  - `/?models=model1,model2` —— 使用 `model1` 和 `model2` 初始化聊天
  - `/?model=model1` —— 将 `model1` 作为该聊天唯一模型

### 2. **YouTube 转录**

- **说明**：`youtube` 参数接收一个 YouTube 视频 ID，让聊天对指定视频执行转录
- **如何设置**：将 YouTube 视频 ID 作为该参数值
- **示例**：`/?youtube=VIDEO_ID`
- **行为**：聊天会针对该 YouTube 视频触发转录功能

### 3. **网站插入**

- **说明**：`load-url` 参数会下载指定网站，并提取内容，将其作为文档上传到聊天中
- **如何设置**：将完整网站 URL 作为该参数值
- **示例**：`/?load-url=https://google.com`
- **行为**：系统会触发对指定网站 URL 的插入流程

### 4. **网络搜索**

- **说明**：启用 `web-search` 后，该聊天会话即可访问[网络搜索](/category/web-search/)功能
- **如何设置**：将该参数设为 `true`
- **示例**：`/?web-search=true`
- **行为**：启用后，聊天可将网络搜索结果纳入回复内容

### 5. **工具选择**

- **说明**：`tools` 或 `tool-ids` 参数用于指定在聊天中启用哪些[tools](/features/extensibility/plugin/tools)
- **如何设置**：将工具 ID 以逗号分隔后作为参数值
- **示例**：`/?tools=tool1,tool2` 或 `/?tool-ids=tool1,tool2`
- **行为**：系统会匹配并激活这些工具，以供当前会话使用

### 6. **通话叠层**

- **说明**：`call` 参数会在聊天界面中启用视频 / 通话叠层
- **如何设置**：将参数设为 `true`
- **示例**：`/?call=true`
- **行为**：启用通话界面叠层，以支持实时转录、视频输入等功能

### 7. **初始查询提示词**

- **说明**：`q` 参数允许为聊天预设初始查询或提示词
- **如何设置**：将查询或提示词文本作为参数值
- **示例**：`/?q=Hello%20there`
- **行为**：聊天会以该提示词作为首条消息自动提交

### 8. **临时聊天会话**

- **说明**：`temporary-chat` 参数会把聊天标记为临时会话。这可能会限制保存聊天历史或应用持久化设置等能力
- **如何设置**：将该参数设为 `true`
- **示例**：`/?temporary-chat=true`
- **行为**：启动一个一次性聊天会话，不保存历史，也不会应用高级持久配置
  - **注意**：出于隐私考虑，临时聊天中的文档处理仅在前端进行。对于需要后端解析的复杂文件（如 DOCX），可能无法完全支持

### 9. **代码解释器**

- **说明**：`code-interpreter` 参数用于启用代码解释器功能
- **如何设置**：将该参数设为 `true`，即可为新聊天启用代码解释器
- **示例**：`/?code-interpreter=true`
- **行为**：激活代码解释器按钮，并在下一次发送提示词时调用代码解释器

### 10. **图像生成**

- **说明**：`image-generation` 参数用于为当前提示词启用图像生成
- **如何设置**：将该参数设为 `true`
- **示例**：`/?image-generation=true`
- **行为**：激活图像生成按钮以生成图像

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>示例用例</summary>

:::tip

**临时聊天会话**  
例如用户希望发起一个不会保存历史的快速聊天，就可以在 URL 中设置 `temporary-chat=true`。这会提供一个适合一次性交互的临时聊天环境。

:::
</details>

## 组合使用多个参数

这些 URL 参数可以组合起来，创建高度定制化的聊天会话。例如：

```bash
/?models=model1,model2&youtube=VIDEO_ID&web-search=true&tools=tool1,tool2&call=true&q=Hello%20there&temporary-chat=true
```

这个 URL 将会：

- 使用 `model1` 和 `model2` 初始化聊天
- 启用 YouTube 转录、网络搜索和指定工具
- 显示通话叠层
- 设置初始提示词为 "Hello there."
- 将该聊天标记为临时会话，不保存任何历史
