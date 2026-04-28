---
sidebar_position: 6
title: "监控"
---

## 📊 监控

<a id="authentication-setup-for-api-key-"></a>

**在用户发现问题之前就先发现问题。**

Open WebUI 提供健康检查和模型接口，便于与你现有的监控系统对接，用于模型连通性检查和端到端响应测试。无论你运行的是单实例还是多节点部署，这些检查都能帮助你确认服务正常、模型可访问，而且推理流程确实在工作。

---

## 为什么要监控？

### 快速发现故障

每 60 秒运行一次健康检查，意味着你可以在一分钟内发现服务中断，而不是等用户来反馈。

### 验证模型连通性

Open WebUI 可能运行正常，而你的模型提供商却已经离线。监控 `/api/models` 接口就能发现这类情况。

### 端到端信心

最深度的检查会发送真实提示并验证响应。如果检查通过，就说明整条链路都正常：API、后端、模型提供商以及推理本身。

---

## 主要功能

| | |
| :--- | :--- |
| ✅ **健康检查接口** | 无需认证的 `/health` 检查，服务运行时返回 `200` |
| 🔗 **模型连通性** | 带认证的 `/api/models` 检查，用于验证提供商连接 |
| 🤖 **深度健康检查** | 发送真实聊天补全请求并验证响应 |
| 🐻 **Uptime Kuma 配置示例** | 每个监控级别都提供可直接使用的配置 |

---

## 第一级：基础健康检查

`/health` 接口公开可访问（无需认证），服务运行时返回 `200 OK`。

```bash
curl http://your-open-webui-instance:8080/health
```

这验证 Web 服务器可用性、应用程序初始化和基本数据库连通性。

### Uptime Kuma 配置（健康检查）

1. **Add New Monitor**，类型选择 **HTTP(s)**
2. **URL:** `http://your-open-webui-instance:8080/health`
3. **Interval:** `60 seconds`
4. **Retries:** `3`

---

## 第二级：模型连通性检查

`/api/models` 端点**需要认证**，它能确认 Open WebUI 可以访问你的模型提供商并列出可用模型。

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://your-open-webui-instance:8080/api/models
```

你需要一个 API key。配置说明请参阅 [API 密钥](/features/authentication-access/api-keys)。

:::tip 专用监控账户
创建一个**非管理员用户**（例如 `monitoring-bot`），从该账户生成 API key，并将其用于所有监控请求。这样即使密钥泄露，也能把影响范围降到最低。
:::

### Uptime Kuma 配置（模型连通性）

1. **Monitor Type:** HTTP(s) - JSON Query
2. **URL:** `http://your-open-webui-instance:8080/api/models`
3. **Method:** GET
4. **Header:** `Authorization: Bearer YOUR_API_KEY`
5. **JSON Query:** `$count(data[*])>0`
6. **Expected Value:** `true`
7. **Interval:** `300 seconds` (5 minutes)

### Advanced JSONata Queries

| 目标 | 查询 |
| :--- | :--- |
| 至少存在一个 Ollama 模型 | `$count(data[owned_by='ollama'])>0` |
| 存在指定模型 | `$exists(data[id='gpt-4o'])` |
| 存在多个模型 | `$count(data[id in ['gpt-4o', 'gpt-4o-mini']]) = 2` |

可以在 [jsonata.org](https://try.jsonata.org/) 上使用示例 API 响应测试这些查询。

---

## 第三级：深度健康检查

发送一条真实的聊天补全请求，以端到端验证整条推理链路。

```bash
curl -X POST http://your-open-webui-instance:8080/api/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Respond with the word HEALTHY"}],
    "model": "llama3.1",
    "temperature": 0
  }'
```

成功响应会返回 `200 OK`，并带有包含 “HEALTHY” 的聊天补全结果。这样可以捕捉模型加载失败、后端处理错误以及第一级和第二级检查无法发现的提供商问题。

:::info
在 Uptime Kuma 中配置第三级检查，需要一个带 POST 请求体、认证头和 JSON 查询的 HTTP(s) 监控项来验证响应。有关 POST 监控配置，请参阅 [Uptime Kuma 文档](https://github.com/louislam/uptime-kuma)。
:::

---

## 下一步

- **[OpenTelemetry](/reference/monitoring/otel)** - 使用 Grafana、Prometheus、Jaeger 等实现分布式追踪、指标和日志
- **[API 密钥](/features/authentication-access/api-keys)** - 启用和生成用于程序化访问的 API key 完整指南
