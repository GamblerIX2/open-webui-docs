---
sidebar_position: 4
title: "强化 Open WebUI 安全"
---

<a id="hardening-open-webui"></a>

# 强化 Open WebUI 安全

Open WebUI 是一个自托管应用，会向已认证用户提供模型推理、工具执行、代码流水线等能力。与数据库、容器仓库、CI 服务器等其他自托管基础设施一样，部署方需要自行管理运行环境、网络暴露方式和配置。Open WebUI 提供了本指南中介绍的控制项；具体如何配置，取决于你的环境与威胁模型。

本指南聚焦于可用于强化部署安全性的配置项。每一节都会说明某个设置的作用、默认值以及如何修改。它并不是一份面面俱到的安全手册；最终，保障部署安全仍是你的责任。你的运行环境、合规要求和威胁模型，将决定哪些项与你最相关。

## 概览 {#hardening-open-webui}

### 网络放置建议 {#network-placement}

:::tip

Open WebUI 的设计预期是运行在私有、可信网络中，类似数据库、容器仓库或 CI 服务器这类自托管基础设施。大多数部署都会放在企业防火墙、VPN 或其他仅允许已知用户访问的网络边界之后。

对于把安全放在优先位置的组织，推荐将 Open WebUI 放在以下一种或多种保护层之后：

- VPN（WireGuard、Tailscale）
- Zero Trust 访问代理（Cloudflare Access、Pomerium）
- 带认证与 IP allowlist 的反向代理

DDoS 防护和暴力破解防护（限速、连接节流、fail2ban）应由代理层或网络层承担。

:::

