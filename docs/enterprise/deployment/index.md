---
sidebar_position: 3
title: "部署选项"
---

# 可扩展的企业部署选项

Open WebUI 的**无状态、容器优先架构**意味着，无论你将它部署为虚拟机中的 Python 进程、托管服务里的容器，还是 Kubernetes 集群中的 Pod，运行的都是同一个应用。不同部署模式的差异在于你如何**编排、扩展和运维**应用，而不是应用本身如何工作。

:::tip 模型推理由部署方式独立
LLM 模型的提供方式与 Open WebUI 的部署方式彼此独立。无论采用哪种部署模式，你都可以使用**托管 API**（OpenAI、Anthropic、Azure OpenAI、Google Gemini）或**自托管推理**（Ollama、vLLM）。有关连接模型的细节，请参阅 [集成](/enterprise/integration)。
:::

---

## 共享基础设施要求

无论选择哪种部署模式，每个可扩展的 Open WebUI 部署都需要同一组后端服务。在扩展到单实例以上之前，请先完成这些配置。

| 组件 | 必需原因 | 可选方案 |
| :--- | :--- | :--- |
| **PostgreSQL** | 多实例部署需要真正的数据库。SQLite 不支持多个进程并发写入。 | 自管、Amazon RDS、Azure Database for PostgreSQL、Google Cloud SQL |
| **Redis** | 用于会话管理、WebSocket 协调以及实例间配置同步。 | 自管、Amazon ElastiCache、Azure Cache for Redis、Google Memorystore |
| **向量数据库** | 默认 ChromaDB 使用本地 SQLite 后端，不适合多进程访问。 | PGVector（复用 PostgreSQL）、Milvus、Qdrant，或以 HTTP 服务器模式运行 ChromaDB |
| **共享存储** | 上传文件必须能被每个实例访问。 | 共享文件系统（NFS、EFS、CephFS）或对象存储（`S3`、`GCS`、`Azure Blob`） |
| **内容提取** | 默认 `pypdf` 提取器在持续负载下会出现内存泄漏。 | 将 Apache Tika 或 Docling 作为 sidecar 服务运行 |
| **Embedding 引擎** | 默认 SentenceTransformers 模型会在每个 worker 进程中加载约 500 MB 内存。 | OpenAI Embeddings API，或运行 embedding 模型的 Ollama |

### 关键配置

以下环境变量**必须**在所有实例之间保持一致：

```bash
# 共享密钥 —— 所有实例必须完全一致
WEBUI_SECRET_KEY=your-secret-key-here

# 数据库
DATABASE_URL=postgresql://user:password@db-host:5432/openwebui

# 向量数据库
VECTOR_DB=pgvector
PGVECTOR_DB_URL=postgresql://user:password@db-host:5432/openwebui

# Redis
REDIS_URL=redis://redis-host:6379/0
WEBSOCKET_MANAGER=redis
ENABLE_WEBSOCKET_SUPPORT=true

# 内容提取
CONTENT_EXTRACTION_ENGINE=tika
TIKA_SERVER_URL=http://tika:9998

# Embeddings
RAG_EMBEDDING_ENGINE=openai

# 存储 —— 二选一：
# 方案 A：共享文件系统（将同一卷挂载到所有实例，无需环境变量）
# 方案 B：对象存储（所需变量请参见 https://docs.openwebui.com/reference/env-configuration#cloud-storage）
# STORAGE_PROVIDER=s3

# Workers —— 交给编排平台扩缩容
UVICORN_WORKERS=1

# 数据库迁移 —— 只有一个实例应执行迁移
ENABLE_DB_MIGRATIONS=false
```

:::warning 数据库迁移
在**除一个实例外的所有实例**上设置 `ENABLE_DB_MIGRATIONS=false`。升级时，先缩容到单实例，等待迁移完成，再扩回原副本数。并发迁移可能损坏数据库。
:::

完整的逐步扩展指南请参阅 [扩展 Open WebUI](/getting-started/advanced-topics/scaling)，完整环境变量参考请参阅 [环境变量配置](/reference/env-configuration)。

---

## 选择你的部署模式

Open WebUI 支持三种生产级部署模式。每份指南都涵盖该模式特有的架构、扩展策略和关键注意事项。

### [虚拟机上的 Python / Pip 自动扩缩容部署](./python-pip)

