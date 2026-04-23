## 在 WSL（Windows Subsystem for Linux）中使用 Docker

本指南介绍如何在 Windows Subsystem for Linux（WSL）环境中安装 Docker 并运行 Open WebUI。

### 第 1 步：安装 WSL

如果你还没有安装 WSL，请参考 Microsoft 官方文档：

[安装 WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

### 第 2 步：安装 Docker Desktop

Docker Desktop 是在 WSL 环境中运行 Docker 最简单的方式。它会自动处理 Windows 与 WSL 之间的集成。

1.  **下载 Docker Desktop：**
    [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

2.  **安装 Docker Desktop：**
    按照安装步骤完成，并在安装过程中确保选择 “WSL 2” 后端。

### 第 3 步：为 WSL 配置 Docker Desktop

1.  **打开 Docker Desktop：**
    启动 Docker Desktop 应用。

2.  **启用 WSL Integration：**
    - 打开 **Settings > Resources > WSL Integration**。
    - 确保勾选 “Enable integration with my default WSL distro”。
    - 如果你使用的不是默认 WSL 发行版，请在列表中单独勾选。

### 第 4 步：运行 Open WebUI

现在，你就可以在 WSL 终端里按标准 Docker 方式运行 Open WebUI：

```bash
docker pull ghcr.io/open-webui/open-webui:main
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

### 重要说明

- **在 WSL 中运行 Docker 命令：**
  请始终从 WSL 终端中执行 `docker` 命令，而不是 PowerShell 或 Command Prompt。

- **文件系统访问：**
  使用卷挂载（`-v`）时，请确认对应路径对当前 WSL 发行版可访问。
