---
sidebar_position: 10
title: "Unraid 部署（新手友好）"
---

# 在 Unraid 上部署 Open WebUI（新手友好）

:::warning

本教程由社区贡献，不属于 Open WebUI 团队官方支持范围。内容仅用于演示如何根据你的特定场景自定义 Open WebUI。想参与贡献？请查看[贡献教程](/tutorials/contributing-tutorial)。

:::

本指南面向第一次使用 Unraid 的用户，目标是实现稳定的 Docker 部署、持久化数据和安全升级。

## 你将完成什么

- 在 Unraid 中创建 Open WebUI 容器。
- 为 `/app/backend/data` 配置持久化存储。
- 将 Open WebUI 连接到 Ollama。
- 在不丢失数据的情况下升级 Open WebUI。
- 排查反向代理与持久化相关问题。

## 开始前准备

- 已在 Unraid 中启用 Docker。
- 已准备持久化 appdata 路径，例如：`/mnt/user/appdata/open-webui`。
- 可选：Ollama 运行在以下位置之一：
  - Unraid 主机本机；或
  - 可连通的其他机器。

:::important
务必将 `/app/backend/data` 持久化到宿主机路径。若跳过此步骤，重建容器后聊天记录和设置可能丢失。
:::

## 1. 在 Unraid 中创建容器

在 **Docker > Add Container** 中使用以下配置：

| 字段 | 值 |
| --- | --- |
| Name | `open-webui` |
| Repository | `ghcr.io/open-webui/open-webui:main` |
| Network Type | `bridge` |
| Restart Policy | `always` |
| Container Port | `8080` |
| Host Port | `3000`（或其他空闲端口） |

添加路径映射：

| 配置类型 | 容器路径 | 宿主机路径 |
| --- | --- | --- |
| Path | `/app/backend/data` | `/mnt/user/appdata/open-webui` |

## 2. 配置 Ollama 连接

请选择一种方式。

### Ollama 运行在 Unraid 主机

- 额外参数：
  - `--add-host=host.docker.internal:host-gateway`
- 环境变量：
  - `OLLAMA_BASE_URL=http://host.docker.internal:11434`

### Ollama 运行在其他机器

- 环境变量：
  - `OLLAMA_BASE_URL=http://<ollama-lan-ip>:11434`

### Ollama 运行在其他容器

- 将两个容器放到同一个自定义 Docker 网络。
- 设置：
  - `OLLAMA_BASE_URL=http://<ollama-container-name>:11434`

## 3. 首次启动验证

1. 启动容器。
2. 打开 `http://<unraid-ip>:3000`。
3. 完成初始化管理员设置。
4. 进入 **Settings > Admin Settings > Connections**，确认 Ollama 端点配置正确。
5. 确认模型选择器中能看到模型。

## 4. 持久化卷注意事项

- Open WebUI 状态数据存储在 `/app/backend/data`。
- 在 Unraid 模板中设置固定的 `WEBUI_SECRET_KEY`，并在重建容器时保持不变，以避免不必要的会话失效。
- 在更新或重建时保持宿主机映射路径一致。
- 使用目录映射，不要使用文件映射。
- 如持久化失败，请检查 `/mnt/user/appdata/open-webui` 目录权限。

## 5. 升级步骤（安全流程）

1. 备份 `/mnt/user/appdata/open-webui`。
2. 确保模板中的 `WEBUI_SECRET_KEY` 保持不变。
3. 更新或拉取新的 Open WebUI 镜像标签。
4. 使用相同模板和相同 `/app/backend/data` 映射重建容器。
5. 验证聊天记录和设置是否完整。
6. 如有需要，回滚到旧镜像并恢复备份。

更多升级方式请参阅 [Updating Open WebUI](/getting-started/updating)。

## 故障排查

### 无法连接 Ollama

现象：
- `Connection error` in Open WebUI
- 模型无法加载

检查项：
- 确认在 Open WebUI 容器内可访问 `OLLAMA_BASE_URL`。
- 若使用主机上的 Ollama，确认已配置 `--add-host=host.docker.internal:host-gateway`。
- 若 `host.docker.internal` 解析失败，请改用 Unraid 主机的局域网 IP。

### `host.docker.internal` 无法解析

- Add `--add-host=host.docker.internal:host-gateway`.
- 保存模板改动后重启容器。
- 兜底方案：`OLLAMA_BASE_URL=http://<unraid-lan-ip>:11434`。

### 反向代理子路径问题（`/openwebui`）

现象：
- 登录页或静态资源返回 `404`
- WebSocket 断开或长期停留在加载状态

- 确保代理正确转发 WebSocket 升级头。
- 确保子路径路由策略一致（转发前去掉或重写前缀）。
- 设置不带末尾斜杠的 `WEBUI_URL`，例如：
  - `WEBUI_URL=https://example.com/openwebui`
- 若子路径方案仍不稳定，建议改用子域名：
  - `WEBUI_URL=https://ai.example.com`

更多反向代理排障方法请参阅 [Connection Errors](/troubleshooting/connection-error)。

### 更新或重建后数据丢失

- 确认映射是否严格为 `/app/backend/data` 指向持久化宿主机目录。
- 确认没有因路径拼写错误创建第二个空目录。
- 确认 Unraid 权限允许读写。
