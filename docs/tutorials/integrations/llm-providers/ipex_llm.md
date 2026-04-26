---
sidebar_position: 30
title: "Intel GPU (IPEX-LLM)"
---

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

:::note

本指南已通过[手动安装](/getting-started/)方式搭建的 Open WebUI 进行验证。

:::

## 在 Intel GPU 上使用 IPEX-LLM 进行本地 LLM 设置

:::info

[**IPEX-LLM**](https://github.com/intel-analytics/ipex-llm) 是一个用于在 Intel CPU 和 GPU（例如，配有集成显卡的本地 PC、Arc A 系列、Flex 和 Max 等独立显卡）上以极低延迟运行 LLM 的 PyTorch 库。

:::

本教程演示如何将 Open WebUI 与**在 Intel GPU 上运行的 IPEX-LLM 加速 Ollama 后端**配合使用。按照本指南，您甚至可以在低成本 PC（即仅有集成显卡）上流畅地设置 Open WebUI。

## 在 Intel GPU 上启动 Ollama 服务

请参阅 IPEX-LLM 官方文档中的[此指南](https://ipex-llm.readthedocs.io/en/latest/doc/LLM/Quickstart/ollama_quickstart.html)，了解如何在 Intel GPU 上安装和运行由 IPEX-LLM 加速的 Ollama 服务。

:::tip

如果您希望从另一台机器访问 Ollama 服务，请在执行 `ollama serve` 命令前确保设置或导出环境变量 `OLLAMA_HOST=0.0.0.0`。

:::

## 配置 Open WebUI

通过菜单中的 **Settings -> Connections** 访问 Ollama 设置。默认情况下，**Ollama Base URL** 预设为 <https://localhost:11434> ，如下图所示。要验证 Ollama 服务连接状态，点击文本框旁边的**刷新按钮**。如果 WebUI 无法与 Ollama 服务器建立连接，您将看到错误消息 `WebUI could not connect to Ollama`。

![Open WebUI Ollama 设置失败](https://llm-assets.readthedocs.io/en/latest/_images/open_webui_settings_0.png)

如果连接成功，您将看到提示 `Service Connection Verified`，如下图所示。

![Open WebUI Ollama 设置成功](https://llm-assets.readthedocs.io/en/latest/_images/open_webui_settings.png)

:::tip

如果您想使用托管在不同 URL 的 Ollama 服务器，只需将 **Ollama Base URL** 更新为新 URL，然后按**刷新**按钮重新确认与 Ollama 的连接。

:::
