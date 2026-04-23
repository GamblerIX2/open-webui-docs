# Kubernetes 上的 Helm 配置

Helm 可以帮助你管理 Kubernetes 应用。

## 前置要求

- 已准备好 Kubernetes 集群
- 已安装 Helm

## Helm 步骤

1. **添加 Open WebUI Helm 仓库：**

   ```bash
   helm repo add open-webui https://open-webui.github.io/helm-charts
   helm repo update
   ```

2. **安装 Open WebUI Chart：**

   ```bash
   helm install openwebui open-webui/open-webui
   ```

3. **验证安装：**

   ```bash
   kubectl get pods
   ```

:::warning

如果你计划在集群环境中通过多个节点 / pods / workers 扩展 Open WebUI，就需要配置 NoSQL 键值数据库（Redis）。
另外还有一些[环境变量](https://docs.openwebui.com/reference/env-configuration/)必须在所有服务实例之间保持一致，否则会出现一致性问题、会话异常和其他故障！

**重要：** 默认向量数据库（ChromaDB）使用的是本地基于 SQLite 的客户端，**不适用于多副本或多 worker 部署**。SQLite 连接不具备 fork 安全性，多个进程并发写入会直接导致 worker 崩溃。你**必须**通过 [`VECTOR_DB`](https://docs.openwebui.com/reference/env-configuration#vector_db) 切换到外部向量数据库（PGVector、Milvus、Qdrant），或者通过 [`CHROMA_HTTP_HOST`](https://docs.openwebui.com/reference/env-configuration#chroma_http_host) 将 ChromaDB 作为独立 HTTP 服务运行。

关于完整扩展流程，请参见 [扩展 Open WebUI](https://docs.openwebui.com/getting-started/advanced-topics/scaling)。若需排查多副本问题，请查看 [Scaling & HA guide](https://docs.openwebui.com/troubleshooting/multi-replica)。

:::

:::danger 更新时的关键要求
如果你运行的是多副本 / 多 pod（`replicaCount > 1`）或设置了 `UVICORN_WORKERS > 1`，那么在更新期间你**必须**先缩容到单副本 / 单 pod。
1. 将部署缩容到 1 个副本。
2. 应用更新（新镜像版本）。
3. 等待 pod 完全就绪（数据库迁移完成）。
4. 再扩容回目标副本数。

**如果不这样做，可能会因为并发迁移导致数据库损坏。**
:::

## 访问 WebUI

你可以通过端口转发，或配置 Ingress 来访问 Open WebUI。

### Ingress 配置（Nginx）
如果你使用的是 **NGINX Ingress Controller**，可以启用 session affinity（粘性会话）以提升 WebSocket 稳定性。请在 Ingress 资源上添加以下注解：

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "open-webui-session"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
```

这样可以让用户会话尽量保持落在同一个 pod 上，从而减少多副本环境中的 WebSocket 问题（不过只要 Redis 配置正确，这一项的重要性会下降）。

## 卸载

1.  **卸载 Helm Release：**
    ```bash
    helm uninstall openwebui
    ```

2.  **删除 Persistent Volume Claims（警告：会删除所有数据）：**
    Helm 默认不会自动删除 PVC，以防止误删数据。如果你想彻底清除，需要手动删除：
    ```bash
    kubectl delete pvc -l app.kubernetes.io/instance=openwebui
    ```
