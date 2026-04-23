# 使用 Python 更新

如果你是通过 `pip` 在本地安装的 **Open WebUI**，可按以下方式升级到最新版本：

```bash
pip install -U open-webui
```

`-U`（或 `--upgrade`）标志会让 `pip` 升级到最新可用版本。

升级后，重启服务并确认能够正常启动：

```bash
open-webui serve
```

:::warning 多 worker 环境
如果你以 `UVICORN_WORKERS > 1` 运行 Open WebUI（例如生产环境），则**必须**先确保更新迁移在单 worker 下完成，否则可能导致数据库 schema 损坏。

**正确更新步骤：**
1. 使用 `pip` 更新 `open-webui`。
2. 设置 `UVICORN_WORKERS=1` 后启动应用。
3. 等待应用完全启动并完成迁移。
4. 停止应用，再按目标 worker 数重新启动。
:::

有关版本固定、回滚和备份流程，请参见[完整更新指南](/getting-started/updating)。
