---
sidebar_position: 3
title: "部署选项"
---

# 可扩展的企业部署选项

Open WebUI 的**无状态、容器优先架构**意味着：无论你把它部署为虚拟机上的 Python 进程、托管容器服务中的容器，还是 Kubernetes 集群中的 Pod，本质上运行的都是同一个应用。不同部署模式之间的差异，在于你如何**编排、扩展和运维**它，而不是应用本身的行为发生改变。

:::tip 模型推理是独立维度
LLM 模型如何提供服务，与 Open WebUI 如何部署是两个独立问题。无论采用哪种部署模式，你都可以使用**托管 API**（OpenAI、Anthropic、Azure OpenAI、Google Gemini）或**自托管推理**（Ollama、vLLM）。关于模型接入方式，详见[集成](/enterprise/integration)。
:::

---

## 共享基础设施要求 {#shared-infrastructure-requirements}

无论你选择哪一种部署模式，任何需要扩展的 Open WebUI 部署都依赖同一组后端服务。在从单实例扩展之前，请先完成这些基础设施配置。

| 组件 | 为什么必需 | 可选方案 |
| :--- | :--- | :--- |
| **PostgreSQL** | 多实例部署必须使用真正的数据库。SQLite 不支持多个进程并发写入。 | 自托管、Amazon RDS、Azure Database for PostgreSQL、Google Cloud SQL |
| **Redis** | 用于会话管理、WebSocket 协调和实例间配置同步。 | 自托管、Amazon ElastiCache、Azure Cache for Redis、Google Memorystore |
| **向量数据库** | 默认 ChromaDB 使用本地 SQLite 后端，不适合多进程访问。 | PGVector（复用 PostgreSQL）、Milvus、Qdrant，或 HTTP Server 模式的 ChromaDB |
| **共享存储** | 上传文件必须能被所有实例访问。 | 共享文件系统（NFS、EFS、CephFS）或对象存储（`S3`、`GCS`、`Azure Blob`） |
| **内容提取** | 默认 `pypdf` 提取器在持续负载下会发生内存泄漏。 | 以 Sidecar 方式运行 Apache Tika 或 Docling |
| **Embedding 引擎** | 默认 SentenceTransformers 模型会为每个 worker 进程加载约 500 MB 内存。 | OpenAI Embeddings API，或运行 embedding 模型的 Ollama |

### 关键配置 {#critical-configuration}

以下环境变量**必须**在所有实例中保持一致：

```bash
# 共享密钥 —— 所有实例必须完全一致
WEBUI_SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/openwebui

# Vector Database
VECTOR_DB=pgvector
PGVECTOR_DB_URL=postgresql://user:password@db-host:5432/openwebui

# Redis
REDIS_URL=redis://redis-host:6379/0
WEBSOCKET_MANAGER=redis
ENABLE_WEBSOCKET_SUPPORT=true

# Content Extraction
CONTENT_EXTRACTION_ENGINE=tika
TIKA_SERVER_URL=http://tika:9998

# Embeddings
RAG_EMBEDDING_ENGINE=openai

# 存储 —— 二选一：
# 方案 A：共享文件系统（为所有实例挂载同一个卷，无需额外环境变量）
# 方案 B：对象存储（所有所需变量见 https://docs.openwebui.com/reference/env-configuration#cloud-storage）
# STORAGE_PROVIDER=s3

# Workers —— 让编排器负责扩缩容
UVICORN_WORKERS=1

# 数据库迁移 —— 只能有一个实例负责执行迁移
ENABLE_DB_MIGRATIONS=false
```

:::warning 数据库迁移
除一个实例外，**所有实例**都应设置 `ENABLE_DB_MIGRATIONS=false`。更新时，先缩容到单实例，等待迁移完成，再重新扩容。并发迁移可能损坏数据库。
:::

如需完整的逐步扩展指南，请参阅 [Scaling Open WebUI](/getting-started/advanced-topics/scaling)。完整环境变量参考见 [Environment Variable Configuration](/reference/env-configuration)。

---

## 选择你的部署模式

Open WebUI 支持三种生产级部署模式。每份指南都涵盖该模式对应的架构、扩展策略和关键注意事项。

### [自动扩缩容虚拟机上的 Python / Pip](./python-pip)

