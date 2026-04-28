---
sidebar_position: 4
title: "Mistral OCR"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

## 👁️ Mistral OCR

本文提供一个逐步指南，说明如何将 Mistral OCR 集成到 Open WebUI 中。Mistral OCR 是一个光学字符识别工具，专门用于从多种基于图像的文件格式中提取文本——包括扫描版 PDF、图片和手写文档——并将其转换为 JSON 或纯文本等结构化数据。它支持多语言文本识别、版面分析与手写内容理解，能够以强大且可定制的方式简化 AI 文档搜索、总结与数据提取流程。

## 前提条件

- Open WebUI 实例
- Mistral AI 账号

## 集成步骤

### 第 1 步：注册或登录 Mistral AI Console

- 前往 `https://console.mistral.ai`
- 按页面提示完成流程
- 授权成功后，你应该能进入控制台首页

### 第 2 步：生成 API 密钥

- 前往 `API 密钥` 或 `https://console.mistral.ai/api-keys`
- 创建一个新的密钥，并务必复制保存

### 第 3 步：配置 Open WebUI 使用 Mistral OCR

- 登录你的 Open WebUI 实例
- 进入 `管理面板`
- 点击 `设置`
- 打开 `文档` 标签
- 将 `默认` 内容提取引擎下拉框切换为 `Mistral OCR`
- 在对应字段中粘贴 API 密钥
- 保存管理面板设置

## 验证 Mistral OCR

若要通过脚本验证 Mistral OCR 是否工作正常，请参阅 `https://docs.mistral.ai/capabilities/document/`

### 结论

将 Mistral OCR 集成到 Open WebUI，是增强文档处理与内容提取能力的一种简单而有效的方法。按照本指南完成配置后，你就可以把 Mistral OCR 设为默认提取引擎，并利用其先进的文本识别能力。配置完成后，Mistral OCR 将为 Open WebUI 提供强大的多语言文档解析能力，支持多种格式，并显著增强 AI 驱动的文档分析能力。
