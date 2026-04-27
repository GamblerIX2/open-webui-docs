import os
import pathlib

DOCS = pathlib.Path(__file__).resolve().parents[1] / "docs"
filepath = DOCS / "reference/env-configuration.mdx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('title: "Environment Variable Configuration"', 'title: "环境变量配置"'),
    ('## Overview\n\nOpen WebUI provides a large range of environment variables that allow you to customize and configure\nvarious aspects of the application. This page serves as a comprehensive reference for all available\nenvironment variables, providing their types, default values, and descriptions.\nAs new variables are introduced, this page will be updated to reflect the growing configuration options.',
     '## 概述\n\nOpen WebUI 提供了大量的环境变量，允许你定制和配置应用程序的各个方面。本页面作为所有可用环境变量的综合参考，提供它们的类型、默认值和描述。\n随着新变量的引入，本页面将不断更新，以反映日益增加的配置选项。'),
    ('This page is up-to-date with Open WebUI release version [v0.9.0](https://github.com/open-webui/open-webui/releases/tag/v0.9.0), but is still a work in progress to later include more accurate descriptions, listing out options available for environment variables, defaults, and improving descriptions.',
     '本页面与 Open WebUI 发布版本 [v0.9.0](https://github.com/open-webui/open-webui/releases/tag/v0.9.0) 保持同步，但仍在完善中，后续将包含更准确的描述、列出环境变量的可用选项、默认值以及改进的描述。'),
    ('### Important Note on `PersistentConfig` Environment Variables', '### 关于 `PersistentConfig` 环境变量的重要说明'),
    ('When launching Open WebUI for the first time, all environment variables are treated equally and can be used to configure the application. However, for environment variables marked as `PersistentConfig`, their values are persisted and stored internally.',
     '首次启动 Open WebUI 时，所有环境变量都被同等对待，可用于配置应用程序。但是，对于标记为 `PersistentConfig` 的环境变量，它们的值会被持久化并存储在内部。'),
    ('After the initial launch, if you restart the container, `PersistentConfig` environment variables will no longer use the external environment variable values. Instead, they will use the internally stored values.',
     '初始启动后，如果你重新启动容器，`PersistentConfig` 环境变量将不再使用外部环境变量的值。相反，它们将使用内部存储的值。'),
    ('In contrast, regular environment variables will continue to be updated and applied on each subsequent restart.',
     '相比之下，常规环境变量将在随后的每次重启时继续更新并应用。'),
    ('You can update the values of `PersistentConfig` environment variables directly from within Open WebUI, and these changes will be stored internally. This allows you to manage these configuration settings independently of the external environment variables.',
     '你可以直接从 Open WebUI 内部更新 `PersistentConfig` 环境变量的值，这些更改将存储在内部。这使你可以独立于外部环境变量来管理这些配置设置。'),
    ('Please note that `PersistentConfig` environment variables are clearly marked as such in the documentation below, so you can be aware of how they will behave.',
     '请注意，`PersistentConfig` 环境变量在下面的文档中已明确标记，以便你了解它们的行为方式。'),
    ('To disable this behavior and force Open WebUI to always use your environment variables (ignoring the database), set `ENABLE_PERSISTENT_CONFIG` to `False`.',
     '要禁用此行为并强制 Open WebUI 始终使用你的环境变量（忽略数据库），请将 `ENABLE_PERSISTENT_CONFIG` 设置为 `False`。'),
    ('**CRITICAL WARNING:** When `ENABLE_PERSISTENT_CONFIG` is `False`, you may still be able to edit settings in the Admin UI. However, these changes are **NOT saved permanently**. They will persist only for the current session and will be **lost** when you restart the container, as the system will revert to the values defined in your environment variables.',
     '**CRITICAL WARNING（严重警告）：** 当 `ENABLE_PERSISTENT_CONFIG` 为 `False` 时，你可能仍然能够在管理界面中编辑设置。然而，这些更改**不会永久保存**。它们仅在当前会话中持续有效，并在你重新启动容器时**丢失**，因为系统将恢复为环境变量中定义的值。'),
    ('### Troubleshooting Ignored Environment Variables 🛠️', '### 排查被忽略的环境变量 🛠️'),
    ('If you change an environment variable (like `ENABLE_SIGNUP=True`) but don\'t see the change reflected in the UI (e.g., the "Sign Up" button is still missing), it\'s likely because a value has already been persisted in the database from a previous run or a persistent Docker volume.',
     '如果你更改了环境变量（例如 `ENABLE_SIGNUP=True`）但在 UI 中未看到更改反映出来（例如，"注册"按钮仍然缺失），这很可能是因为之前运行的值或持久化的 Docker 卷中的值已经持久化在数据库中。'),
    ('#### Option 1: Using `ENABLE_PERSISTENT_CONFIG` (Temporary Fix)', '#### 选项 1：使用 `ENABLE_PERSISTENT_CONFIG`（临时修复）'),
    ('Set `ENABLE_PERSISTENT_CONFIG=False` in your environment. This forces Open WebUI to read your variables directly. Note that UI-based settings changes will not persist across restarts in this mode.',
     '在你的环境中设置 `ENABLE_PERSISTENT_CONFIG=False`。这会强制 Open WebUI 直接读取你的变量。请注意，在此模式下，基于 UI 的设置更改不会在重启后持久保留。'),
    ('#### Option 2: Update via Admin UI (Recommended)', '#### 选项 2：通过管理界面更新（推荐）'),
    ('The simplest and safest way to change `PersistentConfig` settings is directly through the **Admin Panel** within Open WebUI. Even if an environment variable is set, changes made in the UI will take precedence and be saved to the database.',
     '更改 `PersistentConfig` 设置的最简单、最安全的方法是直接通过 Open WebUI 内的 **管理面板**。即使设置了环境变量，在 UI 中所做的更改也会优先应用并保存到数据库。'),
    ('#### Option 3: Manual Database Update (Last Resort / Lock-out Recovery)', '#### 选项 3：手动数据库更新（最后的手段 / 锁定恢复）'),
    ('If you are locked out or cannot access the UI, you can manually update the SQLite database via Docker:',
     '如果你被锁定或无法访问 UI，你可以通过 Docker 手动更新 SQLite 数据库：'),
    ('*(Replace `ENABLE_SIGNUP` and `true` with the specific setting and value needed.)*', '*(将 `ENABLE_SIGNUP` 和 `true` 替换为所需的特定设置和值。)*'),
    ('#### Option 4: Resetting for a Fresh Install', '#### 选项 4：重置以进行全新安装'),
    ('If you are performing a clean installation and want to ensure all environment variables are fresh:',
     '如果你正在执行全新安装并希望确保所有环境变量都是全新的：'),
    ('1. Stop the container.', '1. 停止容器。'),
    ('2. Remove the persistent volume: `docker volume rm open-webui`.', '2. 删除持久卷：`docker volume rm open-webui`。'),
    ('3. Restart the container.', '3. 重新启动容器。'),
    ('**Warning:** Removing the volume will delete all user data, including chats and accounts.',
     '**警告：** 删除卷将删除所有用户数据，包括聊天和账户。'),
    ('## App/Backend', '## 应用程序/后端'),
    ('The following environment variables are used by `backend/open_webui/config.py` to provide Open WebUI startup',
     '以下环境变量被 `backend/open_webui/config.py` 使用以提供 Open WebUI 启动'),
    ('configuration. Please note that some variables may have different default values depending on',
     '配置。请注意，某些变量的默认值可能会根据'),
    ('whether you\'re running Open WebUI directly or via Docker. For more information on logging',
     '你是直接运行 Open WebUI 还是通过 Docker 运行而有所不同。有关日志记录'),
    ('environment variables, see our [logging documentation](https://docs.openwebui.com/getting-started/advanced-topics/logging).',
     '环境变量的更多信息，请参阅我们的 [日志文档](https://docs.openwebui.com/getting-started/advanced-topics/logging)。'),
    ('### General', '### 常规'),
    ('- Type: ', '- 类型：'),
    ('- Default: ', '- 默认值：'),
    ('- Description: ', '- 描述：'),
    ('- Persistence: This environment variable is a `PersistentConfig` variable.', '- 持久化：这是一个 `PersistentConfig` 变量。'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Let's replace the common section headers
content = content.replace('## Ollama', '## Ollama 配置')
content = content.replace('## OpenAI API', '## OpenAI API 配置')
content = content.replace('## Search', '## 搜索配置')
content = content.replace('## Authentication', '## 认证配置')
content = content.replace('## RAG', '## RAG (检索增强生成) 配置')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("done basic translation")
