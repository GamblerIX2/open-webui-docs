---
sidebar_position: 10
title: "Okta SSO（OIDC）"
---

# 🔗 Okta OIDC SSO 集成

:::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

## 概述

本文档介绍将 Okta OIDC 单点登录（SSO）与 Open WebUI 集成所需的步骤。同时涵盖基于 Okta 群组成员资格管理 Open WebUI 用户群组的**可选**功能，包括**即时（JIT）群组创建**。按照这些步骤操作后，用户可以使用其 Okta 凭据登录 Open WebUI。如果您选择启用群组同步（`ENABLE_OAUTH_GROUP_MANAGEMENT`），用户在登录时将根据其 Okta 群组自动分配到 Open WebUI 中的相关群组。如果同时启用了 JIT 群组创建（`ENABLE_OAUTH_GROUP_CREATION`），Okta 声明中存在但 Open WebUI 中缺失的群组将在登录过程中自动创建。

### 前提条件

*   一个新的或现有的 Open WebUI 实例。
*   具有创建和配置应用程序管理员权限的 Okta 账户。
*   对 OIDC、Okta 应用程序配置和 Open WebUI 环境变量有基本了解。

## 配置 Okta

首先，需要在您的 Okta 组织内配置一个 OIDC 应用程序，并设置群组声明以将群组信息传递给 Open WebUI。

### 1. 在 Okta 中创建/配置 OIDC 应用程序

1.  登录 Okta 管理控制台。
2.  导航至 **Applications > Applications**。
3.  创建新的 **OIDC - OpenID Connect** 应用程序（选择 **Web Application** 类型），或选择现有应用程序用于 Open WebUI。

    ![Okta 创建应用](/images/tutorials/okta/okta-auth-create-app.png)

4.  在设置过程中或在应用程序的 **General** 设置标签中，配置**登录重定向 URI**。添加 Open WebUI 实例的 URI，后跟 `/oauth/oidc/callback`。例如：`https://your-open-webui.com/oauth/oidc/callback`。
5.  记录应用程序 **General** 标签上提供的 **Client ID** 和 **Client secret**，Open WebUI 配置时需要用到。

    ![Okta 客户端密钥](/images/tutorials/okta/okta-auth-clientkey.png)

6.  确保在 **Assignments** 标签下将正确的用户或群组分配给该应用程序。

### 2. 向 ID 令牌添加群组声明

**（可选）** 要在 Open WebUI 中根据 Okta 群组启用自动群组管理，需要将 Okta 配置为在 ID 令牌中发送用户的群组成员资格。如果您只需要 SSO 登录并希望在 Open WebUI 中手动管理群组，可以跳过本节。

1.  在管理控制台中，转到 **Applications > Applications** 并选择您的 OIDC 客户端应用程序。
2.  转到 **Sign On** 标签，在 **OpenID Connect ID Token** 部分点击 **Edit**。
3.  在 **Group claim type** 部分，选择 **Filter**。
4.  在 **Group claims filter** 部分：
    *   输入 `groups` 作为声明名称（如果已有默认值则使用默认值）。
    *   从下拉菜单中选择 **Matches regex**。
    *   在正则表达式字段中输入 `.*`。这将包含用户所属的所有群组。如有需要，可以使用更具体的正则表达式。
5.  点击 **Save**。
6.  点击 **Back to applications** 链接。
7.  在应用程序的 **More** 下拉按钮菜单中，点击 **Refresh Application Data**。

