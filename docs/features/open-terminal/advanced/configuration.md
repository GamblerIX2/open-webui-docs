---
sidebar_position: 2
title: "配置"
---

# 配置参考

Open Terminal 开箱即用，提供合理的默认值。本页面涵盖所有可自定义的设置。

设置按以下顺序应用（后者覆盖前者）：

1. 内置默认值
2. 系统配置文件（`/etc/open-terminal/config.toml`）
3. 用户配置文件（`~/.config/open-terminal/config.toml`）
4. 环境变量（`OPEN_TERMINAL_*`）
5. CLI 标志（`--host`、`--port` 等）

---

## 所有设置

| 设置 | 默认值 | 环境变量 | 说明 |
| :--- | :--- | :--- | :--- |
| **Host** | `0.0.0.0` | — | 监听的网络地址 |
| **Port** | `8000` | — | 端口号 |
| **API Key** | 自动生成 | `OPEN_TERMINAL_API_KEY` | 连接密码 |
| **API Key File** | — | `OPEN_TERMINAL_API_KEY_FILE` | 从文件加载密钥（用于 Docker secrets） |
| **Log Directory** | `~/.local/state/open-terminal/logs` | `OPEN_TERMINAL_LOG_DIR` | 日志文件保存位置 |
| **Max Sessions** | `16` | `OPEN_TERMINAL_MAX_SESSIONS` | 最大并发终端会话数 |
| **Enable Terminal** | `true` | `OPEN_TERMINAL_ENABLE_TERMINAL` | 开启/关闭交互式终端 |
| **Enable Notebooks** | `true` | `OPEN_TERMINAL_ENABLE_NOTEBOOKS` | 开启/关闭 Jupyter notebook 执行 |
| **TERM** | `xterm-256color` | `OPEN_TERMINAL_TERM` | 终端颜色支持 |
| **Execute Timeout** | 未设置 | `OPEN_TERMINAL_EXECUTE_TIMEOUT` | 等待命令输出的时长（秒） |
| **Execute Description** | — | `OPEN_TERMINAL_EXECUTE_DESCRIPTION` | 告知 AI 已安装工具的自定义文本 |
| **Multi-User** | `false` | `OPEN_TERMINAL_MULTI_USER` | 启用[每用户隔离](./multi-user) |
| **CORS Origins** | — | `OPEN_TERMINAL_CORS_ALLOWED_ORIGINS` | 允许的跨域来源 |
| **Allowed Domains** | — | `OPEN_TERMINAL_ALLOWED_DOMAINS` | [出站防火墙](./security#出站流量过滤)：仅允许连接到这些域名 |

---

## 仅限 Docker 的设置

以下设置仅在 Docker 镜像中有效：

| 设置 | 环境变量 | 说明 |
| :--- | :--- | :--- |
| **System Packages** | `OPEN_TERMINAL_PACKAGES` | 启动时安装的系统软件包（空格分隔） |
| **Python Packages** | `OPEN_TERMINAL_PIP_PACKAGES` | 启动时安装的 Python 软件包（空格分隔） |

:::note
这些软件包在每次容器启动时都会重新安装。如果你需要安装大量软件包，考虑[构建自定义镜像](https://github.com/open-webui/open-terminal)。
:::

---

## 配置文件

除环境变量外，你也可以将设置写入文件：

```toml title="~/.config/open-terminal/config.toml"
host = "0.0.0.0"
port = 8000
api_key = "your-secret-key"
log_dir = "/var/log/open-terminal"
max_terminal_sessions = 16
enable_terminal = true
enable_notebooks = true
execute_timeout = 5
execute_description = "This terminal has ffmpeg and ImageMagick installed."
```

{/* TODO: Screenshot — A text editor showing a well-formatted config.toml file. */}

:::tip 为什么使用配置文件？
它可以让你的 API Key 不出现在命令行和 shell 历史记录中。在机器上运行 `ps` 或 `htop` 的任何人都不会看到它。
:::

若要使用自定义位置的配置文件：

```bash
open-terminal run --config /path/to/my-config.toml
```

---

## Docker secrets

对于生产 Docker 部署，可以从 secret 文件加载 API Key：

```yaml title="docker-compose.yml"
services:
  open-terminal:
    image: ghcr.io/open-webui/open-terminal
    environment:
      - OPEN_TERMINAL_API_KEY_FILE=/run/secrets/terminal_api_key
    secrets:
      - terminal_api_key

secrets:
  terminal_api_key:
    file: ./terminal_api_key.txt
```

{/* TODO: Screenshot — Docker Compose file in an editor with the secrets section highlighted. */}

---

## 镜像变体

Open Terminal 提供三种大小的镜像：

| | `latest` | `slim` | `alpine` |
| :--- | :--- | :--- | :--- |
| **适合** | 通用用途、AI Agent | 较小体积 | 最小体积 |
| **大小** | ~4 GB | ~430 MB | ~230 MB |
| **包含** | Node.js、Python、编译器、ffmpeg、Docker CLI、数据科学库 | git、curl、jq | git、curl、jq |
| **可安装软件包** | ✔（有 sudo） | ✘ | ✘ |
| **多用户** | ✔ | ✘ | ✘ |

**如果不确定，使用 `latest`。** 它预装了所有工具，AI 无需等待安装即可使用任何工具。

{/* TODO: Screenshot — A visual comparison of the three image variants showing relative sizes and capabilities. */}

## 相关链接

- [安全最佳实践 →](./security)
- [多用户配置 →](./multi-user)

Open Terminal has sensible defaults out of the box. This page covers all the settings you can customize if you need to.

Settings are applied in this order (later ones override earlier ones):

1. Built-in defaults
2. System config file (`/etc/open-terminal/config.toml`)
3. User config file (`~/.config/open-terminal/config.toml`)
4. Environment variables (`OPEN_TERMINAL_*`)
5. CLI flags (`--host`, `--port`, etc.)

---

## All settings

| Setting | Default | Environment Variable | Description |
| :--- | :--- | :--- | :--- |
| **Host** | `0.0.0.0` | — | Network address to listen on |
| **Port** | `8000` | — | Port number |
| **API Key** | Auto-generated | `OPEN_TERMINAL_API_KEY` | Password for connecting |
| **API Key File** | — | `OPEN_TERMINAL_API_KEY_FILE` | Load the key from a file (for Docker secrets) |
| **Log Directory** | `~/.local/state/open-terminal/logs` | `OPEN_TERMINAL_LOG_DIR` | Where to save log files |
| **Max Sessions** | `16` | `OPEN_TERMINAL_MAX_SESSIONS` | Maximum concurrent terminal sessions |
| **Enable Terminal** | `true` | `OPEN_TERMINAL_ENABLE_TERMINAL` | Turn the interactive terminal on/off |
| **Enable Notebooks** | `true` | `OPEN_TERMINAL_ENABLE_NOTEBOOKS` | Turn Jupyter notebook execution on/off |
| **TERM** | `xterm-256color` | `OPEN_TERMINAL_TERM` | Terminal color support |
| **Execute Timeout** | Unset | `OPEN_TERMINAL_EXECUTE_TIMEOUT` | How long (seconds) to wait for command output |
| **Execute Description** | — | `OPEN_TERMINAL_EXECUTE_DESCRIPTION` | Custom text telling the AI about installed tools |
| **Multi-User** | `false` | `OPEN_TERMINAL_MULTI_USER` | Enable [per-user isolation](./multi-user) |
| **CORS Origins** | — | `OPEN_TERMINAL_CORS_ALLOWED_ORIGINS` | Allowed cross-origin domains |
| **Allowed Domains** | — | `OPEN_TERMINAL_ALLOWED_DOMAINS` | [Egress firewall](./security#egress-filtering): only allow outbound connections to these domains |

---

## Docker-only settings

These only work with the Docker image:

| Setting | Environment Variable | Description |
| :--- | :--- | :--- |
| **System Packages** | `OPEN_TERMINAL_PACKAGES` | Space-separated list of system packages to install at startup |
| **Python Packages** | `OPEN_TERMINAL_PIP_PACKAGES` | Space-separated list of Python packages to install at startup |

:::note
These packages are reinstalled every time the container starts. If you need many packages, consider [building a custom image](https://github.com/open-webui/open-terminal) instead.
:::

---

## Config file

Instead of environment variables, you can put settings in a file:

```toml title="~/.config/open-terminal/config.toml"
host = "0.0.0.0"
port = 8000
api_key = "your-secret-key"
log_dir = "/var/log/open-terminal"
max_terminal_sessions = 16
enable_terminal = true
enable_notebooks = true
execute_timeout = 5
execute_description = "This terminal has ffmpeg and ImageMagick installed."
```

{/* TODO: Screenshot — A text editor showing a well-formatted config.toml file. */}

:::tip Why use a config file?
It keeps your API key out of the command line and shell history. Anyone running `ps` or `htop` on the machine won't see it.
:::

To use a config file in a custom location:

```bash
open-terminal run --config /path/to/my-config.toml
```

---

## Docker secrets

For production Docker deployments, you can load the API key from a secret file:

```yaml title="docker-compose.yml"
services:
  open-terminal:
    image: ghcr.io/open-webui/open-terminal
    environment:
      - OPEN_TERMINAL_API_KEY_FILE=/run/secrets/terminal_api_key
    secrets:
      - terminal_api_key

secrets:
  terminal_api_key:
    file: ./terminal_api_key.txt
```

{/* TODO: Screenshot — Docker Compose file in an editor with the secrets section highlighted. */}

---

## Image variants

Open Terminal comes in three sizes:

| | `latest` | `slim` | `alpine` |
| :--- | :--- | :--- | :--- |
| **Best for** | General use, AI agents | Smaller footprint | Smallest footprint |
| **Size** | ~4 GB | ~430 MB | ~230 MB |
| **Includes** | Node.js, Python, compilers, ffmpeg, Docker CLI, data science libs | git, curl, jq | git, curl, jq |
| **Can install packages** | ✔ (has sudo) | ✘ | ✘ |
| **Multi-user** | ✔ | ✘ | ✘ |

**If you're not sure, use `latest`.** It has everything pre-installed so the AI can work with any tool without waiting for installs.

{/* TODO: Screenshot — A visual comparison of the three image variants showing relative sizes and capabilities. */}

## Related

- [Security best practices →](./security)
- [Multi-user setup →](./multi-user)
