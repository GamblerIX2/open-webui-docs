# 使用虚拟环境

使用 `venv` 创建隔离的 Python 环境。

## Venv 步骤

1. **创建虚拟环境：**

   ```bash
   python3 -m venv venv
   ```

2. **激活虚拟环境：**

   - 在 Linux/macOS 上：

     ```bash
     source venv/bin/activate
     ```

   - 在 Windows 上：

     ```bash
     venv\Scripts\activate
     ```

3. **安装 Open WebUI：**

   ```bash
   pip install open-webui
   ```

4. **启动服务：**

   ```bash
   open-webui serve
   ```

:::tip 出现 “open-webui: command not found”？
如果终端提示找不到命令：
1. 请确认虚拟环境已经**激活**（第 2 步）。
2. 如果仍报错，可直接通过 Python 运行：`python -m open_webui serve`
3. 如果你想把数据存到指定位置，可使用：`DATA_DIR=./data open-webui serve`
:::

## 卸载

1.  **删除虚拟环境：**
    直接删除 `venv` 文件夹即可：
    ```bash
    rm -rf venv
    ```

2.  **删除数据（警告：会删除所有数据）：**
    删除你的数据目录（通常为 `~/.open-webui`，除非你另行配置）：
    ```bash
    rm -rf ~/.open-webui
    ```
