---
sidebar_position: 201
title: "使用 HAProxy 的 HTTPS"
---


## Open WebUI 的 HAProxy 配置

HAProxy（High Availability Proxy，高可用代理）是一款专门的负载均衡和反向代理方案，可配置性很强，设计目标是在较低资源占用下处理大量连接。更多信息请参阅：[https://www.haproxy.org/](https://www.haproxy.org/)

## 安装 HAProxy 和 Let's Encrypt

首先安装 HAProxy 和 Let's Encrypt 的 certbot：

### Red Hat 系发行版

```sudo dnf install haproxy certbot openssl -y```

### Debian 系发行版

```sudo apt install haproxy certbot openssl -y```

## HAProxy 配置基础

HAProxy 的配置默认保存在 ```/etc/haproxy/haproxy.cfg```。这个文件包含了决定 HAProxy 如何运行的全部配置指令。

让 HAProxy 与 Open WebUI 协同工作的基础配置其实很简单。

```shell
 #---------------------------------------------------------------------

# 全局设置

#---------------------------------------------------------------------
global
        # 如果你希望这些日志最终写入 /var/log/haproxy.log，需要：
    #
    # 1）配置 syslog 接收网络日志事件。可通过向
    #    /etc/sysconfig/syslog 中的 SYSLOGD_OPTIONS 添加 '-r' 选项来完成
    #    /etc/sysconfig/syslog
    #
    # 2）将 local2 事件写入 /var/log/haproxy.log 文件。
    #    可以添加如下这一行：
    #   /etc/sysconfig/syslog
    #
    #    local2.*                       /var/log/haproxy.log
    #
    log         127.0.0.1 local2

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon

 # 如有需要，可调高 dh-param
    tune.ssl.default-dh-param 2048

#---------------------------------------------------------------------

# 所有未在各自区块中单独指定的 listen/backend 部分都会继承的通用默认值

#---------------------------------------------------------------------
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       #except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    300s
    timeout queue           2m
    timeout connect         120s
    timeout client          10m
    timeout server          10m
    timeout http-keep-alive 120s
    timeout check           10s
    maxconn                 3000

# HTTP
frontend web
 # 非 SSL
    bind 0.0.0.0:80
 # SSL/TLS
 bind 0.0.0.0:443 ssl crt /path/to/ssl/folder/

     # Let's Encrypt SSL
    acl letsencrypt-acl path_beg /.well-known/acme-challenge/
    use_backend letsencrypt-backend if letsencrypt-acl

 # 子域名方式
    acl chat-acl hdr(host) -i subdomain.domain.tld
     # 路径方式
    acl chat-acl path_beg /owui/
    use_backend owui_chat if chat-acl

# 将 SSL 请求交给 Let's Encrypt
backend letsencrypt-backend
    server letsencrypt 127.0.0.1:8688

# OWUI Chat
backend owui_chat
     # 添加 X-FORWARDED-FOR
    option forwardfor
     # 添加 X-CLIENT-IP
    http-request add-header X-CLIENT-IP %[src]
 http-request set-header X-Forwarded-Proto https if { ssl_fc }
    server chat <ip>:3000

## WebSocket 与 HTTP/2 兼容性

从较新的版本开始（包括 HAProxy 3.x），HAProxy 可能会默认启用 HTTP/2。虽然 HTTP/2 支持 WebSocket（RFC 8441），但某些客户端或后端配置在通过 H2 通道加载图标或数据时，可能会出现“卡死”或无响应的情况。

如果你遇到这些问题：
1. **为 WebSocket 强制使用 HTTP/1.1**：在 `frontend` 或 `defaults` 部分添加 `option h2-workaround-bogus-websocket-clients`。这会阻止 HAProxy 向客户端声明 RFC 8441 支持，从而回退到更稳定的 HTTP/1.1 Upgrade 机制。
2. **后端版本**：确保后端连接使用的是 HTTP/1.1（`mode http` 的默认行为）。

可以在 `defaults` 或 `frontend` 中添加如下内容：
```shell
defaults
    # ... other settings
    option h2-workaround-bogus-websocket-clients
```

你可以看到，我们为 Open WebUI 和 Let's Encrypt 都配置了 ACL 记录（路由器）。若要在 OWUI 中使用 WebSocket，需要先配置 SSL，而最简单的方式就是使用 Let's Encrypt。

你可以选择使用子域名方式或路径方式将流量路由到 Open WebUI。子域名方式需要一个专用子域名（例如 `chat.yourdomain.com`），而路径方式则允许你通过域名下的特定路径访问 Open WebUI（例如 `yourdomain.com/owui/`）。请选择最适合你需求的方式，并相应更新配置。

:::info

你需要将 80 和 443 端口暴露给 HAProxy 服务器。Let's Encrypt 需要这些端口来验证你的域名，HTTPS 流量也依赖它们。你还需要确保 DNS 记录正确指向 HAProxy 服务器。如果你是在家中运行 HAProxy，还需要在路由器中做端口转发，把 80 和 443 转发到 HAProxy 服务器。

:::

## 使用 Let's Encrypt 签发 SSL 证书

在启动 HAProxy 之前，先生成一个自签名证书作为占位，直到 Let's Encrypt 签发正式证书。生成自签名证书的方法如下：

```shell
openssl req -x509 -newkey rsa:2048 -keyout /tmp/haproxy.key -out /tmp/haproxy.crt -days 3650 -nodes -subj "/CN=localhost"
```

然后把密钥和证书合并为 HAProxy 可用的 PEM 文件：

```cat /tmp/haproxy.crt /tmp/haproxy.key > /etc/haproxy/certs/haproxy.pem```

:::info

请务必根据自己的需求和配置更新 HAProxy 设置。

:::

配置好 HAProxy 之后，你就可以使用 certbot 获取并管理 SSL 证书。Certbot 会负责与 Let's Encrypt 的验证流程，并在证书接近过期时自动更新（前提是你启用了 certbot 的自动续期服务）。

你可以运行 `haproxy -c -f /etc/haproxy/haproxy.cfg` 来验证 HAProxy 配置。如果没有错误，就可以用 `systemctl start haproxy` 启动 HAProxy，并用 `systemctl status haproxy` 检查它是否正在运行。

若希望 HAProxy 随系统启动，可执行 `systemctl enable haproxy`。

当 HAProxy 配置完成后，你可以使用 Let's Encrypt 签发正式的 SSL 证书。
首先需要注册 Let's Encrypt，这一步通常只需执行一次：

`certbot register --agree-tos --email your@email.com --non-interactive`

然后申请证书：

```shell
certbot certonly -n --standalone --preferred-challenges http --http-01-port-8688 -d yourdomain.com
```

证书签发后，需要把证书文件和私钥文件合并成一个 HAProxy 可用的 PEM 文件。

```shell
cat /etc/letsencrypt/live/{domain}/fullchain.pem /etc/letsencrypt/live/{domain}/privkey.pem > /etc/haproxy/certs/{domain}.pem
chmod 600 /etc/haproxy/certs/{domain}.pem
chown haproxy:haproxy /etc/haproxy/certs/{domain}.pem
```

随后重启 HAProxy 以应用新证书：
`systemctl restart haproxy`

## HAProxy Manager（便捷部署方案）

如果你希望有工具自动管理 HAProxy 配置和 Let's Encrypt SSL 证书，我写了一个简单的 Python 脚本，并提供了一个 Docker 容器，可用于创建和管理 HAProxy 配置，以及处理 Let's Encrypt 证书的生命周期。

[https://github.com/shadowdao/haproxy-manager](https://github.com/shadowdao/haproxy-manager)

:::warning

如果你使用这个脚本或容器，请不要把 8000 端口公开暴露到公网！

:::
