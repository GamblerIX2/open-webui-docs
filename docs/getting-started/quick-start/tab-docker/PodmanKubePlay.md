# Podman Kube Play 配置

Podman 支持类似 Kubernetes 的语法来部署 Pod、卷等资源，而无需真正运行完整 Kubernetes 集群。[更多关于 Kube Play](https://docs.podman.io/en/latest/markdown/podman-kube-play.1.html)。

如果你尚未安装 Podman，请查看 [Podman 官方安装说明](https://podman.io/docs/installation)。

## 示例 `play.yaml`

下面是一个用于部署的 Podman Kube Play 示例文件：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: open-webui
spec:
  containers:
    - name: container
      image: ghcr.io/open-webui/open-webui:main
      ports:
        - name: http
          containerPort: 8080
          hostPort: 3000
      volumeMounts:
        - mountPath: /app/backend/data
          name: data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName:  open-webui-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: open-webui-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

## 启动

运行以下命令启动 Pod：

```bash
podman kube play ./play.yaml
```

## 使用 GPU 支持

若需 Nvidia GPU 支持，请将容器镜像替换为 `ghcr.io/open-webui/open-webui:cuda`，并在 Pod 资源限制中声明所需设备（GPU）：

```yaml
      [...]
      resources:
        limits:
          nvidia.com/gpu=all: 1
      [...]
```

:::important

要让 open-webui 容器成功访问 GPU，
你需要在 Podman Machine 中安装对应 GPU 的 Container Device Interface（CDI）。可参考 [Podman GPU container access](https://podman-desktop.io/docs/podman/gpu)。

:::
