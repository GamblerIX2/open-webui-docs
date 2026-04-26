---
sidebar_position: 0
title: "认证与 SSO"
---

# 🔐 认证与 SSO 教程

**将 Open WebUI 连接到身份提供商，实现单点登录、LDAP 与组同步。**

这些由社区贡献的指南会分步演示真实认证场景配置。官方 SSO 配置参考请见 [SSO (OAuth, OIDC, Trusted Header)](/features/authentication-access/auth/sso)。

---

| 教程 | 你将完成什么 | 面向对象 |
|----------|-------------------|----------|
| [Okta SSO (OIDC)](./okta-oidc-sso) | 使用 Okta 实现单点登录，支持可选组同步与 MFA | 👤 管理员 · ⏱️ 30 分钟 |
| [Azure AD LDAP](./azure-ad-ds-ldap) | 对接 Azure AD Domain Services 的安全 LDAP 认证 | 👤 管理员 · ⏱️ 45 分钟 |
| [双 OAuth 配置](./dual-oauth-configuration) | 同时启用 Microsoft 与 Google OAuth | 👤 管理员 · ⏱️ 15 分钟 |
| [Entra ID 组名同步](./entra-group-name-sync) | 将 Microsoft Entra 中的 GUID 组标识同步为可读组名 | 👤 管理员 · ⏱️ 30 分钟 |
| [Tailscale](./tailscale) | 通过 Tailscale Serve 实现 HTTPS 与 SSO，并使用 Funnel 安全隧道 | 👤 管理员 · ⏱️ 20 分钟 |
