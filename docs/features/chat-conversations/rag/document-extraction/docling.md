---
sidebar_position: 3
title: "Docling 文档提取"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 🐤 Docling 文档提取

本文提供一个逐步指南，说明如何将 Docling 集成到 Open WebUI 中。Docling 是一个文档处理库，可将多种文件格式——包括 PDF、Word、电子表格、HTML 与图片——转换为 JSON 或 Markdown 等结构化数据。它内置版面检测、表格解析和语言感知处理能力，可通过统一且可扩展的接口，为搜索、总结与检索增强生成等 AI 场景简化文档准备流程。

## 前提条件

- Open WebUI 实例
- 已在系统中安装 Docker
- 已为 Open WebUI 准备 Docker 网络

## 集成步骤

### 第 1 步：运行 Docling-Serve 容器

**基础 CPU 部署：**

```bash
docker run -p 5001:5001 \
  -e DOCLING_SERVE_ENABLE_UI=true \
  quay.io/docling-project/docling-serve
```

**GPU 部署（NVIDIA CUDA）：**

```bash
docker run --gpus all -p 5001:5001 \
  -e DOCLING_SERVE_ENABLE_UI=true \
  quay.io/docling-project/docling-serve-cu128
```

**推荐的生产环境 Docker Compose 部署：**

```yaml
version: "3.8"
services:
  docling-serve:
    image: quay.io/docling-project/docling-serve-cu128:latest
    container_name: docling-serve
    ports:
      - "5001:5001"
    environment:
      # Enable the web UI for testing
      - DOCLING_SERVE_ENABLE_UI=true
      # CRITICAL: Required for picture description with external LLM APIs
      - DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true
      # Maximum wait time for sync requests (seconds) - increase for large documents
      - DOCLING_SERVE_MAX_SYNC_WAIT=600
      # Number of local engine workers
      - DOCLING_SERVE_ENG_LOC_NUM_WORKERS=2
      # CPU thread configuration
      - OMP_NUM_THREADS=4
      - MKL_NUM_THREADS=4
      # IMPORTANT: Keep at 1 to avoid "Task Not Found" errors
      - UVICORN_WORKERS=1
    restart: unless-stopped
    # For GPU support with NVIDIA:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

:::danger 重要：UVICORN_WORKERS 设置

当默认 `LocalOrchestrator` 与 `UVICORN_WORKERS > 1` 一起使用时，你会遇到 **"Task Not Found (404)"** 错误。原因是每个 worker 都维护自己的内存任务存储，从而导致某个 worker 创建的任务无法被另一个 worker 访问。

**除非你已配置 Redis 等共享状态机制，否则始终使用 `UVICORN_WORKERS=1`。**

:::

### 第 2 步：配置 Open WebUI

1. 登录你的 Open WebUI 实例
2. 前往 **管理面板** → **设置** → **文档**
3. 将 **默认** 内容提取引擎下拉框切换为 **Docling**
4. 将提取引擎 URL 设置为 `http://host.docker.internal:5001`（Docker）或 `http://localhost:5001`（原生部署）
5. 保存更改

### 第 3 步：配置图片描述（可选）

若要启用文档中的 AI 图片描述：

1. 在 **文档** 标签中启用 **文档中的图片描述**
2. 选择描述模式：`local` 或 `API`
   - **local**：Vision 模型在 Docling 容器内部运行
   - **API**：Docling 调用外部服务（如 Ollama 或兼容 OpenAI 的 endpoint）

:::danger API 模式的必要条件

当使用 `API` 模式（即调用 Ollama 等外部服务）时，你**必须**在 docling-serve 上设置以下环境变量：

```bash
DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true
```

否则，Docling 会以 `OperationNotAllowed` 错误拒绝向外部服务发起请求。

:::

#### JSON 配置示例

请确保你的配置是**合法 JSON**！

**本地模型配置：**

```json
{
  "repo_id": "HuggingFaceTB/SmolVLM-256M-Instruct",
  "generation_config": {
    "max_new_tokens": 200,
    "do_sample": false
  },
  "prompt": "Describe this image in a few sentences."
}
```

**API 配置（Ollama）：**

```json
{
  "url": "http://host.docker.internal:11434/v1/chat/completions",
  "params": {
    "model": "llava:7b"
  },
  "timeout": 60,
  "prompt": "Describe this image in great detail."
}
```

## Docling-Serve 环境变量参考

