---
sidebar_position: 50
title: "浏览器搜索引擎"
---

# 浏览器搜索引擎集成

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看贡献教程。

:::

Open WebUI 支持直接集成到浏览器。本教程将指导你把 Open WebUI 配置为自定义搜索引擎，让你可以直接在地址栏中发起查询。

## 将 Open WebUI 配置为搜索引擎

### 前置条件

开始前请确认：

- 你已安装 Chrome 或其他受支持浏览器。
- `WEBUI_URL` 环境变量已正确设置，可通过 Docker 环境变量或 `.env` 文件配置，参见[环境变量指南](https://docs.openwebui.com/reference/env-configuration)。

### 第 1 步：设置 WEBUI_URL 环境变量

设置 `WEBUI_URL` 能让浏览器知道查询请求应发送到哪里。

#### 使用 Docker 环境变量

如果你通过 Docker 运行 Open WebUI，可在 `docker run` 命令中设置该环境变量：

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  -e WEBUI_URL="https://<your-open-webui-url>" \
  ghcr.io/open-webui/open-webui:main
```

你也可以把该变量写入 `.env` 文件：

```plaintext
WEBUI_URL=https://<your-open-webui-url>
```

### 第 2 步：将 Open WebUI 添加为自定义搜索引擎

### 在 Chrome 中配置

1. 打开 Chrome 并进入 **Settings**。
2. 在侧栏选择 **Search engine**，点击 **Manage search engines**。
3. 点击 **Add** 新建搜索引擎。
4. 按如下填写：
  - **Search engine**：Open WebUI Search
  - **Keyword**：webui（或你喜欢的任意关键词）
  - **URL with %s in place of query**：

      ```txt
      https://<your-open-webui-url>/?q=%s
      ```

5. 点击 **Add** 保存配置。

### 在 Firefox 中配置

1. 在 Firefox 中打开 Open WebUI。
2. 点击地址栏展开搜索区域。
3. 点击展开后底部绿色圆圈中的加号图标，将 Open WebUI 搜索添加到浏览器搜索引擎列表。

或使用以下方式：

1. 在 Firefox 中打开 Open WebUI。
2. 右键地址栏。
3. 在菜单中选择 “Add Open WebUI”（或类似选项）。

### 可选：指定模型

如果你希望搜索时使用指定模型，可将模型 ID 加入 URL：

```txt
https://<your-open-webui-url>/?models=<model_id>&q=%s
```

:::note

**说明：** 模型 ID 需要进行 URL 编码。空格、斜杠等特殊字符都要编码（例如 `my model` 需写成 `my%20model`）。

:::

## 使用示例

配置完成后，你可以直接在地址栏发起搜索。输入你设置的关键词，再加查询内容：

```txt
webui your search query
```

该命令会跳转到 Open WebUI 并显示对应搜索结果。

## 故障排查

如果遇到问题，请检查：

- 确认 `WEBUI_URL` 配置正确，并指向可访问的 Open WebUI 实例。
- 再次核对浏览器中的搜索引擎 URL 格式是否填写正确。
- 确认网络连接正常，且 Open WebUI 服务正在运行。
