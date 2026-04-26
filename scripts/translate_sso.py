#!/usr/bin/env python3
"""写入 SSO 和 Keycloak 翻译文件"""
import pathlib

BASE = pathlib.Path("d:/Github/open-webui-docs/docs")

def w(rel, content):
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"Written: {rel}")

# ─── sso/index.mdx ─────────────────────────────────────────────────────────
w("features/authentication-access/auth/sso/index.mdx", r'''---
sidebar_position: 1
title: "SSO（OAuth、OIDC、受信任请求头）"
---

:::info

有关所有环境变量的更多信息，请查看[环境变量文档页面](https://docs.openwebui.com/reference/env-configuration/)。
强烈建议查看环境变量页面，以获取有关如何设置变量及其期望值的更多详情。

:::

:::tip

需要 SSO 设置的故障排查帮助？
请查看我们的[故障排查指南](https://docs.openwebui.com/troubleshooting/sso)

:::

:::danger 仅支持一个 OIDC 提供商
目前，您只能通过 `OPENID_PROVIDER_URL` 一次配置**一个** OpenID Connect（OIDC）提供商。
不能同时将 Microsoft **和** Google 作为 OIDC 提供商。

*但是，社区有一个同时使用两者的变通方案！详情请参阅我们的[双 OAuth 教程](/tutorials/auth-sso/dual-oauth-configuration)。*
:::

## OAuth 配置概览

| 环境变量 | 默认值 | 说明 |
|---------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `WEBUI_URL` | — | **必填。** 您的公开 WebUI 地址，例如 `http://localhost:8080`。 |
| `ENABLE_OAUTH_PERSISTENT_CONFIG` | `true` | 将 OAuth 配置持久化到数据库；对于无状态/容器化环境，设置为 `false`。 |
| `ENABLE_OAUTH_SIGNUP` | `false` | 允许在 OAuth 登录时创建账户（与 `ENABLE_SIGNUP` 独立）。 |
| `OAUTH_MERGE_ACCOUNTS_BY_EMAIL` | `false` | 基于匹配邮箱合并 OAuth 登录（注意：如果提供商不验证邮箱，可能不安全）。 |
| `OAUTH_UPDATE_PICTURE_ON_LOGIN` | `false` | 每次登录时从 OAuth 提供商更新用户头像。 |
| `OAUTH_PICTURE_CLAIM` | `picture` | claim 中包含头像的字段。设置为空字符串以禁用图片更新（用户获得默认图标）。 |
| `WEBUI_AUTH_SIGNOUT_REDIRECT_URL` | *空* | 退出后将用户重定向到此 URL。例如 `https://your-company.com/logout-success` |
| `WEBUI_SECRET_KEY` | *空* | 必须设置——尤其是在集群环境中。否则会出现 session 问题和奇怪的 OAuth 问题。 |
| `OAUTH_SESSION_TOKEN_ENCRYPTION_KEY` | `WEBUI_SECRET_KEY` | 用于加密服务器上存储的 OAuth token 的密钥。必须在集群中所有实例间共享。 |
| `OAUTH_CLIENT_INFO_ENCRYPTION_KEY` | `WEBUI_SECRET_KEY` | 用于加密服务器上存储的 OAuth 客户端信息的密钥——用于 MCP 服务器的 OAuth 2.1 认证。 |
| `ENABLE_OAUTH_ID_TOKEN_COOKIE` | `true` | 向后兼容。控制是否设置旧版 `oauth_id_token` cookie。建议设置为 `false`。 |
| `ENABLE_OAUTH_TOKEN_EXCHANGE` | `false` | 为外部应用启用 token 交换端点，允许将 OAuth token 交换为 Open WebUI JWT。 |
| `ENABLE_OAUTH_BACKCHANNEL_LOGOUT` | `false` | 为 IdP 发起的注销启用 OIDC 后端通道注销端点（`POST /oauth/backchannel-logout`）。需要 Redis 进行 JWT 撤销。 |
| `OAUTH_MAX_SESSIONS_PER_USER` | `10` | 每个用户每个提供商的最大并发 OAuth 会话数。防止无限增长同时允许多设备使用。 |

:::warning

**关键配置注意事项：**

1. **必须先设置 WEBUI_URL**：在启用 OAuth 之前，在管理面板中配置 `WEBUI_URL`，因为它用于重定向 URI。

2. **持久化配置行为**：当 `ENABLE_OAUTH_PERSISTENT_CONFIG=true`（默认）时，OAuth 设置在首次启动后存储在数据库中。要在初始设置后更改环境变量，您需要：
   - 设置 `ENABLE_OAUTH_PERSISTENT_CONFIG=false` 以始终从环境变量读取
   - 通过管理面板而不是环境变量更新设置

3. **必需变量**：始终验证您使用的是[环境配置文档](https://docs.openwebui.com/reference/env-configuration/)中的确切变量名。常见错误包括使用不存在的变量如 `OIDC_CONFIG`。

:::

### 服务端 OAuth 会话管理

为解决大型 token 相关问题（例如 AD FS 用户组 claims 超出 cookie 大小限制）并启用自动 token 刷新，Open WebUI 现在支持强大的服务端会话管理系统。

**工作原理：**

1. **服务端存储：** 不再将大型 `access_token` 和 `id_token` 值存储在浏览器 cookie 中，整个 token 负载现在被加密并安全存储在 Open WebUI 数据库的新 `oauth_session` 表中。
2. **安全会话 Cookie：** 用户浏览器收到一个小型、安全的 `httponly` cookie，名为 `oauth_session_id`。此 cookie 充当不透明标识符，本身不包含任何敏感信息。
3. **多设备支持：** 每个用户每个提供商支持多个并发会话。从第二台设备（例如手机）登录**不会**使第一台设备的会话失效。为防止会话无限增长，可配置限制（`OAUTH_MAX_SESSIONS_PER_USER`，默认：10），超过时删除最旧的会话。
4. **自动刷新：** 当下游服务（如工具或 OpenAI 兼容端点）需要 token 时，后端使用 `oauth_session_id` 检索 token。如果 token 已过期或即将过期，系统会在转发前自动使用存储的 `refresh_token` 从提供商获取新 token。这确保服务始终收到有效 token，防止静默失败。
5. **简洁的 Token 访问：** 此架构为内部工具和其他服务提供了一种干净可靠的方式来访问用户 token，无需脆弱的 cookie 解析。

此系统默认启用，但可以使用上述环境变量进行微调。

有关更多信息，请查看[环境变量文档页面](https://docs.openwebui.com/reference/env-configuration/)。

### 外部应用的 OAuth Token 交换

Open WebUI 还支持 **OAuth Token 交换**，允许外部应用通过将 OAuth 提供商的访问 token 交换为 Open WebUI JWT 会话 token 来与 Open WebUI 进行身份认证。这对于已拥有来自身份提供商的 OAuth token 的脚本、CLI 工具或服务的程序化访问非常有用。

**示例使用场景：** 已从身份提供商获取 OAuth 访问 token 的 CLI 工具，可以将其交换为 Open WebUI token 以调用 Open WebUI API。

要启用此功能，设置 `ENABLE_OAUTH_TOKEN_EXCHANGE=true`。有关用法、请求/响应示例和安全注意事项的详情，请参阅 [`ENABLE_OAUTH_TOKEN_EXCHANGE`](/reference/env-configuration#enable_oauth_token_exchange) 环境变量文档。

### OIDC 后端通道注销

Open WebUI 支持 **OIDC 后端通道注销**，允许您的身份提供商（IdP）直接通过服务器到服务器的方式（无需浏览器重定向）通知 Open WebUI 用户注销事件。

要启用此功能，设置 `ENABLE_OAUTH_BACKCHANNEL_LOGOUT=true`。

启用后，Open WebUI 暴露：

- `POST /oauth/backchannel-logout`

该端点期望接收由您的 IdP 颁发的表单编码 `logout_token`，并根据您配置的 OAuth/OIDC 提供商元数据和 JWKS 进行验证。

:::warning

强烈推荐 Redis，实际上是完整注销强制执行所必需的。

- 配置了 Redis 时，Open WebUI 会撤销受影响用户的现有 JWT 并删除存储的 OAuth 会话。
- 没有 Redis 时，Open WebUI 可以删除存储的 OAuth 会话，但已颁发的 JWT 在过期之前仍然有效。

:::

有关实现详情和行为说明，请参阅 [`ENABLE_OAUTH_BACKCHANNEL_LOGOUT`](/reference/env-configuration#enable_oauth_backchannel_logout)。

### Google

要配置 Google OAuth 客户端，请参阅 [Google 的文档](https://support.google.com/cloud/answer/6158849)，了解如何为 **Web 应用**创建 Google OAuth 客户端。
允许的重定向 URI 应包含 `<open-webui>/oauth/google/callback`。

需要以下环境变量：

1. `GOOGLE_CLIENT_ID` - Google OAuth 客户端 ID
1. `GOOGLE_CLIENT_SECRET` - Google OAuth 客户端密钥
1. `OPENID_PROVIDER_URL` - 必须设置才能使注销正常工作。（通常为 `https://accounts.google.com/.well-known/openid-configuration`）

可选的 Google 特定设置：

1. `GOOGLE_OAUTH_AUTHORIZE_PARAMS` - 用于额外 Google `/authorize` 参数的 JSON 对象（例如 `prompt`、`login_hint`、`hd`）。

```bash
GOOGLE_OAUTH_AUTHORIZE_PARAMS={"prompt":"consent","login_hint":"user@example.com","hd":"example.com"}
```

### Microsoft

要配置 Microsoft OAuth 客户端，请参阅 [Microsoft 的文档](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)，了解如何为 **Web 应用**创建 Microsoft OAuth 客户端。
允许的重定向 URI 应包含 `<open-webui>/oauth/microsoft/callback`。此值应用于 `MICROSOFT_REDIRECT_URI` 环境变量。

Microsoft OAuth 支持目前仅限于单个租户，即单个 Entra 组织或个人 Microsoft 账户。

需要以下环境变量：

1. `MICROSOFT_CLIENT_ID` - Microsoft OAuth 客户端 ID
1. `MICROSOFT_CLIENT_SECRET` - Microsoft OAuth 客户端密钥
1. `MICROSOFT_CLIENT_TENANT_ID` - Microsoft 租户 ID - 个人账户使用 `9188040d-6c67-4c5b-b112-36a304b66dad`
1. `MICROSOFT_REDIRECT_URI` - 在 Microsoft OAuth 应用中配置的重定向 URI。必须设置为 `<open-webui>/oauth/microsoft/callback`。
1. `OPENID_PROVIDER_URL` - 必须设置才能使注销正常工作。

#### Token 刷新（`offline_access`）

默认情况下，Microsoft 的身份平台只返回 `access_token`，大约 1 小时后过期。要启用自动 token 刷新（防止用户需要重新认证），请添加 `offline_access` scope：

```
MICROSOFT_OAUTH_SCOPE=openid email profile offline_access
```

`offline_access` scope 指示 Microsoft 还返回**刷新 token**，Open WebUI 的服务端会话中间件使用它在过期前自动获取新的访问 token。

:::warning `offline_access` 缺失的症状

没有 `offline_access`，用户登录超过 1 小时后可能会看到重复的日志警告：

```
WARNING | No refresh token available for session xxx
WARNING | Token refresh failed for user xxx, deleting session
```

基本对话功能（使用 Open WebUI JWT）**不受**影响，但以下功能**将**失败：

- 使用 `auth_type: "system_oauth"` 的 MCP 工具服务器
- OneDrive / SharePoint 文件访问
- 从 Microsoft 自动刷新头像

:::

:::tip

Microsoft Entra ID 中无需额外配置。`offline_access` scope 对于具有客户端密钥的 Web 应用[默认可用](https://learn.microsoft.com/en-us/entra/identity-platform/scopes-oidc#openid-connect-scopes)。

:::

:::tip 使用 Microsoft Entra ID 的角色映射

如果您使用 Entra ID **应用角色**来控制谁在 Open WebUI 中获得 `admin` 或 `user` 访问权限，还需要配置下面的 [OAuth 角色管理](#oauth-角色管理)。特别是确保除了设置 `ENABLE_OAUTH_ROLE_MANAGEMENT=true` 外，还要设置 `OAUTH_ALLOWED_ROLES` 和 `OAUTH_ADMIN_ROLES`——否则所有用户将以默认角色创建，无论其 Entra ID 分配如何。

:::

### GitHub

要配置 GitHub OAuth 客户端，请参阅 [GitHub 的文档](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)，了解如何为 **Web 应用**创建 OAuth App 或 GitHub App。
允许的重定向 URI 应包含 `<open-webui>/oauth/github/callback`。

需要以下环境变量：

1. `GITHUB_CLIENT_ID` - GitHub OAuth App 客户端 ID
1. `GITHUB_CLIENT_SECRET` - GitHub OAuth App 客户端密钥

### OIDC

任何支持 OIDC 的身份认证提供商都可以配置。
`email` claim 为必填项。
`name` 和 `picture` claim 可用时会被使用。
允许的重定向 URI 应包含 `<open-webui>/oauth/oidc/callback`。

使用以下环境变量：

1. `OAUTH_CLIENT_ID` - OIDC 客户端 ID
1. `OAUTH_CLIENT_SECRET` - OIDC 客户端密钥
1. `OPENID_PROVIDER_URL` - **必填。** OIDC well known URL，例如 `https://accounts.google.com/.well-known/openid-configuration`
1. `OAUTH_PROVIDER_NAME` - 在 UI 上显示的提供商名称，默认为 SSO
1. `OAUTH_SCOPES` - 请求的 scope。默认为 `openid email profile`
1. `OPENID_REDIRECT_URI` - 在 OIDC 应用中配置的重定向 URI。必须设置为 `<open-webui>/oauth/oidc/callback`。
1. `OAUTH_AUDIENCE` - 可选的 `audience` 值，将作为附加查询参数传递给 OAuth 提供商的授权端点。

:::warning

**常见 OIDC 错误：**
- 使用不存在的环境变量，如 `OIDC_CONFIG` 或 `WEBUI_OIDC_CLIENT_ID`
- 忘记设置 `OPENID_PROVIDER_URL`（OIDC 强制要求）
- 使用错误的重定向 URI 格式——必须完全是 `<your-domain>/oauth/oidc/callback`

:::

:::tip 社区变通方案：多提供商 OAuth
如果您需要同时支持 Microsoft 和 Google，请查看我们的 **[双 OAuth 配置教程](/tutorials/auth-sso/dual-oauth-configuration)**。
:::

### OAuth 角色管理

任何可以配置为在访问 token 中返回角色的 OAuth 提供商，都可以用来管理 Open WebUI 中的角色。
要使用此功能，将 `ENABLE_OAUTH_ROLE_MANAGEMENT` 设置为 `true`。
您可以配置以下环境变量来匹配 OAuth 提供商返回的角色：

1. `OAUTH_ROLES_CLAIM` - 包含角色的 claim。默认为 `roles`。也可以是嵌套的，例如 `user.roles`。
1. `OAUTH_ALLOWED_ROLES` - 允许登录的角色列表（逗号分隔，获得 open webui `user` 角色）。
1. `OAUTH_ADMIN_ROLES` - 允许以管理员身份登录的角色列表（逗号分隔，获得 open webui `admin` 角色）。
1. `OAUTH_ROLES_SEPARATOR` - 允许为 `OAUTH_*_ROLES` 变量指定替代分隔符。如果 claim 是字符串且包含分隔符，也会按该分隔符拆分。

:::info

如果更改了已登录用户的角色，他们需要退出并重新登录才能获得新角色。

:::

### OAuth 用户组管理

任何可以配置为在访问 token 中返回用户组的 OAuth 提供商，都可以在用户登录时用来管理 Open WebUI 中的用户组。
要启用此同步，将 `ENABLE_OAUTH_GROUP_MANAGEMENT` 设置为 `true`。

您可以配置以下环境变量：

1. `OAUTH_GROUP_CLAIM` - ID/访问 token 中包含用户组成员资格的 claim。默认为 `groups`。也可以是嵌套的，例如 `user.memberOf`。当 `ENABLE_OAUTH_GROUP_MANAGEMENT` 为 true 时必填。
1. `ENABLE_OAUTH_GROUP_CREATION` - 如果为 `true`（且 `ENABLE_OAUTH_GROUP_MANAGEMENT` 也为 `true`），Open WebUI 将执行**即时（JIT）用户组创建**。这意味着在 OAuth 登录时，如果用户的 OAuth claims 中存在但系统中尚不存在的用户组，将自动创建。默认为 `false`。如果为 `false`，只管理*现有* Open WebUI 用户组的成员资格。
1. `OAUTH_GROUP_DEFAULT_SHARE` - 控制通过 JIT 用户组创建创建的用户组的默认共享权限。默认为 `true`（与任何人共享）。设置为 `members` 以仅限组成员共享，或设置为 `false` 完全禁用共享。仅在启用 `ENABLE_OAUTH_GROUP_CREATION` 时适用。

:::warning

严格用户组同步
当 `ENABLE_OAUTH_GROUP_MANAGEMENT` 设置为 `true` 时，用户在 Open WebUI 中的用户组成员资格将在每次登录时**严格同步**为 OAuth claims 中收到的用户组。

*   用户将被**添加**到与其 OAuth claims 匹配的 Open WebUI 用户组。
*   用户将从任何在该登录会话的 OAuth claims 中**不存在**的 Open WebUI 用户组（包括在 Open WebUI 内手动创建或分配的用户组）中**移除**。

确保所有必要的用户组在您的 OAuth 提供商中正确配置，并包含在用户组 claim（`OAUTH_GROUP_CLAIM`）中。

:::

:::warning

管理员用户
管理员用户的用户组成员资格**不**会通过 OAuth 用户组管理自动更新。

:::

:::info

更新需要重新登录

如果用户在 OAuth 提供商中的用户组发生更改，他们需要退出 Open WebUI 并重新登录，更改才能生效。

:::

## 受信任请求头

Open WebUI 能够将身份认证委托给通过 HTTP 请求头传递用户详情的认证反向代理。
本页面提供了几个示例配置。

:::danger

配置不当会允许用户以您的 Open WebUI 实例上的任何用户身份进行认证。
确保只允许认证代理访问 Open WebUI，例如不直接向容器开放任何端口，或设置 `HOST=127.0.0.1` 使其仅在回环接口上监听。

:::

### 通用配置

设置 `WEBUI_AUTH_TRUSTED_EMAIL_HEADER` 环境变量后，Open WebUI 将使用指定请求头的值作为用户的邮箱地址，处理自动注册和登录。

例如，设置 `WEBUI_AUTH_TRUSTED_EMAIL_HEADER=X-User-Email` 并传递 HTTP 请求头 `X-User-Email: example@example.com`，将以邮箱 `example@example.com` 认证该请求。

可选地，您还可以定义 `WEBUI_AUTH_TRUSTED_NAME_HEADER` 来确定使用受信任请求头创建的任何用户的名称。如果用户已存在，则此设置无效。
如果未设置 `WEBUI_AUTH_TRUSTED_NAME_HEADER`，则将邮箱地址用作用户名。

#### 用户组管理

您可以使用 `WEBUI_AUTH_TRUSTED_GROUPS_HEADER` 环境变量在 Open WebUI 中同步用户组。将此变量设置为将包含认证用户逗号分隔用户组名称列表的 HTTP 请求头名称。

当通过 `WEBUI_AUTH_TRUSTED_EMAIL_HEADER` 认证请求时，如果设置了受信任用户组请求头且其存在，Open WebUI 将更新用户的用户组成员资格以匹配请求头中列出的用户组。

- 请求头值必须是逗号分隔的用户组名称列表（例如 `X-User-Groups: admins,editors,users`）。
- 如果请求头不存在或为空，用户的用户组成员资格将不会更新。
- 用户将从请求头中未出现的用户组中取消分配。
- 通过受信任请求头不会自动创建用户组；只会分配 Open WebUI 中已存在的用户组。

#### 角色管理

您可以使用 `WEBUI_AUTH_TRUSTED_ROLE_HEADER` 环境变量，通过认证反向代理控制用户的角色。将此变量设置为将包含认证用户所需角色的 HTTP 请求头名称。

- 请求头值必须是 `admin`、`user` 或 `pending` 之一（不区分大小写，已去除空格）。
- 当请求头存在且有效时，每次登录都会更新用户的角色以匹配请求头值。
- 如果请求头包含无效值，则角色不会更改并记录警告。
- 如果请求头不存在或为空，用户现有的角色保持不变。

:::warning

配置后，此请求头允许客户端通过 HTTP 请求头设置管理员级别的访问权限。您**必须**确保只有您的受信任反向代理或身份提供商才能设置此请求头。允许不受信任的客户端直接访问 Open WebUI 将使任何人都能提升到管理员权限。这与其他受信任请求头的安全模型相同——参见本节顶部的警告。

:::

### Tailscale Serve

:::tip
有关涵盖安装、HTTPS、身份认证和 Docker Compose 设置的完整端到端指南，请参阅 [**Tailscale 集成教程**](/tutorials/auth-sso/tailscale)。
:::

[Tailscale Serve](https://tailscale.com/kb/1242/tailscale-serve) 允许您在 tailnet 中共享服务，Tailscale 将设置请求头 `Tailscale-User-Login`，其值为请求者的邮箱地址。

以下是一个带有相应 Docker Compose 文件的示例 serve 配置，该配置启动了一个 Tailscale 边车容器，将 Open WebUI 以 `open-webui` 标签和主机名 `open-webui` 暴露给 tailnet，可通过 `https://open-webui.TAILNET_NAME.ts.net` 访问。
您需要创建一个具有设备写入权限的 OAuth 客户端，作为 `TS_AUTHKEY` 传递给 Tailscale 容器。

```json title="tailscale/serve.json"
{
    "TCP": {
        "443": {
            "HTTPS": true
        }
    },
    "Web": {
        "${TS_CERT_DOMAIN}:443": {
            "Handlers": {
                "/": {
                    "Proxy": "http://open-webui:8080"
                }
            }
        }
    }
}
```

```yaml title="docker-compose.yaml"
---
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui:/app/backend/data
    environment:
      - WEBUI_AUTH_TRUSTED_EMAIL_HEADER=Tailscale-User-Login
      - WEBUI_AUTH_TRUSTED_NAME_HEADER=Tailscale-User-Name
    restart: unless-stopped
  tailscale:
    image: tailscale/tailscale:latest
    environment:
      - TS_AUTH_ONCE=true
      - TS_AUTHKEY=${TS_AUTHKEY}
      - TS_EXTRA_ARGS=--advertise-tags=tag:open-webui
      - TS_SERVE_CONFIG=/config/serve.json
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_HOSTNAME=open-webui
    volumes:
      - tailscale:/var/lib/tailscale
      - ./tailscale:/config
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - net_admin
      - sys_module
    restart: unless-stopped

volumes:
  open-webui: {}
  tailscale: {}
```

:::warning

如果 Tailscale 在与 Open WebUI 相同的网络上下文中运行，则默认情况下用户将能够直接访问 Open WebUI，而无需通过 Serve 代理。
您需要使用 Tailscale 的 ACL 将访问限制为仅 443 端口。

:::

### Cloudflare Tunnel 与 Cloudflare Access

[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-remote-tunnel/) 可以与 [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/policies/access/) 一起使用，通过 SSO 保护 Open WebUI。
Cloudflare 对此的文档很少，但 `Cf-Access-Authenticated-User-Email` 会设置为已认证用户的邮箱地址。

以下是一个设置 Cloudflare 边车的 Docker Compose 文件示例。
配置通过控制台完成。
从控制台获取隧道 token，将隧道后端设置为 `http://open-webui:8080`，并确保勾选并配置"通过 Access 保护"。

```yaml title="docker-compose.yaml"
---
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui:/app/backend/data
    environment:
      - WEBUI_AUTH_TRUSTED_EMAIL_HEADER=Cf-Access-Authenticated-User-Email
    restart: unless-stopped
  cloudflared:
    image: cloudflare/cloudflared:latest
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
    command: tunnel run
    restart: unless-stopped

volumes:
  open-webui: {}
```

### oauth2-proxy

[oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/) 是一个实现社交 OAuth 提供商和 OIDC 支持的认证反向代理。

鉴于潜在配置的数量众多，以下是使用 Google OAuth 的潜在设置示例。
请参阅 `oauth2-proxy` 的文档，了解详细设置和任何潜在的安全注意事项。

```yaml title="docker-compose.yaml"
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui:/app/backend/data
    environment:
      - 'WEBUI_AUTH_TRUSTED_EMAIL_HEADER=X-Forwarded-Email'
      - 'WEBUI_AUTH_TRUSTED_NAME_HEADER=X-Forwarded-User'
    restart: unless-stopped
  oauth2-proxy:
    image: quay.io/oauth2-proxy/oauth2-proxy:v7.6.0
    environment:
      OAUTH2_PROXY_HTTP_ADDRESS: 0.0.0.0:4180
      OAUTH2_PROXY_UPSTREAMS: http://open-webui:8080/
      OAUTH2_PROXY_PROVIDER: google
      OAUTH2_PROXY_CLIENT_ID: REPLACEME_OAUTH_CLIENT_ID
      OAUTH2_PROXY_CLIENT_SECRET: REPLACEME_OAUTH_CLIENT_ID
      OAUTH2_PROXY_EMAIL_DOMAINS: REPLACEME_ALLOWED_EMAIL_DOMAINS
      OAUTH2_PROXY_REDIRECT_URL: REPLACEME_OAUTH_CALLBACK_URL
      OAUTH2_PROXY_COOKIE_SECRET: REPLACEME_COOKIE_SECRET
      OAUTH2_PROXY_COOKIE_SECURE: "false"
    restart: unless-stopped
    ports:
      - 4180:4180/tcp
```

### Authentik

要配置 [Authentik](https://goauthentik.io/) OAuth 客户端，请参阅[文档](https://integrations.goauthentik.io/miscellaneous/open-webui/)，了解如何创建应用和 `OAuth2/OpenID Provider`。
允许的重定向 URI 应包含 `<open-webui>/oauth/oidc/callback`。

创建提供商时，请记录 `App-name`、`Client-ID` 和 `Client-Secret`，并用于 open-webui 环境变量：

```
      - 'ENABLE_OAUTH_SIGNUP=true'
      - 'OAUTH_MERGE_ACCOUNTS_BY_EMAIL=true'
      - 'OAUTH_PROVIDER_NAME=Authentik'
      - 'OPENID_PROVIDER_URL=https://<authentik-url>/application/o/<App-name>/.well-known/openid-configuration'
      - 'OAUTH_CLIENT_ID=<Client-ID>'
      - 'OAUTH_CLIENT_SECRET=<Client-Secret>'
      - 'OAUTH_SCOPES=openid email profile'
      - 'OPENID_REDIRECT_URI=https://<open-webui>/oauth/oidc/callback'
```

### Authelia

[Authelia](https://www.authelia.com/) 可以配置为返回用于受信任请求头认证的请求头。
文档见[此处](https://www.authelia.com/integration/trusted-header-sso/introduction/)。
''')

