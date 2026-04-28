---
sidebar_position: 3
title: "使用 Helm 的 Kubernetes"
---

# 使用 Helm 的 Kubernetes

可在任意 Kubernetes 发行版（EKS、AKS、GKE、OpenShift、Rancher、自建集群）上，使用官方 Open WebUI Helm Chart 进行部署。

:::info 前置条件
继续之前，请先确认你已经配置好了[共享基础设施要求](/enterprise/deployment#shared-infrastructure-requirements)——包括 PostgreSQL、Redis、向量数据库、共享存储和内容提取服务。
:::

## 何时选择这种模式

- 你的组织已经在运行 Kubernetes，并具备平台工程能力
- 你需要声明式 IaC 与 GitOps 工作流
- 你需要更高级的扩缩容（HPA）、滚动更新和 Pod Disruption Budget
- 你正在为数百到数千用户的关键任务环境部署

## 架构

```mermaid
flowchart LR
    subgraph K8s["Kubernetes Cluster"]

        subgraph mgmt["Cluster Management"]
            Ingress["Ingress Controller"]
            HPA["HPA"]
        end

        subgraph genai["GenAI Namespace"]
            subgraph Deploy["Open WebUI Deployment"]
                P1["Pod 1"]
                P2["Pod 2"]
                P3["Pod N"]
            end
        end

        subgraph data["Data Namespace"]
            PG["PostgreSQL + PGVector"]
            Redis["Redis"]
            Storage["Shared Storage"]
            Tika["Tika"]
        end

    end

    Ingress --> Deploy
    HPA -.- Deploy
    Deploy --> data
```

## Helm Chart 配置

```bash
# 添加仓库
helm repo add open-webui https://open-webui.github.io/helm-charts
helm repo update

# 使用自定义 values 安装
helm install openwebui open-webui/open-webui -f values.yaml
```

你的 `values.yaml` 应覆盖默认值，并指向共享基础设施。Chart 已为许多常见设置提供专用配置项——在可用时，应优先使用这些配置项，而不是直接传裸环境变量：

```yaml
# values.yaml 覆盖示例（完整结构请参考 chart 文档）
replicaCount: 3

# -- 数据库：使用外部 PostgreSQL 实例
databaseUrl: "postgresql://user:password@db-host:5432/openwebui"

# -- WebSocket 与 Redis：chart 可以在集群内自动部署 Redis，
#    也可以通过 websocket.url 指向外部 Redis 实例
websocket:
  enabled: true
  manager: redis
# url: "redis://my-external-redis:6379/0"  # 如使用外部 Redis，请取消注释
  redis:
    enabled: true  # set to false if using external Redis

# -- Tika：chart 可在集群内自动部署 Tika
tika:
  enabled: true

# -- Ollama：如果使用外部模型 API 或独立 Ollama 部署，请关闭
ollama:
  enabled: false

# -- 存储：多副本场景建议使用对象存储而不是本地 PVC
persistence:
  provider: s3  # or "gcs" / "azure"
  s3:
    bucket: "my-openwebui-bucket"
    region: "us-east-1"
    accessKeyExistingSecret: "openwebui-s3-creds"
    accessKeyExistingAccessKey: "access-key"
    secretKeyExistingSecret: "openwebui-s3-creds"
    secretKeyExistingSecretKey: "secret-key"
  # -- 或者，也可以用共享文件系统（RWX PVC）替代对象存储：
  # provider: local
  # accessModes:
  #   - ReadWriteMany
  # storageClass: "efs-sc"

# -- Ingress：若通过 ingress controller 对外暴露，请在此配置
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

# -- 其余没有专用 chart 配置项的设置
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

## 扩展策略

- **Horizontal Pod Autoscaler (HPA)**：基于 CPU 或内存利用率扩缩容。每个 Pod 保持 `UVICORN_WORKERS=1`，由 Kubernetes 管理副本数。
- **资源请求与限制**：设置合理的 CPU / 内存 request 和 limit，确保调度器正确放置 Pod，并使 HPA 获取准确指标。
- **Pod Disruption Budget**：配置 PDB，确保在自愿性中断（节点驱逐、集群升级）期间仍有最少数量的 Pod 保持可用。

## 更新流程

:::danger 关键更新流程
在多副本场景下，每次更新时你**必须**遵循以下流程：

1. 先将部署缩容到 **1 个副本**
2. 应用新镜像版本（单副本上设置 `ENABLE_DB_MIGRATIONS=true`）
3. 等待 Pod **完全就绪**（数据库迁移完成）
4. 再扩容回目标副本数（并设置 `ENABLE_DB_MIGRATIONS=false`）

跳过该流程会带来并发迁移导致数据库损坏的风险。
:::

## 关键注意事项

| 注意事项 | 说明 |
| :--- | :--- |
| **存储** | 上传文件应使用 **ReadWriteMany (RWX)** 共享文件系统（EFS、CephFS、NFS）或对象存储（S3、GCS、Azure Blob）。`ReadWriteOnce` 卷无法支持多 Pod。 |
| **密钥** | 凭证应存储在 Kubernetes Secrets 中，并通过 `secretKeyRef` 引用。对于 GitOps 工作流，可集成 External Secrets、Sealed Secrets 等外部密钥方案。 |
| **数据库** | 生产环境建议使用托管 PostgreSQL 服务（RDS、Cloud SQL、Azure DB）。集群内 PostgreSQL Operator（CloudNativePG、Zalando）虽可行，但会增加运维负担。 |
| **Redis** | 对于大多数部署，单个 Redis 实例配合 `timeout 1800` 和 `maxclients 10000` 已足够。只有当 Redis 本身也必须高可用时，才需要 Sentinel 或 Cluster。 |
| **网络** | 尽量让所有服务处于同一可用区。数据库延迟目标应低于 2 ms。并审查网络策略，确保 Pod 能访问 PostgreSQL、Redis 和存储后端。 |

完整 Helm 配置指南请参阅 [Quick Start guide](/getting-started/quick-start)。多副本问题排查见 [Multi-Replica Troubleshooting](/troubleshooting/multi-replica)。

---

**需要帮助规划企业部署？** 我们的团队正与全球组织合作，共同设计和落地生产级 Open WebUI 环境。

[**联系企业销售 → sales@openwebui.com**](mailto:sales@openwebui.com)
