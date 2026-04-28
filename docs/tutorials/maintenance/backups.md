---
sidebar_position: 1000
title: "备份"
---

# 备份您的实例

 :::warning
本教程由社区贡献，不受 Open WebUI 团队官方维护或审核。如有问题，请直接联系原作者。
:::

 没有人喜欢数据丢失！

 如果您正在自托管 Open WebUI，可能希望制定某种正式的备份计划，以确保保留配置的第二份和第三份副本。

 本指南旨在为用户提供一些基本建议，说明如何进行备份。

 本指南假设用户已通过 Docker 安装 Open WebUI（或计划这样做）。

## 确保数据持久化

首先，在使用 Docker 部署您的应用栈之前，请确保 Docker Compose 使用了持久化数据存储。如果您使用的是 [Github 仓库中的 Docker Compose](https://github.com/open-webui/open-webui/blob/main/docker-compose.yaml)，这一点已经处理好了。但自定义配置时很容易遗漏这一验证。

Docker 容器是临时性的，必须将数据持久化到宿主机文件系统以确保其存续。

## 使用 Docker 卷

如果您使用的是项目仓库中的 Docker Compose，将通过 Docker 卷部署 Open Web UI。

Ollama 和 Open WebUI 的挂载配置为：

```yaml
ollama:
  volumes:
    - ollama:/root/.ollama
```

```yaml
open-webui:
  volumes:
    - open-webui:/app/backend/data
```

要查找宿主机上的实际绑定路径，运行：

`docker volume inspect ollama`

以及

`docker volume inspect open-webui`

## 使用直接宿主机绑定

一些用户使用直接（固定）绑定到宿主机文件系统的方式部署 Open Web UI，如下所示：

```yaml
services:
  ollama:
    container_name: ollama
    image: ollama/ollama:${OLLAMA_DOCKER_TAG-latest}
    volumes:
      - /opt/ollama:/root/.ollama
  open-webui:
    container_name: open-webui
    image: ghcr.io/open-webui/open-webui:${WEBUI_DOCKER_TAG-main}
    volumes:
      - /opt/open-webui:/app/backend/data
```

如果您是这样部署的，需要记录根目录上的路径。

## 编写备份任务脚本

无论您的实例如何配置，都建议检查服务器上应用的数据存储，了解需要备份的数据。您应该会看到类似如下的结构：

```txt
├── audit.log
├── cache/
├── uploads/
├── vector_db/
└── webui.db
```

## 持久化数据存储中的文件

| 文件/目录 | 描述 |
|---|---|
| `audit.log` | 用于审计事件的日志文件。 |
| `cache/` | 用于存储缓存数据的目录。 |
| `uploads/` | 用于存储用户上传文件的目录。 |
| `vector_db/` | 包含 ChromaDB 向量数据库的目录。 |
| `webui.db` | 用于持久存储其他实例数据的 SQLite 数据库。 |

# 文件级备份方案

备份应用数据的第一种方式是采用文件级备份方法，确保 Open Web UI 的持久化数据得到妥善备份。

技术服务的备份方式几乎无穷无尽，但 `rsync` 作为增量任务的热门选择，将在此作为示例使用。

用户可以针对整个 `data` 目录一次性备份所有实例数据，也可以创建更有选择性的备份任务，针对各个组件分别备份。您还可以为目标添加更具描述性的名称。

一个示范性的 rsync 任务如下所示：

```bash

#!/bin/bash

# Configuration
SOURCE_DIR="."  # Current directory (where the file structure resides)
B2_BUCKET="b2://OpenWebUI-backups" # Your Backblaze B2 bucket
B2_PROFILE="your_rclone_profile" # Your rclone profile name

# Ensure rclone is configured with your B2 credentials

# Define source and destination directories
SOURCE_UPLOADS="$SOURCE_DIR/uploads"
SOURCE_VECTORDB="$SOURCE_DIR/vector_db"
SOURCE_WEBUI_DB="$SOURCE_DIR/webui.db"

DEST_UPLOADS="$B2_BUCKET/user_uploads"
DEST_CHROMADB="$B2_BUCKET/ChromaDB"
DEST_MAIN_DB="$B2_BUCKET/main_database"

# Exclude cache and audit.log
EXCLUDE_LIST=(
    "cache/"
    "audit.log"
)

# Construct exclude arguments for rclone
EXCLUDE_ARGS=""
for EXCLUDE in "${EXCLUDE_LIST[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude '$EXCLUDE'"
done

# Function to perform rclone sync with error checking
rclone_sync() {
    SOURCE="$1"
    DEST="$2"
    echo "Syncing '$SOURCE' to '$DEST'..."
    rclone sync "$SOURCE" "$DEST" $EXCLUDE_ARGS --progress --transfers=32 --checkers=16 --profile "$B2_PROFILE"
    if [ $? -ne 0 ]; then
        echo "Error: rclone sync failed for '$SOURCE' to '$DEST'"
        exit 1
    fi
}

# Perform rclone sync for each directory/file
rclone_sync "$SOURCE_UPLOADS" "$DEST_UPLOADS"
rclone_sync "$SOURCE_VECTORDB" "$DEST_CHROMADB"
rclone_sync "$SOURCE_WEBUI_DB" "$DEST_MAIN_DB"

echo "Backup completed successfully."
exit 0
```

## 带容器中断的 Rsync 任务

为保持数据完整性，通常建议在冷文件系统上运行数据库备份。我们的默认示范备份任务可以稍作修改，在运行备份脚本之前停止应用栈，备份完成后再重新启动。

当然，这种方式的缺点是会导致实例停机。建议在不使用实例的时间段运行该任务，或者采用每日"软备份"（在运行中的数据上）和更稳健的每周备份（在冷数据上）相结合的策略。

```bash

#!/bin/bash

# Configuration
COMPOSE_FILE="docker-compose.yml" # Path to your docker-compose.yml file
B2_BUCKET="b2://OpenWebUI-backups" # Your Backblaze B2 bucket
B2_PROFILE="your_rclone_profile" # Your rclone profile name
SOURCE_DIR="."  # Current directory (where the file structure resides)

# Define source and destination directories
SOURCE_UPLOADS="$SOURCE_DIR/uploads"
SOURCE_VECTORDB="$SOURCE_DIR/vector_db"
SOURCE_WEBUI_DB="$SOURCE_DIR/webui.db"

DEST_UPLOADS="$B2_BUCKET/user_uploads"
DEST_CHROMADB="$B2_BUCKET/ChromaDB"
DEST_MAIN_DB="$B2_BUCKET/main_database"

# Exclude cache and audit.log
EXCLUDE_LIST=(
    "cache/"
    "audit.log"
)

# Construct exclude arguments for rclone
EXCLUDE_ARGS=""
for EXCLUDE in "${EXCLUDE_LIST[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude '$EXCLUDE'"
done

# Function to perform rclone sync with error checking
rclone_sync() {
    SOURCE="$1"
    DEST="$2"
    echo "Syncing '$SOURCE' to '$DEST'..."
    rclone sync "$SOURCE" "$DEST" $EXCLUDE_ARGS --progress --transfers=32 --checkers=16 --profile "$B2_PROFILE"
    if [ $? -ne 0 ]; then
        echo "Error: rclone sync failed for '$SOURCE' to '$DEST'"
        exit 1
    fi
}

# 1. Stop the Docker Compose environment
echo "Stopping Docker Compose environment..."
docker-compose -f "$COMPOSE_FILE" down

# 2. Perform the backup
echo "Starting backup..."
rclone_sync "$SOURCE_UPLOADS" "$DEST_UPLOADS"
rclone_sync "$SOURCE_VECTORDB" "$DEST_CHROMADB"
rclone_sync "$SOURCE_WEBUI_DB" "$DEST_MAIN_DB"

# 3. Start the Docker Compose environment
echo "Starting Docker Compose environment..."
docker-compose -f "$COMPOSE_FILE" up -d

echo "Backup completed successfully."
exit 0
```

## 使用 SQLite 和 ChromaDB 备份功能备份到 B2 远程存储的脚本

```bash

#!/bin/bash

#

# Backup script to back up ChromaDB and SQLite to Backblaze B2 bucket

# openwebuiweeklies, maintaining 3 weekly snapshots.

# Snapshots are independent and fully restorable.

# Uses ChromaDB and SQLite native backup mechanisms.

# Excludes audit.log, cache, and uploads directories.

#

# Ensure rclone is installed and configured correctly.

# Install rclone: https://rclone.org/install/

# Configure rclone: https://rclone.org/b2/

# Source directory (containing ChromaDB and SQLite data)
SOURCE="/var/lib/open-webui/data"

# B2 bucket name and remote name
B2_REMOTE="openwebuiweeklies"
B2_BUCKET="b2:$B2_REMOTE"

# Timestamp for the backup directory
TIMESTAMP=$(date +%Y-%m-%d)

# Backup directory name
BACKUP_DIR="open-webui-backup-$TIMESTAMP"

# Full path to the backup directory in the B2 bucket
DESTINATION="$B2_BUCKET/$BACKUP_DIR"

# Number of weekly snapshots to keep
NUM_SNAPSHOTS=3

# Exclude filters (applied *after* database backups)
EXCLUDE_FILTERS="--exclude audit.log --exclude cache/** --exclude uploads/** --exclude vector_db"

# ChromaDB Backup Settings (Adjust as needed)
CHROMADB_DATA_DIR="$SOURCE/vector_db"  # Path to ChromaDB data directory
CHROMADB_BACKUP_FILE="$SOURCE/chromadb_backup.tar.gz" # Archive file for ChromaDB backup

# SQLite Backup Settings (Adjust as needed)
SQLITE_DB_FILE="$SOURCE/webui.db" # Path to the SQLite database file
SQLITE_BACKUP_FILE="$SOURCE/webui.db.backup" # Temporary file for SQLite backup

# Function to backup ChromaDB
backup_chromadb() {
  echo "Backing up ChromaDB..."

  # Create a tar archive of the vector_db directory
  tar -czvf "$CHROMADB_BACKUP_FILE" -C "$SOURCE" vector_db

  echo "ChromaDB backup complete."
}

# Function to backup SQLite
backup_sqlite() {
  echo "Backing up SQLite database..."
  # Backup the SQLite database using the .backup command
  sqlite3 "$SQLITE_DB_FILE" ".backup '$SQLITE_BACKUP_FILE'"

  # Move the backup file to the source directory
  mv "$SQLITE_BACKUP_FILE" "$SOURCE/"

  echo "SQLite backup complete."
}

# Perform database backups
backup_chromadb
backup_sqlite

# Perform the backup with exclusions
rclone copy "$SOURCE" "$DESTINATION" $EXCLUDE_FILTERS --progress

# Remove old backups, keeping the most recent NUM_SNAPSHOTS
find "$B2_BUCKET" -type d -name "open-webui-backup-*" | sort -r | tail -n +$((NUM_SNAPSHOTS + 1)) | while read dir; do
  rclone purge "$dir"
done

echo "Backup completed to $DESTINATION"
```

---

## 时间点快照

除了进行备份之外，用户还可能希望创建时间点快照，这些快照可以存储在本地（服务器上）、远程或两者都存储。

```bash

#!/bin/bash

# Configuration
SOURCE_DIR="."  # Directory to snapshot (current directory)
SNAPSHOT_DIR="/snapshots" # Directory to store snapshots
TIMESTAMP=$(date +%Y%m%d%H%M%S) # Generate timestamp

# Create the snapshot directory if it doesn't exist
mkdir -p "$SNAPSHOT_DIR"

# Create the snapshot name
SNAPSHOT_NAME="snapshot_$TIMESTAMP"
SNAPSHOT_PATH="$SNAPSHOT_DIR/$SNAPSHOT_NAME"

# Perform the rsync snapshot
echo "Creating snapshot: $SNAPSHOT_PATH"
rsync -av --delete --link-dest="$SNAPSHOT_DIR/$(ls -t "$SNAPSHOT_DIR" | head -n 1)" "$SOURCE_DIR/" "$SNAPSHOT_PATH"

# Check if rsync was successful
if [ $? -eq 0 ]; then
  echo "Snapshot created successfully."
else
  echo "Error: Snapshot creation failed."
  exit 1
fi

exit 0
```

## 使用 Crontab 调度任务

添加备份脚本并配置好备份存储后，建议对脚本进行质量检验，确保其按预期运行。强烈建议开启日志记录。

使用 crontab 按所需频率设置新脚本的运行计划。

# 商业工具

除了自编备份脚本之外，您还可以使用商业解决方案，这类工具通常通过在服务器上安装代理来抽象备份操作的复杂性。这超出了本文的讨论范围，但它们是方便的解决方案。

---

# 宿主机级别备份

您的 Open WebUI 实例可能部署在您控制的宿主机（物理机或虚拟机）上。

宿主机级别的备份是对整个虚拟机（而非运行中的应用）进行快照或备份。

有些用户可能将其作为主要或唯一的保护手段，而另一些用户可能将其作为额外的数据保护层。

# 我需要多少份备份？

备份数量取决于您个人对风险的承受程度。但请记住，最佳实践是*不要*将应用本身视为备份副本（即使它运行在云端！）。这意味着，如果您在 VPS 上部署了实例，保留两份独立备份副本仍然是合理的建议。

适合许多家庭用户需求的备份方案示例：

## 示范备份方案 1（主存储 + 2 份副本）

| 频率 | 目标 | 技术 | 描述 |
|---|---|---|---|
| 每日增量 | 云存储（S3/B2） | rsync | 每日增量备份推送到云存储桶（S3 或 B2）。 |
| 每周增量 | 本地存储（家庭 NAS） | rsync | 每周增量备份从服务器拉取到本地存储（例如家庭 NAS）。 |

## 示范备份方案 2（主存储 + 3 份副本）

这个备份方案稍微复杂，但更为全面——每日向两个云存储提供商推送，以获得额外冗余。

| 频率 | 目标 | 技术 | 描述 |
|---|---|---|---|
| 每日增量 | 云存储（S3） | rsync | 每日增量备份推送到 S3 云存储桶。 |
| 每日增量 | 云存储（B2） | rsync | 每日增量备份推送到 Backblaze B2 云存储桶。 |
| 每周增量 | 本地存储（家庭 NAS） | rsync | 每周增量备份从服务器拉取到本地存储（例如家庭 NAS）。 |

# 扩展主题

为了使本指南保持合理的详尽程度，以下附加主题未作详细介绍，但根据您为实例数据保护计划投入的时间，这些主题可能值得关注：

| 主题 | 描述 |
|---|---|
| SQLite 内置备份 | 考虑使用 SQLite 的 `.backup` 命令实现一致的数据库备份方案。 |
| 加密 | 修改备份脚本以加入静态加密。有关数据库级加密，请参阅 [数据库 Schema 文档](/reference/database-schema)。 |
| 灾难恢复与测试 | 制定灾难恢复计划，并定期测试备份和恢复流程。 |
| 其他备份工具 | 探索其他命令行备份工具，如 `borgbackup` 或 `restic`，以获得更高级的功能。 |
| 邮件通知与 Webhook | 实现邮件通知或 webhook，以监控备份成功或失败的情况。 |
