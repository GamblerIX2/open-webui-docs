---
sidebar_position: 900
title: "数据库迁移"
sidebar_label: 手动迁移
description: 当 Open WebUI 自动迁移失败或需要人工介入时，手动运行 Alembic 数据库迁移的完整指南。
keywords: [alembic, migration, database, troubleshooting, sqlite, postgresql, docker]
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## 概览

Open WebUI 会在启动时自动执行数据库迁移。**绝大多数情况下都不需要手动迁移**；只有在自动迁移失败、数据库维护或开发者明确要求时，才应该人工介入。

:::info 什么时候需要手动迁移
仅在以下场景中考虑手动迁移：

- Open WebUI 在启动日志中明确报出迁移错误
- 你正在执行离线数据库维护
- 版本升级后自动迁移失败
- 你要在不同数据库类型之间迁移（SQLite ↔ PostgreSQL）
- 开发者明确要求你手动运行迁移
:::

:::tip 升级后迁移报错的快速判断
**“No such table”** —— 迁移没有真正应用。进入容器，设置所需环境变量（见 [第 2 步](#step-2-diagnose-current-state)），然后运行 `alembic upgrade head`。详情见 [No such table 错误](#no-such-table-errors)。

**“Table already exists”** —— 某次迁移只完成了一部分。你需要先为这次“半完成”的迁移做 stamp，再继续 upgrade。详情见 [Table already exists 错误](#table-already-exists-errors)。

**跨多个大版本升级后接连报错**（例如先 duplicate column，再 table already exists，再 no such column）—— 说明数据库跨多个迁移处于“半迁移”状态。请按迁移链逐个处理。详见 [跨大版本升级后的连续失败](#multiple-failures-after-a-major-version-jump)。
:::

:::danger 关键警告
手动迁移操作失误会直接损坏数据库。**开始前务必创建并验证备份。**
:::

## 前置检查清单

在开始之前，请确认：

- [ ] 你拥有 Open WebUI 安装环境的 **root/admin 权限**
- [ ] 已确认数据库位置（Docker 默认是 `/app/backend/data/webui.db`）
- [ ] **Open WebUI 已完全停止**（没有任何运行中的进程）
- [ ] **备份已创建并验证**
- [ ] 你可以进入容器，或进入运行 Open WebUI 的 Python 环境

:::warning 先停止所有进程
数据库迁移不能在 Open WebUI 仍然运行时执行。手动迁移前，**必须**先停止所有 Open WebUI 进程。
:::

## 第 1 步：创建并验证备份

### 备份数据库

<Tabs groupId="database-type">
  <TabItem value="sqlite" label="SQLite（默认）" default>
    ```bash title="Terminal"
    # 先确认数据库位置
    docker inspect open-webui | grep -A 5 Mounts

    # 创建带时间戳的备份
    cp /path/to/webui.db /path/to/webui.db.backup.$(date +%Y%m%d_%H%M%S)
    ```
  </TabItem>
  <TabItem value="postgresql" label="PostgreSQL">
    ```bash title="Terminal"
    pg_dump -h localhost -U your_user -d open_webui_db > backup_$(date +%Y%m%d_%H%M%S).sql
    ```
  </TabItem>
</Tabs>

### 验证备份可用性

**关键：** 在继续之前，先确认备份文件真的能读。

<Tabs groupId="database-type">
  <TabItem value="sqlite" label="SQLite" default>
    ```bash title="Terminal - Verify Backup"
    sqlite3 /path/to/webui.db.backup "SELECT count(*) FROM user;"
    sqlite3 /path/to/webui.db ".schema" > current-schema.sql
    sqlite3 /path/to/webui.db.backup ".schema" > backup-schema.sql
    diff current-schema.sql backup-schema.sql
    ```
  </TabItem>
  <TabItem value="postgresql" label="PostgreSQL">
    ```bash title="Terminal - Verify Backup"
    head -n 20 backup_*.sql
    grep -c "CREATE TABLE" backup_*.sql
    ```
  </TabItem>
</Tabs>

:::tip 备份存放位置
请把备份保存在**不同于数据库本体的磁盘或卷**上，以降低磁盘故障时同时丢失原库和备份的风险。
:::

## 第 2 步：诊断当前状态 {#step-2-diagnose-current-state}

在尝试修复前，先收集当前数据库状态信息。

### 进入运行环境

<Tabs groupId="install-type">
  <TabItem value="docker" label="Docker" default>
    ```bash title="Terminal"
    docker stop open-webui

    docker run --rm -it       -v open-webui:/app/backend/data       --entrypoint /bin/bash       ghcr.io/open-webui/open-webui:main
    ```

    :::note 确认当前位置
    进入容器后先运行：
    ```bash
    pwd
    ```
    Alembic 配置文件位于 `/app/backend/open_webui/alembic.ini`。无论你当前在哪个目录，最终都需要切换到这里。
    :::
  </TabItem>
  <TabItem value="local" label="本地安装">
    ```bash title="Terminal"
    cd /path/to/open-webui/backend/open_webui
    source ../../venv/bin/activate  # Linux/Mac
    # venv\Scriptsctivate  # Windows
    ```
  </TabItem>
</Tabs>

### 切换到 Alembic 目录并设置环境变量

```bash title="Terminal - Navigate and Configure Environment"
pwd
cd /app/backend/open_webui  # Docker
# 或
cd /path/to/open-webui/backend/open_webui  # Local
ls -la alembic.ini
```

### 设置必需环境变量

<Tabs groupId="install-type">
  <TabItem value="docker" label="Docker" default>

```bash title="Terminal - Set Environment Variables (Docker)"
export DATABASE_URL="sqlite:////app/backend/data/webui.db"
# export DATABASE_URL="postgresql://user:password@localhost:5432/open_webui_db"

export WEBUI_SECRET_KEY=$(cat /app/backend/.webui_secret_key)
# 如果上面失败，可尝试：
# export WEBUI_SECRET_KEY=$(cat /app/backend/data/.webui_secret_key)
# 如果都不存在，可手动生成：
# export WEBUI_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

echo "DATABASE_URL: $DATABASE_URL"
echo "WEBUI_SECRET_KEY: ${WEBUI_SECRET_KEY:0:10}..."
```

  </TabItem>
  <TabItem value="local" label="本地安装">

```bash title="Terminal - Set Environment Variables (Local)"
export DATABASE_URL="sqlite:///../data/webui.db"
# export DATABASE_URL="sqlite:////full/path/to/webui.db"
# export DATABASE_URL="postgresql://user:password@localhost:5432/open_webui_db"

export WEBUI_SECRET_KEY=$(cat ../data/.webui_secret_key)
# 或手动 export 你已有的密钥

echo "DATABASE_URL: $DATABASE_URL"
echo "WEBUI_SECRET_KEY: ${WEBUI_SECRET_KEY:0:10}..."
```

:::note 本地安装说明
本地安装常常把 `DATABASE_URL` 写在 `.env` 中，但 Alembic 的 `env.py` 不一定会自动加载 `.env`。运行 Alembic 命令前，请先在 shell 中显式 `export` 这些变量。
:::

  </TabItem>
</Tabs>

:::danger 两个变量都必须设置
如果缺少 `WEBUI_SECRET_KEY`，Alembic 命令会直接因 `Required environment variable not found` 失败。Open WebUI 的 `env.py` 会先校验该变量是否存在，Alembic 甚至还没来得及连上数据库就会退出。
:::

:::warning SQLite 路径语法
- `sqlite:////app/...` = 总共 4 个 `/`，表示绝对路径
- `sqlite:///../data/...` = 总共 3 个 `/`，表示相对路径
:::

### 运行诊断命令

以下命令都是只读的，可以放心执行：

```bash title="Terminal - Diagnostics (Safe - Read Only)"
alembic current -v
alembic heads
alembic history
alembic upgrade head --sql | head -30
alembic branches
```

**如何理解输出：**
- `alembic current` = 数据库当前认为自己处在哪个 revision
- `alembic heads` = 代码当前期望的最新 revision
- `alembic upgrade head --sql` = 预览即将执行的 SQL（不会真正应用）
- 如果 `current` 早于 `heads`，说明还有 pending migrations
- 如果 `current` 与 `heads` 相等，数据库已经是最新

<details>
<summary>检查数据库中真实存在的表</summary>

<Tabs groupId="database-type">
  <TabItem value="sqlite" label="SQLite" default>
    ```bash title="Terminal"
    sqlite3 /app/backend/data/webui.db ".tables"
    sqlite3 /app/backend/data/webui.db "SELECT * FROM alembic_version;"
    ```
  </TabItem>
  <TabItem value="postgresql" label="PostgreSQL">
    ```bash title="Terminal"
    psql -h localhost -U user -d dbname -c "\dt"
    psql -h localhost -U user -d dbname -c "SELECT * FROM alembic_version;"
    ```
  </TabItem>
</Tabs>

</details>

## 第 3 步：应用迁移

### 标准升级（最常见）

如果诊断结果表明存在 pending migrations（`current < heads`），直接升级到最新：

```bash title="Terminal - Upgrade to Latest"
cd /app/backend/open_webui
alembic upgrade head
```

如果输出中看到：

```bash
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, add_new_column
```

这是正常现象。尤其对 SQLite 而言，`Will assume non-transactional DDL` 只是提示，不是错误。

:::note SQLite 的 “Will assume non-transactional DDL”
SQLite 不支持 schema 变更回滚，因此 Alembic 只能在没有事务保护的情况下执行迁移。大表加索引、数据回填、表重建时，都可能要跑几分钟。若数据库非常大，请安排维护窗口并耐心等待。
:::

### 升级到指定版本

```bash title="Terminal - Upgrade to Specific Version"
alembic history
alembic upgrade ae1027a6acf
```

### 回滚（Downgrade）

:::danger 有数据丢失风险
回滚可能会删除列或表，进而造成**永久性数据丢失**。只有在完全理解后果时才应执行。
:::

```bash title="Terminal - Downgrade Migrations"
alembic downgrade -1
alembic downgrade <revision_id>
alembic downgrade base
```

## 第 4 步：验证迁移结果

迁移执行后，请做完整验证：

```bash title="Terminal - Post-Migration Verification"
alembic current
alembic upgrade head --sql | head -20
sqlite3 /app/backend/data/webui.db ".tables" | grep -E "user|chat|model"
sqlite3 /app/backend/data/webui.db "SELECT COUNT(*) FROM user;"
```

### 测试应用启动

<Tabs groupId="install-type">
  <TabItem value="docker" label="Docker" default>
    ```bash title="Terminal"
    exit
    docker start open-webui
    docker logs -f open-webui
    ```
  </TabItem>
  <TabItem value="local" label="本地安装">
    ```bash title="Terminal"
    python -m open_webui.main
    ```
  </TabItem>
</Tabs>

**成功启动时常见日志：**

```
INFO:     [db] Database initialization complete
INFO:     [main] Open WebUI starting on http://0.0.0.0:8080
```

**启动后建议做 smoke test：**
- 能打开登录页
- 能用原账号正常登录
- 能查看聊天历史
- 浏览器控制台没有新的 JavaScript 错误

## 故障排查

<span id="no-such-table-errors"></span>
### “No such table” 错误 {#no-such-table-errors}

**症状：** 启动时报类似：

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: access_grant
```

**原因：** 一个或多个 Alembic 迁移没有真正执行成功，常见原因包括：
- 自动升级过程中迁移静默失败
- 升级中途被打断
- 环境里设置了 `ENABLE_DB_MIGRATIONS=False`
- 多个 worker 或副本同时执行迁移

**解决方法：**
进入容器，按第 2 步设置环境变量后，执行：

```bash
cd /app/backend/open_webui
alembic upgrade head
```

:::warning `ENABLE_DB_MIGRATIONS=True` 不是补救手段
这个变量只表示“下次启动时尝试自动迁移”，它**不能**修复已经失败或跳过的迁移。数据库一旦处于错误状态，仍需手动执行迁移。
:::

<span id="table-already-exists-errors"></span>
### “Table already exists” 错误 {#table-already-exists-errors}

**症状：** 运行 `alembic upgrade head` 时出现：

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table chat_message already exists
```

**原因：** 某次迁移只执行了一半——表创建成功了，但 Alembic 的版本记录没有更新，因此它下次又尝试重复创建同一张表。

**诊断：**
```bash
alembic current
alembic history
```

**解决方法：**
1. **最安全：从备份恢复，然后重新迁移**
2. **没有备份时：删除半创建的表，再重新运行迁移**（必须先确认数据源仍然完整）
3. **最后手段：对特定 revision 执行 `alembic stamp <revision_id>`，然后再 `alembic upgrade head`**

:::warning `stamp` 会跳过数据回填
如果该迁移除了建表，还会把旧数据复制到新表，那么 `stamp` 会跳过这部分逻辑。旧数据通常不会被删除，但应用可能已经不再读取旧列，功能就会表现出“数据缺失”。
:::

<span id="multiple-failures-after-a-major-version-jump"></span>
### 跨大版本升级后的连续失败 {#multiple-failures-after-a-major-version-jump}

**症状：** 例如从 0.7.x 直接升级到 0.8.x/0.9.x 后，先是启动时报 `no such column`，接着手动迁移时又先后出现 `duplicate column`、`already exists` 等错误。

**原因：** 多个迁移步骤在历史某次启动中只完成了部分 schema 变更，但 `alembic_version` 没有同步前进，结果数据库变成“前几个迁移做了一半、后几个还没开始”的混合状态。

**诊断：**
```bash
alembic current
alembic heads
alembic history
sqlite3 /app/backend/data/webui.db "PRAGMA table_info(channel_member);"
sqlite3 /app/backend/data/webui.db "SELECT name FROM sqlite_master WHERE type='table' AND name='chat_message';"
```

**恢复思路：逐个 revision 向前推进**

```bash
alembic history
alembic upgrade <first_pending_revision>
```

- 如果成功，继续升级下一个 revision
- 如果报 `duplicate column` 或 `already exists`，说明该 revision 的 schema 变更其实已经存在，可以对**那个特定 revision** 执行 `alembic stamp <revision>`，再继续升级
- 如果报的是其他错误（如类型不匹配、外键错误、Python traceback），先停下来排查，不要继续 blind stamp

:::info 什么情况下 stamp 是安全的？
当你已经确认该 revision 对应的 schema 变更**确实已经在数据库中存在**，也就是错误本身已经证明了这点（例如 “already exists” 或 “duplicate column”）时，对**具体 revision** 执行 `stamp` 才是安全的。不要随意 `alembic stamp head`。
:::

### “Required environment variable not found”

**原因：** 缺少 `WEBUI_SECRET_KEY`。

**解决方法：** 按第 2 步补齐 `WEBUI_SECRET_KEY`，再重试 Alembic 命令。

### “No config file 'alembic.ini' found”

**原因：** 当前目录不对。

**解决方法：**
```bash
docker ps
find /app -name "alembic.ini" 2>/dev/null
cd /app/backend/open_webui
ls -la alembic.ini
```

### “Target database is not up to date”

**原因：** 数据库版本与代码期望的 schema 不匹配。

**诊断：**
```bash
alembic current
alembic heads
```

**处理方式：**
- 如果 `current` 落后于 `heads`：执行 `alembic upgrade head`
- 如果 `current` 已经等于 `heads`，但表结构依然出错：通常意味着数据库已被手工改坏或某次迁移半失败，建议从备份恢复
- 如果是全新空库：直接运行 `alembic upgrade head`

:::danger 不要把 `alembic stamp head` 当成“修复命令”
`alembic stamp head` 的含义是“假装所有迁移都执行过了”，它**不会**真的执行任何迁移。对用户来说，这通常只会制造更严重、且更隐蔽的数据库损坏。
:::

### 看到 “Will assume non-transactional DDL” 后像是卡住了

这个提示本身不是错误。若确实长时间无进展：
- 先等 3-5 分钟，很多大表迁移确实很慢
- 检查数据库是否被其他进程锁住
- 确认宿主机磁盘与卷性能是否足够
- 如果 `PRAGMA integrity_check` 返回异常，请先从备份恢复

### 不要使用 `alembic revision --autogenerate`

这条命令是给**开发者生成新迁移文件**用的，不是给普通用户应用现有迁移用的。你真正需要的是：

```bash
alembic upgrade head
```

如果你误生成了错误的迁移文件，请删除它，并恢复 `migrations/` 目录到仓库原状。

### PostgreSQL 外键错误

如果你在 PostgreSQL 中看到类似：

```
psycopg2.errors.InvalidForeignKey: there is no unique constraint matching given keys for referenced table "user"
```

通常说明旧 schema 缺少主键或唯一约束。常见处理方式是手动补充缺失约束，例如：

```sql
ALTER TABLE public."user" ADD CONSTRAINT user_pk PRIMARY KEY (id);
```

### Duplicate column 错误

这类错误通常表示 schema 已被部分改动，最常见于：
- 之前某次迁移只执行了一部分
- 手工修改过数据库
- 跨多个大版本升级时跳过了中间版本

SQLite 不支持直接 `DROP COLUMN`，如果必须修复，通常要：
1. 先备份数据库
2. 用 `PRAGMA table_info(<table>)` 查出重复列
3. 重建一张正确结构的新表
4. 把数据复制过去
5. 替换旧表
6. 再继续运行 `alembic upgrade head`

如果你不熟悉 SQL，请在这一步停止，并把 `PRAGMA table_info(...)` 输出、完整错误信息和升级路径带到 GitHub / Discord 寻求帮助。

### Peewee 到 Alembic 的迁移过渡问题

很老的 Open WebUI 版本（0.4.x 之前）使用 Peewee 迁移，新版本使用 Alembic。理论上 Open WebUI 会自动处理过渡，但若你从非常老的版本直接升级，仍有可能失败。

可以先检查旧表：

```bash
sqlite3 /app/backend/data/webui.db "SELECT * FROM migratehistory;" 2>/dev/null
```

若你正在从非常旧的版本（例如 < 0.3.x）升级，通常更推荐：**重新安装 + 数据导出/导入**，而不是硬跨多个大版本做 schema 迁移。

## 高级操作

### 生产环境与多服务器部署

:::warning 滚动升级可能导致失败
如果你在多服务器部署中同时运行新旧两个版本的代码，而数据库 schema 还没有完成升级，就可能出现新代码期望新 schema、旧代码又不兼容新 schema 的情况。
:::

**推荐部署策略：**

<Tabs>
  <TabItem value="separate-job" label="独立迁移 Job" default>

在部署新应用代码前，先以一次性任务运行迁移：

```bash title="Kubernetes Job Example"
kubectl apply -f migration-job.yaml
kubectl wait --for=condition=complete job/openwebui-migration
kubectl rollout restart deployment/openwebui
```

  </TabItem>
  <TabItem value="maintenance" label="维护窗口">

在迁移期间让应用离线：

```bash title="Maintenance Workflow"
docker-compose down
docker run --rm -v open-webui:/app/backend/data   ghcr.io/open-webui/open-webui:main   bash -c "cd /app/backend/open_webui && alembic upgrade head"
docker-compose up -d
```

  </TabItem>
  <TabItem value="blue-green" label="蓝绿部署">

保持两套完全相同的环境，在新环境完成迁移并验证后再切流：

```bash title="Blue-Green Workflow"
# 1. 新环境先接入已迁移数据库
# 2. 在新环境部署新代码
# 3. 完整验证
# 4. 把流量从旧环境切到新环境
# 5. 保留旧环境作为快速回滚方案
```

  </TabItem>
</Tabs>

### 仅生成 SQL，不直接应用

若你需要审核迁移 SQL，可使用：

```bash title="Terminal - Generate Migration SQL"
alembic upgrade head --sql
```

适用场景：
- 企业环境中的 DBA 审核
- 想先理解具体会发生哪些 schema 变更
- 受限环境中的离线迁移流程

### 离线迁移（无网络）

如果你的数据库服务器是离线或隔离环境，可以：
1. 在可访问代码的机器上生成迁移 SQL
2. 把 SQL 文件传到生产环境
3. 手动应用 SQL
4. **只在确认 SQL 已成功应用后**，再更新 `alembic_version`

:::danger 手动更新 alembic_version 风险极高
只有在你**确认对应迁移已经真实执行完成**的前提下，才应该修改 `alembic_version`。否则就是在向 Alembic “撒谎”，后果通常是永久性数据库损坏。
:::

## 恢复流程

### 从失败迁移中恢复

:::danger SQLite 没有回滚
SQLite 迁移是**非事务性的**。一旦迁移执行到一半失败，数据库就可能停留在“半迁移”状态。最安全的恢复方式通常就是从备份还原。
:::

**半迁移常见症状：**
- 某些表存在，某些表结构却不对
- 外键错误
- 迁移本应添加的列缺失
- 应用报“缺少数据库字段”

**建议恢复流程：**
```bash
docker stop open-webui
sqlite3 /path/to/webui.db.backup "PRAGMA integrity_check;"
cp /path/to/webui.db.backup /path/to/webui.db
```

然后先分析失败根因，再重新尝试迁移。

### 验证数据库完整性

<Tabs groupId="database-type">
  <TabItem value="sqlite" label="SQLite" default>
    ```bash title="Terminal - SQLite Integrity Check"
    sqlite3 /app/backend/data/webui.db "PRAGMA integrity_check;"
    ```
  </TabItem>
  <TabItem value="postgresql" label="PostgreSQL">
    ```bash title="Terminal - PostgreSQL Integrity Check"
    psql -h localhost -U user -d dbname -c "SELECT * FROM pg_stat_database WHERE datname='open_webui_db';"
    psql -h localhost -U user -d dbname -c "VACUUM ANALYZE;"
    ```
  </TabItem>
</Tabs>

## 迁移后检查清单

成功迁移后，请确认：

- [ ] `alembic current` 显示 `(head)`
- [ ] Open WebUI 可以无错误启动
- [ ] 可以正常登录
- [ ] 核心功能可用（聊天、模型选择等）
- [ ] 日志中没有新的数据库错误
- [ ] 数据完整（用户、聊天、模型都还在）
- [ ] 在确认稳定运行 1 周后，再归档旧备份

:::tip 保留近期备份
重大迁移前的备份，建议至少保留 1-2 周。很多问题并不会在启动时立刻出现，而是要到某条具体业务路径触发后才会暴露。
:::

## 获取帮助

如果按照本指南处理后迁移仍然失败，请先收集下面这些诊断信息：

```bash title="Terminal - Collect Diagnostic Data"
docker logs open-webui 2>&1 | head -20
cd /app/backend/open_webui
alembic current -v
alembic history
sqlite3 /app/backend/data/webui.db ".tables"
sqlite3 /app/backend/data/webui.db "SELECT * FROM alembic_version;"
alembic upgrade head
```

**求助时请提供：**
1. Open WebUI 版本
2. 安装方式（Docker / 本地）
3. 数据库类型（SQLite / PostgreSQL）
4. `alembic current` 与 `alembic history` 输出
5. 完整错误信息
6. 错误发生时你正在执行的操作

:::note
不要公开分享你的 `webui.db` 文件——其中包含用户凭据与敏感数据。请只分享文本形式的诊断输出。
:::
