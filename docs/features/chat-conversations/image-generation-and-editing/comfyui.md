---
sidebar_position: 3
title: "ComfyUI"
---

:::warning
本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。
:::

ComfyUI 是一个强大且模块化的 Stable Diffusion 节点式图形界面，为用户提供了对图像生成流程的高度控制。了解更多信息或下载安装，请访问其 [GitHub page](https://github.com/comfyanonymous/ComfyUI)。

若要运行 ComfyUI 并让 Open WebUI 能访问它，你必须在启动时添加 `--listen` 参数，并绑定到 `0.0.0.0`。这样它才能接受来自局域网其他设备的连接。

启动后，ComfyUI 界面通常可通过 `http://<your_comfyui_ip>:8188` 访问。

![Screenshot of the ComfyUI server startup command with the --listen flag highlighted.](/images/image-generation-and-editing/comfyui-listen-flag.png)

## 将 ComfyUI 连接到 Open WebUI

由于 Open WebUI 通常运行在 Docker 中，你必须确保容器能通过 `host.docker.internal` 访问宿主机上的 ComfyUI 应用。

1. **检查宿主机绑定：** 确保 ComfyUI 使用 `--listen 0.0.0.0` 启动（见上文）
2. **检查防火墙：** 如果宿主机启用了防火墙（如 UFW），请确认已放行 8188 端口（`sudo ufw allow 8188/tcp`）

3. **Docker 运行命令（Linux 原生 Docker）：**  
对于未使用 Docker Desktop 的 Linux 用户，运行 Open WebUI 容器时需要显式映射 host gateway：

```docker
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e COMFYUI_BASE_URL=http://host.docker.internal:8188/ \
  -e ENABLE_IMAGE_GENERATION=True \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

当 ComfyUI 安装并运行完成后，你就可以在 Open WebUI 的管理员设置中连接它。

## 图像提示词生成

该功能会使用语言模型，根据你的初始输入自动生成更详细、更有创意的提示词，从而提升图像生成效果。

**Image Prompt Generation** 开关位于 **Admin Panel > Settings > Images** 的 “Image Generation” 区域中，并且在选择图像生成引擎之前就可以设置。

若要自定义用于生成提示词的模板，请前往 **Admin Panel > Settings > Interface > Tasks**。

![Screenshot showing the Image Prompt Generation toggle location in Images settings](/images/image-generation-and-editing/image-prompt-generation-toggle.png)

## 创建图像（Image Generation）

1. **进入图像设置：** 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**

2. **启用并配置 ComfyUI：**
    - 确保页面顶部的 **Image Generation** 开关已启用
    - 在 **Create Image** 部分，将 **Image Generation Engine** 设为 `ComfyUI`
    - **Model**：选择用于生成图像的基础模型
    - **Image Size**：定义输出分辨率（例如 512x512、1024x1024）
    - **Steps**：采样步数；数值越高，图像质量通常越高，但生成时间也更长
    - 在 **ComfyUI Base URL** 字段中输入运行中的 ComfyUI 地址（例如 `http://host.docker.internal:8188/`）
    - 点击 URL 字段旁的 **refresh icon**（🔄）验证连接；成功后应出现提示
    - 如果你的 ComfyUI 实例需要 API key，请在 **ComfyUI API Key** 字段中填写

    ![Screenshot of the Open WebUI Images settings page with ComfyUI selected for image generation.](/images/image-generation-and-editing/comfyui-generation-settings.png)

3. **上传你的 ComfyUI Workflow：**
    - 首先，你需要从 ComfyUI 导出正确格式的 workflow。在 ComfyUI 界面左上角点击 ComfyUI logo，再点击 **Settings**，搜索并启用 **"Dev Mode"** 选项，其说明通常为 **"Enable dev mode options (API save, etc.)"**

    ![Screenshot of the ComfyUI settings with the "Dev Mode" toggle highlighted.](/images/image-generation-and-editing/comfyui-dev-mode.png)

    - 仍在 ComfyUI 中时，加载你想使用的**图像生成** workflow，然后点击 ComfyUI logo，在 **File** 子菜单中选择 **"Export (API)"**。系统会提示你为文件命名，请使用一个方便识别的名称并下载

    ![Screenshot of the "Save (API Format)" button in the ComfyUI interface.](/images/image-generation-and-editing/comfyui-save-api-format.png)
    - 返回 Open WebUI，在 **ComfyUI Workflow** 区域点击 **Upload**，然后选择刚刚下载的 JSON workflow 文件

    ![Screenshot of the ComfyUI Workflow section in Open WebUI, showing the upload button.](/images/image-generation-and-editing/comfyui-workflow-upload.png)

4. **映射 Workflow Nodes：**
    导入 workflow 后，你必须将 workflow 中的 node ID 映射到 Open WebUI 对应字段。每个参数都有两个输入框：

    - **Key（左侧字段）**：workflow 中的输入参数名（例如 `text`、`ckpt_name`、`seed`）
    - **Node Ids（右侧字段）**：包含该输入的 node ID，多个 ID 用逗号分隔

    UI 中会显示 6 个可配置的图像生成参数：

    | Parameter | Default Key | Required | Description |
    |-----------|-------------|----------|-------------|
    | Prompt* | `text` | Yes | 正向提示词文本 |
    | Model | `ckpt_name` | No | Checkpoint 模型名 |
    | Width | `width` | No | 输出图像宽度 |
    | Height | `height` | No | 输出图像高度 |
    | Steps | `steps` | No | 采样步数 |
    | Seed | `seed` | No | 用于复现的随机种子 |

    **注意：** 必填参数带星号（*）。严格来说，只有 prompt 的 node ID 是必须填写的。

    你可以在 ComfyUI 中点击某个 node，并查看其详细信息来找到对应的 node ID。

    ![Screenshot of the ComfyUI Workflow Nodes section in Open WebUI, showing the mapping fields.](/images/image-generation-and-editing/comfyui-node-mapping.png)

    :::info
    你可能需要在 Open WebUI 的 `ComfyUI Workflow Nodes` 区域中调整某个 `Key`，以匹配你的 workflow node。比如，默认的 `seed` key 可能要根据 workflow 结构改成 `noise_seed`。
    :::

    :::tip
    某些 workflow（例如使用 Flux 模型的 workflow）可能需要在单个字段中填写多个 node ID。若某个 node 输入框需要多个 ID，请使用逗号分隔（例如 `1` 或 `1, 2`）。
    :::

5. **保存配置：**
    - 点击页面底部的 **Save** 按钮完成配置。之后你就可以在 Open WebUI 中使用 ComfyUI 进行图像生成了。

![Screenshot of an image being generated in the chat using ComfyUI.](/images/image-generation-and-editing/comfyui-create-image-in-chat.png)

## 编辑图像

Open WebUI 同样支持通过 ComfyUI 进行图像编辑，从而修改已有图片。

1. **进入图像设置：** 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**

2. **配置图像编辑：**
    - 在 **Edit Image** 区域中，将 **Image Edit Engine** 设为 `ComfyUI`
    - **Model**：选择用于编辑任务的模型
    - **Image Size**：指定输出图像的目标分辨率
    - **ComfyUI Base URL** 与 **API Key**：这两个字段与图像生成设置共用
    - **ComfyUI Workflow**：上传一个专门用于图像编辑的 workflow 文件，流程与图像生成相同
    - **Map Workflow Nodes**：图像编辑有 5 个可配置参数，默认值与图像生成不同：

    | Parameter | Default Key | Required | Description |
    |-----------|-------------|----------|-------------|
    | Image* | `image` | Yes | 待编辑的输入图像 |
    | Prompt* | `prompt` | Yes | 编辑提示词文本 |
    | Model | `unet_name` | No | Diffusion 模型名 |
    | Width | `width` | No | 输出图像宽度 |
    | Height | `height` | No | 输出图像高度 |

    **注意：** 与图像生成不同，图像编辑不支持 negative prompt、steps、seed 或 batch size 参数。

    ![Screenshot of the Open WebUI Images settings page with ComfyUI selected for image editing.](/images/image-generation-and-editing/comfyui-editing-settings.png)

![Screenshot of an image being edited in the chat using ComfyUI.](/images/image-generation-and-editing/comfyui-edit-image-in-chat.png)

### 深入理解：如何把 ComfyUI Nodes 映射到 Open WebUI

理解 node ID 映射，往往是将 ComfyUI 与 Open WebUI 这类外部服务集成时最容易卡住的一步。通过 API 集成 ComfyUI，本质上就是把 Open WebUI 的通用控制项（如 “Model”、“Width”、“Prompt”）映射到静态 ComfyUI workflow JSON 中的特定 node 输入。

#### 将 Workflow Nodes 映射到 Open WebUI

Open WebUI 的 **ComfyUI Workflow Nodes** 区域允许你把通用控制项映射到静态 ComfyUI workflow JSON 中的特定 node 输入。每一行有两个字段：

| Field | Description | Example |
|-------|-------------|---------|
| **Key**（左侧） | node 的 `inputs` 块中的输入参数名 | `text`、`ckpt_name`、`seed` |
| **Node Ids**（右侧） | 目标 node ID，可为逗号分隔 | `6` 或 `1, 2, 3` |

#### 在 ComfyUI 中识别 Node ID 和 Input Key

在配置 Open WebUI 之前，你必须先用文本编辑器直接检查导出的 workflow JSON 文件。Node ID 是 ComfyUI 在 JSON 结构中标识某个 node 的唯一编号；JSON 对象的顶层 key 通常就是这些 node ID。

![Screenshot of the ComfyUI interface with a node selected, highlighting the node ID in the properties panel.](/images/image-generation-and-editing/comfyui-node-mapping.png)

**识别 Input Key（参数名）**

Key 就是该 node JSON 结构里你要控制的确切字段名（例如 `seed`、`width`、`ckpt_name`）。

1. **查看 JSON**：打开你的 API workflow JSON（如 `workflow_api.json`）
2. **找到 Node ID**：定位到对应 node 的那一段（例如 `"37"`）
3. **识别 Key**：在 `"inputs"` 块中找到你要控制的变量

**示例：CheckpointLoaderSimple Node（ID 37）**

```json
"37": {
  "inputs": {
      "ckpt_name": "qwen_image_fp8_e4m3fn.safetensors"
  },
  "class_type": "CheckpointLoaderSimple",
  "_meta": {
    "title": "Load Checkpoint"
  }
},
```

**示例：KSampler Node（ID 3）**

```json
"3": {
  "inputs": {
      "seed": 42,
      "steps": 20,
      "cfg": 8.0,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0
  },
  "class_type": "KSampler",
  "_meta": {
    "title": "KSampler"
  }
},
```

![Screenshot of the ComfyUI interface with the KSampler node selected, highlighting the node ID and the 'seed' and 'steps' input fields.](/images/image-generation-and-editing/comfyui-unet-name-node.png)

#### 按任务类型区分的默认 Key 值

**图像生成：**
- Prompt: `text`
- Model: `ckpt_name`
- Width: `width`
- Height: `height`
- Steps: `steps`
- Seed: `seed`

**图像编辑：**
- Image: `image`
- Prompt: `prompt`
- Model: `unet_name`
- Width: `width`
- Height: `height`

#### 示例：映射 KSampler 的 Seed

假设你想控制 KSampler node 的 `seed`，它的 node ID 是 `3`。那么在 Open WebUI 设置中的 `Seed` 区域应填写：

| Key | Node Ids |
|-----|----------|
| `seed` | `3` |

#### 处理多个 Node ID

如果多个 node 需要使用相同值（例如多个 sampler 共享同一个 seed），请填写逗号分隔的多个 ID：

| Key | Node Ids |
|-----|----------|
| `seed` | `3, 15, 22` |

#### 处理复杂 / 多模态 Nodes（Qwen 示例）

对于某些特殊 node，Key 可能不只是简单文本字段。

| Parameter | Key | Node Ids | Note |
|-----------|-----|----------|------|
| **Prompt** | `text` 或 `prompt` | `76` | 取决于 node 类型（CLIPTextEncode 或 TextEncodeQwen） |
| **Model** | `ckpt_name` | `37` | 用于 CheckpointLoaderSimple |
| **Model** | `unet_name` | varies | 用于某些 workflow 中的 UNETLoader |
| **Image Input** | `image` | `78` | 该 key 会把文件名传递给 LoadImage node |

#### 排查不匹配错误

如果 ComfyUI 卡住或抛出校验错误，请结合日志和 JSON 结构排查：

| Error Type | Cause & Debugging | Solution |
|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Value not in list: ckpt_name: 'xyz.safetensors'` | 你映射了正确的 node ID（如 37），但传入值（如 `xyz.safetensors`）对该 node 类型来说不是合法模型名（例如把 VAE 模型错误传给了 checkpoint loader） | 修正 Open WebUI 中图像生成或编辑使用的模型名，确保它与 ComfyUI node 所期望的模型类型一致 |
| `Missing input <key>` | 你的 workflow 需要某个输入（如 `cfg` 或 `sampler_name`），但 Open WebUI 没有发送该值，因为该字段未映射 | 要么在 workflow JSON 中硬编码默认值，要么把对应输入 key 映射到正确的 node ID |

只要精确匹配 Node ID 与具体 Key，Open WebUI 就能在提交 prompt 给 ComfyUI 前，正确覆盖 workflow JSON 中的默认值。

## 示例配置：Qwen 图像生成与编辑

本节提供一个额外示例，演示如何为 Qwen 模型配置图像生成与编辑。

### Qwen 图像生成

#### 模型下载

- **Diffusion Model**: [qwen_image_fp8_e4m3fn.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_fp8_e4m3fn.safetensors)
- **Text Encoder**: [qwen_2.5_vl_7b_fp8_scaled.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors)
- **VAE**: [qwen_image_vae.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors)

#### 模型存放位置

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   │   └── qwen_image_fp8_e4m3fn.safetensors
│   ├── 📂 vae/
│   │   └── qwen_image_vae.safetensors
│   └── 📂 text_encoders/
│       └── qwen_2.5_vl_7b_fp8_scaled.safetensors
```

#### Qwen 生成 Workflow Node 映射

| Parameter | Key | Node Ids |
|-----------|-----|----------|
| Prompt | `prompt` | （取决于你的 workflow） |
| Model | `ckpt_name` | （checkpoint loader node ID） |

### Qwen 图像编辑

#### 模型下载

- **Diffusion Model**: [qwen_image_edit_fp8_e4m3fn.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_fp8_e4m3fn.safetensors)
- **Text Encoder**: [qwen_2.5_vl_7b_fp8_scaled.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors)
- **VAE**: [qwen_image_vae.safetensors](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors)

#### 模型存放位置

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   │   └── qwen_image_edit_fp8_e4m3fn.safetensors
│   ├── 📂 vae/
│   │   └── qwen_image_vae.safetensors
│   └── 📂 text_encoders/
│       └── qwen_2.5_vl_7b_fp8_scaled.safetensors
```

#### Qwen 编辑 Workflow Node 映射

| Parameter | Key | Node Ids |
|-----------|-----|----------|
| Image | `image` | （load image node ID） |
| Prompt | `prompt` | （text encoder node ID） |
| Model | `unet_name` | （UNET loader node ID） |

## 示例配置：FLUX.1 图像生成

本节提供一个额外示例，说明如何为 FLUX.1 模型配置图像生成。

### FLUX.1 Dev

#### 模型下载

- **Diffusion Model**: [flux1-dev.safetensors](https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/flux1-dev.safetensors)
- **Text Encoder 1**: [clip_l.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true)
- **Text Encoder 2**: [t5xxl_fp16.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors?download=true)（推荐在 VRAM 大于 32GB 时使用）
- **VAE**: [ae.safetensors](https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true)

#### 模型存放位置

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   │   └── flux1-dev.safetensors
│   ├── 📂 vae/
│   │   └── ae.safetensors
│   └── 📂 text_encoders/
│       ├── clip_l.safetensors
│       └── t5xxl_fp16.safetensors
```

### FLUX.1 Schnell

#### 模型下载

- **Diffusion Model**: [flux1-schnell.safetensors](https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/flux1-schnell.safetensors)
- **Text Encoder 1**: [clip_l.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors?download=true)
- **Text Encoder 2**: [t5xxl_fp8_e4m3fn.safetensors](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors?download=true)（推荐在 VRAM 大于 32GB 时使用）
- **VAE**: [ae.safetensors](https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors?download=true)

#### 模型存放位置

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   │   └── flux1-schnell.safetensors
│   ├── 📂 vae/
│   │   └── ae.safetensors
│   └── 📂 text_encoders/
│       ├── clip_l.safetensors
│       └── t5xxl_fp8_e4m3fn.safetensors
```

## 配置 SwarmUI

SwarmUI 使用 ComfyUI 作为后端。若要让 Open WebUI 与 SwarmUI 协同工作，你需要在 `ComfyUI Base URL` 末尾追加 `ComfyBackendDirect`。此外，还建议为 SwarmUI 启用局域网访问。完成这些调整后，SwarmUI 在 Open WebUI 中的设置方式，与前文所述的 ComfyUI 图像生成步骤基本一致。

![Install SwarmUI with LAN Access](https://github.com/user-attachments/assets/a6567e13-1ced-4743-8d8e-be526207f9f6)

### SwarmUI API URL

你在 `ComfyUI Base URL` 中填写的地址通常如下：

`http://<your_swarmui_address>:7801/ComfyBackendDirect`
