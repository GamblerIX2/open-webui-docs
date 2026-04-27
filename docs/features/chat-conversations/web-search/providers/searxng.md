---
sidebar_position: 12
title: "SearXNG"
---

:::warning

本教程来自社区贡献，并非 Open WebUI 官方支持内容。它仅作为演示，说明如何按你的具体场景自定义 Open WebUI。欢迎贡献更多内容，可查看 contributing 教程。

:::

:::tip

若要查看所有与 Web Search 相关的环境变量（包括并发设置、结果数量等），请参阅 [Environment Configuration documentation](/reference/env-configuration#web-search)。

:::

本指南说明如何在 Docker 中使用 SearXNG 为 Open WebUI 配置 web search。

## SearXNG（Docker）

> "**SearXNG is a free internet metasearch engine which aggregates results from various search services and databases. Users are neither tracked nor profiled.**"

## 1. 配置 SearXNG

若要让 SearXNG 更适合 Open WebUI 使用，请按以下步骤配置：

**第 1 步：`git clone` SearXNG Docker，并进入目录**

1. 克隆 `searxng-docker` 仓库

   克隆后会生成一个名为 `searxng-docker` 的目录，其中包含 SearXNG 配置文件。更多说明请参阅 [SearXNG documentation](https://docs.searxng.org/)。

```bash
git clone https://github.com/searxng/searxng-docker.git
```

然后进入 `searxng-docker` 目录，后续命令都在其中执行：

```bash
cd searxng-docker
```

**第 2 步：找到并修改 `.env` 文件**

1. 取消注释 `.env` 中的 `SEARXNG_HOSTNAME` 并进行设置：

```bash

# By default listen on https://localhost

# To change this:

# * uncomment SEARXNG_HOSTNAME, and replace <host> by the SearXNG hostname

# * uncomment LETSENCRYPT_EMAIL, and replace <email> by your email (require to create a Let's Encrypt certificate)

SEARXNG_HOSTNAME=localhost

# LETSENCRYPT_EMAIL=<email>

# Optional:

# If you run a very small or a very large instance, you might want to change the amount of used uwsgi workers and threads per worker

# More workers (= processes) means that more search requests can be handled at the same time, but it also causes more resource usage

# SEARXNG_UWSGI_WORKERS=4

# SEARXNG_UWSGI_THREADS=4
```

**第 3 步：修改 `docker-compose.yaml`**

3. 通过修改 `docker-compose.yaml` 去掉 `localhost` 限制：

如果 8080 端口已被占用，请在运行前把命令中的 `0.0.0.0:8080` 改成 `0.0.0.0:[available port]`。

按你的操作系统执行对应命令：

- **Linux**
```bash
sed -i 's/127.0.0.1:8080/0.0.0.0:8080/' docker-compose.yaml
```

- **macOS**
```bash
sed -i '' 's/127.0.0.1:8080/0.0.0.0:8080/' docker-compose.yaml
```

**第 4 步：授予必要权限**

4. 在项目根目录运行以下命令，让容器能够创建新的配置文件：

```bash
sudo chmod a+rwx searxng
```

**第 5 步：创建一个宽松的 `limiter.toml`**

5. 创建一个较宽松的 `searxng-docker/searxng/limiter.toml`：

*如果该文件已存在，请把缺失的内容补进去。*

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>searxng-docker/searxng/limiter.toml</summary>

```bash

# This configuration file updates the default configuration file

# See https://github.com/searxng/searxng/blob/master/searx/botdetection/limiter.toml

[botdetection.ip_limit]

# activate link_token method in the ip_limit method
link_token = false

[botdetection.ip_lists]
block_ip = []
pass_ip = []
```

</details>

**第 6 步：删除默认 `settings.yml`**

6. 如果存在默认的 `searxng-docker/searxng/settings.yml`，请先删除，因为它会在 SearXNG 首次启动时重新生成：

```bash
rm searxng/settings.yml
```

**第 7 步：重新生成 `settings.yml`**

7. 先短暂启动容器，以生成一份新的 settings.yml：

如果你当前有多个同名容器（如 caddy、redis 或 searxng），需要先在 docker-compose.yaml 中重命名它们以避免冲突。

```bash
docker compose up -d ; sleep 10 ; docker compose down
```

首次运行完成后，出于安全考虑，请在 `docker-compose.yaml` 中加入 `cap_drop: - ALL`。

如果 Open WebUI 与 Searxng 处于同一个 Docker network 中，你也可以去掉 `0.0.0.0`，仅保留端口映射；此时 Open WebUI 可直接通过容器名访问 Searxng。

<details>
<summary>docker-compose.yaml</summary>

```yaml
searxng:
    container_name: searxng
    image: docker.io/searxng/searxng:latest
    restart: unless-stopped
    networks:
      - searxng
    ports:
      - "0.0.0.0:8080:8080" # use 8080:8080 if containers are in the same Docker network
    volumes:
      - ./searxng:/etc/searxng:rw
      - searxng-data:/var/cache/searxng:rw
    environment:
      - SEARXNG_BASE_URL=https://${SEARXNG_HOSTNAME:-localhost}/
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"
    cap_drop:
      - ALL
```

</details>

**第 8 步：添加输出格式**

8. 在 `searxng-docker/searxng/settings.yml` 中加入 HTML 和 JSON 格式：

- **Linux**
```bash
sed -i 's/- html/- html\n    - json/' searxng/settings.yml
```

- **macOS**
```bash
sed -i '' 's/- html/- html\n    - json/' searxng/settings.yml
```

**第 9 步：启动服务**

9. 执行以下命令启动容器：

```bash
docker compose up -d
```

此时 searXNG 会运行在 `http://localhost:8080`（或你之前指定的端口）。

## 2. 另一种简化配置方式

如果你不想修改默认配置，也可以创建一个空的 `searxng-docker` 文件夹，然后继续后续配置步骤。

### Docker Compose 设置

将以下环境变量加入你的 Open WebUI `docker-compose.yaml`：

```yaml
services:
  open-webui:
    environment:
      ENABLE_WEB_SEARCH: True
      WEB_SEARCH_ENGINE: "searxng"
      WEB_SEARCH_RESULT_COUNT: 3
      WEB_SEARCH_CONCURRENT_REQUESTS: 10
      SEARXNG_QUERY_URL: "http://searxng:8080/search?q=<query>"
```

为 SearXNG 创建一个 `.env` 文件：

```env
# SearXNG
SEARXNG_HOSTNAME=localhost:8080/
```

接着，在 SearXNG 的 `docker-compose.yaml` 中加入以下内容：

```yaml
services:
  searxng:
    container_name: searxng
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    env_file:
      - .env
    restart: unless-stopped
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
      - DAC_OVERRIDE
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"
```

现在整个 stack 已经可以通过以下命令启动：

```bash
docker compose up -d
```

:::note

首次运行时，你必须先从 `docker-compose.yaml` 中移除 `searxng` 服务下的 `cap_drop: - ALL`，否则 SearXNG 无法成功创建 `/etc/searxng/uwsgi.ini`。原因是 `cap_drop: - ALL` 会移除所有 capability，其中也包括创建 `uwsgi.ini` 所需的权限。首次运行完成后，出于安全考虑，应重新加回 `cap_drop: - ALL`。

:::

**为 Open WebUI 集成配置 SearXNG**

容器启动后，你还需要让 SearXNG 支持 Open WebUI 所需的 JSON 查询格式：

1. 启动约 30 秒后先停止容器，以便初始配置文件生成完成：

```bash
docker compose down
```

2. 进入 `./searxng` 目录并编辑 `settings.yml`：

```bash
cd searxng
```

3. 用你喜欢的编辑器打开 `settings.yml`，找到 `search` 段落，在 formats 列表中加入 `json`：

```yaml
search:
  safe_search: 0
  autocomplete: ""
  default_lang: ""
  formats:
    - html
    - json  # Add this line to enable JSON format support for Open WebUI
```

或者你也可以用下面命令自动添加：

```bash
sed -i '/formats:/,/]/s/html/html\n    - json/' searxng/settings.yml
```

4. 保存文件后，重新启动容器：

```bash
docker compose up -d
```

:::warning

如果不加入 JSON 格式支持，SearXNG 会阻止来自 Open WebUI 的查询，你会在 Open WebUI 日志中看到 `403 Client Error: Forbidden` 错误。

:::

你也可以直接通过 `docker run` 启动 SearXNG：

```bash
docker run --name searxng --env-file .env -v ./searxng:/etc/searxng:rw -p 8080:8080 --restart unless-stopped --cap-drop ALL --cap-add CHOWN --cap-add SETGID --cap-add SETUID --cap-add DAC_OVERRIDE --log-driver json-file --log-opt max-size=1m --log-opt max-file=1 searxng/searxng:latest
```

## 3. 确认连通性

在命令行中，从 Open WebUI 容器实例验证它是否能访问 SearXNG：

```bash
docker exec -it open-webui curl http://host.docker.internal:8080/search?q=this+is+a+test+query&format=json
```

## 4. 图形界面配置

1. 前往：`Admin Panel` -> `Settings` -> `Web Search`
2. 打开 `Enable Web Search`
3. 将 `Web Search Engine` 从下拉框设为 `searxng`
4. 将 `Searxng Query URL` 设为以下格式之一：

- `http://localhost:8080/search?q=<query>`（使用宿主机与宿主机端口，适用于 Docker 部署）
- `http://searxng:8080/search?q=<query>`（使用容器名与暴露端口，适用于 Docker 部署）
- `http://host.docker.internal:8080/search?q=<query>`（使用 `host.docker.internal` DNS 名称与宿主机端口，适用于 Docker 部署）
- `http://<searxng.local>/search?q=<query>`（使用本地域名，适用于局域网访问）
- `https://<search.domain.com>/search?q=<query>`（使用自定义域名，适用于公网或私有部署）

**请注意，`/search?q=<query>` 这一部分是必需的。**

5. 根据需要调整 `Search Result Count` 与 `Concurrent Requests`
6. 保存更改

![SearXNG GUI Configuration](/images/tutorial_searxng_config.png)

:::tip Troubleshooting

如果你在 web search 上遇到问题，请查看 [Web Search Troubleshooting Guide](/troubleshooting/web-search)，其中涵盖了代理配置、连接超时和内容为空等常见问题。

:::

## 5. 在聊天中使用 Web Search

若要访问 Web Search，请点击 + 图标旁边的 Integrations 按钮。

在那里你可以切换 Web Search 的开 / 关。

![Web Search UI Toggle](/images/web_search_toggle.png)

完成以上步骤后，你就成功为 Open WebUI 配置好了 SearXNG，并能够在聊天中使用 SearXNG 引擎进行网页搜索。

#### 注意

你需要在聊天中手动显式打开 / 关闭该功能。

这是按会话生效的；例如刷新页面，或切换到另一个聊天后，该开关会自动关闭。