将 `open-webui serve` 以 systemd 管理的进程形式，部署在云自动扩缩容虚拟机组（AWS ASG、Azure VMSS、GCP MIG）中。适合已经具备 VM 基础设施和较强 Linux 运维能力的团队，或受监管要求必须进行操作系统层直接控制的场景。

### [容器服务](./container-service)

在 AWS ECS/Fargate、Azure Container Apps、Google Cloud Run 等托管平台上运行官方 Open WebUI 容器镜像。适合希望获得容器优势（不可变镜像、版本化部署、无需管理操作系统），但又不想引入 Kubernetes 复杂度的团队。

### [使用 Helm 的 Kubernetes](./kubernetes-helm)

在任意 Kubernetes 发行版（EKS、AKS、GKE、OpenShift、Rancher、自建集群）上使用官方 Open WebUI Helm Chart 部署。适合需要声明式基础设施、进阶自动扩缩容与 GitOps 工作流的大规模关键任务级场景。

---

## 部署模式对比

| | **Python / Pip（VM）** | **容器服务** | **Kubernetes（Helm）** |
| :--- | :--- | :--- | :--- |
| **运维复杂度** | 中等 —— 需管理 OS 补丁和 Python 运行环境 | 低 —— 容器由平台托管 | 较高 —— 需要 K8s 专业能力 |
| **自动扩缩容** | 云 ASG/VMSS + 健康检查 | 平台原生，配置较少 | HPA，控制更精细 |
| **容器隔离** | 无 —— 进程直接运行在 OS 上 | 完整容器隔离 | 完整容器 + namespace 隔离 |
| **滚动更新** | 手动（缩容、更新、再扩容） | 平台托管滚动部署 | 声明式滚动更新，并支持回滚 |
| **基础设施即代码** | Terraform/Pulumi + 配置管理 | 任务/服务定义（CloudFormation、Bicep、Terraform） | Helm Chart + GitOps（Argo CD、Flux） |
| **最适用场景** | 以虚拟机为核心的团队，或受监管限制的环境 | 想要容器收益但不想承担 K8s 复杂度的团队 | 大规模、关键任务级部署 |
| **团队最低能力要求** | Linux 运维、Python | 容器基础、云平台 | Kubernetes、Helm、云原生模式 |

---

## 可观测性

无论采用哪种部署模式，生产环境都应具备监控与可观测性。

### 健康检查

- **`/health`** —— 基础存活检查。应用正常运行时返回 HTTP 200。可用于负载均衡器和自动扩缩容健康检查。
- **`/api/models`** —— 验证应用是否能连接到已配置的模型后端。需要 API key。

### OpenTelemetry

Open WebUI 支持使用 **OpenTelemetry** 进行分布式追踪和 HTTP 指标采集。启用方式如下：

```bash
ENABLE_OTEL=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4318
OTEL_SERVICE_NAME=open-webui
```

它会自动为 FastAPI、SQLAlchemy、Redis 和 HTTP 客户端注入观测能力，从而帮助你了解请求延迟、数据库查询性能和跨服务链路。

### 结构化日志

启用 JSON 格式日志，以便接入 Datadog、Loki、CloudWatch、Splunk 等日志平台：

```bash
LOG_FORMAT=json
GLOBAL_LOG_LEVEL=INFO
```

完整监控配置详情请参阅 [Monitoring](/reference/monitoring) 和 [OpenTelemetry](/reference/monitoring/otel)。

---

## 下一步

- **[架构与高可用性](/enterprise/architecture)** —— 深入了解 Open WebUI 的无状态设计与高可用能力。
- **[安全](/enterprise/security)** —— 合规框架、SSO/LDAP 集成、RBAC 与审计日志。
- **[集成](/enterprise/integration)** —— 连接 AI 模型、Pipeline，并扩展平台能力。
- **[Scaling Open WebUI](/getting-started/advanced-topics/scaling)** —— 完整的逐步技术扩展指南。
- **[Multi-Replica Troubleshooting](/troubleshooting/multi-replica)** —— 多副本扩展部署中的常见问题解决方案。

---

**需要帮助规划企业部署？** 我们的团队正与全球组织合作，共同设计和落地生产级 Open WebUI 环境。

[**联系企业销售 → sales@openwebui.com**](mailto:sales@openwebui.com)
