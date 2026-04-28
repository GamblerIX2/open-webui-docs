#!/usr/bin/env python3
"""批量写入翻译后的 auth 文件（LDAP、SCIM、SSO、Keycloak）"""
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1] / "docs"

def w(rel, content):
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"Written: {rel}")

# ─── ldap.mdx ──────────────────────────────────────────────────────────────
w("features/authentication-access/auth/ldap.mdx", r'''---
sidebar_position: 2
title: "LDAP 身份认证"
---

# OpenLDAP 集成

本指南提供了为 Open WebUI 设置 OpenLDAP 身份认证的完整演练。内容涵盖使用 Docker 创建测试 OpenLDAP 服务器、用示例用户进行初始化、配置 Open WebUI 连接，以及常见问题排查。

## 1. 使用 Docker 设置 OpenLDAP

运行测试 OpenLDAP 服务器最简单的方式是使用 Docker。以下 `docker-compose.yml` 文件将创建一个 OpenLDAP 容器和一个可选的 phpLDAPadmin 容器（提供基于 Web 的管理界面）。

```yaml title="docker-compose.yml"
version: "3.9"
services:
  ldap:
    image: osixia/openldap:1.5.0
    container_name: openldap
    environment:
      LDAP_ORGANISATION: "Example Inc"
      LDAP_DOMAIN: "example.org"
      LDAP_ADMIN_PASSWORD: admin
      LDAP_TLS: "false"
    volumes:
      - ./ldap/var:/var/lib/ldap
      - ./ldap/etc:/etc/ldap/slapd.d
    ports:
      - "389:389"
    networks: [ldapnet]

  phpldapadmin:
    image: osixia/phpldapadmin:0.9.0
    environment:
      PHPLDAPADMIN_LDAP_HOSTS: "ldap"
    ports:
      - "6443:443"
    networks: [ldapnet]

networks:
  ldapnet:
    driver: bridge
```

- `osixia/openldap` 镜像仅通过 `LDAP_DOMAIN` 和 `LDAP_ADMIN_PASSWORD` 就能自动创建基础组织结构。
- `osixia/phpldapadmin` 镜像提供管理 LDAP 目录的 Web 界面，可在 `https://localhost:6443` 访问。

运行 `docker-compose up -d` 启动容器。通过检查日志验证 LDAP 服务器已启动：`docker logs openldap`。您应该能看到"started slapd"消息。

## 2. 添加示例用户（LDIF）

要测试登录，您需要向 LDAP 目录添加一个示例用户。创建名为 `seed.ldif` 的文件，内容如下：

```ldif title="seed.ldif"
dn: ou=users,dc=example,dc=org
objectClass: organizationalUnit
ou: users

dn: uid=jdoe,ou=users,dc=example,dc=org
objectClass: inetOrgPerson
cn: John Doe
sn: Doe
uid: jdoe
mail: jdoe@example.org
userPassword: {PLAIN}password123
```

**关于密码：** `userPassword` 字段在此测试环境中设置为明文值，方便操作。在生产环境中，应始终使用哈希密码。可以使用 `slappasswd` 或 `openssl passwd` 生成哈希密码，例如：

```bash
# 使用 slappasswd（在容器内部）
docker exec openldap slappasswd -s your_password

# 使用 openssl
openssl passwd -6 your_password
```

将 LDIF 文件复制到容器并使用 `ldapadd` 添加条目：

```bash
docker cp seed.ldif openldap:/seed.ldif
docker exec openldap ldapadd -x -D "cn=admin,dc=example,dc=org" -w admin -f /seed.ldif
```

操作成功会显示"adding new entry"消息。

## 3. 验证 LDAP 连接

在配置 Open WebUI 之前，验证 LDAP 服务器可访问且用户存在。

```bash
ldapsearch -x -H ldap://localhost:389 \
  -D "cn=admin,dc=example,dc=org" -w admin \
  -b "dc=example,dc=org" "(uid=jdoe)"
```

如果命令返回 `jdoe` 用户条目，则 LDAP 服务器已就绪。

## 4. 配置 Open WebUI

现在，配置您的 Open WebUI 实例以使用 LDAP 服务器进行身份认证。

### 环境变量

为您的 Open WebUI 实例设置以下环境变量。

:::info

Open WebUI 仅在首次启动时读取这些环境变量。后续更改必须在 UI 的管理设置面板中进行，除非您设置了 `ENABLE_PERSISTENT_CONFIG=false`。

:::

```env
# 启用 LDAP
ENABLE_LDAP="true"

# --- 服务器设置 ---
LDAP_SERVER_LABEL="OpenLDAP"
LDAP_SERVER_HOST="localhost"  # 或您的 LDAP 服务器 IP/主机名
LDAP_SERVER_PORT="389"        # 明文/StartTLS 使用 389，LDAPS 使用 636
LDAP_USE_TLS="false"          # LDAPS 或 StartTLS 设置为 "true"
LDAP_VALIDATE_CERT="false"    # 生产环境使用有效证书时设置为 "true"

# --- 绑定凭据 ---
LDAP_APP_DN="cn=admin,dc=example,dc=org"
LDAP_APP_PASSWORD="admin"

# --- 用户 Schema ---
LDAP_SEARCH_BASE="dc=example,dc=org"
LDAP_ATTRIBUTE_FOR_USERNAME="uid"
LDAP_ATTRIBUTE_FOR_MAIL="mail"
# LDAP_SEARCH_FILTER 是可选项，用于附加过滤条件。
# Open WebUI 会自动添加用户名过滤器，因此请勿包含
# %(user)s 或 %s 等用户占位符语法——这些不受支持。
# 简单设置可留空，或添加组成员过滤器，例如：
# LDAP_SEARCH_FILTER="(memberOf=cn=allowed-users,ou=groups,dc=example,dc=org)"
```

### UI 配置

也可以直接在 UI 中配置这些设置：

1. 以管理员身份登录。
2. 导航到 **设置** > **通用**。
3. 启用 **LDAP 身份认证**。
4. 填写与上述环境变量对应的字段。
5. 保存设置并重启 Open WebUI。

## 5. 登录

打开一个新的隐身浏览器窗口并导航到您的 Open WebUI 实例。

-   **登录 ID：** `jdoe`
-   **密码：** `password123`（或您设置的密码）

登录成功后，Open WebUI 会自动创建一个具有"用户"角色的新用户账户。管理员可以稍后根据需要提升用户角色。

## 6. 常见错误排查

以下是 LDAP 集成过程中常见错误的解决方案。

### `port must be an integer`

```
ERROR | open_webui.routers.auths:ldap_auth:447 - LDAP authentication error: port must be an integer - {}
```

**原因：** `LDAP_SERVER_PORT` 环境变量以带引号的字符串传递（例如 `"389"`）。

**解决方案：**
-   确保 `.env` 文件或 export 命令中的 `LDAP_SERVER_PORT` 值没有引号：`LDAP_SERVER_PORT=389`。
-   从 `LDAP_SERVER_HOST` 中删除协议（`http://`、`ldap://`）。它应该只是主机名或 IP（例如 `localhost`）。

### `[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred`

```
ERROR | LDAP authentication error: ("('socket ssl wrapping error: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)',)",) - {}
```

**原因：** TLS 握手失败。客户端（Open WebUI）正在尝试启动 TLS 连接，但服务器（OpenLDAP）未为其配置或期望不同的协议。

**解决方案：**
-   **如果不打算使用 TLS：** 设置 `LDAP_USE_TLS="false"` 并连接到标准明文端口 `389`。
-   **如果打算使用 LDAPS：** 确保您的 LDAP 服务器已配置 TLS 并监听端口 `636`。设置 `LDAP_SERVER_PORT="636"` 和 `LDAP_USE_TLS="true"`。
-   **如果打算使用 StartTLS：** 您的 LDAP 服务器必须支持 StartTLS 扩展。在端口 `389` 上连接并设置 `LDAP_USE_TLS="true"`。

### `err=49 text=`（凭据无效）

```
openldap | ... conn=1001 op=0 RESULT tag=97 err=49 text=
```

**原因：** LDAP 服务器拒绝了绑定尝试，因为识别名（DN）或密码不正确。这发生在第二次绑定尝试时，Open WebUI 尝试使用用户提供的凭据进行身份认证。

**解决方案：**
1. **验证密码：** 确保使用的是正确的明文密码。LDIF 文件中的 `userPassword` 值就是服务器期望的。如果是哈希值，必须提供原始明文密码。
2. **检查用户 DN：** 用于绑定的 DN（`uid=jdoe,ou=users,dc=example,dc=org`）必须正确。
3. **使用 `ldapwhoami` 测试：** 直接对 LDAP 服务器验证凭据，将问题与 Open WebUI 隔离。
''')

