# Docker Compose 配置

使用 Docker Compose 可以更方便地管理多容器 Docker 应用。

Docker Compose 需要额外安装 `docker-compose-v2`。

:::warning

**注意：** 一些旧版 Docker Compose 教程仍使用 version 1 语法，例如 `docker-compose build`。请确认你使用的是 version 2 语法，即 `docker compose build`（中间是空格，不是连字符）。

:::

## 示例 `docker-compose.yml`

下面是一个用于部署 Open WebUI 的示例配置：

```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
volumes:
  open-webui:
```

### 使用 Slim 镜像

如果你的环境存储空间或带宽有限，可以使用不预打包模型的 slim 镜像：

```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main-slim
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
volumes:
  open-webui:
```

:::note

**说明：** slim 镜像会在首次使用时下载所需模型（whisper、embedding 模型），因此第一次启动可能更慢，但镜像体积会明显更小。

:::

## 启动服务

运行以下命令启动服务：

```bash
docker compose up -d
```

## 辅助脚本

代码库中包含一个名为 `run-compose.sh` 的辅助脚本。它可以帮助你选择部署时应包含哪些 Docker Compose 文件，从而简化搭建过程。

---

:::note

**说明：** 如果需要 Nvidia GPU 支持，请把镜像从 `ghcr.io/open-webui/open-webui:main` 改为 `ghcr.io/open-webui/open-webui:cuda`，并在 `docker-compose.yml` 的服务定义中增加以下内容：

:::

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

这样就能在可用时让应用使用 GPU 资源。

## 卸载

如果要卸载通过 Docker Compose 运行的 Open WebUI，请按以下步骤操作：

1.  **停止并删除服务：**
    在包含 `docker-compose.yml` 的目录中运行：
    ```bash
    docker compose down
    ```

2.  **删除数据卷（可选，警告：会删除所有数据）：**
    如果你希望彻底移除数据（聊天、设置等）：
    ```bash
    docker compose down -v
    ```
    或手动删除：
    ```bash
    docker volume rm <your_project_name>_open-webui
    ```

3.  **删除镜像（可选）：**
    ```bash
    docker rmi ghcr.io/open-webui/open-webui:main
    ```
