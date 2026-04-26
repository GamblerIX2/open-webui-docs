---
sidebar_position: 0
title: "教程"
---

# 🎓 教程

**由 Open WebUI 社区贡献的真实场景分步指南。**

这些教程覆盖了具体任务，包括连接身份提供商、集成开发工具、管理部署等。每篇指南都围绕一个可落地的场景，帮助你从头到尾完成配置。

:::tip 我该从哪里开始？
如果你在找**初始安装**，请看 [Getting Started](/getting-started)。如果你想看**功能文档**，请看 [Features](/features)。教程面向已经跑起来 Open WebUI、并希望**进一步扩展能力**的用户。
:::

---

## 认证与 SSO

配置单点登录、LDAP 与身份联合。

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Okta SSO (OIDC)](/tutorials/auth-sso/okta-oidc-sso) | 使用 Okta 实现单点登录，支持可选的组同步与 MFA | 👤 管理员 · ⏱️ 30 分钟 |
| [Azure AD LDAP](/tutorials/auth-sso/azure-ad-ds-ldap) | 对接 Azure AD Domain Services 的安全 LDAP 认证 | 👤 管理员 · ⏱️ 45 分钟 |
| [双 OAuth 配置](/tutorials/auth-sso/dual-oauth-configuration) | 同时启用 Microsoft 与 Google OAuth | 👤 管理员 · ⏱️ 15 分钟 |
| [Entra ID 组名同步](/tutorials/auth-sso/entra-group-name-sync) | 从 Microsoft Entra 获取可读组名 | 👤 管理员 · ⏱️ 30 分钟 |
| [Tailscale](/tutorials/auth-sso/tailscale) | 通过 Tailscale Serve 实现 HTTPS 与 SSO，并使用 Funnel 隧道 | 👤 管理员 · ⏱️ 20 分钟 |

[浏览全部认证与 SSO 教程 →](/tutorials/auth-sso)

---

## Integrations

将 Open WebUI 连接到 LLM 提供商、监控平台、开发工具与外部服务。

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [Azure OpenAI（Entra ID）](/tutorials/integrations/llm-providers/azure-openai) | 对 Azure OpenAI 实现无密钥认证 | 👤 管理员 · ⏱️ 30–60 分钟 |
| [DeepSeek R1 Dynamic](/tutorials/integrations/llm-providers/deepseekr1-dynamic) | 通过 llama.cpp 运行完整 671B DeepSeek-R1 | 👤 开发者 · ⏱️ 45 分钟 |
| [Intel GPU（IPEX-LLM）](/tutorials/integrations/llm-providers/ipex_llm) | 在 Intel GPU 上加速 Ollama | 👤 开发者 · ⏱️ 20 分钟 |
| [Helicone](/tutorials/integrations/monitoring/helicone) | 监控 LLM API 调用、成本与延迟 | 👤 管理员 · ⏱️ 15 分钟 |
| [Langfuse](/tutorials/integrations/monitoring/langfuse) | 追踪 LLM 使用并评估提示词质量 | 👤 管理员 · ⏱️ 20 分钟 · ⚠️ 可能过时 |
| [Continue.dev](/tutorials/integrations/dev-tools/continue-dev) | 将 Open WebUI 作为 VS Code 后端使用 | 👤 开发者 · ⏱️ 15 分钟 |
| [Jupyter Notebooks](/tutorials/integrations/dev-tools/jupyter) | 结合 Jupyter 使用代码解释器 | 👤 开发者 · ⏱️ 20 分钟 |
| [iTerm2](/tutorials/integrations/dev-tools/iterm2) | 在 macOS 终端中调用模型 | 👤 开发者 · ⏱️ 10 分钟 |
| [Firefox Sidebar](/tutorials/integrations/dev-tools/firefox-sidebar) | 将 Open WebUI 固定到 Firefox AI 侧栏 | 👤 用户 · ⏱️ 5 分钟 |
| [浏览器搜索引擎](/tutorials/integrations/dev-tools/browser-search-engine) | 将 Open WebUI 添加为浏览器搜索引擎 | 👤 用户 · ⏱️ 5 分钟 |
| [Notion（MCP）](/tutorials/integrations/mcp-notion) | 通过 Model Context Protocol 连接 Notion | 👤 用户 · ⏱️ 5 分钟 |
| [OneDrive 与 SharePoint](/tutorials/integrations/onedrive-sharepoint) | 将 Microsoft 365 文档接入 Open WebUI | 👤 管理员 · ⏱️ 30 分钟 |
| [LibreTranslate](/tutorials/integrations/libre-translate) | 增加自托管翻译能力 | 👤 管理员 · ⏱️ 15 分钟 |

[浏览全部集成教程 →](/tutorials/integrations)

---

## Maintenance

保持部署健康稳定：备份、存储、离线模式与数据库管理。

| 教程 | 你将完成什么 | 详情 |
|----------|-------------------|---------|
| [备份](/tutorials/maintenance/backups) | 备份并恢复全部 Open WebUI 数据 | 👤 管理员 · ⏱️ 15 分钟 |
| [数据库管理](/tutorials/maintenance/database) | 管理、迁移并排查数据库问题 | 👤 管理员 · ⏱️ 20 分钟 |
| [离线模式](/tutorials/maintenance/offline-mode) | 在无互联网访问条件下运行 Open WebUI | 👤 管理员 · ⏱️ 30 分钟 |
| [S3 存储](/tutorials/maintenance/s3-storage) | 将上传内容存储到兼容 S3 的对象存储 | 👤 管理员 · ⏱️ 20 分钟 |

[浏览全部维护教程 →](/tutorials/maintenance)

---

## 更多内容

| 页面 | 说明 |
|------|------------|
| [参与文档贡献](/tutorials/contributing-tutorial) | 配置 Fork、撰写教程并向文档仓库提交 PR |
| [社区指南与视频 →](/tutorials/community) | 社区提供的部署教程、评测与实操演示 |
