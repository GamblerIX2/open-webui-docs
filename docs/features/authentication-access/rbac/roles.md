---
sidebar_position: 3
title: "角色"
---


Open WebUI 定义了三种主要的**系统角色**，用于确定用户账户的基础访问级别。这些角色与[用户组](./groups.md)和[权限](./permissions.md)有所不同。

| 角色 | 关键字 | 说明 |
| :--- | :--- | :--- |
| **管理员** | `admin` | **超级用户**。对系统拥有完全控制权。 |
| **用户** | `user` | **标准用户**。受 RBAC 权限约束。 |
| **待审批** | `pending` | **受限**。在获得批准之前无法访问。 |

## 角色详情

### 管理员（`admin`）
管理员角色专为系统维护人员设计。
*   **完全访问**：默认访问所有资源和设置。
*   **管理权限**：可以管理用户、用户组和全局配置。
*   **绕过检查**：默认情况下绕过大多数权限检查。

:::warning 管理员限制与最佳实践
虽然管理员通常拥有不受限制的访问权限，但某些系统配置可能会出于安全和隐私原因限制其能力：
*   **隐私控制**：像 `ENABLE_ADMIN_CHAT_ACCESS=False` 这样的环境变量可以防止管理员查看用户的对话。
*   **特定功能异常可能存在**：某些功能可以在标准管理员绕过行为之外强制执行额外检查。特别是对于 API Keys，只要启用了 `ENABLE_API_KEYS`，管理员就可以生成密钥。
*   **访问控制例外**：如果禁用了 `BYPASS_ADMIN_ACCESS_CONTROL`，管理员可能需要明确权限才能访问私有模型/知识库/笔记资源。

为获得稳健的安全态势，我们建议通过用户组将管理员纳入您的权限体系，而不仅仅依赖角色的隐式绕过。这确保了在启用绕过限制时能保持一致的访问。
:::

### 标准用户（`user`）
这是团队成员的默认功能角色。
*   **受权限约束**：没有隐式访问权限。所有能力必须通过**全局默认权限**或**用户组成员资格**来授予。
*   **累加权限**：如[权限](./permissions.md)部分所述，其有效权限是所有授予的总和。

### 待审批用户（`pending`）
新注册用户（如果已配置）或已停用用户的默认状态。
*   **零访问**：无法执行任何操作或查看任何内容。
*   **需要审批**：必须由现有管理员提升为 `user` 或 `admin`。

:::note
`admin` 角色对所有内容实际上都有 `check_permission() == True`。细粒度权限（如禁用"网络搜索"）通常**不**适用于管理员。
:::

## 角色分配

### 初始设置
*   **第一个用户：** 在全新安装中创建的第一个账户会自动被分配**管理员**角色。
*   **无头管理员创建：** 对于自动化/容器化部署，可以使用环境变量自动创建管理员账户（见下文）。
*   **后续用户：** 新注册用户被分配**默认用户角色**。

### 配置
可以通过 `DEFAULT_USER_ROLE` 环境变量控制新用户的默认角色：

```bash
DEFAULT_USER_ROLE=pending
# 选项：'pending'、'user'、'admin'
```
*   **pending（推荐用于公共/共享实例）：** 新用户在管理员于管理面板中明确激活之前无法登录。
*   **user：** 新用户以默认权限立即获得访问权限。
*   **admin：**（谨慎使用）新用户成为完全管理员。

## 更改角色
管理员可以随时通过**管理面板 > 用户**更改用户的角色。
*   将用户提升为 `admin` 会授予其完全控制权。
*   将管理员降级为 `user` 会使其再次受到权限系统约束。

## 无头管理员账户创建

对于**自动化部署**（Docker、Kubernetes、云平台），手动交互不切实际时，Open WebUI 支持在首次启动时使用环境变量自动创建管理员账户。

### 工作原理

配置以下环境变量时：
- `WEBUI_ADMIN_EMAIL`：管理员账户的邮箱地址
- `WEBUI_ADMIN_PASSWORD`：管理员账户的密码
- `WEBUI_ADMIN_NAME`：（可选）管理员显示名称（默认为"Admin"）

Open WebUI 将自动：
1. 在启动时检查数据库中是否存在任何用户
2. 如果数据库为空（全新安装），使用提供的凭据创建管理员账户
3. 安全地对密码进行哈希处理并存储
4. 自动禁用注册（`ENABLE_SIGNUP=False`）以防止未经授权的账户创建

### 使用场景

此功能在以下场景特别有用：
- **CI/CD 流水线**：使用密钥管理系统中的凭据自动预配 Open WebUI 实例
- **Docker/Kubernetes 部署**：消除容器启动和手动创建管理员之间的时间间隔
- **自动化测试**：创建具有预配置管理员账户的可重现测试环境
- **无头服务器**：部署无法通过 UI 手动创建账户的实例

### 配置示例

#### Docker Compose
```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - WEBUI_ADMIN_EMAIL=admin@example.com
      - WEBUI_ADMIN_PASSWORD=${ADMIN_PASSWORD}  # 使用密钥管理
      - WEBUI_ADMIN_NAME=System Administrator
    # ... 其他配置
```

#### Kubernetes Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: openwebui-admin
type: Opaque
stringData:
  admin-email: admin@example.com
  admin-password: your-secure-password
  admin-name: System Administrator
---
apiVersion: v1
kind: Pod
metadata:
  name: open-webui
spec:
  containers:
  - name: open-webui
    image: ghcr.io/open-webui/open-webui:main
    env:
    - name: WEBUI_ADMIN_EMAIL
      valueFrom:
        secretKeyRef:
          name: openwebui-admin
          key: admin-email
    - name: WEBUI_ADMIN_PASSWORD
      valueFrom:
        secretKeyRef:
          name: openwebui-admin
          key: admin-password
    - name: WEBUI_ADMIN_NAME
      valueFrom:
        secretKeyRef:
          name: openwebui-admin
          key: admin-name
```

### 重要说明

:::warning 安全注意事项
- **使用密钥管理**：切勿在 Docker Compose 文件或 Dockerfile 中硬编码 `WEBUI_ADMIN_PASSWORD`。请使用 Docker secrets、Kubernetes secrets 或环境变量注入。
- **强密码**：在生产部署中使用强且唯一的密码。
- **设置后更改**：考虑在初始部署后通过 UI 更改管理员密码以提高安全性。
- **自动禁用注册**：创建管理员账户后，注册将自动禁用。如果需要，可以稍后通过**管理面板 > 设置 > 通用**重新启用。
:::

:::info 行为详情
- **仅在全新安装时**：管理员账户**仅**在数据库中没有用户时创建。如果用户已存在，这些环境变量将被忽略。
- **密码哈希**：密码使用与手动账户创建相同的机制进行安全哈希，确保安全性。
- **一次性操作**：这是首次启动时的一次性操作。使用相同环境变量的后续重启不会修改现有管理员账户。
:::

有关这些环境变量的完整文档，请参阅[环境配置指南](/reference/env-configuration#webui_admin_email)。
