---
sidebar_position: 200
title: "使用 Nginx 的 HTTPS"
---

<!-- markdownlint-disable MD060 -->

## 使用 Nginx 的 HTTPS

确保用户与 Open WebUI 之间的通信安全至关重要。HTTPS（HyperText Transfer Protocol Secure）会对传输数据进行加密，防止窃听和篡改。通过将 Nginx 配置为反向代理，你可以轻松为 Open WebUI 部署添加 HTTPS，同时提升安全性和可信度。

本指南提供三种设置 HTTPS 的方式：

- **自签名证书**：适合开发和内部使用，使用 Docker。
- **Let's Encrypt**：适合需要受信任 SSL 证书的生产环境，使用 Docker。
- **Windows + 自签名证书**：面向 Windows 上的开发和内部使用的简化说明，无需 Docker。

:::danger 关键：为 WebSocket 连接配置 CORS

WebSocket 连接中一个非常常见、而且很难排查的问题，是跨源资源共享（CORS）策略配置错误。当你把 Open WebUI 放在像 Nginx Proxy Manager 这样的反向代理后面时，**必须**在 Open WebUI 配置中设置 `CORS_ALLOW_ORIGIN` 环境变量。

如果不这样做，即使你在 Nginx Proxy Manager 中启用了 “Websockets support”，WebSocket 连接也会失败。

### HTTP/2 与 WebSockets

如果你在 Nginx 服务器上启用了 **HTTP/2**，请确保代理配置在连接 Open WebUI 后端时仍然使用 **HTTP/1.1**。这点非常重要，因为大多数 WebUI 功能（如流式传输和实时更新）都依赖 WebSocket，而在许多代理环境中，通过 HTTP/1.1 的 `Upgrade` 方式会比新的 RFC 8441（H2 上的 WebSocket）更稳定。

在 Nginx 的 location 块中，始终加入：

```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

:::

:::danger 关键：为 SSE 流式传输关闭代理缓冲

**这是导致 Markdown 乱码和流式响应损坏的最常见原因。**

当 Nginx 的 `proxy_buffering` 处于启用状态（默认就是启用！）时，它会随意重新分块 SSE 流。这会把 Markdown 标记拆散——例如 `**bold**` 会变成 `**` + `bold` + `**`——从而导致输出损坏，出现可见的 `##`、`**` 或缺词。

**你必须在 Nginx 的 location 块中加入以下指令：**

```nginx
# CRITICAL: Disable buffering for SSE streaming
proxy_buffering off;
proxy_cache off;
```

**如果忘了这一步，典型症状包括：**

- 原始 Markdown 标记可见（`##`、`**`、`###`）
- 粗体/标题标记显示异常
- 响应中随机缺少单词或段落
- 关闭缓冲时正常，开启时就出问题

**额外好处：** 关闭缓冲后，流式响应还会**明显更快**，因为内容会直接流向客户端，不再经过 Nginx 的缓冲延迟。

:::

请选择最适合你部署需求的方法。

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import NginxProxyManager from '../tab-nginx/NginxProxyManager.md';
import SelfSigned from '../tab-nginx/SelfSigned.md';
import LetsEncrypt from '../tab-nginx/LetsEncrypt.md';
import Windows from '../tab-nginx/Windows.md';

<!-- markdownlint-disable-next-line MD033 -->
<Tabs>
    <TabItem value="NginxProxyManager" label="Nginx Proxy Manager">
    <NginxProxyManager />
  </TabItem>
  <TabItem value="letsencrypt" label="Let's Encrypt">
    <LetsEncrypt />
  </TabItem>
    <TabItem value="selfsigned" label="自签名证书">
    <SelfSigned />
  </TabItem>
  <TabItem value="windows" label="Windows">
    <Windows />
  </TabItem>
</Tabs>

## 完整的优化版 NGINX 配置

本节提供一个适用于生产环境的 NGINX 配置，专门针对 Open WebUI 的流式传输、WebSocket 连接以及高并发部署进行了优化。

### 上游配置

定义一个带 keepalive 连接的 upstream，以降低连接建立开销：

