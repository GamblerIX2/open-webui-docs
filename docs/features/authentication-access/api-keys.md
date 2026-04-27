---
sidebar_position: 500
title: "API Keys"
---

# 🔑 API Keys

**Open WebUI 的程序化访问——适用于脚本、机器人和集成。**

API Keys 是个人访问令牌，允许外部代码调用 Web 界面使用的相同端点。您在浏览器中能做的任何事情——对话补全、模型列举、文件上传、RAG 查询——您的脚本都可以通过单个 `Authorization: Bearer` 请求头来完成。每个密钥继承创建者的权限，因此无需学习单独的权限模型。

---

## 为什么使用 API Keys？

### 无需浏览器的自动化

脚本、CI/CD 流水线、监控机器人和第三方工具都需要程序化访问。API Keys 为它们提供了稳定的凭证，不会随浏览器会话过期。

### 相同权限，不同接口

API Key 代表您行事。它继承您的角色和用户组权限——管理 Web 界面的相同访问控制也适用于每个 API 请求。

### 可撤销且可审计

为每个密钥起一个描述性名称（例如"CI 流水线"、"监控机器人"）以跟踪使用情况。如果密钥泄露，立即删除——无需重置密码、无需使会话失效，只需单击一次。

---

## 主要功能

| | |
| :--- | :--- |
| 🔐 **Bearer token 认证** | 标准 `Authorization: Bearer` 请求头，适用于任何 HTTP 客户端或 SDK |
| 🛡️ **限定于用户范围** | 密钥继承创建用户的角色和用户组权限 |
| 🚫 **端点限制** | 可选择限制密钥可访问的 API 路由 |
| 👥 **权限门控** | 非管理员用户需要全局管理员开关加上每用户组的功能权限 |

---

## 入门指南

### 第一步：全局启用 API Keys（管理员操作）

1. 以**管理员**身份登录
2. 打开 **管理面板 > 设置 > 通用**
3. 滚动到 **认证** 部分
4. 切换 **启用 API Keys** 为开
5. 点击 **保存**

:::info
这是全局主开关。关闭时，任何人——包括管理员——都无法生成密钥。开启时：
- **管理员**用户可以立即生成密钥
- **非管理员**用户仍需要 API Keys 功能权限（第二步）
:::

*（可选）* 启用 **API Key 端点限制**，以限制 API Keys 可调用的路由。将允许的端点指定为逗号分隔的列表（例如 `/api/v1/models,/api/v1/chat/completions`）。

### 第二步：向非管理员用户授予权限（管理员操作）

非管理员用户需要 **API Keys** 功能权限。使用以下任一方式授予：

#### 方式 A：默认权限（所有用户）

1. **管理面板 > 用户 > 用户组 > 默认权限**
2. 在 **功能权限** 下，切换 **API Keys** 为开
3. 点击 **保存**

:::warning
这会授予所有具有"user"角色的用户生成 API Keys 的能力。要进行更严格的控制，请使用方式 B。
:::

#### 方式 B：用户组（特定用户）

1. **管理面板 > 用户 > 用户组**
2. 选择或创建一个用户组（例如"API 用户"）
3. 在 **权限 > 功能权限** 下，切换 **API Keys** 为开
4. 点击 **保存**

:::tip
创建一个专用的"API 用户"或"监控"用户组，只将需要程序化访问的账户添加进去。这遵循最小权限原则。
:::

### 第三步：生成密钥

1. 点击**个人资料图标**（左下角侧边栏）
2. 选择 **设置 > 账户**
3. 在 **API Keys** 部分，点击 **生成新 API Key**
4. 为其起一个描述性名称（例如"监控机器人"）
5. **立即复制密钥**——您以后将无法再次查看它

:::warning
将 API Keys 视为密码。将其存储在密钥管理器中，永远不要将其提交到版本控制，也不要在公共频道中分享。如果密钥泄露，立即删除并生成新的。
:::

---

## 使用您的 API Key

在 `Authorization` 请求头中将密钥作为 Bearer token 传递：

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8080/api/models
```

```python
import requests
import pathlib

response = requests.get(
    "http://localhost:8080/api/models",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
print(response.json())
```

有关完整的端点参考——对话补全、Ollama 代理、RAG、文件管理等——请参阅 [API 端点](/reference/api-endpoints)。

---

## 最佳实践

### 专用服务账户

专门为自动化创建一个**非管理员用户**（例如 `monitoring-bot`、`ci-pipeline`），从该账户生成密钥。如果密钥泄露，攻击者只能获得该用户的权限——而不是管理员访问权限。

### 端点限制

启用 **API Key 端点限制**，只将您的集成实际需要的路由加入白名单。监控机器人只需要 `/api/models` 和 `/api/chat/completions`——不要给它访问 `/api/v1/files/` 或管理员端点的权限。

### 密钥轮换

定期删除旧密钥并生成新密钥，特别是对于长期运行的集成。为密钥起名时加上日期或版本以跟踪轮换（"监控机器人 - 2025-Q1"）。

---

## 故障排查

**在设置 > 账户中看不到 API Keys 部分？**

- **检查全局开关：** 确认管理员已在 **管理面板 > 设置 > 通用 > 启用 API Keys** 中启用 API Keys。参见 [`ENABLE_API_KEYS`](/reference/env-configuration#enable_api_keys)。
- **检查您的权限（非管理员用户）：** 确认您的账户或用户组在 **功能权限** 下具有 **API Keys** 功能权限。参见 [`USER_PERMISSIONS_FEATURES_API_KEYS`](/reference/env-configuration#user_permissions_features_api_keys)。

**收到 `401 Unauthorized` 响应？**

- 验证密钥格式是否正确：`Authorization: Bearer sk-...`
- 检查密钥是否已被删除
- 如果启用了端点限制，确认您调用的路由在允许列表中

---
