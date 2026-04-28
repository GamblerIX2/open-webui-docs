# 在 Windows 上使用自签名证书和 Nginx（无需 Docker）

对于基础的内部/开发部署，你可以使用 nginx 和自签名证书把 Open WebUI 代理到 https，从而在局域网中使用麦克风输入等功能。（默认情况下，大多数浏览器都不会允许在非 localhost 的不安全网址上使用麦克风。）

本指南假设你已经通过 pip 安装了 Open WebUI，并正在运行 `open-webui serve`。

## 第 1 步：安装用于生成证书的 openssl

你首先需要安装 openssl。

你可以从 [Shining Light Productions (SLP)](https://slproweb.com/) 网站下载并安装预编译二进制文件。

或者，如果你已经安装了 [Chocolatey](https://chocolatey.org/)，可以直接快速安装 OpenSSL：

1. 打开命令提示符或 PowerShell。
2. 运行以下命令安装 OpenSSL：

   ```bash
   choco install openssl -y
   ```

---

### **验证安装**

安装完成后，打开命令提示符并输入：

```bash
openssl version
```

如果它输出 OpenSSL 版本号（例如 `OpenSSL 3.x.x ...`），说明安装成功。

## 第 2 步：安装 nginx

从 [nginx.org](https://nginx.org) 下载 Windows 版官方 Nginx，或者使用 Chocolatey 之类的包管理器。
将下载好的 ZIP 文件解压到某个目录（例如 `C:\nginx`）。

## 第 3 步：生成证书

运行以下命令：

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx.key -out nginx.crt
```

将生成的 `nginx.key` 和 `nginx.crt` 文件移动到你选择的文件夹，或者直接放到 `C:\nginx` 目录中。

## 第 4 步：配置 nginx

用文本编辑器打开 `C:\nginx\conf\nginx.conf`。

如果你希望 Open WebUI 可以在本地 LAN 中访问，请先用 `ipconfig` 查看你的 LAN IP 地址，例如 `192.168.1.15`。

将配置修改为如下内容：

```conf

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;

#error_log  logs/error.log  notice;

#error_log  logs/error.log  info;

#pid        logs/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  120;

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        listen 80;
        server_name 192.168.1.15;

        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name 192.168.1.15;

        ssl_certificate C:\\nginx\\nginx.crt;
        ssl_certificate_key C:\\nginx\\nginx.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers on;

        location ~* ^/(auth|api|oauth|admin|signin|signup|signout|login|logout|sso)/ {
            proxy_pass http://localhost:8080;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_buffering off;
            proxy_cache off;
            client_max_body_size 20M;
            proxy_read_timeout 10m;

            add_header Cache-Control "no-store, no-cache, must-revalidate" always;
            expires -1;
        }

        # 个人资料和模型图片 - 缓存以提升性能
        location ~ ^/api/v1/(users/[^/]+/profile/image|models/model/profile/image)$ {
            proxy_pass http://localhost:8080;
            proxy_http_version 1.1;
            proxy_set_header Host $host;

            # 图片缓存 1 天
            expires 1d;
            add_header Cache-Control "public, max-age=86400";
        }

        location ~* \.(css|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
            proxy_pass http://localhost:8080;
            proxy_http_version 1.1;
            proxy_set_header Host $host;

            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        location / {
            proxy_pass http://localhost:8080;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_buffering off;
            proxy_cache off;
            client_max_body_size 20M;

            # 长时间 LLM 补全的扩展超时（30 分钟）
            proxy_read_timeout 1800;
            proxy_send_timeout 1800;
            proxy_connect_timeout 1800;

            add_header Cache-Control "public, max-age=300, must-revalidate";
        }
    }
}
```

保存文件后，运行 `nginx -t` 检查配置是否有语法或错误。根据你的安装方式，可能需要先 `cd C:\nginx`。

运行 `nginx` 启动服务。如果 nginx 服务已经在运行，可以通过 `nginx -s reload` 重新加载新配置。

---

现在你应该可以通过 `https://192.168.1.15`（或你的实际 LAN IP）访问 Open WebUI。请根据需要允许 Windows 防火墙放行相关访问。