# ─── scim.mdx ──────────────────────────────────────────────────────────────
w("features/authentication-access/auth/scim.mdx", r'''---
sidebar_position: 3
title: "SCIM 2.0"
---

# SCIM 2.0 支持

Open WebUI 支持 SCIM 2.0（跨域身份管理系统），用于从 Okta、Azure AD 和 Google Workspace 等身份提供商自动化用户和用户组预配。

## 概述

SCIM 是一个允许自动化用户预配的开放标准。启用后，您的身份提供商可以自动：
- 在将用户添加到您的组织时在 Open WebUI 中创建用户
- 在信息更改时更新用户信息
- 在用户从您的组织中移除时停用用户
- 管理用户组成员资格

## 配置

SCIM 完全通过环境变量进行配置。SCIM 设置没有 UI 配置选项。

### 环境变量

通过设置以下环境变量配置 SCIM：

- **`SCIM_ENABLED`**：设置为 `true` 以启用 SCIM 支持（默认：`false`）
- **`SCIM_TOKEN`**：用于 SCIM 身份认证的 Bearer token（启用 SCIM 时必填）
- **`SCIM_AUTH_PROVIDER`**：要与 SCIM `externalId` 值关联的 OAuth 提供商名称（例如 `microsoft`、`oidc`）。`externalId` 存储和账户关联所必需。

:::warning

安全说明
SCIM token 应该是安全的随机生成字符串。您可以使用以下命令生成：
```bash
openssl rand -base64 32
```
请妥善保管此 token，因为它提供对用户管理操作的访问权限。

:::

### 配置示例

```bash
# 启用 SCIM
export SCIM_ENABLED=true

# 设置安全 token（替换为您自己生成的 token）
export SCIM_TOKEN="your-secure-token-here"

# 设置用于 externalId 关联的 OAuth 提供商名称
export SCIM_AUTH_PROVIDER="microsoft"
```

## SCIM API 配置

配置您的身份提供商时，请使用以下设置：

- **SCIM 基础 URL**：`<your-openwebui-url>/api/v1/scim/v2/`
- **身份认证**：Bearer Token
- **Token**：`Bearer <your-scim-token>`

### 主流身份提供商配置示例

#### Okta
1. 在 Okta 中添加 SCIM 应用
2. 将 SCIM 连接器基础 URL 设置为：`https://your-domain.com/api/v1/scim/v2/`
3. 将身份认证设置为"HTTP Header"
4. 添加值为 `Bearer your-scim-token` 的 Authorization 请求头

## 支持的 SCIM 操作

Open WebUI 的 SCIM 实现支持以下操作：

### 用户操作
- **创建用户**（`POST /Users`）：创建新用户账户
- **获取用户**（`GET /Users/{id}`）：检索用户信息
- **更新用户**（`PUT /Users/{id}`、`PATCH /Users/{id}`）：更新用户属性
- **删除用户**（`DELETE /Users/{id}`）：停用用户账户
- **列出用户**（`GET /Users`）：列出所有用户（支持过滤）

### 用户组操作
- **创建用户组**（`POST /Groups`）：创建新用户组
- **获取用户组**（`GET /Groups/{id}`）：检索用户组信息
- **更新用户组**（`PUT /Groups/{id}`、`PATCH /Groups/{id}`）：更新用户组成员
- **删除用户组**（`DELETE /Groups/{id}`）：移除用户组
- **列出用户组**（`GET /Groups`）：列出所有用户组（支持过滤）

### 支持的属性

#### 用户属性
- `userName`：用户的邮箱地址（必填，唯一）
- `name.givenName`：名
- `name.familyName`：姓
- `emails`：邮箱地址（提供多个时，使用标记了 `primary: true` 的条目）
- `active`：用户状态（活跃/非活跃）
- `externalId`：来自身份提供商的外部标识符（按提供商存储在用户的 `scim` JSON 字段中，参见 [externalId 与账户关联](#externalid-与账户关联)）

#### 用户组属性
- `displayName`：用户组名称（必填）
- `members`：用户成员数组
- `externalId`：来自身份提供商的外部标识符

## 过滤支持

SCIM API 支持对用户和用户组进行过滤：

```
GET /api/v1/scim/v2/Users?filter=userName eq "user@example.com"
GET /api/v1/scim/v2/Users?filter=externalId eq "abc-123"
GET /api/v1/scim/v2/Groups?filter=displayName eq "Engineering"
```

支持的过滤运算符：
- `eq`：等于
- `ne`：不等于
- `co`：包含
- `sw`：以...开头
- `ew`：以...结尾
- `pr`：存在（有值）
- `gt`：大于
- `ge`：大于或等于
- `lt`：小于
- `le`：小于或等于

## externalId 与账户关联

配置 `SCIM_AUTH_PROVIDER` 后，Open WebUI 将 `externalId` 值存储在用户 `scim` JSON 字段中的每提供商结构里：

```json
{
  "microsoft": { "external_id": "abc-123" },
  "okta": { "external_id": "def-456" }
}
```

这实现了以下几种行为：

- **通过 externalId 查找用户**：当身份提供商发送 `filter=externalId eq "..."` 请求时，Open WebUI 会在 `scim` 字段中搜索已配置提供商的匹配条目。
- **OAuth 回退**：如果通过 `externalId` 未找到用户，Open WebUI 会回退到与 OAuth `sub` 值匹配，自动将 SCIM 预配的账户与现有 OAuth 认证用户关联。
- **创建和更新**：通过 SCIM 创建或更新用户时，`externalId` 存储在 `scim` 字段中，并在后续响应中返回。

:::warning

如果在启用 SCIM 的情况下未设置 `SCIM_AUTH_PROVIDER`，任何需要 `externalId` 的操作（创建、查找或更新）都将返回 `500` 错误。启动时也会记录警告提醒您。

:::

## 故障排查

### 常见问题

1. **401 未授权错误**
   - 验证 `SCIM_ENABLED` 是否设置为 `true`
   - 检查身份提供商中的 Bearer token 是否与 `SCIM_TOKEN` 匹配
   - 确保 Authorization 请求头格式为：`Bearer <token>`

2. **404 未找到错误**
   - 验证 SCIM 基础 URL 是否以 `/api/v1/scim/v2/` 结尾
   - 检查路径是否包含 `/api/v1` 前缀

3. **用户创建失败**
   - 确保 `userName` 字段包含有效的邮箱地址
   - 检查邮箱或 `externalId` 是否已被使用

4. **externalId 操作返回 500 错误**
   - 验证 `SCIM_AUTH_PROVIDER` 是否设置为正确的 OAuth 提供商名称

### 测试 SCIM 端点

您可以使用 curl 测试 SCIM 端点：

```bash
# 测试身份认证并列出用户
curl -H "Authorization: Bearer your-scim-token" \
  https://your-domain.com/api/v1/scim/v2/Users

# 获取特定用户
curl -H "Authorization: Bearer your-scim-token" \
  https://your-domain.com/api/v1/scim/v2/Users/user-id

# 创建测试用户
curl -X POST \
  -H "Authorization: Bearer your-scim-token" \
  -H "Content-Type: application/scim+json" \
  -d '{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName": "test@example.com",
    "externalId": "idp-user-id-123",
    "displayName": "Test User",
    "name": {
      "givenName": "Test",
      "familyName": "User"
    },
    "emails": [{
      "value": "test@example.com",
      "primary": true
    }],
    "active": true
  }' \
  https://your-domain.com/api/v1/scim/v2/Users
```

## 安全注意事项

1. **使用 HTTPS**：在生产环境中始终使用 HTTPS 来保护 Bearer token
2. **安全 Token 存储**：安全地存储 SCIM token 并定期轮换
3. **IP 白名单**：考虑将 SCIM API 访问限制到您身份提供商的 IP 地址
4. **审计日志**：SCIM 操作会被记录以供安全审计

## 局限性

- 目前不支持自定义 Schema 扩展
- 未实现批量操作
- 不支持用于资源版本控制的 ETag

## 与 SSO 集成

SCIM 与 SSO（单点登录）结合使用效果最佳。典型设置包括：
1. SCIM 用于自动化用户预配
2. OIDC 用于用户身份认证

这确保用户被自动创建并可以立即使用其企业凭据进行身份认证。

有关 SSO 配置，请参阅 [SSO 文档](https://docs.openwebui.com/features/authentication-access/auth/sso/)。
''')

print("LDAP and SCIM done")
