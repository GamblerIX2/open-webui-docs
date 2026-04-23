# 使用 Conda 安装

1. **创建 Conda 环境：**

   ```bash
   conda create -n open-webui python=3.11
   ```

2. **激活环境：**

   ```bash
   conda activate open-webui
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
1. 请确认 Conda 环境已经**激活**（`conda activate open-webui`）。
2. 如果仍报错，可以直接通过 Python 运行：`python -m open_webui serve`
3. 如果你想把数据存到指定位置，可使用（Linux/Mac）：`DATA_DIR=./data open-webui serve`；或（Windows）：`$env:DATA_DIR=".\data"; open-webui serve`
:::

## 卸载

1.  **删除 Conda 环境：**
    ```bash
    conda remove --name open-webui --all
    ```

2.  **删除数据（警告：会删除所有数据）：**
    删除你的数据目录（通常是 `~/.open-webui`，除非你另行配置）：
    ```bash
    rm -rf ~/.open-webui
    ```
