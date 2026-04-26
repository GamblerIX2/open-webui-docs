## 前置条件

- 已安装并运行 [Docker Engine](https://docs.docker.com/engine/install/)
- Open WebUI 正在运行（或准备好一同部署）
- [Open WebUI 企业版许可证](https://openwebui.com/enterprise)（生产环境使用必须）

## 使用 Docker Compose 快速开始

此 Compose 文件将 Open WebUI 和 Terminals 编排器一起部署。

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - >-
        TERMINAL_SERVER_CONNECTIONS=[{
          "id": "terminals",
          "name": "Terminals",
          "enabled": true,
          "url": "http://terminals:3000",
          "key": "${TERMINALS_API_KEY}",
          "auth_type": "bearer",
          "config": {
            "access_grants": [{
              "principal_type": "user",
              "principal_id": "*",
              "permission": "read"
            }]
          }
        }]
    volumes:
      - open-webui:/app/backend/data
    networks:
      - webui
    depends_on:
      - terminals

  terminals:
    image: ghcr.io/open-webui/terminals:latest
    environment:
      - TERMINALS_BACKEND=docker
      - TERMINALS_API_KEY=${TERMINALS_API_KEY}
      - TERMINALS_IMAGE=ghcr.io/open-webui/open-terminal:latest
      - TERMINALS_NETWORK=open-webui-network
      - TERMINALS_IDLE_TIMEOUT_MINUTES=30
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - terminals-data:/app/data
    networks:
      - webui

volumes:
  open-webui:
  terminals-data:

networks:
  webui:
    name: open-webui-network
```

在 Compose 文件旁边的 `.env` 文件中设置共享 API 密钥：

```env
TERMINALS_API_KEY=change-me-to-a-strong-random-value
```

然后启动所有内容：

```bash
docker compose up -d
```

Open WebUI 将在 `http://localhost:3000` 上可用。当任何用户激活终端时，编排器会自动配置其个人容器。

:::warning Docker 套接字访问
编排器需要访问 Docker 套接字 (`/var/run/docker.sock`) 来管理容器。在生产环境中，请使用 Docker 套接字代理，如 [Tecnativa/docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)，以限制其可以进行的 API 调用。
:::

---

<details>
<summary>配置参考</summary>

| 变量 | 默认值 | 描述 |
| :--- | :--- | :--- |
| `TERMINALS_BACKEND` | `docker` | 后端类型。在此部署模式下设置为 `docker`。 |
| `TERMINALS_API_KEY` | (空) | 用于认证来自 Open WebUI 请求的共享密钥。必须提供。 |
| `TERMINALS_IMAGE` | `ghcr.io/open-webui/open-terminal:latest` | 用户终端的默认容器镜像。 |
| `TERMINALS_PORT` | `3000` | 编排器监听的端口。 |
| `TERMINALS_HOST` | `0.0.0.0` | 编排器绑定的地址。 |
| `TERMINALS_NETWORK` | (空) | 用户容器的 Docker 网络。设置后，容器通过名称进行通信。 |
| `TERMINALS_DOCKER_HOST` | `127.0.0.1` | 发布容器端口的地址。仅在没有 `TERMINALS_NETWORK` 时相关。 |
| `TERMINALS_DATA_DIR` | `data/terminals` | 存储每个用户工作区数据的宿主机目录。 |
| `TERMINALS_IDLE_TIMEOUT_MINUTES` | `0` (禁用) | 容器停止前的非活动分钟数。对于典型使用，请设置为 `30`。 |
| `TERMINALS_MAX_CPU` | (空) | 用户容器的 CPU 限制（例如 `2`）。 |
| `TERMINALS_MAX_MEMORY` | (空) | 用户容器的内存限制（例如 `4Gi`）。 |
| `TERMINALS_OPEN_WEBUI_URL` | (空) | 如果设置，则针对此 Open WebUI 实例验证传入的 JWT，而不是使用 `TERMINALS_API_KEY`。 |

</details>

---

<details>
<summary>容器生命周期详情</summary>

**命名。** 容器命名为 `terminals-{policy_id}-{user_id}`，从而便于使用 `docker ps --filter "label=managed-by=terminals"` 进行过滤。

**健康检查。** 创建容器后，编排器会轮询其 `/health` 端点，直到返回 HTTP 200（最多 15 秒）。只有这样它才开始代理流量。

**协调（Reconciliation）。** 如果编排器重新启动，它会通过标签重新发现现有的正在运行的容器，并从容器配置中恢复它们的 API 密钥。这可以防止创建重复的容器。

**冲突处理。** 如果同名的容器已经存在（例如，来自之前失败的清理），编排器会强制删除旧容器并最多重试 3 次。

</details>

---

## 限制

- **单主机。** 所有用户容器都在一个 Docker 主机上运行。如需高可用性或服务更大的团队，请使用 Kubernetes Operator 后端。
- **没有内置高可用性。** 如果编排器宕机，活动的终端会话将被中断（尽管容器继续运行并在重新启动时被协调）。
- **需要 Docker 套接字。** 编排器需要访问 Docker 套接字来管理容器。
