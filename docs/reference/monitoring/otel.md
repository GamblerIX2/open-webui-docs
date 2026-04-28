---
sidebar_position: 7
title: "OpenTelemetry"
---

<!-- markdownlint-disable MD060 -->

Open WebUI 支持通过 OpenTelemetry（OTel）协议（OTLP）导出**分布式追踪和指标**。这使你可以与现代可观测性技术栈（例如 **Grafana LGTM**〔Loki、Grafana、Tempo、Mimir〕）以及 **Jaeger**、**Tempo** 和 **Prometheus** 集成，从而实时监控请求、数据库/Redis 查询、响应时间等。

:::warning 额外依赖

如果你是从源码或通过 `pip` 运行 Open WebUI（也就是不使用官方 Docker 镜像），OpenTelemetry 依赖项**可能不会默认安装**。你可能需要手动安装它们：

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

:::

## 🚀 使用 Docker Compose 快速开始

启用可观测性的最快方式是使用预配置的 Docker Compose：

```bash

# 启动 Open WebUI 和最新的 Grafana LGTM 栈
docker compose -f docker-compose.otel.yaml up -d
```

`docker-compose.otel.yaml` 文件会配置以下组件：

| 服务        | 端口                                   | 描述                                                 |
| ----------- | -------------------------------------- | ---------------------------------------------------- |
| **grafana** | 3000（UI）、4317（OTLP/gRPC）、4318（HTTP） | Grafana LGTM（Loki + Grafana + Tempo + Mimir）一体化栈 |
| **open-webui** | 8088（默认）→ 8080                  | 启用了 OTEL 的 WebUI，映射到宿主机端口 8088           |

启动后，请访问 [http://localhost:3000](http://localhost:3000) 上的 Grafana 仪表板。
登录信息：`admin` / `admin`

## ⚙️ 环境变量

你可以使用下面这些环境变量（与 Compose 文件中的配置一致）在 Open WebUI 中配置 OpenTelemetry：

| 变量                                  | 默认值                              | 描述                                                       |
| ------------------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| `ENABLE_OTEL`                         | 在 Compose 中为 **true**            | OpenTelemetry 的总开关                                     |
| `ENABLE_OTEL_TRACES`                  | 在 Compose 中为 **true**            | 启用分布式追踪导出                                         |
| `ENABLE_OTEL_METRICS`                 | 在 Compose 中为 **true**            | 启用 FastAPI HTTP 指标导出                                 |
| `OTEL_EXPORTER_OTLP_ENDPOINT`         | 在 Compose 中为 `http://grafana:4317` | OTLP gRPC/HTTP 收集器端点 URL                              |
| `OTEL_EXPORTER_OTLP_INSECURE`         | 在 Compose 中为 **true**            | 使用不安全连接（无 TLS）连接 OTLP                          |
| `OTEL_SERVICE_NAME`                   | `open-webui`                        | 服务名称（会显示在追踪和指标中）                           |
| `OTEL_METRICS_EXPORT_INTERVAL_MILLIS` | `10000`                             | 指标导出间隔（毫秒）（10 秒约等于 6 次/分钟；`60000` 约 1 次/分钟） |
| `OTEL_BASIC_AUTH_USERNAME` / `OTEL_BASIC_AUTH_PASSWORD` | *(为空)* | 如果收集器需要，可配置基本认证凭据                         |

:::tip

你可以根据需要在 `.env` 文件或 Compose 文件中覆盖默认值。

:::

```yaml
  open-webui:
    environment:
      - ENABLE_OTEL=true
      - ENABLE_OTEL_TRACES=true
      - ENABLE_OTEL_METRICS=true
      - OTEL_EXPORTER_OTLP_INSECURE=true # OTLP 使用不安全连接；生产环境中你可能希望移除这一项
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://grafana:4317
      - OTEL_SERVICE_NAME=open-webui
      # 如有需要，可在此设置 OTEL_BASIC_AUTH_USERNAME/PASSWORD
```

## 📊 数据收集

### 分布式追踪

Open WebUI 后端自动检测：

- **FastAPI**（路由）
- **SQLAlchemy**（数据库查询）
- **Redis**
- **requests**、**httpx**、**aiohttp**（外部调用）

每个追踪跨度都会包含丰富的数据，例如：

- `db.instance`, `db.statement`, `redis.args`
- `http.url`, `http.method`, `http.status_code`
- 异常时的错误详情 (`error.message`, `error.kind`)

### 指标收集

WebUI 通过 OpenTelemetry 导出以下指标：

| 指标                    | 类型     | 单位 | 标签                                         |
| ----------------------- | -------- | ---- | -------------------------------------------- |
| `http.server.requests`  | 计数器   | 1    | `http.method`、`http.route`、`http.status_code` |
| `http.server.duration`  | 直方图   | ms   | 同上                                         |

指标会通过 OTLP 发送（默认每 10 秒一次，可通过 `OTEL_METRICS_EXPORT_INTERVAL_MILLIS` 配置），并可以在 **Grafana** 中通过 Prometheus/Mimir 进行可视化。

## 🔧 自定义收集器设置

如果你想使用不同的（外部）OpenTelemetry 收集器或技术栈：

```bash
docker run -d --name open-webui \
  -p 8088:8080 \
  -e ENABLE_OTEL=true \
  -e ENABLE_OTEL_TRACES=true \
  -e ENABLE_OTEL_METRICS=true \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317 \
  -e OTEL_EXPORTER_OTLP_INSECURE=true \
  -e OTEL_SERVICE_NAME=open-webui \
  -v open-webui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main
```

## 🚨 故障排除

**追踪/指标没有显示在 Grafana 中？**

- 仔细检查 `ENABLE_OTEL`、`ENABLE_OTEL_TRACES` 和 `ENABLE_OTEL_METRICS` 是否都设为 `true`
- 端点是否正确？（`OTEL_EXPORTER_OTLP_ENDPOINT`）
- 检查 Open WebUI 日志（`docker logs open-webui`）以查找 OTLP 错误
- 收集器的 OTLP 端口（`4317`）应保持开放且可达。可以尝试：
  `curl http://localhost:4317` (根据需要替换主机)

**需要认证？**

- 为受认证保护的收集器设置 `OTEL_BASIC_AUTH_USERNAME` 和 `OTEL_BASIC_AUTH_PASSWORD`
- 如果使用 SSL/TLS，请相应调整或移除 `OTEL_EXPORTER_OTLP_INSECURE`