# ─── sso/keycloak.mdx ──────────────────────────────────────────────────────
w("features/authentication-access/auth/sso/keycloak.mdx", r'''---
title: "Keycloak"
---

:::warning

本教程为社区贡献内容，不受 Open WebUI 团队官方支持，仅作为如何针对特定使用场景自定义 Open WebUI 的演示。想要贡献内容？请查看贡献教程。

:::

本指南介绍如何将 Open WebUI 与 Keycloak 集成以实现 OIDC 单点登录（SSO）。

## 1. 环境准备与端口更改

### Open WebUI 服务器端口
- **默认端口**：`8080`

### Keycloak 端口冲突问题
Keycloak 默认也使用 `8080` 端口，导致冲突。请将 Keycloak 端口更改为 `9090`。

```bash
bin/kc.sh start-dev --http-port=9090
```
{/* TODO: 插入 Keycloak 端口更改控制台输出图片 */}

## 2. 创建 Keycloak Realm

1. 打开浏览器访问 `http://localhost:9090`，创建管理员账户。
2. 在 `http://localhost:9090/admin` 登录管理控制台。
3. 从顶部的 realm 下拉菜单中，点击 **Add realm**。
4. 输入 `openwebui` 作为 **Realm name**，点击 **Create**。

![创建 realm](/images/features/auth/keycloak/create-realm.png)

## 3. 创建 OpenID Connect 客户端

:::info

确保已选中 `openwebui` realm。默认为 `master`。

:::

![选择 realm](/images/features/auth/keycloak/select-realm.png)

1. 确保已选中刚创建的 `openwebui` realm。
2. 在左侧菜单中，点击 **Clients** → **Create client**。
3. 将 **Client ID** 设置为 `open-webui`。
4. 保持 **Client protocol** 为 `openid-connect`。
5. 将 **Access Type** 设置为 `confidential`，点击 **Save**。

![访问设置客户端](/images/features/auth/keycloak/access-setting-client.png)

## 4. 启用客户端认证并获取凭据

默认情况下，Keycloak 26.x 将客户端认证设置为"None"，需要手动配置。

1. 进入 **Clients** → **open-webui** → **Settings**。
2. 检查 **Client Authenticator** 下拉菜单。
3. 将"None"更改为 **Client ID and secret**，点击 **Save**。
4. 点击 **Advanced** 选项卡。
5. 在 **Client authentication** 部分，点击 **Reveal secret** 并复制密钥。
6. 将此密钥粘贴到 `.env` 文件中的 `OAUTH_CLIENT_SECRET` 变量。

{/* TODO: 插入高级选项卡客户端认证器设置图片 */}

## 5. 创建测试用户

1. 在左侧菜单中，进入 **Users** → **Add user**。
2. 填写 **Username**、**Email** 等信息，点击 **Save**。
3. 点击新创建的用户，进入 **Credentials** 选项卡。
4. 输入新密码，取消勾选 **Temporary**，点击 **Set Password**。
    - *示例：用户名 `testuser`，密码 `Test1234!`*

## 6. 配置 Open WebUI .env 文件

在 `.env` 文件中添加或修改以下变量。

```env
# 启用 OAuth2/OIDC 登录
ENABLE_OAUTH_SIGNUP=true

# Keycloak 客户端信息
OAUTH_CLIENT_ID=open-webui
OAUTH_CLIENT_SECRET=<YOUR_COPIED_SECRET>

# OIDC Discovery Document URL
OPENID_PROVIDER_URL=http://localhost:9090/realms/openwebui/.well-known/openid-configuration

# （可选）SSO 按钮标签
OAUTH_PROVIDER_NAME=Keycloak

# （可选）OAuth 回调 URL
OPENID_REDIRECT_URI=http://localhost:8080/oauth/oidc/callback
```
**修改 `.env` 文件后，重启 Open WebUI 服务器。**

## 7. HTTP 与 HTTPS

-   **HTTP（开发/测试环境）**：
    -   协议：`http://`
    -   示例：`http://localhost:9090`
-   **HTTPS（生产环境推荐）**：
    -   需要 Keycloak TLS 设置或带 SSL 终止的反向代理。
    ```bash
    bin/kc.sh start --https-port=9090 \
      --https-key-store=keystore.jks \
      --https-key-store-password=<password>
    ```

## 8. 测试集成

1. 访问 `http://localhost:8080`，您应该会看到"Continue with Keycloak"按钮。
2. 点击该按钮，应该会重定向到 Keycloak 登录页面。
3. 使用 `testuser` / `Test1234!` 登录，应该成功重定向回 Open WebUI。

{/* TODO: 插入实际登录界面图片 */}

## 9. 配置 Keycloak 用户组映射

### 9.1. 概述
默认情况下，Keycloak 客户端不在 token 中包含用户组信息。按照以下步骤传递用户组信息。

### 9.2. 找到 Mapper 创建入口
1. 进入 Keycloak 管理控制台：`http://localhost:9090/admin`。
2. 选择 `openwebui` realm。
3. 导航到 **Clients**，选择 `open-webui` 客户端。
4. 进入 **Client scopes** 选项卡。
5. 选择将包含用户组信息的 scope（例如 `profile` 或 `open-webui-dedicated`）。

    ![scope 客户端](/images/features/auth/keycloak/scope-client.png)

6. 在所选 scope 的详情中，进入 **Mappers** 选项卡。

### 9.3. 创建 Mapper
点击 **Create** 或 **Add builtin** 开始创建新 mapper。

### 9.4. Mapper 设置
使用适当的设置配置 mapper，以包含用户组成员资格。

![mapper 设置用户组客户端](/images/features/auth/keycloak/mappers-setting-group-client.png)

### 9.5. 保存并应用
-   **保存** mapper 配置。
-   **重启** Open WebUI 服务器以应用更改。

### 9.6. 配置 Open WebUI 环境变量
在 `.env` 文件中添加或修改以下变量：

```env
# 启用用户组同步
ENABLE_OAUTH_GROUP_MANAGEMENT=true

# （可选）启用即时用户组创建
ENABLE_OAUTH_GROUP_CREATION=true

# token 中用户组的 claim 键
OAUTH_GROUP_CLAIM=groups
```
''')

print("SSO and Keycloak done")
