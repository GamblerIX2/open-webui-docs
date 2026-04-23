### 使用 `uv` 安装

`uv` 运行时管理器可以为 Open WebUI 这类应用提供顺畅的 Python 环境管理。按以下步骤开始：

#### 1. 安装 `uv`

根据你的操作系统选择合适的安装命令：

- **macOS/Linux**：

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows**：

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

#### 2. 运行 Open WebUI

安装好 `uv` 后，就可以直接运行 Open WebUI。建议设置 `DATA_DIR`，避免数据丢失。下面分别给出了各平台示例：

- **macOS/Linux**：

  ```bash
  DATA_DIR=~/.open-webui uvx --python 3.11 open-webui@latest serve
  ```

- **Windows**（PowerShell）：

  ```powershell
  $env:DATA_DIR="C:\open-webui\data"; uvx --python 3.11 open-webui@latest serve
  ```

:::tip 为什么要设置 DATA_DIR？
设置 `DATA_DIR` 可以确保你的聊天与设置保存到可预期的位置。如果不设置，`uvx` 可能会把数据放在进程结束后就被清理掉的临时目录中。
:::

## 卸载

如果你是通过 `uvx` 运行 Open WebUI，可按以下方式移除：

1.  **停止服务：**
    在运行它的终端中按 `Ctrl+C`。

2. **从 UV 中卸载：**
    运行 `uv tool uninstall open-webui`

3.  **可用的清理命令：**
    `uvx` 会以临时方式或从缓存中运行应用。如需移除缓存组件：
    ```bash
    uv cache clean
    ```

4.  **删除数据（警告：会删除所有数据）：**
    删除你的数据目录（默认为 `~/.open-webui`，或你在 `DATA_DIR` 中指定的路径）：
    ```bash
    rm -rf ~/.open-webui
    ```
