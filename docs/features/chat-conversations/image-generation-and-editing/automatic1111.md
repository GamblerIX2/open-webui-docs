---
sidebar_position: 2
title: "AUTOMATIC1111"
---

:::warning
本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。
:::

Open WebUI 支持通过 **AUTOMATIC1111** [API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API) 进行图像生成。以下是快速开始步骤：

### 初始设置

1. 确保你已安装 [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. 启动 AUTOMATIC1111，并附加额外参数以启用 API 访问：

```python
/webui.sh --api --listen
```

3. 如果你希望通过 Docker 安装预设好环境变量的 WebUI，可使用以下命令：

```docker
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -e AUTOMATIC1111_BASE_URL=http://host.docker.internal:7860/ -e ENABLE_IMAGE_GENERATION=True -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

### 配置 Open WebUI 连接 AUTOMATIC1111

1. 在 Open WebUI 中前往 **Admin Panel** > **Settings** > **Images**
2. 将 `Image Generation Engine` 设置为 `Default (Automatic1111)`
3. 在 API URL 字段中，输入可访问 AUTOMATIC1111 API 的地址：

![Screenshot of the Open WebUI Images settings page with Default (Automatic1111) selected and the API URL field highlighted.](/images/image-generation-and-editing/automatic1111-settings.png)

```txt
http://<your_automatic1111_address>:7860/
```

如果你的 Open WebUI Docker 与 AUTOMATIC1111 运行在同一台主机上，请使用 `http://host.docker.internal:7860/`。
