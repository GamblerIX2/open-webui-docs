# 使用 Let's Encrypt

Let's Encrypt 提供免费且被大多数浏览器信任的 SSL 证书，非常适合保护生产环境。🔐

本指南采用两阶段流程：

1. **第一阶段：** 临时运行 Nginx，证明你拥有该域名，并从 Let's Encrypt 获取证书。
2. **第二阶段：** 重新配置 Nginx，使用新证书提供安全的 HTTPS 连接。

## 前提条件 {#prerequisites}

* 一个 **域名**（例如 `my-webui.com`），并带有指向服务器公网 IP 的 **DNS `A` 记录**。
* 已在服务器上安装 **Docker** 和 **Docker Compose**。
* 具备在终端中执行命令的基础知识。

:::info
**注意！** Let's Encrypt **不能**为 IP 地址签发证书。你**必须**使用域名。
:::

-----

### 第 1 步：为证书验证准备初始配置

首先创建所需文件，并准备一个临时的 Nginx 配置，让 Let's Encrypt 的服务器可以验证你的域名。

1. **请确保你已经完成上面的[前提条件](#prerequisites)。**

2. **创建目录结构**

   在项目根目录执行以下命令，为 Nginx 配置和 Let's Encrypt 证书创建目录：

   ```bash
   mkdir -p nginx/conf.d ssl/certbot/conf ssl/certbot/www
   ```

3. **创建临时的 Nginx 配置**

   创建文件 `nginx/conf.d/open-webui.conf`。这个初始配置只监听 80 端口，并为 Certbot 提供验证文件。

   ⚠️ **记得把 `<YOUR_DOMAIN_NAME>` 替换成你的真实域名。**

   ```nginx
   # nginx/conf.d/open-webui.conf

   server {
       listen 80;
       listen [::]:80;
       server_name <YOUR_DOMAIN_NAME>;

       # Let's Encrypt 验证挑战路由
       location /.well-known/acme-challenge/ {
           root /var/www/certbot;
       }

       # 其余请求暂时返回 404
       location / {
           return 404;
       }
   }
   ```

4. **更新你的 `docker-compose.yml`**

   将 `nginx` 服务添加到 `docker-compose.yml` 中，并确保 `open-webui` 服务使用共享的 Docker 网络。

   ```yaml
   services:
     nginx:
       image: nginx:alpine
       restart: always
       ports:
         # 将 HTTP 和 HTTPS 端口暴露到宿主机
         - "80:80"
         - "443:443"
       volumes:
         # 挂载 Nginx 配置和 SSL 证书数据
         - ./nginx/conf.d:/etc/nginx/conf.d
         - ./ssl/certbot/conf:/etc/letsencrypt
         - ./ssl/certbot/www:/var/www/certbot
       depends_on:
         - open-webui
       networks:
         - open-webui-network

     open-webui:
       # 你的现有 open-webui 配置……
       # ...
       # 确保它在同一个网络中
       networks:
         - open-webui-network
       # 只在 Docker 网络内部暴露端口。
       # 你不需要把它发布到宿主机（即这里不需要 `ports` 配置）。
       expose:
         - 8080

   networks:
       open-webui-network:
           driver: bridge
   ```

-----

### 第 2 步：获取 SSL 证书

接下来我们将运行一个脚本，借助 Docker 获取证书。

1. **创建证书申请脚本**

   在项目根目录创建一个名为 `enable_letsencrypt.sh` 的可执行脚本。

   ⚠️ **记得把 `<YOUR_DOMAIN_NAME>` 和 `<YOUR_EMAIL_ADDRESS>` 替换成你的真实信息。**

   ```bash
   #!/bin/bash
   # enable_letsencrypt.sh

   DOMAIN="<YOUR_DOMAIN_NAME>"
   EMAIL="<YOUR_EMAIL_ADDRESS>"

   echo "### 正在为 $DOMAIN 获取 SSL 证书 ###"

   # 启动 Nginx 以提供挑战文件
   docker compose up -d nginx

   # 在容器中运行 Certbot 获取证书
   docker run --rm \
     -v "./ssl/certbot/conf:/etc/letsencrypt" \
     -v "./ssl/certbot/www:/var/www/certbot" \
     certbot/certbot certonly \
     --webroot \
     --webroot-path=/var/www/certbot \
     --email "$EMAIL" \
     --agree-tos \
     --no-eff-email \
     --force-renewal \
     -d "$DOMAIN"

   if [[ $? != 0 ]]; then
       echo "错误：无法获取 SSL 证书。"
       docker compose stop nginx
       exit 1
   fi

   # 在应用最终配置前先停止 Nginx
   docker compose stop nginx
   echo "### 证书获取成功！ ###"
   ```

2. **让脚本可执行**

   ```bash
   chmod +x enable_letsencrypt.sh
   ```

3. **运行脚本**

   执行脚本。它会自动启动 Nginx、申请证书，然后停止 Nginx。

   ```bash
   ./enable_letsencrypt.sh
   ```

-----

### 重要：缓存配置

在 Open WebUI 中使用 NGINX 时，正确的缓存配置对性能至关重要，同时还要确保认证保持安全。下面的配置包含：

- **缓存**：静态资源（CSS、JS、字体、图片），以提升性能
- **不缓存**：认证端点、API 调用、SSO/OAuth 回调和会话数据
- **结果**：页面加载更快，同时不会破坏登录功能

下面的配置会自动落实这些规则。

### 第 3 步：完成用于 HTTPS 的 Nginx 配置

证书保存到 `ssl` 目录后，现在可以更新 Nginx 配置以启用 HTTPS。

1. **更新用于 SSL 的 Nginx 配置**

   **将** `nginx/conf.d/open-webui.conf` **的全部内容替换为下面的最终配置。**

   ⚠️ **把 `<YOUR_DOMAIN_NAME>` 的 4 处都替换成你的域名。**

   ```nginx
   # nginx/conf.d/open-webui.conf

   # 将所有 HTTP 流量重定向到 HTTPS
   server {
       listen 80;
       listen [::]:80;
       server_name <YOUR_DOMAIN_NAME>;

       location /.well-known/acme-challenge/ {
           root /var/www/certbot;
       }

       location / {
           return 301 https://$host$request_uri;
       }
   }

   server {
       listen 443 ssl;
       listen [::]:443 ssl;
       http2 on;
       server_name <YOUR_DOMAIN_NAME>;

       ssl_certificate /etc/letsencrypt/live/<YOUR_DOMAIN_NAME>/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/<YOUR_DOMAIN_NAME>/privkey.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-RSA-AES128-GCM-SHA256';
       ssl_prefer_server_ciphers off;

       location ~* ^/(auth|api|oauth|admin|signin|signup|signout|login|logout|sso)/ {
           proxy_pass http://open-webui:8080;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_read_timeout 10m;
           proxy_buffering off;
           proxy_cache off;
           client_max_body_size 20M;

           proxy_no_cache 1;
           proxy_cache_bypass 1;
           add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0" always;
           add_header Pragma "no-cache" always;
           expires -1;
       }

       # 个人资料和模型图片 - 缓存以提升性能
       location ~ ^/api/v1/(users/[^/]+/profile/image|models/model/profile/image)$ {
           proxy_pass http://open-webui:8080;
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # 图片缓存 1 天
           expires 1d;
           add_header Cache-Control "public, max-age=86400";
       }

       location ~* \.(css|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
           proxy_pass http://open-webui:8080;
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # 静态资源缓存 7 天
           expires 7d;
           add_header Cache-Control "public, immutable";
       }

       location / {
           proxy_pass http://open-webui:8080;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # 长时间 LLM 补全的扩展超时（30 分钟）
           proxy_read_timeout 1800;
           proxy_send_timeout 1800;
           proxy_connect_timeout 1800;

           proxy_buffering off;
           proxy_cache off;
           client_max_body_size 20M;

           add_header Cache-Control "public, max-age=300, must-revalidate";
       }
   }
   ```

2. **启动所有服务**

   使用最终的安全配置启动 Nginx 和 Open WebUI：

   ```bash
   docker compose up -d
   ```

-----

### 第 4 步：访问你的安全 WebUI

现在你可以通过 HTTPS 安全访问 Open WebUI 实例了。

➡️ **`https://<YOUR_DOMAIN_NAME>`**

-----

### （可选）第 5 步：设置自动续期

Let's Encrypt 证书会在 90 天后过期。你应该设置一个 `cron` 任务来自动续期。

1. 打开 crontab 编辑器：

    ```bash
    sudo crontab -e
    ```

2. 添加以下行，以便每天凌晨 3:30 运行续期检查。只有当证书接近过期时，它才会执行续期。

    ```cron
    30 3 * * * /usr/bin/docker run --rm -v "<absolute_path>/ssl/certbot/conf:/etc/letsencrypt" -v "<absolute_path>/ssl/certbot/www:/var/www/certbot" certbot/certbot renew --quiet --webroot --webroot-path=/var/www/certbot --deploy-hook "/usr/bin/docker compose -f <absolute_path>/docker-compose.yml restart nginx"
    ```
