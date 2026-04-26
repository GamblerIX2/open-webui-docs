---
sidebar_position: 30
title: "LibreTranslate"
---

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

## 概述

LibreTranslate 是一个免费开源的机器翻译 API，支持多种语言。LibreTranslate 可自托管、支持离线使用且易于安装，与其他 API 不同，它不依赖 Google 或 Azure 等专有服务商进行翻译。其翻译引擎由开源的 [Argos Translate](https://github.com/argosopentech/argos-translate) 库驱动。您可以将 LibreTranslate 与 Open WebUI 集成以利用其机器翻译功能。本文档提供了在 Docker 中设置 LibreTranslate 并在 Open WebUI 中配置集成的分步指南。

## 在 Docker 中设置 LibreTranslate

按照以下步骤在 Docker 中设置 LibreTranslate：

### 第 1 步：创建 Docker Compose 文件

在您选择的目录中创建一个名为 `docker-compose.yml` 的新文件，并添加以下配置：

```yml
services:
  libretranslate:
    container_name: libretranslate
    image: libretranslate/libretranslate:v1.6.0
    restart: unless-stopped
    ports:
      - "5000:5000"
    env_file:
      - stack.env
    volumes:
      - libretranslate_api_keys:/app/db
      - libretranslate_models:/home/libretranslate/.local:rw
    tty: true
    stdin_open: true
    healthcheck:
      test: ['CMD-SHELL', './venv/bin/python scripts/healthcheck.py']

volumes:
  libretranslate_models:
  libretranslate_api_keys:
```

### 第 2 步：创建 `stack.env` 文件

在与 `docker-compose.yml` 文件相同的目录中创建名为 `stack.env` 的新文件，并添加以下配置：

```bash

# LibreTranslate
LT_DEBUG="false"
LT_UPDATE_MODELS="true"
LT_SSL="false"
LT_SUGGESTIONS="false"
LT_METRICS="false"
LT_HOST="0.0.0.0"

LT_API_KEYS="false"

LT_THREADS="12"
LT_FRONTEND_TIMEOUT="2000"
```

### 第 3 步：运行 Docker Compose 文件

运行以下命令启动 LibreTranslate 服务：

```bash
docker-compose up -d
```

这将以分离模式启动 LibreTranslate 服务。

## 在 Open WebUI 中配置集成

在 Docker 中启动并运行 LibreTranslate 后，您可以在 Open WebUI 中配置集成。目前有多个社区集成可供选择，包括：

- [LibreTranslate Filter Function](https://openwebui.com/posts/4993ae7e-bd2a-41dc-9e88-9941854495cc)
- [LibreTranslate Action Function](https://openwebui.com/posts/103a14c1-174a-4445-bb9b-d48640e43b07)
- [MultiLanguage LibreTranslate Action Function](https://openwebui.com/posts/f250971e-8163-4a0b-a30c-45fdfb2ba4f8)
- [LibreTranslate Filter Pipeline](https://github.com/open-webui/pipelines/blob/main/examples/filters/libretranslate_filter_pipeline.py)

选择最适合您需求的集成，并按照说明在 Open WebUI 中进行配置。

LibreTranslate pipeline 和 function 支持的语言：
基本上涵盖 LibreTranslate 中的所有语言，以下是列表：

```txt
Albanian, Arabic, Azerbaijani, Bengali, Bulgarian, Catalan, Valencian, Chinese, Czech, Danish, Dutch, English, Flemish, Esperanto, Estonian, Finnish, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Irish, Italian, Japanese, Korean, Latvian, Lithuanian, Malay, Persian, Polish, Portuguese, Romanian, Moldavian, Moldovan, Russian, Slovak, Slovenian, Spanish, Castilian, Swedish, Tagalog, Thai, Turkish, Ukrainian, Urdu
```

## 故障排除

- 确保 LibreTranslate 服务正在运行且可访问。
- 验证 Docker 配置是否正确。
- 检查 LibreTranslate 日志是否有任何错误。

## Benefits of Integration

Integrating LibreTranslate with Open WebUI provides several benefits, including:

- Machine translation capabilities for a wide range of languages.
- Improved text analysis and processing.
- Enhanced functionality for language-related tasks.

## Conclusion

Integrating LibreTranslate with Open WebUI is a straightforward process that can enhance the functionality of your Open WebUI instance. By following the steps outlined in this documentation, you can set up LibreTranslate in Docker and configure the integration within Open WebUI.
