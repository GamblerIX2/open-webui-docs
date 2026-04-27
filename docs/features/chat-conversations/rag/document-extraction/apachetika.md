---
sidebar_position: 2
title: "Apache Tika 提取"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 🪶 Apache Tika 提取

本文提供一个逐步指南，说明如何将 Apache Tika 集成到 Open WebUI 中。Apache Tika 是一个内容分析工具包，可用于检测并提取一千多种文件类型中的元数据与文本内容。所有这些文件类型都可通过统一接口解析，因此 Tika 在搜索引擎索引、内容分析、翻译等场景中都非常有用。

## 前提条件

- Open WebUI 实例
- 已在系统中安装 Docker
- 已为 Open WebUI 准备 Docker network

# 集成步骤

### 第 1 步：创建 Apache Tika 的 Docker Compose 文件，或直接运行 Docker 命令

你有两种方式运行 Apache Tika：

**方式 1：使用 Docker Compose**

在与你的 Open WebUI 实例相同目录下创建一个名为 `docker-compose.yml` 的新文件，并加入以下配置：

```yml
services:
  tika:
    image: apache/tika:latest-full
    container_name: tika
    ports:
      - "9998:9998"
    restart: unless-stopped
```

然后执行以下命令启动：

```bash
docker-compose up -d
```

**方式 2：使用 Docker Run 命令**

你也可以直接运行以下命令启动 Apache Tika：

```bash
docker run -d --name tika \
  -p 9998:9998 \
  --restart unless-stopped \
  apache/tika:latest-full
```

请注意：如果你选择使用 Docker run，并且希望让该容器与 Open WebUI 处于同一个网络中，则需要显式加上 `--network` 参数。

### 第 2 步：配置 Open WebUI 使用 Apache Tika

若要在 Open WebUI 中把 Apache Tika 作为上下文提取引擎，请按以下步骤操作：

- 登录你的 Open WebUI 实例
- 进入 `Admin Panel`
- 点击 `Settings`
- 打开 `Documents` 标签
- 将 `Default` 内容提取引擎下拉框切换为 `Tika`
- 将上下文提取引擎 URL 更新为 `http://tika:9998`
- 保存更改

## 在 Docker 中验证 Apache Tika

若要验证 Apache Tika 在 Docker 环境中是否正常工作，可按以下步骤进行：

### 1. 启动 Apache Tika Docker 容器

首先，确保 Apache Tika Docker 容器已经运行。你可以使用以下命令启动：

```bash
docker run -p 9998:9998 apache/tika
```

此命令会启动 Apache Tika 容器，并将容器的 9998 端口映射到本机的 9998 端口。

### 2. 验证服务是否正常运行

你可以通过发送 GET 请求来验证 Apache Tika 服务是否已启动：

```bash
curl -X GET http://localhost:9998/tika
```

此命令应返回以下响应：

```txt
This is Tika Server. Please PUT
```

### 3. 验证集成

你也可以尝试发送一个文件进行分析，以测试集成是否正常。可以用以下 `curl` 命令测试 Apache Tika：

```bash
curl -T test.txt http://localhost:9998/tika
```

请将 `test.txt` 替换为你本机上一份实际文本文件的路径。

Apache Tika 会返回该文件的已检测元数据和内容类型。

### 使用脚本验证 Apache Tika

如果你想把验证流程自动化，下面这个脚本会向 Apache Tika 发送一个文件，并检查返回结果中是否包含预期元数据。若元数据存在，脚本会输出成功信息和文件元数据；否则会输出错误信息以及 Apache Tika 的响应。

```python
import requests

def verify_tika(file_path, tika_url):
    try:
        # Send the file to Apache Tika and verify the output
        response = requests.put(tika_url, files={'file': open(file_path, 'rb')})

        if response.status_code == 200:
            print("Apache Tika successfully analyzed the file.")
            print("Response from Apache Tika:")
            print(response.text)
        else:
            print("Error analyzing the file:")
            print(f"Status code: {response.status_code}")
            print(f"Response from Apache Tika: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = "test.txt"  # Replace with the path to your file
    tika_url = "http://localhost:9998/tika"

    verify_tika(file_path, tika_url)
```

运行该脚本的说明如下：

### 前提条件

- 系统中已安装 Python 3.x
- 已安装 `requests` 库（可通过 `pip install requests` 安装）
- Apache Tika Docker 容器已运行（例如使用 `docker run -p 9998:9998 apache/tika` 启动）
- 将 `"test.txt"` 替换为你要发送给 Apache Tika 的文件路径

### 运行脚本

1. 将脚本保存为 `verify_tika.py`（例如使用 Notepad 或 Sublime Text）
2. 打开终端或命令提示符
3. 使用 `cd` 命令进入脚本所在目录
4. 执行 `python verify_tika.py`
5. 脚本将输出 Apache Tika 是否工作正常的结果

:::note

注意：如果你遇到问题，请确认 Apache Tika 容器运行正常，并且文件确实被发送到了正确 URL。

:::

### 小结

按照以上步骤，你就可以验证 Apache Tika 是否在 Docker 环境中正常工作。你可以通过上传文件进行分析、通过 GET 请求验证服务状态，或者使用脚本自动化验证流程。如果遇到问题，请确保 Apache Tika 容器运行正常，并确认文件发送地址无误。

## 故障排查

- 确保 Apache Tika 服务正在运行，并且 Open WebUI 实例可以访问它
- 查看 Docker logs，确认 Apache Tika 服务没有报错
- 确认 Open WebUI 中配置的上下文提取引擎 URL 正确无误

## 集成优势

将 Apache Tika 集成到 Open WebUI 可带来以下优势：

- **更强的元数据提取能力**：Apache Tika 在提取准确、相关元数据方面能力更强
- **支持多种文件格式**：Apache Tika 支持大量文件格式，非常适合需要处理多样文档类型的组织
- **增强内容分析能力**：Apache Tika 的高级内容分析能力可以帮助你从文件中提取更多有价值的信息

## 结论

将 Apache Tika 集成到 Open WebUI 是一个相对直接的过程，并且能够显著增强 Open WebUI 实例的元数据提取能力。按照本文步骤操作后，你就可以轻松将 Apache Tika 设置为上下文提取引擎。
