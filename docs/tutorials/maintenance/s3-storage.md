---
sidebar_position: 40
title: "S3 存储"
---

# 🪣 切换到 S3 存储

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

本指南介绍如何将 Open WebUI 配置中默认的 `local` 存储切换为 Amazon S3。

## 前提条件

在学习本教程之前，您需要具备以下条件：

- 一个有效的 AWS 账户
- 有效的 AWS Access Key 和 Secret Key
- 在 AWS 中具有创建 S3 存储桶并上传对象的 IAM 权限
- 已在系统上安装 Docker

## 什么是 Amazon S3

直接引用 AWS 官网的说明：

"Amazon S3 是一项对象存储服务，具有业界领先的可扩展性、数据可用性、安全性和性能。可存储和保护任意数量的数据，适用于数据湖、网站、云原生应用、备份、归档、机器学习和分析等各类使用场景。Amazon S3 专为 99.999999999%（11 个 9）的持久性而设计，为全球数百万客户存储数据。"

了解更多关于 S3 的信息，请访问：[Amazon S3 官方页面](https://aws.amazon.com/s3/)

# 配置方法

## 1. 所需环境变量

要配置此选项，需要收集以下环境变量：

| **Open-WebUI 环境变量** | **示例值** |
|-------------------------------------|---------------------------------------------|
| `S3_ACCESS_KEY_ID`                  | ABC123                                      |
| `S3_SECRET_ACCESS_KEY`              | SuperSecret                                 |
| `S3_ENDPOINT_URL`                   | https://s3.us-east-1.amazonaws.com          |
| `S3_REGION_NAME`                    | us-east-1                                   |
| `S3_BUCKET_NAME`                    | my-awesome-bucket-name                      |

- S3_ACCESS_KEY_ID：您 AWS 账户访问密钥的标识符，可在 AWS 管理控制台或 AWS CLI 中创建访问密钥时获取。
- S3_SECRET_ACCESS_KEY：AWS 访问密钥对的密钥部分，在 AWS 中创建访问密钥时提供，请妥善保存。
- S3_ENDPOINT_URL：指向 S3 服务端点的 URL，通常可在 AWS 服务文档或账户设置中找到。
- S3_REGION_NAME：S3 存储桶所在的 AWS 区域，例如 "us-east-1"，可在 AWS 管理控制台的 S3 存储桶详情中查看。
- S3_BUCKET_NAME：您在 AWS 中创建存储桶时指定的唯一名称。

有关可用 S3 端点 URL 的完整列表，请参阅：[Amazon S3 常规端点](https://docs.aws.amazon.com/general/latest/gr/s3.html)

有关所有 `云存储` 配置选项，请参阅 [Open-WebUI 云存储配置](https://docs.openwebui.com/reference/env-configuration#cloud-storage) 文档。

## 2. 运行 Open-WebUI

在启动 Open-WebUI 实例之前，还需要设置一个名为 `STORAGE_PROVIDER` 的环境变量。该变量告知 Open-WebUI 您要使用的存储提供商。默认情况下，`STORAGE_PROVIDER` 为空，即 Open-WebUI 使用本地存储。

| **存储提供商** | **类型** | **描述** | **默认值** |
|----------------------|----------|-------------------------------------------------------------------------------------------------|-------------|
| `local`              | str      | 提供空字符串（`' '`）时默认使用本地存储                                | 是         |
| `s3`                 | str      | 使用 S3 客户端库及 Amazon S3 存储中提到的相关环境变量         | 否          |
| `gcs`                | str      | 使用 GCS 客户端库及 Google Cloud Storage 中提到的相关环境变量     | 否          |

要使用 Amazon S3，需要将 `STORAGE_PROVIDER` 设置为 "S3"，并配置步骤 1 中收集的所有环境变量（`S3_ACCESS_KEY_ID`、`S3_SECRET_ACCESS_KEY`、`S3_ENDPOINT_URL`、`S3_REGION_NAME`、`S3_BUCKET_NAME`）。

这里还将 `ENV` 设置为 "dev"，这样可以查看 Open-WebUI 的 Swagger 文档，以便进一步测试并确认 S3 存储配置是否正常工作。

```sh
docker run -d \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  -e STORAGE_PROVIDER="s3" \
  -e S3_ACCESS_KEY_ID="ABC123" \
  -e S3_SECRET_ACCESS_KEY="SuperSecret" \
  -e S3_ENDPOINT_URL="https://s3.us-east-1.amazonaws.com" \
  -e S3_REGION_NAME="us-east-1" \
  -e S3_BUCKET_NAME="my-awesome-bucket-name" \
  -e ENV="dev" \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

## 3. 测试配置

现在 Open-WebUI 已经运行，让我们上传一个简单的 `Hello, World` 文本文件来测试配置。

![在 Open-WebUI 中上传文件](/images/tutorials/amazon-s3/amazon-s3-upload-file.png)

并确认我们能从所选 LLM 获得响应。

![在 Open-WebUI 中获取响应](/images/tutorials/amazon-s3/amazon-s3-oui-response.png)

很好！看起来 Open-WebUI 中的一切都按预期运行了。现在让我们验证文本文件是否确实已上传并存储在指定的 S3 存储桶中。通过 AWS 管理控制台可以看到，S3 存储桶中现在有一个文件。除了我们上传的文件名（`hello.txt`）外，还可以看到对象名称后面附加了一个唯一 ID。这就是 Open-WebUI 追踪所有已上传文件的方式。

![在 Open-WebUI 中获取响应](/images/tutorials/amazon-s3/amazon-s3-object-in-bucket.png)

使用 Open-WebUI 的 Swagger 文档，我们可以通过 `/api/v1/files/{id}` 端点并传入唯一 ID（4405fabb-603e-4919-972b-2b39d6ad7f5b）获取该文件的所有相关信息。

![Inspect the file by ID](/images/tutorials/amazon-s3/amazon-s3-get-file-by-id.png)