| 变量 | 默认值 | 说明 |
| -------- | ------- | ---- |
| `DOCLING_SERVE_ENABLE_UI` | `false` | 在 `/ui` endpoint 启用 Web UI |
| `DOCLING_SERVE_ENABLE_REMOTE_SERVICES` | `false` | **API 模式图片描述所必需** |
| `DOCLING_SERVE_MAX_SYNC_WAIT` | `120` | 同步请求最大等待秒数 |
| `DOCLING_SERVE_ENG_LOC_NUM_WORKERS` | `1` | 本地引擎 worker 数量 |
| `DOCLING_SERVE_ARTIFACTS_PATH` | `/app/data` | 模型 artifacts 存储路径 |
| `UVICORN_WORKERS` | `1` | Uvicorn worker 数量（**务必保持为 1！**） |
| `OMP_NUM_THREADS` | `4` | CPU 处理时的 OpenMP 线程数 |
| `MKL_NUM_THREADS` | `4` | Intel MKL 线程数 |

## Docling 参数参考（Open WebUI）

可通过 **管理面板 > 文档** 中的 `DOCLING_PARAMS` JSON，或通过环境变量进行配置。

| 参数 | 类型 | 说明 | 允许值 |
| ----------- | ---- | ---- | ---------------- |
| `pdf_backend` | `string` | PDF 解析引擎 | `dlparse_v1`, `dlparse_v2`, `dlparse_v4`, `pypdfium2` |
| `table_mode` | `string` | 表格提取质量 | `fast`, `accurate` |
| `ocr_engine` | `string` | OCR 库 | `tesseract`, `easyocr`, `ocrmac`, `rapidocr` |
| `do_ocr` | `bool` | 是否启用 OCR | `true`, `false` |
| `force_ocr` | `bool` | 是否对数字 PDF 强制 OCR | `true`, `false` |
| `pipeline` | `string` | 处理复杂度 | `standard`, `fast` |
| `ocr_lang` | `list[string]` | OCR 语言 | 见下方说明 |

:::tip 语言代码

- **Tesseract**：使用 3 位 ISO 639-2（例如 `eng`、`deu`、`fra`）
- **EasyOCR**：使用 2 位 ISO 639-1（例如 `en`、`de`、`fr`）
:::

**配置示例：**

```json
{
  "do_ocr": true,
  "pdf_backend": "dlparse_v4",
  "table_mode": "accurate",
  "ocr_engine": "tesseract",
  "ocr_lang": ["eng"]
}
```

## 验证集成

1. 访问 Docling UI：`http://127.0.0.1:5001/ui`
2. 上传一个测试文档，确认它能返回 markdown 输出
3. 在 Open WebUI 中向知识库上传一个文件，确认处理流程可成功完成

## 故障排查

### "Task result not found. Please wait for a completion status."

**原因：** 使用了多个 Uvicorn worker，而任务存储又是内存级别。

**解决方案：** 在 docling-serve 配置中将 `UVICORN_WORKERS=1`。

### "Connections to remote services is only allowed when set explicitly"

**原因：** 图片描述的 API 模式需要显式开启对外服务访问。

**解决方案：** 在 docling-serve 环境变量中加入 `DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true`。

### `/v1alpha/convert/file` 返回 404 Not Found

**原因：** 使用了过旧版本的 docling-serve 或 Open WebUI。

**解决方案：**

- 将 Open WebUI 更新到最新版（新版使用 `/v1/convert/file`）
- 将 docling-serve 更新到 v1.0+（新版使用 `/v1` API）

### 大文档出现超时错误

**原因：** `DOCLING_SERVE_MAX_SYNC_WAIT` 对文档处理时间来说太低。

**解决方案：** 提高 `DOCLING_SERVE_MAX_SYNC_WAIT`（例如设为 `600`，即 10 分钟）。

### OCR 不工作或语言识别错误

**原因：** 针对当前 OCR engine，`ocr_lang` 使用了错误格式。

**解决方案：**

- Tesseract 使用 3 位代码：`["eng", "deu"]`
- EasyOCR 使用 2 位代码：`["en", "de"]`

### "Error calling Docling" 但没有具体细节

**排查步骤：**

1. 查看 docling-serve 日志：`docker logs docling-serve`
2. 直接通过 `http://localhost:5001/ui` 测试 Docling
3. 验证 Open WebUI 与 docling-serve 容器之间的网络连通性

## 结论

将 Docling 集成到 Open WebUI 后，文档处理能力会明显增强。需要牢记的关键点包括：

- **始终设置 `UVICORN_WORKERS=1`**，避免任务路由问题
- 在使用 API 模式图片描述时，**务必开启 `DOCLING_SERVE_ENABLE_REMOTE_SERVICES=true`**
- 对大文档，**适当提高 `DOCLING_SERVE_MAX_SYNC_WAIT`**
- 在所有配置字段中，**务必校验 JSON 语法**
