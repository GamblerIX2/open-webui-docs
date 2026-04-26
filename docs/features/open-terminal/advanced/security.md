---
sidebar_position: 3
title: "安全"
---

# 安全最佳实践

Open Terminal 赋予 AI 运行命令和管理文件的真实能力。以下是确保这种能力被安全使用的方法。

---

## 使用 Docker

**始终使用 Docker**，除非你明确需要直接访问你的机器。Docker 将 Open Terminal 隔离在自己的容器中：它有自己的文件系统、自己的进程，除非你明确允许，否则无法访问宿主计算机上的任何内容。

```bash
docker run -d --name open-terminal -p 8000:8000 \
  --memory 2g --cpus 2 \
  -v open-terminal:/home/user \
  -e OPEN_TERMINAL_API_KEY=your-secret-key \
  ghcr.io/open-webui/open-terminal
```

`--memory 2g` 和 `--cpus 2` 标志可防止失控进程消耗你机器的全部资源。

{/* TODO: Screenshot — A simple diagram showing your computer on the left, a Docker container in the middle (labeled "Open Terminal — isolated"), and an arrow showing that only the /home/user volume is shared. The rest of the host filesystem is blocked off. */}

:::warning 不使用 Docker 运行
不使用 Docker（裸机模式）时，AI 可以使用你用户账户的权限运行任何命令——包括删除文件、安装软件，或访问你账户能访问的任何内容。裸机模式仅用于你自己的个人机器上的个人项目。
:::

---

## 始终设置密码

没有 API Key 时，**任何能访问该端口的人都拥有完整权限**——他们可以运行命令、读取文件并控制终端。

```bash
-e OPEN_TERMINAL_API_KEY=a-strong-password-here
```

在生产环境中，请使用[配置文件](./configuration#config-file)或 [Docker secrets](./configuration#docker-secrets)，而不是在命令行中明文传入密钥。

{/* TODO: Screenshot — Example showing the docker logs command revealing an auto-generated API key, with a note saying "change this to your own strong password". */}

---

## 使用管理员连接（而非用户连接）

连接到 Open WebUI 时，优先使用**管理员配置**方式：

| | 管理员配置 | 用户配置 |
| :--- | :--- | :--- |
| API Key 可见性 | 保存在服务端，不对用户暴露 | 存储在用户浏览器中 |
| 请求经过 | Open WebUI 后端 | 直接从浏览器发出 |
| 终端网络访问来源 | 仅 Open WebUI 服务器 | 每位用户的计算机 |

管理员配置的连接可防止 API Key 进入用户浏览器，并让你控制谁有访问权限。

{/* TODO: Screenshot — Admin settings showing the Open Terminal connection. The API key field shows dots (masked). A note points out that this key never reaches users' browsers. */}

---

## 限制资源

防止失控脚本消耗所有可用的 CPU 和内存：

```yaml title="docker-compose.yml"
deploy:
  resources:
    limits:
      memory: 2G
      cpus: "2.0"
```

如果进程超出这些限制，Docker 会对其进行限流（CPU）或终止（内存）。你的服务器保持健康运行。

{/* TODO: Screenshot — Docker stats or htop inside the container showing CPU and memory usage within the configured limits. */}

---

## 网络隔离

对于最安全的配置，将 Open Terminal 放置在只有 Open WebUI 能访问的**私有 Docker 网络**中：

```yaml title="docker-compose.yml"
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    ports:
      - "3000:8080"
    networks:
      - public
      - internal

  open-terminal:
    image: ghcr.io/open-webui/open-terminal
    # Notice: no ports exposed to the outside
    networks:
      - internal

networks:
  public:
  internal:
    internal: true   # No internet access from this network
```

这意味着：
- Open WebUI 可以通过 `http://open-terminal:8000` 访问 Open Terminal
- Open Terminal **无法**从互联网直接访问
- Open Terminal **无法发出出站互联网请求**

{/* TODO: Screenshot — Network diagram showing the public network (internet → Open WebUI) and the internal network (Open WebUI → Open Terminal). The internal network has no path to the internet. */}

---

## 出站流量过滤

如果 Open Terminal 需要*一定的*互联网访问权限（例如安装软件包），你可以将其限制在特定域名：

```bash
-e OPEN_TERMINAL_ALLOWED_DOMAINS="pypi.org,github.com,*.npmjs.org"
```

只有这些域名可以访问。其他所有域名均被阻止。这可以防止：
- 未经授权的数据离开容器
- 下载意外的软件
- 访问你未预期的内部服务

{/* TODO: Screenshot — Terminal showing two curl commands: one to an allowed domain (succeeds) and one to a blocked domain (fails with "connection refused"). */}

---

## Docker socket warning

The Docker container can optionally access your host's Docker (to let the AI build images, run containers, etc.):

```bash
-v /var/run/docker.sock:/var/run/docker.sock
```

:::danger Only for trusted environments
Mounting the Docker socket gives the container **full control** over your host's Docker. This is effectively root access on your machine. Anyone with terminal access could:
- Run containers that mount your entire filesystem
- Access your host's network
- Manage every container on your machine

Only do this if you fully trust everyone who has access to the terminal.
:::

{/* TODO: Screenshot — A warning diagram showing the Docker socket as a direct bridge to the host, with arrows pointing to "can access host filesystem", "can access host network", "can manage all containers". */}

---

## Security checklist

| ✅ | Recommendation |
| :--- | :--- |
| ☐ | Use Docker, not bare metal |
| ☐ | Set a strong API key |
| ☐ | Use admin-configured connections |
| ☐ | Set memory and CPU limits |
| ☐ | Use network isolation (internal Docker network) |
| ☐ | Enable egress filtering if internet access isn't needed |
| ☐ | Don't mount the Docker socket unless necessary |
| ☐ | Use `slim` or `alpine` images if you don't need runtime package installs |

## Related

- [All configuration options →](./configuration)
- [Multi-user setup →](./multi-user)
