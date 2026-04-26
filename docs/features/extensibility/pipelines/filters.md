---
sidebar_position: 2
title: "Filters"
---

## Filters

Filters 用于对传入的用户消息和传出的助手（LLM）消息执行操作。过滤器中可以执行的操作包括：将消息发送到监控平台（如 Langfuse 或 DataDog）、修改消息内容、屏蔽有毒消息、将消息翻译成另一种语言，或对特定用户的消息进行速率限制。示例列表维护在 [Pipelines 仓库](https://github.com/open-webui/pipelines/tree/main/examples/filters)中。Filters 可以作为 Function 执行，也可以在 Pipelines 服务器上执行。一般工作流如下图所示。

<div align="center">
  <a href="#">
    ![Filter Workflow](/images/pipelines/filters.png)
  </a>
</div>

在模型或 Pipe 上启用过滤器 Pipeline 后，来自用户的传入消息（即"inlet"）会传递给过滤器进行处理。过滤器在向 LLM 模型请求对话完成之前对消息执行所需的操作。最后，过滤器在将传出的 LLM 消息（即"outlet"）发送给用户之前对其进行后处理。
