### 使用 pip 安装

这是通过 Python 安装 Open WebUI 最简单的方式。

#### 1. 安装 Open WebUI

```bash
pip install open-webui
```

#### 2. 启动服务

```bash
open-webui serve
```

Open WebUI 现在运行在 [http://localhost:8080](http://localhost:8080)。

:::tip 出现 “open-webui: command not found”？
1. 如果你使用了虚拟环境，请确认它已经激活。
2. 也可以直接这样运行：`python -m open_webui serve`
3. 如果你想把数据存到指定位置：`DATA_DIR=./data open-webui serve`
:::

## 卸载

1. **卸载包：**
    ```bash
    pip uninstall open-webui
    ```

2. **删除数据（可选，会删除所有数据）：**
    ```bash
    rm -rf ~/.open-webui
    ```