在云自动扩缩容组（AWS ASG、Azure VMSS、GCP MIG）的虚拟机上，以 systemd 管理 `open-webui serve` 进程。适合已经采用 VM 基础设施、具备较强 Linux 运维能力，或因监管要求必须直接控制操作系统层的团队。

### [容器服务](./container-service)

在 AWS ECS/Fargate、Azure Container Apps 或 Google Cloud Run 等托管平台上运行官方 Open WebUI 容器镜像。适合希望获得容器优势（不可变镜像、版本化部署、无需管理操作系统），但不想承担 Kubernetes 复杂度的团队。

### [使用 Helm 的 Kubernetes](./kubernetes-helm)

在任意 Kubernetes 发行版（EKS、AKS、GKE、OpenShift、Rancher、自管集群）上使用官方 Open WebUI Helm Chart 部署。适合需要声明式基础设施即代码、高级自动扩缩容和 GitOps 工作流的大规模关键业务场景。

---

## 部署方式对比

| | **Python / Pip（VM）** | **容器服务** | **Kubernetes（Helm）** |
| :--- | :--- | :--- | :--- |
| **运维复杂度** | 中等 —— 需要打补丁和管理 Python | 低 —— 平台托管容器 | 较高 —— 需要 K8s 专业能力 |
| **自动扩缩容** | 使用云 ASG/VMSS 配合健康检查 | 平台原生，配置较少 | HPA，控制更细粒度 |
| **容器隔离** | 无 —— 进程直接运行在操作系统上 | 完整容器隔离 | 容器 + 命名空间双重隔离 |
| **滚动更新** | 手动（缩容、更新、再扩容） | 平台托管滚动发布 | 声明式滚动更新并支持回滚 |
| **基础设施即代码** | VM + 配置管理使用 Terraform/Pulumi | 任务/服务定义（CloudFormation、Bicep、Terraform） | Helm Chart + GitOps（Argo CD、Flux） |
| **最适合** | 以 VM 为中心运维、存在监管约束的团队 | 想获得容器优势但不想引入 K8s 的团队 | 大规模、关键业务部署 |
| **最低团队能力要求** | Linux 运维、Python | 容器基础、云平台 | Kubernetes、Helm、云原生模式 |

---

## 可观测性

无论选择哪种部署模式，生产部署都应包含监控与可观测性。

### 健康检查

- **`/health`** —— 基础存活检查。当应用运行时返回 HTTP 200。可用于负载均衡器和自动扩缩容器的健康检查。
- **`/api/models`** —— 验证应用是否能连接到已配置的模型后端。需要 API key。

### OpenTelemetry

Open WebUI 支持使用 **OpenTelemetry** 进行分布式追踪和 HTTP 指标采集。可通过以下配置启用：

```bash
ENABLE_OTEL=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4318
OTEL_SERVICE_NAME=open-webui
```

该功能会自动为 FastAPI、SQLAlchemy、Redis 和 HTTP 客户端注入监控，从而帮助你观察请求延迟、数据库查询性能以及跨服务调用链路。

### 结构化日志

启用 JSON 格式日志，以便接入日志聚合平台（Datadog、Loki、CloudWatch、Splunk）：

```bash
LOG_FORMAT=json
GLOBAL_LOG_LEVEL=INFO
```

完整监控配置请参阅 [Monitoring](/reference/monitoring) 和 [OpenTelemetry](/reference/monitoring/otel)。

---

## 后续步骤

- **[架构与高可用](/enterprise/architecture)** —— 深入了解 Open WebUI 的无状态设计与高可用能力。
- **[安全](/enterprise/security)** —— 合规框架、SSO/LDAP 集成、RBAC 与审计日志。
- **[集成](/enterprise/integration)** —— 连接 AI 模型、Pipelines 并扩展功能。
- **[扩展 Open WebUI](/getting-started/advanced-topics/scaling)** —— 完整的逐步技术扩展指南。
- **[多副本故障排查](/troubleshooting/multi-replica)** —— 处理扩展部署中常见问题。

---

**需要帮助规划企业部署吗？** 我们的团队正在帮助全球组织设计并实施生产级 Open WebUI 环境。

[**联系企业销售 → sales@openwebui.com**](mailto:sales@openwebui.com)