如果你是第一次部署 Open WebUI，建议先查看本文底部的[速查表](#quick-reference)，获取按优先级整理的摘要，然后再阅读与你部署场景相关的章节。

---

## Secret Key {#secret-key}

`WEBUI_SECRET_KEY` 用于签发 JWT（登录 token），并派生 OAuth 会话数据的加密密钥。

**默认行为：**

通过 Docker（`start.sh`）或 `open-webui serve` 运行时，应用会先检查环境变量中是否设置了 `WEBUI_SECRET_KEY`。如果没有，它会自动生成一个随机密钥，并保存到数据目录中的 `.webui_secret_key`。之后重启时会重新加载这个已保存的密钥。这意味着在单实例部署中，通常无需手动配置。

**什么时候必须显式设置：**

如果你在负载均衡器后运行多个 Open WebUI 实例，所有实例必须共享同一个密钥。否则，一个实例签发的 token 会被另一个实例拒绝，导致登录失败。你可以通过 `openssl rand -base64 32` 生成密钥，并以环境变量形式传给所有副本。

**轮换：** 更换该密钥会让所有现有会话失效，用户需要重新登录。

---

## 认证与注册

### 注册 {#registration}

注册在第一个用户创建前保持开放，该用户会自动成为管理员。此后，注册会自动关闭，无需额外配置。

新账户的默认角色是 `pending`，这意味着管理员批准之前，用户无法访问任何功能。即使管理员重新启用注册（`ENABLE_SIGNUP=true`），`pending` 这一默认角色仍可确保新用户不会在未批准前直接进入系统。

```bash
# 新用户会先进入 "pending" 状态，等待管理员批准（默认行为）
DEFAULT_USER_ROLE=pending
```

### 密码校验 {#password-validation}

默认情况下，Open WebUI 不强制密码复杂度。要启用：

```bash
ENABLE_PASSWORD_VALIDATION=true
PASSWORD_VALIDATION_REGEX_PATTERN='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
PASSWORD_VALIDATION_HINT='Minimum 8 characters with uppercase, lowercase, number, and special character.'
```

密码在存储前会使用 bcrypt 哈希。由于 bcrypt 会在 72 字节处截断输入，Open WebUI 也会强制这一限制。

### 通过环境变量创建管理员账户

对于自动化部署，你可以在启动时直接创建管理员账户：

```bash
WEBUI_ADMIN_EMAIL=admin@yourcompany.com
WEBUI_ADMIN_PASSWORD=your-strong-password
WEBUI_ADMIN_NAME=Admin
```

这只会在数据库中还没有任何用户时生效。管理员创建完成后，注册会自动关闭。

### 仅使用 SSO 的环境

如果所有认证都交由 OAuth/OIDC 提供商处理，你可以完全隐藏本地登录表单：

```bash
ENABLE_LOGIN_FORM=false
```

这会从 UI 中移除邮箱/密码登录入口，引导所有用户走 SSO 流程。你也可以在后端层面禁用本地密码认证：

```bash
ENABLE_PASSWORD_AUTH=false
```

如果你希望“登录页密码行为”和“账号页改密行为”分开控制，还可以隐藏 **Settings > Account** 中的修改密码表单：

```bash
ENABLE_PASSWORD_CHANGE_FORM=false
```

这对于以 SSO 为主的部署很有用，因为本地密码改动本就不应对用户展示。

---

## 会话与 Cookie 安全

### Cookie 设置 {#cookie-settings}

当通过 HTTPS 提供 Open WebUI 服务时（见 [HTTPS 配置](/reference/https)），建议同时这样配置 Cookie：

```bash
WEBUI_SESSION_COOKIE_SECURE=true
WEBUI_SESSION_COOKIE_SAME_SITE=strict
```

| 变量 | 默认值 | 作用 |
|---|---|---|
| `WEBUI_SESSION_COOKIE_SECURE` | `false` | 设为 `true` 后，Cookie 只会通过 HTTPS 发送 |
| `WEBUI_SESSION_COOKIE_SAME_SITE` | `lax` | 控制 Cookie 是否会随跨站请求发送，`strict` 保护最强 |

除非分别用 `WEBUI_AUTH_COOKIE_SECURE` 和 `WEBUI_AUTH_COOKIE_SAME_SITE` 覆盖，否则这些设置同样会作用于 OAuth Cookie。

### Token 过期时间

JWT 决定用户能保持登录多久。默认值是 `4w`（4 周）。你可以缩短它：

```bash
JWT_EXPIRES_IN=24h
```

将 `JWT_EXPIRES_IN=-1` 设为无限期不过期。Open WebUI 会对此输出警告。

### Token 撤销 {#token-revocation}

:::warning Token 撤销依赖 Redis

如果没有 Redis，**用户登出后 token 不会失效**。该 token 会一直保持有效，直到自然过期（默认 4 周）。这意味着：

- 被盗或泄露的 token 无法通过登出来撤销
- 用户改密码后，已有会话不会立刻失效
- 管理员停用账户后，也不会立刻阻断访问
- OIDC back-channel logout 无法撤销 token

配置 Redis 后，Open WebUI 才支持按 token 精确撤销。当用户登出、修改密码或被管理员停用时，其 token 会被加入一个会自动过期的撤销列表。这才是面向生产的预期行为。

**如果你暂时无法部署 Redis，** 请缩短 `JWT_EXPIRES_IN`（例如 `1h` 或 `4h`）以缩小暴露窗口。Redis 配置请参考 [Redis 教程](/tutorials/integrations/redis)。

:::

---

## CORS {#cors}

跨域资源共享（CORS）决定了哪些网站可以在浏览器中向你的 Open WebUI API 发起请求。例如，如果你的实例部署在 `https://chat.yourcompany.com`，CORS 就决定了来自其他域名脚本是否可以与它交互。

默认 `CORS_ALLOW_ORIGIN` 为 `*`，意味着允许任意来源。Open WebUI 在启动时会对此发出警告。

如需限制到你的域名：

```bash
CORS_ALLOW_ORIGIN=https://chat.yourcompany.com
```

多个来源之间用分号分隔：

```bash
CORS_ALLOW_ORIGIN=https://chat.yourcompany.com;https://internal.yourcompany.com
```

如果你使用带自定义 URL scheme 的桌面应用，可通过以下方式加入：

```bash
CORS_ALLOW_CUSTOM_SCHEME=app
```

---

## 安全响应头 {#security-headers}

Open WebUI 内置 `SecurityHeadersMiddleware`，可以为响应注入 HTTP 安全头。默认情况下这些头都不会启用，因此你需要通过环境变量逐项开启。

下面是一套适合生产部署的起始配置：

```bash
# HTTP Strict Transport Security：告诉浏览器只使用 HTTPS
HSTS=max-age=31536000;includeSubDomains

# 阻止页面被嵌入到其他站点的 iframe 中
XFRAME_OPTIONS=DENY

# 阻止浏览器进行 MIME 类型嗅探
XCONTENT_TYPE=nosniff

# 控制请求中携带多少 Referrer 信息
REFERRER_POLICY=strict-origin-when-cross-origin

# 限制浏览器功能访问权限
PERMISSIONS_POLICY=camera=(),microphone=(),geolocation=()

# Content Security Policy
CONTENT_SECURITY_POLICY=default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'

# Content Security Policy 的 report-only 模式（只记录违规，不强制拦截）
CONTENT_SECURITY_POLICY_REPORT_ONLY=default-src 'self'; report-uri /csp-report

# Cross-Origin 隔离相关响应头
CROSS_ORIGIN_EMBEDDER_POLICY=require-corp    # 可选值：unsafe-none, require-corp, credentialless
CROSS_ORIGIN_OPENER_POLICY=same-origin       # 可选值：unsafe-none, same-origin-allow-popups, same-origin
CROSS_ORIGIN_RESOURCE_POLICY=same-origin     # 可选值：same-site, same-origin, cross-origin

# Reporting API 端点配置
REPORTING_ENDPOINTS=default="https://your-report-collector.example/reports"
```

:::tip

如果你启用了 Content Security Policy，请先从宽松策略开始，再逐步收紧。过于严格的 CSP 会直接破坏前端。可以先用 `CONTENT_SECURITY_POLICY_REPORT_ONLY` 做验证，浏览器开发者工具会告诉你哪些资源被拦截了。

:::

:::warning Cross-Origin Isolation

同时设置 `CROSS_ORIGIN_EMBEDDER_POLICY=require-corp` 与 `CROSS_ORIGIN_OPENER_POLICY=same-origin` 会启用跨源隔离。这可能导致来自第三方源的资源（例如外部图片、脚本或 iframe）无法加载，除非这些资源明确返回合适的 CORS 头。上线前请充分测试。

:::

---

## HTTPS 与 TLS {#https-and-tls}

Open WebUI 本身不负责 TLS 终止。请将它放在处理 HTTPS 的反向代理（Nginx、Caddy、HAProxy）之后。具体配置见 [HTTPS Reference](/reference/https)。

在 HTTPS 就位后：

```bash
WEBUI_SESSION_COOKIE_SECURE=true
HSTS=max-age=31536000;includeSubDomains
```

### 可信代理 IP

Open WebUI 使用 `--forwarded-allow-ips` 判断哪些代理被信任，可以发送 `X-Forwarded-For` 头。默认值是 `*`（信任全部），这在 Open WebUI 位于隔离网络、且前面只有单个反向代理时通常是合理的。如果你的网络拓扑更复杂，请限制为代理自身的 IP：

```bash
FORWARDED_ALLOW_IPS=192.168.1.100
```

---

## OAuth 与 SSO {#oauth-and-sso}

如果你使用 OAuth/OIDC 提供商做认证，可以借助以下配置进一步控制访问范围。

### 域名与组限制 {#domain-and-group-restrictions}

```bash
# 只允许特定邮箱域名的用户登录
OAUTH_ALLOWED_DOMAINS=yourcompany.com

# 阻止特定 IdP 组
OAUTH_BLOCKED_GROUPS='["contractors-external", "temp-accounts"]'
```

### 角色映射

将 IdP 角色映射到 Open WebUI 角色，让访问控制由身份提供商统一管理：

```bash
ENABLE_OAUTH_ROLE_MANAGEMENT=true
OAUTH_ROLES_CLAIM=roles
OAUTH_ADMIN_ROLES=admin,superadmin
OAUTH_ALLOWED_ROLES=user,admin,superadmin
```

### 账户合并

```bash
OAUTH_MERGE_ACCOUNTS_BY_EMAIL=false
```

如果启用，当 OAuth 登录邮箱与已有本地账户一致时，系统会自动合并两者。**不建议启用。** 它依赖你的 OAuth 提供商可靠验证邮箱所有权。如果提供商无法保证邮箱已验证，那么控制同一邮箱的用户就可能接管已有账户。除非你已确认提供商强制执行邮箱验证，否则请保持 `false`。

### 会话限制

```bash
# 每个用户、每个提供商允许的最大并发 OAuth 会话数（默认：10）
OAUTH_MAX_SESSIONS_PER_USER=5

# 启用 IdP 发起的后端通道登出（需要 Redis）
ENABLE_OAUTH_BACKCHANNEL_LOGOUT=true
```

---

## Trusted Header Authentication

如果你的反向代理本身负责认证（如 Authelia、Authentik、oauth2-proxy），它可以通过 HTTP 头把已认证用户身份传给 Open WebUI。**这种方式可行，但风险很大，具体取决于配置是否严谨**——配置错误会让任意客户端通过伪造请求头冒充任意用户：

```bash
WEBUI_AUTH_TRUSTED_EMAIL_HEADER=X-Forwarded-Email
WEBUI_AUTH_TRUSTED_NAME_HEADER=X-Forwarded-Name
```

:::warning

使用 trusted headers 时，你的代理**必须**先从客户端请求中剥离这些头，再注入自己可信的值。如果代理没有先剥离，任何客户端都可以自己发送伪造头并冒充任意用户。这是 trusted header 认证最常见的错误配置。请查阅你的代理文档，确认如何清理上游头。

:::

---

## LDAP

如果你通过 LDAP 做认证，请启用 TLS 来保护传输中的凭据：

```bash
ENABLE_LDAP=true
LDAP_USE_TLS=true
LDAP_VALIDATE_CERT=true
LDAP_CA_CERT_FILE=/path/to/ca-cert.pem
```

如果不启用 TLS，LDAP 凭据会以明文传输。如有需要，你还可以通过 `LDAP_CIPHERS` 限制密码套件。

---

## 数据库

### PostgreSQL {#postgresql}

对于生产部署，PostgreSQL 比默认 SQLite 提供更好的并发性与可靠性：

```bash
DATABASE_URL=postgresql://user:password@db-host:5432/openwebui
```

迁移步骤见[扩展指南](/getting-started/advanced-topics/scaling#step-1--switch-to-postgresql)。请使用强且唯一的凭据，并将数据库放在内部网络中。

### SQLCipher {#sqlcipher}

如果你仍使用 SQLite，但需要静态数据加密，Open WebUI 支持 SQLCipher：

```bash
DATABASE_TYPE=sqlite+sqlcipher
```

### 连接池调优

对于 PostgreSQL，请根据使用规模调整连接池：

```bash
DATABASE_POOL_SIZE=15
DATABASE_POOL_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
```

整个部署的总连接数 = 连接池大小 × 实例数。请确保这一数值低于 PostgreSQL 的 `max_connections`（默认 100）。

---

## API Keys

API key 允许以创建者本人的权限，以编程方式访问 Open WebUI。

```bash
# 启用 API key 创建（默认：非管理员不可创建）
ENABLE_API_KEYS=true
```

### 端点限制 {#endpoint-restrictions}

你可以限制某个 key 能调用哪些 API 路由：

```bash
ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS=true
API_KEYS_ALLOWED_ENDPOINTS=/api/chat/completions,/api/v1/models
```

当你把 key 分发给外部服务或自动化系统时，这很有用——即使 key 泄露，也能降低它可访问的范围。

### 用户权限

默认只有管理员可以创建 API key。要允许普通用户创建：

```bash
USER_PERMISSIONS_FEATURES_API_KEYS=true
```

---

## 访问控制 {#access-control}

Open WebUI 使用分层权限模型：角色、用户组以及资源级访问授权共同生效。

### 角色

| 角色 | 能力 |
|---|---|
| `admin` | 完整系统访问、用户管理、所有配置项 |
| `user` | 聊天访问、已授权模型与资源 |
| `pending` | 在管理员批准前无访问权限 |

### 关键设置

```bash
# 新用户默认角色（默认：pending）
DEFAULT_USER_ROLE=pending

# 管理员是否绕过资源级访问控制（默认：true）
BYPASS_ADMIN_ACCESS_CONTROL=true

# 管理员是否可查看所有用户聊天（默认：true）
ENABLE_ADMIN_CHAT_ACCESS=true

# 是否所有用户都能访问所有模型，而不受组限制（默认：false）
BYPASS_MODEL_ACCESS_CONTROL=false
```

### OpenAI API passthrough {#openai-api-passthrough}

```bash
ENABLE_OPENAI_API_PASSTHROUGH=false
```

OpenAI router 包含一个兜底代理端点（`/{path:path}`），可以使用管理员配置的 API key，把任意请求转发给上游兼容 OpenAI 的 API。**此功能默认关闭，也建议保持关闭。** 一旦启用，任意已认证用户都可以借助管理员凭据访问任意上游端点——包括 Open WebUI 本身并未原生支持的端点——而且不受模型级访问控制约束。除非你明确需要直通上游 API，并完全理解其安全影响，否则不要启用。

### 数据共享与导出 {#data-sharing-and-export}

以下功能决定了数据可以如何共享或导出：

```bash
# 允许用户将聊天分享给其他已认证用户（默认：true）
ENABLE_COMMUNITY_SHARING=true

# 允许管理员从数据库批量导出所有用户聊天（默认：true）
ENABLE_ADMIN_EXPORT=true

# 允许用户使用自己的 API key 直连模型提供商，
# 绕过服务端代理（默认：false）
ENABLE_DIRECT_CONNECTIONS=false
```

`ENABLE_COMMUNITY_SHARING` 允许用户为聊天生成分享链接。任何已认证且持有链接的用户都可以查看该聊天。如果你的部署涉及敏感对话，可考虑设为 `false`。

`ENABLE_DIRECT_CONNECTIONS` 启用后，用户可以在浏览器中配置自己的 API key 和模型端点。注意这些连接仍由后端发起，因此用户的 API key 会传到 Open WebUI 服务器。默认关闭。

### Workspace 权限

这些设置控制普通用户在共享工作区中的可操作范围：

```bash
USER_PERMISSIONS_WORKSPACE_MODELS_ACCESS=false
USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ACCESS=false
USER_PERMISSIONS_WORKSPACE_TOOLS_ACCESS=false
USER_PERMISSIONS_WORKSPACE_PROMPTS_ACCESS=false
```

默认都为 `false`。如需向特定用户组开放某些能力，可通过组级覆盖实现。

---

## 审计日志 {#audit-logging}

审计日志用于记录 API 活动，以满足合规、调试和使用分析需求。默认关闭。

```bash
AUDIT_LOG_LEVEL=METADATA
```

| 级别 | 记录内容 |
|---|---|
| `NONE` | 不记录（默认） |
| `METADATA` | 用户、IP、user agent、方法、URL、时间戳 |
| `REQUEST` | 元数据 + 请求体 |
| `REQUEST_RESPONSE` | 元数据 + 请求体和响应体 |

### 输出配置

```bash
# 写入文件（默认路径：/app/backend/data/audit.log）
ENABLE_AUDIT_LOGS_FILE=true
AUDIT_LOGS_FILE_PATH=/app/backend/data/audit.log
AUDIT_LOG_FILE_ROTATION_SIZE=10MB

# 同时输出到 stdout，适合日志聚合器
ENABLE_AUDIT_STDOUT=true

# 每个请求/响应体最多记录的字节数（默认：2048）
MAX_BODY_LOG_SIZE=2048
```

### 路径过滤

```bash
# 仅审计特定路径（白名单模式）
AUDIT_INCLUDED_PATHS=auths,users,configs

# 排除特定路径（黑名单模式，默认）
AUDIT_EXCLUDED_PATHS=/chats,/chat,/folders
```

认证端点（signin、signout、signup）无论路径过滤如何都会被审计。请求体中的密码会自动脱敏。

---

## 网络与外发请求

### 外发 TLS {#outbound-tls}

Open WebUI 会向模型 API、embedding 提供商、工具服务器和网页搜索服务发起外部 HTTPS 请求。默认会开启证书校验：

```bash
REQUESTS_VERIFY=true
AIOHTTP_CLIENT_SESSION_SSL=true
AIOHTTP_CLIENT_SESSION_TOOL_SERVER_SSL=true
ENABLE_WEB_LOADER_SSL_VERIFICATION=true
```

### 离线模式 {#offline-mode}

对于隔离网络环境：

```bash
OFFLINE_MODE=true
```

这会禁用 HuggingFace Hub 下载、版本检查和其他外发请求。模型与 embeddings 必须已经在本地可用。

### SSRF 防护 {#ssrf-prevention}

RAG 网页加载器可以从 URL 拉取内容。默认情况下，它不能访问本地网络地址：

```bash
ENABLE_RAG_LOCAL_WEB_FETCH=false
```

设为 `true` 后，网页加载器就可以访问私有 IP 范围，这在某些环境中可能必要，但也会引入 SSRF 风险。

Open WebUI 还会默认阻止访问云厂商元数据端点（AWS `169.254.169.254`、GCP `metadata.google.internal`、Azure `metadata.azure.com`、Alibaba Cloud `100.100.100.200`）。你也可以继续扩展这份黑名单：

```bash
WEB_FETCH_FILTER_LIST=!internal.yourcompany.com,!10.0.0.0/8
```

条目前加 `!` 表示阻止。

### 文件上传限制

默认情况下，上传文件既没有大小限制，也没有数量限制。为防止存储被占满，建议设置：

```bash
# 单文件最大大小（MB，默认无限制）
RAG_FILE_MAX_SIZE=50

# 单次上传操作的最大文件数（默认无限制）
RAG_FILE_MAX_COUNT=10

# 限制允许的文件扩展名（留空 = 全部允许）
RAG_ALLOWED_FILE_EXTENSIONS=.pdf,.txt,.md,.docx,.csv
```

---

## Tools、Functions 与 Pipelines {#tools-functions-and-pipelines}

Tools 和 Functions 会在你的服务器上执行任意 Python 代码，权限级别与 Open WebUI 进程本身相同。这是它们的工作机制，因此它们可以读取文件、发起网络请求、访问环境变量并与数据库交互。

关于其安全模型的详细说明，请参见 [Security Policy](/security#tools-functions-and-pipelines-security)。

由于 Tools 和 Functions 会执行服务端代码，因此任何拥有创建或导入权限的用户，实际上都等同于拥有 Open WebUI 进程级别的权限。这是扩展机制的天然属性。默认情况下，只有管理员可以创建和导入 Tools / Functions。下面这些设置用于控制相关权限。

### 代码执行

Open WebUI 默认启用了两个代码执行相关能力：

```bash
# 允许执行聊天回复中的代码块（默认：true，执行引擎：pyodide）
ENABLE_CODE_EXECUTION=true
CODE_EXECUTION_ENGINE=pyodide

# 允许模型在推理过程中运行代码（默认：true，执行引擎：pyodide）
ENABLE_CODE_INTERPRETER=true
CODE_INTERPRETER_ENGINE=pyodide
```

默认引擎是 `pyodide`，它通过 WebAssembly 在浏览器中运行 Python，不会在服务器上执行代码。如果你切换到 Jupyter（`jupyter`），代码就会在 Jupyter 服务器端运行，也就具备服务端访问权限。如果使用此引擎，请务必额外保护好 Jupyter 实例。

### Safe Mode

如果某个 Function 在启动时导致问题，你可以通过 Safe Mode 禁用全部 Functions：

```bash
SAFE_MODE=true
```

这样你就能重新进入管理面板，手动关闭出问题的 Function。

### 依赖安装 {#dependency-installation}

Tools 和 Functions 可以在 frontmatter 中声明 Python 依赖。默认情况下，这些依赖会通过 pip 自动安装：

```bash
# 设为 false 可阻止根据 tool/function frontmatter 自动执行 pip install
ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS=false
```

关闭后，上传的 Tools 就不能在运行时自动拉取任意包。对于生产部署，尤其是那些允许非管理员创建 Tools 的环境，建议设为 `false`。

### Workspace 访问

控制谁可以创建、导入与共享 Tools / Functions：

```bash
USER_PERMISSIONS_WORKSPACE_TOOLS_ACCESS=false
USER_PERMISSIONS_WORKSPACE_TOOLS_IMPORT=false
USER_PERMISSIONS_WORKSPACE_SKILLS_ACCESS=false
```

默认都为 `false`，意味着只有管理员可以管理 Tools 和 Functions。除非你有明确需求且信任被授权用户，否则请保持严格限制。

---

## 容器加固 {#container-hardening}

### 基础镜像

默认 Dockerfile 使用 `python:3.11-slim-bookworm`。如果你的组织要求使用加固过或已审批的基础镜像，可以通过修改 Dockerfile 中的 `FROM` 行来替换它。这在要求最小化、已做漏洞扫描的企业基础镜像环境中很常见。

### 非 root 运行 {#non-root-execution}

Dockerfile 支持以非 root 用户运行：

```bash
docker build --build-arg UID=1000 --build-arg GID=1000 .
```

### OpenShift 兼容性

对于会以任意 UID 运行容器的环境（如 OpenShift）：

```bash
docker build --build-arg USE_PERMISSION_HARDENING=true .
```

### 数据目录

数据目录（`/app/backend/data`）包含数据库、上传文件、缓存插件以及自动生成的 secret key。请使用合适的文件系统权限保护该目录，并将它纳入你的备份策略。

### 开发功能

Docker 镜像默认设置 `ENV=prod`，因此会禁用 `/docs` 上的 Swagger/OpenAPI 文档界面。如果你手动运行，请确保设置 `ENV=prod`，避免这些端点暴露出来。

---

## 可观测性 {#observability}

### 结构化日志 {#structured-logging}

```bash
LOG_FORMAT=json
GLOBAL_LOG_LEVEL=INFO
```

JSON 日志适合接入 ELK、Datadog、Splunk 等日志聚合系统。

### OpenTelemetry

```bash
ENABLE_OTEL=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317
OTEL_SERVICE_NAME=open-webui
```

完整配置请参阅 [Monitoring](/reference/monitoring) 与 [Open WebUI 日志](/getting-started/advanced-topics/logging)。

---

## SCIM 预配

SCIM 2.0 允许你的身份提供商自动管理用户账户：

```bash
ENABLE_SCIM=true
SCIM_TOKEN=your-bearer-token
SCIM_AUTH_PROVIDER=oidc
```

SCIM token 是一个拥有完整用户管理权限的静态 bearer token。请像保护管理员凭据一样保护它，定期轮换，并且只通过 HTTPS 传输。

---

## 保持 Open WebUI 最新 {#keeping-open-webui-updated}

运行最新版本的 Open WebUI，有助于让你的部署持续获得最新的安全补丁和修复。请关注[changelog](https://github.com/open-webui/open-webui/releases) 中与安全相关的更新，并尽快应用。

对于 Docker 部署，请拉取最新镜像并重建容器：

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

对于多副本部署，请遵循[滚动更新流程](/troubleshooting/multi-replica#updates-and-migrations)，避免停机。

---

## 速查表 {#quick-reference}

下表总结了本指南中的关键加固动作，每一行都链接到对应章节。

| 动作 | 默认值 | 生产环境建议 |
|---|---|---|
| [保持在私有网络中](#hardening-open-webui) | 无限制 | VPN、防火墙或 zero-trust 代理 |
| [通过 HTTPS 提供服务](#https-and-tls) | HTTP | 通过反向代理启用 HTTPS |
| [设置 `WEBUI_SECRET_KEY`](#secret-key)（多副本） | 自动生成 | 显式共享密钥 |
| [检查注册策略](#registration) | 第一个用户后禁用 | 保持禁用，或使用 `pending` 角色 |
| [启用密码校验](#password-validation) | 关闭 | `ENABLE_PASSWORD_VALIDATION=true` |
| [加固 Cookie](#cookie-settings) | `Secure=false`、`SameSite=lax` | `Secure=true`、`SameSite=strict` |
| [启用 token 撤销](#token-revocation) | 无撤销（无 Redis） | 配置 Redis 或缩短 `JWT_EXPIRES_IN` |
| [限制 CORS](#cors) | `*` | 仅允许你的明确域名 |
| [设置安全响应头](#security-headers) | 无 | HSTS、X-Frame-Options、CSP、Cross-Origin 策略 |
| [限制 OAuth 域名](#domain-and-group-restrictions) | 全部允许 | `OAUTH_ALLOWED_DOMAINS=yourdomain.com` |
| [启用审计日志](#audit-logging) | `NONE` | `METADATA` 或更高 |
| [限制 API key 端点](#endpoint-restrictions) | 所有端点 | `ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS=true` |
| [保持 API passthrough 关闭](#openai-api-passthrough) | 已关闭 | 继续保持 `ENABLE_OPENAI_API_PASSTHROUGH=false` |
| [禁用自动 pip 安装](#dependency-installation) | 已启用 | `ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS=false` |
| [检查社区共享](#data-sharing-and-export) | `true` | 有敏感数据时关闭 |
| [检查 direct connections](#data-sharing-and-export) | `false` | 非必要不要开启 |
| [使用 PostgreSQL](#postgresql) | SQLite | PostgreSQL |
| [确认外发 TLS 校验](#outbound-tls) | 已启用 | 保持开启 |
| [启用离线模式](#offline-mode) | 关闭 | 隔离网络环境设为 `OFFLINE_MODE=true` |
| [结构化日志](#structured-logging) | 文本 | `LOG_FORMAT=json` |
| [保持更新](#keeping-open-webui-updated) | N/A | 使用最新稳定版 |

---

## 安全优先的部署基线

对于把安全放在首位的组织，以下做法构成推荐部署基线。每一项都覆盖部署中的不同层面，组合起来可以形成纵深防御。括号中的链接可跳转到上文对应配置章节。

### 网络与传输

1. **将 Open WebUI 放在 VPN、反向代理或 zero-trust 访问层之后，并启用限速与 IP allowlist。** Open WebUI 适合运行在私有、可信网络中。不要在没有额外访问控制层的情况下直接暴露到公网。请在代理上配置连接速率限制、重复认证尝试限制、已知 IP 范围访问限制，并使用 fail2ban 等工具阻断恶意来源。将 `--forwarded-allow-ips` 限制为代理自身 IP，避免头部伪造。[详情](#network-placement)

2. **所有流量都使用 HTTPS，并启用完整安全头。** 使用能够终止 TLS 的反向代理。把会话 Cookie 配置为 `Secure=true` 与 `SameSite=strict`。生产环境不要通过明文 HTTP 提供 Open WebUI。启用 HSTS、Content Security Policy、X-Frame-Options、X-Content-Type-Options、Referrer-Policy 和 Permissions-Policy。不要把 CORS 保持为 `*`；只允许确实需要访问的域名。[详情](#https-and-tls)

### 认证与访问控制

3. **保持注册关闭。** Open WebUI 会在第一个用户注册后自动关闭注册。任何新账户默认角色都是 `pending`，必须经过管理员明确批准后才能访问功能。对可信网络之外可访问的实例，不要重新开启开放注册。[详情](#registration)

4. **使用身份提供商的 SSO，并关闭本地认证。** 集成组织现有的 OAuth/OIDC 或 LDAP。限制可登录的邮箱域名和 IdP 组，将 IdP 角色映射到 Open WebUI 角色，并完全关闭本地登录表单与密码认证。限制每用户并发会话数，借助 Redis 启用 backchannel logout，以便用户被回收时会话能立刻失效；除非你的提供商保证邮箱已验证，否则不要启用 OAuth 账户合并。[详情](#oauth-and-sso)

5. **强制密码复杂度并缩短会话时长。** 如果仍使用本地账户，请启用密码校验。把默认 4 周的 JWT 过期时间缩短到适合你的环境（例如 8 到 24 小时）。生产环境不要禁用 token 过期。[详情](#password-validation)

6. **定期审查用户账户和权限。** 清理不活跃账户，审计组成员关系，并确认工作区权限仍符合预期。可使用 SCIM 预配，通过身份提供商自动化账户生命周期管理。[详情](#access-control)

### Tools、Functions 与扩展

7. **将 Tool 和 Function 的创建权限严格限制给管理员，导入前审查所有代码。** 默认只有管理员可以创建、导入和管理 Tools / Functions。不要给不可信用户开放工作区权限。把第三方 Tool 看作与你基础设施上运行的其他代码一样进行审查。未经查看源码，不要导入任何 Tool。[详情](#tools-functions-and-pipelines)

8. **如果不需要，就关闭自动依赖安装和代码执行。** 设置 `ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS=false`，阻止 Tool 在运行时拉取任意包。如果部署不需要聊天中执行代码，直接全部关闭；如果需要，请保持默认 `pyodide` 引擎，因为它运行在浏览器端而不是服务器端。在没有额外保护 Jupyter 实例的情况下，不要切换到 Jupyter 引擎。保持 direct connections 与 direct tool servers 关闭。[详情](#dependency-installation)

### 数据保护

9. **限制数据共享、文件上传和 API key 访问。** 设置最大文件大小、文件数量和允许的文件扩展名。若业务上不需要，可关闭社区共享（`ENABLE_COMMUNITY_SHARING=false`）和管理员批量导出（`ENABLE_ADMIN_EXPORT=false`）。将 API key 创建权限限制在管理员范围，并启用端点限制，让每个 key 只能访问特定路由。[详情](#data-sharing-and-export)

10. **对静态数据进行加密，并保持定期备份。** 对 SQLite 使用 SQLCipher；对 PostgreSQL 使用磁盘级加密或透明数据加密。定期备份，并将备份存放在独立安全域中，同时定期演练恢复流程。[详情](#sqlcipher)

### 外发网络控制

11. **保持 SSRF 防护、外发 TLS 校验和网络限制开启。** 不要启用本地网页抓取。默认配置会阻止访问私有 IP 范围和云厂商元数据端点；你应继续将自身内部域名加入黑名单。不要关闭外发连接的证书校验。对于隔离网络环境，请启用离线模式以禁用所有外发调用。[详情](#ssrf-prevention)

### 供应链与变更管理

12. **使用官方容器镜像，或直接从源码构建。** 从 `ghcr.io/open-webui/open-webui` 或 Docker Hub 上的 `openwebui/open-webui` 拉取镜像。若要完全掌控供应链，可使用官方 Dockerfile 从[源码](https://github.com/open-webui/open-webui)构建。不要使用非官方或第三方镜像。[详情](#container-hardening)

13. **固定到具体版本，并在部署前验证更新。** 使用带标签的发行版，而不是 `:main` 或 `:latest`。升级前查看 changelog，先在预发布环境验证，再推广到生产，并确保具备回滚能力。生产环境不要自动更新。[详情](#keeping-open-webui-updated)

### 容器与基础设施

14. **以非 root 身份运行，并在分段网络中使用最小权限。** 使用非 root UID/GID，尽量采用只读文件系统挂载，移除不必要的 Linux capabilities，并设置 `--security-opt=no-new-privileges`。对数据目录应用严格权限（如 `0700`）。将 PostgreSQL 部署在独立网络段，并使用强凭据，避免直接暴露到公网。[详情](#non-root-execution)

### 可观测性与事件响应

15. **将审计日志至少开启到 METADATA 级别，并转发到你的 SIEM。** 始终记录认证端点。配置保留策略，并将日志转发到组织现有的日志基础设施。使用 JSON 日志格式，如果条件允许，还可以启用 OpenTelemetry 做分布式追踪。[详情](#audit-logging)

16. **监控异常。** 跟踪 CPU、内存、网络与磁盘使用情况。对接告警系统，尽早发现异常计算消耗、异常外发流量或存储突增。[详情](#observability)

17. **准备事件响应方案。** 明确被盗账户、未授权访问和异常资源消耗时的处理流程。你需要知道如何禁用用户账户、撤销会话（需要 Redis）、轮换 secret key，以及审查审计日志。
