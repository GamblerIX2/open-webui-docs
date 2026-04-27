---
sidebar_position: 6
title: "监控"
---

# 📊 监控

<a id="authentication-setup-for-api-key-"></a>

**在用户发现问题之前就知道出了什么。**

Open WebUI 提供健康检查和模型接口，与客居间监控、模型连通性检查和端到端响应测试对接简单直接。无论你运行的是单一实例还是多节点部署，这些检查都能让你确信服务正常运行、模型可访问并且推理确实工作。

---

## 为什么要监控？

### 快速发现敌障

每 60 秒运行一次健康检查，意味着你在一分钟内就能知道服务中断，而不是等到用户来反馈。

### 验证模型连通性

Open WebUI 可能运行正常，而你的模型提供商却已下线。监控 `/api/models` 接口可以发现这种情况。

### 端到端信心

最深度的检查会发送真实提示并验证响应。如果检查通过，你就知道整个流水线均正常运作：API、后端、模型提供商和推理。

---

## 主要功能

| | |
| :--- | :--- |
| ✅ **健康检查接口** | 无需认证的 `/health` 检查，服务运行时返回 `200` |
| 🔗 **模型连通性** | 带认证的 `/api/models` 检查验证提供商连接 |
| 🤖 **深度健康检查** | 发送真实聊天补全请求并验证响应 |
| 🐻 **Uptime Kuma 配方** | 每个监控级别的即用配置 |

---

## 第一级：基础健康检查

`/health` 接口公开可访问（无需认证），服务运行时返回 `200 OK`。

```bash
curl http://your-open-webui-instance:8080/health
```

这验证 Web 服务器可用性、应用程序初始化和基本数据库连通性。

### Uptime Kuma Setup

1. **Add New Monitor** with type **HTTP(s)**
2. **URL:** `http://your-open-webui-instance:8080/health`
3. **Interval:** `60 seconds`
4. **Retries:** `3`

---

## Level 2: Model Connectivity Check

The `/api/models` endpoint **requires authentication** and confirms that Open WebUI can reach your model providers and list available models.

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://your-open-webui-instance:8080/api/models
```

You'll need an API key. See [API Keys](/features/authentication-access/api-keys) for setup instructions.

:::tip Dedicated Monitoring Account
Create a **non-admin user** (e.g., `monitoring-bot`), generate an API key from that account, and use it for all monitoring requests. This limits blast radius if the key is ever compromised.
:::

### Uptime Kuma Setup

1. **Monitor Type:** HTTP(s) - JSON Query
2. **URL:** `http://your-open-webui-instance:8080/api/models`
3. **Method:** GET
4. **Header:** `Authorization: Bearer YOUR_API_KEY`
5. **JSON Query:** `$count(data[*])>0`
6. **Expected Value:** `true`
7. **Interval:** `300 seconds` (5 minutes)

### Advanced JSONata Queries

| Goal | Query |
| :--- | :--- |
| At least one Ollama model | `$count(data[owned_by='ollama'])>0` |
| Specific model exists | `$exists(data[id='gpt-4o'])` |
| Multiple models exist | `$count(data[id in ['gpt-4o', 'gpt-4o-mini']]) = 2` |

Test queries at [jsonata.org](https://try.jsonata.org/) with a sample API response.

---

## Level 3: Deep Health Check

Send a real chat completion to verify the entire inference pipeline end-to-end.

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

A successful response returns `200 OK` with a chat completion containing "HEALTHY". This catches model loading failures, backend processing errors, and provider-side issues that Levels 1 and 2 would miss.

:::info
Setting up Level 3 in Uptime Kuma requires an HTTP(s) monitor with a POST body, authentication headers, and a JSON query to validate the response. See [Uptime Kuma docs](https://github.com/louislam/uptime-kuma) for POST monitor configuration.
:::

---

## Next Steps

- **[OpenTelemetry](/reference/monitoring/otel)** - Distributed tracing, metrics, and logs with Grafana, Prometheus, Jaeger, and more
- **[API Keys](/features/authentication-access/api-keys)** - Full guide on enabling and generating API keys for programmatic access
