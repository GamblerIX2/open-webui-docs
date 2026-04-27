---
sidebar_position: 3
title: "使用 Helm 的 Kubernetes"
---

# 使用 Helm 的 Kubernetes

在任意 Kubernetes 发行版（EKS、AKS、GKE、OpenShift、Rancher、自管集群）上使用官方 Open WebUI Helm Chart 进行部署。

:::info 前置条件
继续之前，请先完成[共享基础设施要求](/enterprise/deployment#shared-infrastructure-requirements)的配置——包括 PostgreSQL、Redis、向量数据库、共享存储和内容提取。
:::

## 何时选择这种模式

- 你的组织已经运行 Kubernetes，并具备平台工程能力
- 你需要声明式基础设施即代码和 GitOps 工作流
- 你需要高级扩缩容（HPA）、滚动更新以及 Pod disruption budget
- 你面向的是数百到数千用户的关键业务环境

## 架构

```mermaid
flowchart LR
    subgraph K8s["Kubernetes 集群"]

        subgraph mgmt["集群管理"]
            Ingress["Ingress Controller"]
            HPA["HPA"]
        end

        subgraph genai["GenAI 命名空间"]
            subgraph Deploy["Open WebUI Deployment"]
                P1["Pod 1"]
                P2["Pod 2"]
                P3["Pod N"]
            end
        end

        subgraph data["数据命名空间"]
            PG["PostgreSQL + PGVector"]
            Redis["Redis"]
            Storage["共享存储"]
            Tika["Tika"]
        end

    end

    Ingress --> Deploy
    HPA -.- Deploy
    Deploy --> data
```

## Helm Chart 设置

```bash
# 添加仓库
helm repo add open-webui https://open-webui.github.io/helm-charts
helm repo update

# 使用自定义 values 安装
helm install openwebui open-webui/open-webui -f values.yaml
```

你的 `values.yaml` 应覆盖默认值，以指向共享基础设施。对于常见设置，Chart 已提供专门字段——可用时优先使用这些字段，而不是原始环境变量：

```yaml
# values.yaml 覆盖示例（完整 schema 请参见 chart 文档）
replicaCount: 3

# -- 数据库：使用外部 PostgreSQL 实例
databaseUrl: "postgresql://user:password@db-host:5432/openwebui"

# -- WebSocket 与 Redis：chart 可在集群内自动部署 Redis，
#    也可以通过 websocket.url 指向外部 Redis 实例
websocket:
  enabled: true
  manager: redis
  # url: "redis://my-external-redis:6379/0"  # 取消注释以使用外部 Redis
  redis:
    enabled: true  # 如果使用外部 Redis，请设为 false

# -- Tika：chart 可在集群内自动部署 Tika
tika:
  enabled: true

# -- Ollama：如果使用外部模型 API 或独立的 Ollama 部署，请禁用
ollama:
  enabled: false

# -- 存储：多副本场景使用对象存储，而不是本地 PVC
persistence:
  provider: s3  # 或 "gcs" / "azure"
  s3:
    bucket: "my-openwebui-bucket"
    region: "us-east-1"
    accessKeyExistingSecret: "openwebui-s3-creds"
    accessKeyExistingAccessKey: "access-key"
    secretKeyExistingSecret: "openwebui-s3-creds"
    secretKeyExistingSecretKey: "secret-key"
  # -- 也可以使用共享文件系统（RWX PVC）替代对象存储：
  # provider: local
  # accessModes:
  #   - ReadWriteMany
  # storageClass: "efs-sc"

# -- Ingress：如果需要通过 ingress controller 暴露服务，请配置
ingress:
  enabled: true
  class: "nginx"
  host: "ai.example.com"
  tls: true
  existingSecret: "openwebui-tls"
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "open-webui-session"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"

# -- 其余没有专用 chart 字段的设置
extraEnvVars:
  - name: WEBUI_SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: openwebui-secrets
        key: secret-key
  - name: VECTOR_DB
    value: "pgvector"
  - name: PGVECTOR_DB_URL
    valueFrom:
      secretKeyRef:
        name: openwebui-secrets
        key: database-url
  - name: UVICORN_WORKERS
    value: "1"
  - name: ENABLE_DB_MIGRATIONS
    value: "false"
  - name: RAG_EMBEDDING_ENGINE
    value: "openai"
```

## 扩缩容策略

- **Horizontal Pod Autoscaler (HPA)**：根据 CPU 或内存利用率扩缩容。每个 Pod 保持 `UVICORN_WORKERS=1`，由 Kubernetes 管理副本数。
- **资源请求与限制**：设置合适的 CPU 和内存 request/limit，确保调度器正确放置 Pod，并让 HPA 拿到准确指标。
- **Pod disruption budgets**：配置 PDB，确保在自愿中断（节点排空、集群升级）期间始终保留最小可用 Pod 数。

## 更新流程

:::danger 关键更新流程
在运行多个副本时，**每次更新都必须**遵循以下过程：

1. 将部署缩容到 **1 个副本**
2. 应用新镜像版本（并在单副本上设置 `ENABLE_DB_MIGRATIONS=true`）
3. 等待 Pod **完全就绪**（数据库迁移完成）
4. 再扩回目标副本数（并设置 `ENABLE_DB_MIGRATIONS=false`）

跳过这一步可能因并发迁移而导致数据库损坏。
:::

## 关键注意事项

| 注意事项 | 说明 |
| :--- | :--- |
| **存储** | 上传文件应使用 **ReadWriteMany (RWX)** 共享文件系统（EFS、CephFS、NFS）或对象存储（S3、GCS、Azure Blob）。ReadWriteOnce 卷无法用于多 Pod 场景。 |
| **密钥** | 将凭据保存在 Kubernetes Secrets 中，并通过 `secretKeyRef` 引用。对于 GitOps 工作流，可接入外部密钥运维方案（External Secrets、Sealed Secrets）。 |
| **数据库** | 生产环境建议使用托管 PostgreSQL 服务（RDS、Cloud SQL、Azure DB）。集群内 PostgreSQL Operator（CloudNativePG、Zalando）也可行，但会增加运维负担。 |
| **Redis** | 对大多数部署来说，单实例 Redis 配合 `timeout 1800` 和 `maxclients 10000` 已足够。只有在 Redis 本身也需要高可用时，才需要 Redis Sentinel 或 Cluster。 |
| **网络** | 尽量将所有服务放在同一可用区内，并将数据库延迟控制在 2 ms 以下。审计网络策略，确保 Pod 能访问 PostgreSQL、Redis 和存储后端。 |

完整 Helm 配置指南请参阅[快速开始指南](/getting-started/quick-start)。如需排查多副本问题，请参阅[多副本故障排查](/troubleshooting/multi-replica)。

---

**需要帮助规划企业部署吗？** 我们的团队正在帮助全球组织设计并实施生产级 Open WebUI 环境。

[**联系企业销售 → sales@openwebui.com**](mailto:sales@openwebui.com)
