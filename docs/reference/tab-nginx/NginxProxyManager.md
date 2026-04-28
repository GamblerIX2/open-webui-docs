# Nginx Proxy Manager

Nginx Proxy Manager（NPM）可以让你轻松管理反向代理，并使用 Let's Encrypt 的有效 SSL 证书为本地应用（如 Open WebUI）提供保护。
这种配置可以启用 HTTPS 访问；由于许多移动浏览器的安全要求，这对于使用语音输入等功能很有必要，同时又不会把应用的特定端口直接暴露到互联网。

## 前提条件

- 一台运行 Docker 的家用服务器，以及已经运行中的 open-webui 容器。
- 一个域名（可以是 DuckDNS 这类免费域名，也可以是 Namecheap/GoDaddy 这类付费域名）。
- 对 Docker 和 DNS 配置有基本了解。

## Nginx Proxy Manager 步骤

1. **创建 Nginx 文件目录：**

   ```bash
   mkdir ~/nginx_config
   cd ~/nginx_config
   ```

2. **使用 Docker 设置 Nginx Proxy Manager：**

   ```bash
   nano docker-compose.yml
   ```

```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```

启动容器：

```bash
docker-compose up -d
```

1. **配置 DNS 和域名：**

   - 登录你的域名提供商（例如 DuckDNS）并创建域名。
   - 将域名指向你的代理本地 IP（例如 `192.168.0.6`）。
   - 如果使用 DuckDNS，请从其仪表板获取 API token。

**这里有一个简单示例，展示在 [DuckDNS 域名页](https://www.duckdns.org/domains) 中如何操作**

1. **设置 SSL 证书：**

- 使用 `http://server_ip:81` 访问 Nginx Proxy Manager。例如：``192.168.0.6:81``

- 使用默认凭据登录（`admin@example.com` / `changeme`）。按提示修改它们。
- 进入 **SSL 证书 → 添加 SSL 证书 → Let's Encrypt**。
- 填写你从 DuckDNS 获得的邮箱和域名。一个域名带星号，另一个不带。例如：``*.hello.duckdns.org`` 和 ``hello.duckdns.org``。
- 选择 **使用 DNS 验证**，选择 DuckDNS，然后粘贴你的 API token。例如：
```dns_duckdns_token=f4e2a1b9-c78d-e593-b0d7-67f2e1c9a5b8```
- 同意 Let's Encrypt 条款并保存。若有需要，可调整传播时间（120 秒）。

1. **创建 Proxy Host：**

- 对于每个服务（例如 openwebui、nextcloud），进入 **主机 → 代理主机 → 添加代理主机**。

- 填入域名（例如 `openwebui.hello.duckdns.org`）。
- 协议选择 HTTP（默认），启用 ``WebSocket 支持``，并指向你的 Docker IP（如果 open-webui 和 NGINX Manager 运行在同一台机器上，这个 IP 和前面一样，例如 ``192.168.0.6``）。
- 选择之前生成的 SSL 证书，强制启用 SSL，并开启 HTTP/2。

:::danger 关键：为 WebSocket 连接配置 CORS

WebSocket 连接中非常常见、而且很难排查的问题，是跨源资源共享（CORS）策略配置错误。当你把 Open WebUI 放在 Nginx Proxy Manager 这样的反向代理后面时，**必须**在 Open WebUI 配置中设置 `CORS_ALLOW_ORIGIN` 环境变量。

如果不这样做，即使你在 Nginx Proxy Manager 中启用了 “WebSocket 支持”，WebSocket 连接也会失败。

:::

:::danger 关键：为流式传输关闭代理缓冲

**这是导致 Markdown 乱码和流式响应损坏的最常见原因。**

在 Nginx Proxy Manager 中，进入代理主机 → **高级** 选项卡 → 并在 **自定义 Nginx 配置** 字段中添加以下指令：

```nginx
proxy_buffering off;
proxy_cache off;
```

如果不这样做，Nginx 会重新分块 SSE 流，导致 Markdown 格式被打散（出现可见的 `##`、`**`、缺词等问题）。这也会让流式响应更快。

:::

:::tip 长补全的超时设置

复杂任务的长时间 LLM 补全（30 分钟以上）可能超过默认的 60 秒超时。请在 **高级** 选项卡 → **自定义 Nginx 配置** 中添加以下指令：

```nginx
proxy_read_timeout 1800;
proxy_send_timeout 1800;
proxy_connect_timeout 1800;
```

这会把超时时间设置为 30 分钟。你可以根据使用场景自行调整。

:::

:::tip 缓存最佳实践

虽然 Nginx Proxy Manager 会自动处理大部分配置，但你仍应注意：

- **静态资源**（CSS、JS、图片）默认会被缓存，以提升性能
- **认证端点** 永远不应被缓存
- 如果你在 NPM 的 “高级” 选项卡中添加自定义缓存规则，请确保排除 `/api/`、`/auth/`、`/signup/`、`/signin/`、`/sso/`、`/admin/`、`/signout/`、`/oauth/`、`/login/` 和 `/logout/` 等路径

默认的 NPM 配置已经正确处理了这些情况——只有在你非常清楚自己在做什么时，才去修改缓存规则。

:::

**示例：**
如果你通过 `https://openwebui.hello.duckdns.org` 访问界面，那么必须设置：

```bash
CORS_ALLOW_ORIGIN="https://openwebui.hello.duckdns.org"
```

你也可以提供一个以分号分隔的允许域名列表。**不要跳过这一步。**

:::

1. **把你的 URL 添加到 open-webui（否则会出现 HTTPS 错误）：**

- 进入 open-webui → 管理面板 → 设置 → 常规
- 在 **Webhook URL** 文本框中输入你通过 Nginx 反向代理连接 open-webui 所用的 URL。例如：``hello.duckdns.org``（在这种配置下不是必需）或 ``openwebui.hello.duckdns.org``（在这种配置下是必需的）。

### 访问 WebUI

你可以通过 HTTPS 访问 Open WebUI，例如 ``hello.duckdns.org`` 或 ``openwebui.hello.duckdns.org``（按你的实际配置而定）。

:::note

防火墙提示：请注意，本地防火墙软件（如 Portmaster）可能会阻止 Docker 内部网络流量或所需端口。如果遇到问题，请检查防火墙规则，确保此配置所需的通信已被允许。

:::