```nginx
upstream openwebui {
    server 127.0.0.1:3000;
    keepalive 128;              # Persistent connections
    keepalive_timeout 1800s;    # 30 minutes
    keepalive_requests 10000;
}
```

### 超时配置

长时间运行的 LLM 补全需要更长的超时时间：

```nginx
location /api/ {
    proxy_connect_timeout 1800;   # 30 minutes
    proxy_send_timeout 1800;
    proxy_read_timeout 1800;
}

# WebSocket connections need even longer timeouts
location ~ ^/(ws/|socket\.io/) {
    proxy_connect_timeout 86400;  # 24 hours
    proxy_send_timeout 86400;
    proxy_read_timeout 86400;
}
```

### 请求头和请求体大小限制

防止大请求或 OAuth token 导致错误：

```nginx
# In http {} or server {} block
client_max_body_size 100M;           # Large file uploads
proxy_buffer_size 128k;              # Large headers (OAuth tokens)
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
large_client_header_buffers 4 32k;
```

### 常见的流式传输误区

| 设置 | 对流式传输的影响 |
|------|------------------|
| 在 `application/json` 上启用 `gzip on` | 🔴 为压缩而缓冲 |
| `proxy_buffering on` | 🔴 缓冲整个响应 |
| `proxy_request_buffering on` | 应该关闭 |
| `tcp_nodelay on` | 🔴 **最关键：** 禁用 Nagle 算法，立即发送数据包（可避免 200ms 延迟） |
| `chunked_transfer_encoding on` | 🟡 可能破坏 SSE |
| 在 `/api/` 上启用 `proxy_cache` | 🟡 带来额外开销 |
| `X-Accel-Buffering "yes"` | 为了更安全，这个头应设置为 `no` |
| `HTTP/2` | 如果遇到流式问题、延迟，或者前端在最后一个块到达前就结束了流式输出，改用 HTTP 1.1 而不是 HTTP/2 也可能有帮助 |

### 完整示例配置

```nginx
upstream openwebui {
    server 127.0.0.1:3000;
    keepalive 128;
    keepalive_timeout 1800s;
    keepalive_requests 10000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 配置……

    # 压缩 - 排除流式内容类型
    gzip on;
    gzip_types text/plain text/css application/javascript image/svg+xml;
    # 不要包含：application/json、text/event-stream

    # API 端点 - 针对流式优化
    location /api/ {
        proxy_pass http://openwebui;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 关键：为流式传输关闭所有缓冲
        gzip off;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_cache off;
        tcp_nodelay on;
        add_header X-Accel-Buffering "no" always;
        add_header Cache-Control "no-store" always;

        # 为 LLM 补全设置更长的超时时间
        proxy_connect_timeout 1800;
        proxy_send_timeout 1800;
        proxy_read_timeout 1800;
    }

    # WebSocket 端点
    location ~ ^/(ws/|socket\.io/) {
        proxy_pass http://openwebui;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        gzip off;
        proxy_buffering off;
        proxy_cache off;

        # 为持久连接设置 24 小时超时
        proxy_connect_timeout 86400;
        proxy_send_timeout 86400;
        proxy_read_timeout 86400;
    }

    # 静态资源 - 可以缓冲和缓存
    location /static/ {
        proxy_pass http://openwebui;
        proxy_buffering on;
        proxy_cache_valid 200 7d;
        add_header Cache-Control "public, max-age=604800, immutable";
    }

    # 默认 location
    location / {
        proxy_pass http://openwebui;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 缓存配置

合理的缓存可以显著提升 Open WebUI 的性能，减少后端负载并加快页面加载。本节为希望实现服务端和客户端缓存的高级用户提供指导。

### 缓存区域

在 nginx 的 `http` 块中定义缓存区域，用于存储缓存响应：

```nginx
# General cache for pages and assets
proxy_cache_path /var/cache/nginx/openwebui levels=1:2 
    keys_zone=OPENWEBUI_CACHE:10m max_size=1g inactive=60m use_temp_path=off;

# Dedicated cache for images (profile pictures, model avatars)
proxy_cache_path /var/cache/nginx/openwebui_images levels=1:2 
    keys_zone=OPENWEBUI_IMAGES:10m max_size=2g inactive=7d use_temp_path=off;
