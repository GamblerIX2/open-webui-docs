---
sidebar_position: 30
title: "Jupyter Notebooks"
---

> [!WARNING]
> 本文档基于当前版本（0.5.16）编写，持续更新中。

# Jupyter Notebook 集成

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

从 v0.5.11 开始，Open-WebUI 发布了一个名为 `代码解释器中的 Jupyter Notebook 支持` 的新功能。该功能允许您将 Open-WebUI 与 Jupyter 集成。此后的几个版本中已对该功能进行了多次改进，请仔细查阅版本发布说明。

本教程将带您了解连接两个服务的基本设置步骤。

- [查看 v0.5.11 发布说明](https://github.com/open-webui/open-webui/releases/tag/v0.5.11)
- [查看 v0.5.15 发布说明](https://github.com/open-webui/open-webui/releases/tag/v0.5.14)

## 什么是 Jupyter Notebooks

Jupyter Notebook 是一个开源 Web 应用程序，允许用户创建和共享包含实时代码、方程式、可视化图表和叙述性文本的文档。它在数据科学、科学计算和教育领域尤其受欢迎，因为它使用户能够将可执行代码（Python、R 或 Julia 等语言）与解释性文本、图像和交互式可视化图表整合在一个文档中。Jupyter Notebooks 在数据分析和探索方面特别有用，因为它允许用户以小而可管理的代码块执行代码，同时记录思考过程和发现。这种格式使实验、调试代码以及创建全面、可共享的报告变得更加容易，这些报告既能展示分析过程又能呈现结果。

更多信息请访问 Jupyter 官网：[Project Jupyter](https://jupyter.org/)

## 第 0 步：配置摘要

以下是本教程将要完成的目标配置。

![代码执行配置](/images/tutorials/jupyter/jupyter-code-execution.png)

# 第 1 步：启动 OUI 和 Jupyter

为此，我使用了 `docker-compose` 来启动包含两个服务及 LLM 的整合栈，但分别运行各个 Docker 容器也应该可以工作。

```yaml title="docker-compose.yml"
version: "3.8"

services:
open-webui:
image: ghcr.io/open-webui/open-webui:latest
container_name: open-webui
ports:
- "3000:8080"
volumes:
- open-webui:/app/backend/data

jupyter:
image: jupyter/minimal-notebook:latest
container_name: jupyter-notebook
ports:
- "8888:8888"
volumes:
- jupyter_data:/home/jovyan/work
environment:
- JUPYTER_ENABLE_LAB=yes
- JUPYTER_TOKEN=123456

volumes:
open-webui:
jupyter_data:
```

在保存 `docker-compose` 文件的目录中运行以下命令即可启动上述服务栈：

```bash title="运行 docker-compose"
docker-compose up -d
```

现在您应该可以通过以下 URL 访问两个服务：

| 服务 | URL |
| ---------- | ----------------------- |
| Open-WebUI | `http://localhost:3000` |
| Jupyter | `http://localhost:8888` |

访问 Jupyter 服务时，您需要上面定义的 `JUPYTER_TOKEN`。本教程使用了示例令牌值 `123456`。

![代码执行配置](/images/tutorials/jupyter/jupyter-token.png)

# 第 2 步：为 Jupyter 配置代码执行

Open-WebUI 和 Jupyter 都运行后，我们需要在 Admin Panel -> Settings -> Code Execution 中配置 Open-WebUI 的代码执行以使用 Jupyter。由于 Open-WebUI 持续发布和改进该功能，建议始终查看 [`configs.py` 文件](https://github.com/open-webui/open-webui/blob/6fedd72e3973e1d13c9daf540350cd822826bf27/backend/open_webui/routers/configs.py#L72)以获取最新配置。截至 v0.5.16，包含以下配置：

| Open-WebUI 环境变量 | 值 |
| ------------------------------------- | -------------------------------- |
| `ENABLE_CODE_INTERPRETER` | True |
| `CODE_EXECUTION_ENGINE` | jupyter |
| `CODE_EXECUTION_JUPYTER_URL` | http://host.docker.internal:8888 |
| `CODE_EXECUTION_JUPYTER_AUTH` | token |
| `CODE_EXECUTION_JUPYTER_AUTH_TOKEN` | 123456 |
| `CODE_EXECUTION_JUPYTER_TIMEOUT` | 60 |
| `CODE_INTERPRETER_ENGINE` | jupyter |
| `CODE_INTERPRETER_JUPYTER_URL` | http://host.docker.internal:8888 |
| `CODE_INTERPRETER_JUPYTER_AUTH` | token |
| `CODE_INTERPRETER_JUPYTER_AUTH_TOKEN` | 123456 |
| `CODE_INTERPRETER_JUPYTER_TIMEOUT` | 60 |
| `CODE_INTERPRETER_JUPYTER_TIMEOUT` | 60 |

## 第 3 步：测试连接

首先，让我们确认 Jupyter 目录中的内容。如下图所示，我们只有一个空的 `work` 文件夹。

![代码执行配置](/images/tutorials/jupyter/jupyter-empty.png)

### 创建 CSV

让我们运行第一个提示词。确保已选择 `Code Execution` 按钮。

```txt
提示词：使用虚假数据创建两个 CSV 文件。第一个 CSV 应使用原生 Python 创建，第二个应使用 pandas 库创建。将 CSV 命名为 data1.csv 和 data2.csv
```

![代码执行配置](/images/tutorials/jupyter/jupyter-create-csv.png)

我们可以看到 CSV 文件已创建，现在可以在 Jupyter 中访问。

![代码执行配置](/images/tutorials/jupyter/jupyter-view-csv.png)

### 创建可视化图表

让我们运行第二个提示词。同样，确保已选择 `Code Execution` 按钮。

```txt
提示词：使用 matplotlib 和 seaborn 在 Python 中创建几个可视化图表并保存到 jupyter
```

![代码执行配置](/images/tutorials/jupyter/jupyter-create-viz.png)

我们可以看到可视化图表已创建，现在可以在 Jupyter 中访问。

![代码执行配置](/images/tutorials/jupyter/jupyter-view-viz.png)

### 创建 Notebook

让我们一起运行最后一个提示词。在这个提示词中，我们将仅通过提示词创建一个全新的 notebook。

```txt
提示词：编写 Python 代码来读写 JSON 文件，并将其保存到我的名为 notebook.ipynb 的 notebook 中
```

![代码执行配置](/images/tutorials/jupyter/jupyter-create-notebook.png)

我们可以看到 notebook 已创建，现在可以在 Jupyter 中访问。

![代码执行配置](/images/tutorials/jupyter/jupyter-view-notebook.png)

## 关于工作流的说明

在测试此功能时，我注意到有几次 Open-WebUI 不会自动将在 Open-WebUI 中生成的代码或输出保存到我的 Jupyter 实例。为了强制输出我创建的文件/项目，我通常采用以下两步工作流：首先创建所需的代码产物，然后要求它将其保存到我的 Jupyter 实例。

![代码执行配置](/images/tutorials/jupyter/jupyter-workflow.png)

## 您是如何使用此功能的？

您是否正在使用代码执行功能和/或 Jupyter？如果是，请联系我。我很想了解您如何使用它，以便我可以继续向本教程添加更多使用此功能的精彩示例！
