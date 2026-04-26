---
sidebar_position: 1
title: "DeepSeek R1 Dynamic"
---

衷心感谢 **UnslothAI** 的卓越贡献！得益于他们的辛勤工作，我们现在可以在 **Llama.cpp** 上以动态 1.58 位量化形式（压缩至仅 131GB）运行**完整的 DeepSeek-R1** 671B 参数模型！最棒的是？您不再需要担心必须拥有大型企业级 GPU 或服务器——在个人机器上运行此模型已成为可能（尽管对大多数消费级硬件来说速度较慢）。

:::note

Ollama 上唯一真正的 **DeepSeek-R1** 模型是此处提供的 **671B 版本**：[https://ollama.com/library/deepseek-r1:671b](https://ollama.com/library/deepseek-r1:671b)。其他版本均为**蒸馏**模型。

:::

本指南重点介绍使用 **Llama.cpp** 与 **Open WebUI** 集成运行**完整 DeepSeek-R1 动态 1.58 位量化模型**。本教程以 **M4 Max + 128GB RAM** 机器为例进行演示，您可以根据自己的配置调整相关设置。

---

## 第 1 步：安装 Llama.cpp

您可以选择：

- [下载预编译二进制文件](https://github.com/ggerganov/llama.cpp/releases)
- **或自行构建**：按照 [Llama.cpp 构建指南](https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md)中的说明操作

## 第 2 步：下载 UnslothAI 提供的模型

前往 [Unsloth 的 Hugging Face 页面](https://huggingface.co/unsloth/DeepSeek-R1-GGUF)下载适合的 DeepSeek-R1 **动态量化版本**。本教程使用 **1.58 位（131GB）** 版本，该版本高度优化且出乎意料地功能完整。

:::tip

了解您的"工作目录"——Python 脚本或终端会话运行的位置。模型文件默认会下载到该目录的子文件夹中，请确保您知道其路径！例如，如果您在 `/Users/yourname/Documents/projects` 中运行以下命令，下载的模型将保存在 `/Users/yourname/Documents/projects/DeepSeek-R1-GGUF` 下。

:::

要了解更多关于 UnslothAI 的开发过程以及这些动态量化版本如此高效的原因，请查看他们的博客文章：[UnslothAI DeepSeek R1 动态量化](https://unsloth.ai/blog/deepseekr1-dynamic)。

以下是以编程方式下载模型的方法：

```python

# 运行前请先安装 Hugging Face 依赖：

# pip install huggingface_hub hf_transfer

from huggingface_hub import snapshot_download

snapshot_download(
    repo_id = "unsloth/DeepSeek-R1-GGUF",  # 指定 Hugging Face 仓库
    local_dir = "DeepSeek-R1-GGUF",         # 模型将下载到此目录
    allow_patterns = ["*UD-IQ1_S*"],        # 仅下载 1.58 位版本
)
```

下载完成后，您将在如下目录结构中找到模型文件：

```txt
DeepSeek-R1-GGUF/
├── DeepSeek-R1-UD-IQ1_S/
│   ├── DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf
│   ├── DeepSeek-R1-UD-IQ1_S-00002-of-00003.gguf
│   ├── DeepSeek-R1-UD-IQ1_S-00003-of-00003.gguf
```

:::info

🛠️ 在后续步骤中请更新路径以**匹配您的具体目录结构**。例如，如果您的脚本在 `/Users/tim/Downloads` 中，GGUF 文件的完整路径将是：
`/Users/tim/Downloads/DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf`。

:::

## 第 3 步：确保 Open WebUI 已安装并运行

如果您尚未安装 **Open WebUI**，不用担心！设置非常简单。只需按照 [Open WebUI 文档](https://docs.openwebui.com/)操作。安装完成后，启动应用程序——我们将在后续步骤中连接它以与 DeepSeek-R1 模型交互。

## 第 4 步：使用 Llama.cpp 服务模型

模型下载完成后，下一步是使用 **Llama.cpp 的服务器模式**运行它。开始之前：

1. **找到 `llama-server` 二进制文件。**
   如果您是从源代码构建的（如第 1 步所述），`llama-server` 可执行文件将位于 `llama.cpp/build/bin` 中。使用 `cd` 命令导航到此目录：

   ```bash
   cd [path-to-llama-cpp]/llama.cpp/build/bin
   ```

   将 `[path-to-llama-cpp]` 替换为您克隆或构建 Llama.cpp 的位置。例如：

   ```bash
   cd ~/Documents/workspace/llama.cpp/build/bin
   ```

2. **指向您的模型文件夹。**
   使用第 2 步中创建的下载 GGUF 文件的完整路径。启动模型服务时，指定分割 GGUF 文件的第一部分（例如 `DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf`）。

以下是启动服务器的命令：

```bash
./llama-server \
    --model /[your-directory]/DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --port 10000 \
    --ctx-size 1024 \
    --n-gpu-layers 40
```

:::tip

🔑 **根据您的机器自定义的参数：**

- **`--model`：** 将 `/[your-directory]/` 替换为第 2 步中下载 GGUF 文件的路径。
- **`--port`：** 服务器默认端口为 `8080`，您可以根据端口可用性自行更改。
- **`--ctx-size`：** 确定上下文长度（令牌数量）。如果硬件允许，可以增大此值，但要注意 RAM/VRAM 使用量的增加。
- **`--n-gpu-layers`：** 设置要卸载到 GPU 以加快推理速度的层数。具体数量取决于 GPU 的内存容量——请参考 Unsloth 的表格获取具体建议。

:::

例如，如果您的模型下载到 `/Users/tim/Documents/workspace`，命令如下：

```bash
./llama-server \
    --model /Users/tim/Documents/workspace/DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --port 10000 \
    --ctx-size 1024 \
    --n-gpu-layers 40
```

服务器启动后，将在以下地址托管一个**本地 OpenAI 兼容 API** 端点：

```txt
http://127.0.0.1:10000
```

:::info

🖥️ **Llama.cpp 服务器运行中**

![服务器截图](/images/tutorials/deepseek/serve.png)

运行命令后，您应该看到确认服务器已激活并在端口 10000 上监听的消息。

:::

请**保持此终端会话运行**，因为它为后续所有步骤提供模型服务。

## 第 5 步：将 Llama.cpp 连接到 Open WebUI

1. 进入 Open WebUI 中的 **Admin Settings**。
2. 导航至 **Connections > OpenAI Connections**。
3. 为新连接添加以下详细信息：
   - URL：`http://127.0.0.1:10000/v1`（在 Docker 中运行 Open WebUI 时使用 `http://host.docker.internal:10000/v1`）
   - API Key：`none`

:::info

🖥️ **在 Open WebUI 中添加连接**

![连接截图](/images/tutorials/deepseek/connection.png)

运行命令后，您应该看到确认服务器已激活并在端口 10000 上监听的消息。

:::

保存连接后，您可以直接从 Open WebUI 开始查询 **DeepSeek-R1**！🎉

---

## 示例：生成响应

现在您可以使用 Open WebUI 的聊天界面与 **DeepSeek-R1 动态 1.58 位模型**交互。

![响应截图](/images/tutorials/deepseek/response.png)

---

## 注意事项

- **性能：**
  在个人硬件上运行像 DeepSeek-R1 这样的 131GB 超大模型将会**很慢**。即使使用 M4 Max（128GB RAM），推理速度也相当有限。但它能正常工作这一事实本身就证明了 UnslothAI 优化工作的价值。

- **VRAM/内存要求：**
  确保有足够的 VRAM 和系统 RAM 以获得最佳性能。使用低端 GPU 或纯 CPU 设置时，速度会更慢（但仍然可行！）。

---

得益于 **UnslothAI** 和 **Llama.cpp**，运行最大的开源推理模型之一 **DeepSeek-R1**（1.58 位版本）终于变得触手可及。虽然在消费级硬件上运行此类模型具有挑战性，但无需大型计算基础设施即可实现这一目标，是一项重大的技术里程碑。

⭐ 衷心感谢社区推动开放 AI 研究的边界。

祝实验愉快！🚀