```

:::note 创建缓存目录

在 nginx 使用这些目录之前，你必须先创建它们并设置正确的所有权：

```bash
sudo mkdir -p /var/cache/nginx/openwebui /var/cache/nginx/openwebui_images
sudo chown -R www-data:www-data /var/cache/nginx
```

把 `www-data` 替换成你的 nginx 用户（可通过 `ps aux | grep nginx` 查看）。常见替代包括 `nginx` 和 `nobody`。

:::

### 缓存哪些内容

| 内容类型 | 缓存时长 | 说明 |
|----------|----------|------|
| 静态资源（CSS、JS、字体） | 7–30 天 | 对版本化资源使用 `immutable` |
| 个人资料/模型图片 | 1 天 | 在新鲜度和性能之间取得平衡 |
| 静态文件（/static/） | 7 天 | Favicon、默认头像 |
| HTML 页面 | 5 分钟 | 短缓存并进行重新验证 |
| 上传文件内容 | 1 天 | 用户上传内容、生成的图片 |

### 永远不要缓存什么

:::danger 关键：绝不要缓存认证

以下路径**绝不要**缓存，以防止安全问题和登录异常：

- `/api/v1/auths/` - 认证端点
- `/oauth/` - OAuth/SSO 回调
- `/api/`（通用）- 动态 API 响应
- `/ws/` - WebSocket 连接

认证端点始终应包含以下指令：

```nginx
proxy_no_cache 1;
proxy_cache_bypass 1;
add_header Cache-Control "no-store, no-cache, must-revalidate";
```

:::

### 示例：图片缓存

个人资料图片和模型头像从缓存中受益很大：

```nginx
# User and model profile images
location ~ ^/api/v1/(users/[^/]+/profile/image|models/model/profile/image)$ {
    proxy_pass http://your_backend;
    
    proxy_cache OPENWEBUI_IMAGES;
    proxy_cache_valid 200 302 1d;
    proxy_cache_valid 404 1m;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_lock on;
    proxy_cache_key "$request_uri$is_args$args";
    
    # 即使后端没有缓存头，也强制缓存
    proxy_ignore_headers Cache-Control Expires Set-Cookie;
    proxy_hide_header Set-Cookie;
    
    # 客户端缓存
    add_header Cache-Control "public, max-age=86400, stale-while-revalidate=604800" always;
    add_header X-Cache-Status $upstream_cache_status always;
    
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 示例：静态资源缓存

```nginx
location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|otf|eot)$ {
    proxy_pass http://your_backend;
    
    proxy_cache OPENWEBUI_CACHE;
    proxy_cache_valid 200 302 60m;
    proxy_cache_valid 404 1m;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_lock on;
    
    add_header Cache-Control "public, max-age=2592000";  # 30 days
    add_header X-Cache-Status $upstream_cache_status;
    
    etag on;
    if_modified_since exact;
}
```

### 缓存调试

添加 `X-Cache-Status` 头可以验证缓存是否生效：

```nginx
add_header X-Cache-Status $upstream_cache_status always;
```

在浏览器 DevTools 中查看该头：

- `HIT` - 由缓存提供
- `MISS` - 从后端获取，随后写入缓存
- `EXPIRED` - 缓存已过期并被刷新
- `BYPASS` - 故意跳过缓存

### 权衡

:::warning 缓存失效

当图片被强力缓存时，用户在更改头像后可能不会立即看到更新。可以考虑：

- 如果用户经常更新图片，使用**更短的缓存时间**（例如 1 小时）
- 如果部署比较稳定，使用**更长的缓存时间**（例如 1 天）以获得更好性能
- 可以通过以下命令手动清空缓存：`rm -rf /var/cache/nginx/openwebui_images/*`

:::

---

## 下一步

完成 HTTPS 配置后，可以通过以下地址安全访问 Open WebUI：

- [https://localhost](https://localhost)

Ensure that your DNS records are correctly configured if you're using a domain name. For production environments, it's recommended to use Let's Encrypt for trusted SSL certificates.

---