*有关更高级的群组声明配置，请参阅 Okta 文档中的[自定义令牌](https://developer.okta.com/docs/guides/customize-tokens-returned-from-okta/main/)和[群组函数](https://developer.okta.com/docs/reference/okta-expression-language/#group-functions)。*

### 3. 应用 MFA（例如 Google Authenticator）

为增强安全性，您可以为通过 Okta 登录 Open WebUI 的用户强制执行多因素认证（MFA）。以下示例演示如何将 Google Authenticator 设置为附加因素。

1.  **配置认证器**：
    *   在 Okta 管理控制台中，导航至 **Security > Authenticators**。
    *   点击 **Add Authenticator**，添加 **Google Authenticator**。
    *   在设置过程中，可将 **"User verification"** 设置为 **"Required"** 以增强安全性。

2.  **创建并应用登录策略**：
    *   转到 **Security > Authenticators**，然后点击 **Sign On** 标签。
    *   点击 **Add a policy** 创建新策略（例如 "WebUI MFA Policy"）。
    *   在刚创建的策略中，点击 **Add rule**。
    *   配置规则：
        *   将 **"IF User's IP is"** 设置为 **"Anywhere"**。
        *   将 **"THEN Access is"** 设置为 **"Allowed after successful authentication"**。
        *   在 **"AND User must authenticate with"** 下，选择 **"Password + Another factor"**。
        *   确保您想要的因素（例如 Google Authenticator）在 **"AND Possession factor constraints are"** 下已包含。
    *   最后，将此策略分配给您的 Open WebUI 应用程序。转到 **Applications > Applications**，选择您的 OIDC 应用程序，在 **Sign On** 标签下选择您创建的策略。

现在，当用户登录 Open WebUI 时，他们需要提供 Okta 密码以及来自 Google Authenticator 的附加验证码。

:::note

重新认证频率
默认情况下，Okta 的登录策略可能不会在同一设备或浏览器的每次登录时提示 MFA，以改善用户体验。如果需要每次会话都强制 MFA，可以在您创建的策略规则中调整此设置。找到 **"Prompt for re-authentication"** 设置，将其设置为 **"Every sign-in attempt"**。

:::

## 配置 Open WebUI

要在 Open WebUI 中启用 Okta OIDC SSO，需要设置以下核心环境变量。如果希望启用可选的群组管理功能，还需要额外的变量。

```bash

# --- OIDC Core Settings ---

# Enable OAuth signup if you want users to be able to create accounts via Okta

# ENABLE_OAUTH_SIGNUP="true"

# Your Okta application's Client ID
OAUTH_CLIENT_ID="YOUR_OKTA_CLIENT_ID"

# Your Okta application's Client Secret
OAUTH_CLIENT_SECRET="YOUR_OKTA_CLIENT_SECRET"

# Your Okta organization's OIDC discovery URL

# Format: https://<your-okta-domain>/.well-known/openid-configuration

# Or for a specific authorization server: https://<your-okta-domain>/oauth2/<auth-server-id>/.well-known/openid-configuration
OPENID_PROVIDER_URL="YOUR_OKTA_OIDC_DISCOVERY_URL"

# Name displayed on the login button (e.g., "Login with Okta")
OAUTH_PROVIDER_NAME="Okta"

# Scopes to request (default is usually sufficient)

# OAUTH_SCOPES="openid email profile groups" # Ensure 'groups' is included if not default

# --- OAuth Group Management (Optional) ---

# Set to "true" only if you configured the Groups Claim in Okta (Step 2)

# and want Open WebUI groups to be managed based on Okta groups upon login.

# This syncs existing groups. Users will be added/removed from Open WebUI groups

# to match their Okta group claims.

# ENABLE_OAUTH_GROUP_MANAGEMENT="true"

# Required only if ENABLE_OAUTH_GROUP_MANAGEMENT is true.

# The claim name in the ID token containing group information (must match Okta config)

# OAUTH_GROUP_CLAIM="groups"

# Optional: Enable Just-in-Time (JIT) creation of groups if they exist in Okta claims but not in Open WebUI.

# Requires ENABLE_OAUTH_GROUP_MANAGEMENT="true".

# If set to false (default), only existing groups will be synced.

# ENABLE_OAUTH_GROUP_CREATION="false"
```

将 `YOUR_OKTA_CLIENT_ID`、`YOUR_OKTA_CLIENT_SECRET` 和 `YOUR_OKTA_OIDC_DISCOVERY_URL` 替换为 Okta 应用程序配置中的实际值。

要根据 Okta 声明启用群组同步，将 `ENABLE_OAUTH_GROUP_MANAGEMENT="true"` 设置为 `true`，并确保 `OAUTH_GROUP_CLAIM` 与 Okta 中配置的声明名称匹配（默认为 `groups`）。

要*同时*启用自动即时（JIT）创建存在于 Okta 但尚未在 Open WebUI 中的群组，将 `ENABLE_OAUTH_GROUP_CREATION="true"` 设置为 `true`。如果您只想管理 Open WebUI 中已存在群组的成员资格，可以将其保留为 `false`。

:::warning

群组成员资格管理
当 `ENABLE_OAUTH_GROUP_MANAGEMENT` 设置为 `true` 时，用户在 Open WebUI 中的群组成员资格将在每次登录时与其 Okta 声明中收到的群组**严格同步**。这意味着：
*   用户将被**添加**到与其 Okta 声明匹配的 Open WebUI 群组中。
*   如果某个 Open WebUI 群组（包括在 Open WebUI 中手动创建或分配的群组）**不**存在于该登录会话的 Okta 声明中，用户将被从该群组中**移除**。

确保所有必要的群组在 Okta 中正确配置和分配，并包含在群组声明中。

:::

:::info

多节点部署中的会话持久性

在跨多个节点部署 Open WebUI 时（例如在 Kubernetes 集群中或负载均衡器后面），确保会话持久性对于无缝用户体验至关重要，尤其是在使用 SSO 的情况下。将 `WEBUI_SECRET_KEY` 环境变量设置为**所有** Open WebUI 实例上**相同的安全唯一值**。

:::

```bash

# 示例：生成强密钥（例如使用 openssl rand -hex 32）
WEBUI_SECRET_KEY="YOUR_UNIQUE_AND_SECURE_SECRET_KEY"
```

如果该密钥在所有节点上不一致，当用户的会话被路由到不同节点时可能会被强制重新登录，因为由一个节点签发的会话令牌在另一个节点上无效。默认情况下，Docker 镜像在首次启动时会生成随机密钥，不适用于多节点设置。

:::tip

禁用标准登录表单

如果您打算*仅*允许通过 Okta（以及可能配置的其他 OAuth 提供商）登录，可以通过设置以下环境变量来禁用标准邮箱/密码登录表单：

:::


```bash
ENABLE_LOGIN_FORM="false"
```

:::danger

重要前提
将 `ENABLE_LOGIN_FORM="false"` 设置为 `false` **需要**同时将 `ENABLE_OAUTH_SIGNUP="true"` 设置为 `true`。如果在未启用 OAuth 注册的情况下禁用登录表单，**用户（包括管理员）将无法登录。** 在禁用标准登录表单之前，请确保至少配置了一个 OAuth 提供商并启用了 `ENABLE_OAUTH_SIGNUP`。

:::

Restart your Open WebUI instance after setting these environment variables.

## Verification

1.  Navigate to your Open WebUI login page. You should see a button labeled "Login with Okta" (or whatever you set for `OAUTH_PROVIDER_NAME`).
2.  Click the button and authenticate through the Okta login flow.
3.  Upon successful authentication, you should be redirected back to Open WebUI and logged in.
4.  If `ENABLE_OAUTH_GROUP_MANAGEMENT` is true, log in as a non-admin user. Their groups within Open WebUI should now strictly reflect their current group memberships in Okta (any memberships in groups *not* in the Okta claim will be removed). If `ENABLE_OAUTH_GROUP_CREATION` is also true, any groups present in the user's Okta claims that did not previously exist in Open WebUI should now have been created automatically. Note that admin users' groups are not automatically updated via SSO.
5.  Check the Open WebUI server logs for any OIDC or group-related errors if you encounter issues.

## Troubleshooting

*   **400 Bad Request/Redirect URI Mismatch:** Double-check that the **Sign-in redirect URI** in your Okta application exactly matches `<your-open-webui-url>/oauth/oidc/callback`.
*   **Groups Not Syncing:** Verify that the `OAUTH_GROUP_CLAIM` environment variable matches the claim name configured in the Okta ID Token settings. Ensure the user has logged out and back in after group changes - a login flow is required to update OIDC. Remember admin groups are not synced.
*   **Configuration Errors:** Review the Open WebUI server logs for detailed error messages related to OIDC configuration.

*   Refer to the official [Open WebUI SSO Documentation](/features/authentication-access/auth/sso).
*   Consult the [Okta Developer Documentation](https://developer.okta.com/docs/).
