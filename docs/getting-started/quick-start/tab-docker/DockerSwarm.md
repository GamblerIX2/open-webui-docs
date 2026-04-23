## Docker Swarm

这种安装方式要求你熟悉 Docker Swarm，因为它会使用 stack 文件在 Docker Swarm 中将 3 个独立容器部署为服务。

其中包含独立运行的 ChromaDB、Ollama 与 Open WebUI 容器。
另外还预填了一些[环境变量](https://docs.openwebui.com/reference/env-configuration)，以便更直观地说明部署方式。

:::info 为什么要将 ChromaDB 作为独立容器运行

这个 stack 正确地将 ChromaDB 部署为**独立的 HTTP 服务容器**，Open WebUI 通过 `CHROMA_HTTP_HOST` 和 `CHROMA_HTTP_PORT` 与其连接。对于任何多 worker 或多副本部署，这都是**必须的**。

默认的 ChromaDB 模式（未设置 `CHROMA_HTTP_HOST`）使用本地基于 SQLite 的 `PersistentClient`，**不具备 fork 安全性**——多个 worker 进程并发写入会立刻导致 worker 崩溃。将 ChromaDB 作为独立服务运行，可以通过 HTTP 连接避免直接访问 SQLite。

如果你打算把 `openWebUI` 服务扩展到多个副本，还应同时把主数据库切换到 PostgreSQL，并配置 Redis。完整要求请参见 [Scaling & HA guide](https://docs.openwebui.com/troubleshooting/multi-replica)。

:::

请根据你的硬件情况选择相应命令：

- **开始前：**

  需要先在宿主机上创建用于卷的数据目录，或者改用你自己的自定义路径 / 卷。

  当前示例使用的是与 `docker-stack.yaml` 位于同一目录下的隔离目录 `data`。

      - **例如：**

        ```bash
        mkdir -p data/open-webui data/chromadb data/ollama
        ```

- **启用 GPU：**

#### Docker-stack.yaml

    ```yaml
    version: '3.9'

    services:
      openWebUI:
        image: ghcr.io/open-webui/open-webui:main
        depends_on:
            - chromadb
            - ollama
        volumes:
          - ./data/open-webui:/app/backend/data
        environment:
          DATA_DIR: /app/backend/data
          OLLAMA_BASE_URLS: http://ollama:11434
          CHROMA_HTTP_PORT: 8000
          CHROMA_HTTP_HOST: chromadb
          CHROMA_TENANT: default_tenant
          VECTOR_DB: chroma
          WEBUI_NAME: Awesome ChatBot
          CORS_ALLOW_ORIGIN: "*" # 当前默认值；正式上线前应修改
          RAG_EMBEDDING_ENGINE: ollama
          RAG_EMBEDDING_MODEL: nomic-embed-text-v1.5
          RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE: "True"
        ports:
          - target: 8080
            published: 8080
            mode: overlay
        deploy:
          replicas: 1
          restart_policy:
            condition: any
            delay: 5s
            max_attempts: 3

      chromadb:
        hostname: chromadb
        image: chromadb/chroma:0.5.15
        volumes:
          - ./data/chromadb:/chroma/chroma
        environment:
          - IS_PERSISTENT=TRUE
          - ALLOW_RESET=TRUE
          - PERSIST_DIRECTORY=/chroma/chroma
        ports:
          - target: 8000
            published: 8000
            mode: overlay
        deploy:
          replicas: 1
          restart_policy:
            condition: any
            delay: 5s
            max_attempts: 3
        healthcheck:
          test: ["CMD-SHELL", "curl localhost:8000/api/v1/heartbeat || exit 1"]
          interval: 10s
          retries: 2
          start_period: 5s
          timeout: 10s

      ollama:
        image: ollama/ollama:latest
        hostname: ollama
        ports:
          - target: 11434
            published: 11434
            mode: overlay
        deploy:
          resources:
            reservations:
              generic_resources:
                - discrete_resource_spec:
                    kind: "NVIDIA-GPU"
                    value: 0
          replicas: 1
          restart_policy:
            condition: any
            delay: 5s
            max_attempts: 3
        volumes:
          - ./data/ollama:/root/.ollama

    ```

- **额外要求：**

      1. 确保已启用 CUDA，请按你的操作系统和 GPU 对应说明完成。
      2. 启用 Docker GPU 支持，参见 [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html " on Nvidia's site.")
      3. 参考[此指南，配置 Docker Swarm 使用 GPU](https://gist.github.com/tomlankhorst/33da3c4b9edbde5c83fc1244f010815c#configuring-docker-to-work-with-your-gpus)
  - 请确认 `/etc/nvidia-container-runtime/config.toml` 中已启用 *GPU Resource*，并取消注释 `swarm-resource = "DOCKER_RESOURCE_GPU"` 以启用 GPU 资源广播。修改这些文件后，必须在每个节点上重启 Docker daemon。

- **仅 CPU：**

    修改 `docker-stack.yaml` 中的 Ollama 服务，删除 `generic_resources:` 相关行：

    ```yaml
        ollama:
      image: ollama/ollama:latest
      hostname: ollama
      ports:
        - target: 11434
          published: 11434
          mode: overlay
      deploy:
        replicas: 1
        restart_policy:
          condition: any
          delay: 5s
          max_attempts: 3
      volumes:
        - ./data/ollama:/root/.ollama
    ```

- **部署 Docker Stack：**

  ```bash
  docker stack deploy -c docker-stack.yaml -d super-awesome-ai
  ```
