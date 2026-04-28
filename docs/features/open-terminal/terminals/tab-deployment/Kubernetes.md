## 前置条件

- 一个正在运行的 Kubernetes 集群 (v1.24+)
- 已安装 [Helm](https://helm.sh/docs/intro/install/) v3
- 已配置 `kubectl` 以访问你的集群
- [Open WebUI 企业版许可证](https://openwebui.com/enterprise)（生产环境使用必须）

## 使用 Helm 部署

Open WebUI Helm chart 包含 Terminals 作为可选子 chart。在你的 values 文件中添加 `terminals` 部分：

```yaml
# values.yaml
terminals:
  enabled: true
  apiKey: ""  # Auto-generated if left empty

  crd:
    install: true

  operator:
    image:
      repository: ghcr.io/open-webui/terminals-operator
      tag: latest

  orchestrator:
    image:
      repository: ghcr.io/open-webui/terminals
      tag: latest
    backend: kubernetes-operator
    terminalImage: "ghcr.io/open-webui/open-terminal:latest"
    idleTimeoutMinutes: 30
```

然后安装或升级：

```bash
helm upgrade --install open-webui open-webui/open-webui \
  -f values.yaml \
  --namespace open-webui --create-namespace
```

:::tip 自动配置连接
当 `terminals.enabled` 为 `true` 时，chart 会自动设置 `TERMINAL_SERVER_CONNECTIONS` 指向集群内的编排器。不需要手动配置连接。
:::

### 验证

```bash
# 检查所有 pod 是否正在运行
kubectl get pods -n open-webui -l app.kubernetes.io/part-of=open-terminal

# 检查 CRD 是否已安装
kubectl get crd terminals.openwebui.com
```

---

## 部署了什么

当 `terminals.enabled: true` 时，chart 将创建：

| 资源 | 目的 |
| :--- | :--- |
| **CRD** (`terminals.openwebui.com`) | 定义 `Terminal` 自定义资源 |
| **Operator 部署** | Kopf 控制器，监听 Terminal CR 并配置 Pod、Service、PVC、Secret |
| **编排器部署 + 服务** | FastAPI 服务，接收来自 Open WebUI 的请求并代理到用户 Pod |
| **Secret** | 共享 API 密钥（如果未提供则自动生成） |

对于**每个用户终端**，Operator 会创建一个 Pod、Service、Secret（API 密钥），以及可选的用于持久化存储的 PVC。

---

## 生命周期

当用户激活终端时，编排器会创建一个 `Terminal` CR。Operator 会配置一个带有 Service、Secret 和可选 PVC 的 Pod。一旦 Pod 通过就绪检查，编排器就会将流量代理到它。

当终端空闲时间超过 `idleTimeoutMinutes` 时，Operator 会删除 Pod，但保留 PVC 和 Secret。在下一次请求时，将创建一个连接了相同 PVC 的新 Pod，因此在空闲周期内**用户数据能够持久化**。

```bash
# 列出所有终端
kubectl get terminals -n open-webui

# 检查特定的终端
kubectl describe terminal <name> -n open-webui

# 删除终端（子资源会自动被垃圾回收）
kubectl delete terminal <name> -n open-webui
```

---

## 监控

```bash
# Operator 日志
kubectl logs -n open-webui deployment/<release>-terminals-operator --tail=50

# 编排器日志
kubectl logs -n open-webui deployment/<release>-terminals-orchestrator --tail=50
```

---

<details>
<summary>Terminal CRD 参考</summary>

### Spec 字段

| 字段 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `userId` | 字符串 | *(必填)* | Open WebUI 用户 ID |
| `image` | 字符串 | `ghcr.io/open-webui/open-terminal:latest` | 容器镜像 |
| `resources.requests.cpu` | 字符串 | `100m` | CPU 请求 |
| `resources.requests.memory` | 字符串 | `256Mi` | 内存请求 |
| `resources.limits.cpu` | 字符串 | `1` | CPU 限制 |
| `resources.limits.memory` | 字符串 | `1Gi` | 内存限制 |
| `idleTimeoutMinutes` | 整数 | `30` | Pod 停止前的空闲超时 |
| `packages` | 数组 | `[]` | 预安装的 Apt 包 |
| `pipPackages` | 数组 | `[]` | 预安装的 Pip 包 |
| `persistence.enabled` | 布尔值 | `true` | 启用持久化存储 |
| `persistence.size` | 字符串 | `1Gi` | PVC 大小 |
| `persistence.storageClass` | 字符串 | *(集群默认)* | 存储类 |

### Status 字段

| 字段 | 描述 |
| :--- | :--- |
| `phase` | `Pending`, `Provisioning`, `Running`, `Idle`, 或 `Error` |
| `podName` | 终端 Pod 的名称 |
| `serviceUrl` | 终端的集群内 URL |
| `apiKeySecret` | 保存终端 API 密钥的 Secret |
| `lastActivityAt` | 上次代理请求的时间戳 |

</details>

<details>
<summary>完整 Helm values 参考</summary>

| 键 | 默认值 | 描述 |
| :--- | :--- | :--- |
| `terminals.enabled` | `false` | 启用 Terminals 子 chart |
| `terminals.apiKey` | (空) | 共享 API 密钥（如果为空则自动生成） |
| `terminals.existingSecret` | (空) | 预存在的 Secret 名称 (键: `api-key`) |
| `terminals.crd.install` | `true` | 安装 Terminal CRD |
| `terminals.operator.image.repository` | `ghcr.io/open-webui/terminals-operator` | Operator 镜像 |
| `terminals.operator.image.tag` | `latest` | Operator 镜像标签 |
| `terminals.operator.replicaCount` | `1` | Operator 副本数 |
| `terminals.orchestrator.image.repository` | `ghcr.io/open-webui/terminals` | 编排器镜像 |
| `terminals.orchestrator.image.tag` | `latest` | 编排器镜像标签 |
| `terminals.orchestrator.backend` | `kubernetes-operator` | 后端类型 |
| `terminals.orchestrator.terminalImage` | `ghcr.io/open-webui/open-terminal:latest` | 用户 Pod 的默认镜像 |
| `terminals.orchestrator.idleTimeoutMinutes` | `30` | 空闲超时（分钟） |
| `terminals.orchestrator.service.type` | `ClusterIP` | 编排器 Service 类型 |
| `terminals.orchestrator.service.port` | `8080` | 编排器 Service 端口 |

</details>

<details>
<summary>RBAC 要求（仅限手动安装）</summary>

如果不使用 Helm chart，Operator 的 ServiceAccount 需要一个具有以下权限的 ClusterRole：

| 资源 | 动作 (Verbs) |
| :--- | :--- |
| `terminals.openwebui.com` | get, list, watch, create, update, patch, delete |
| `pods`, `services`, `persistentvolumeclaims`, `secrets` | get, list, watch, create, update, patch, delete |
| `events` | create |
| `configmaps`, `leases` | get, list, watch, create, update, patch |

</details>
