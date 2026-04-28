---
sidebar_position: 6
title: "聊天参数"
---

在 Open WebUI 中，**System Prompt** 和 **Advanced Parameters** 共有三层设置粒度：按聊天、按模型、按账号。这个分层体系既保证了灵活性，也保留了结构化管理和控制能力。

## System Prompt 与 Advanced Parameters 层级图

| **Level** | **Definition** | **Modification Permissions** | **Override Capabilities** |
| --- | --- | --- | --- |
| **Per-Chat** | 针对某个具体聊天实例设置的 system prompt 和 advanced parameters | 用户可修改，但不能覆盖模型级设置 | 不能覆盖模型级设置 |
| **Per-Account** | 针对某个用户账号设置的默认 system prompt 和 advanced parameters | 用户可设置，但可能被模型级设置覆盖 | 用户设置可被模型级设置覆盖 |
| **Per-Model** | 针对某个模型设置的默认 system prompt 和 advanced parameters | 管理员可设置，用户不可修改 | 管理员设置优先，用户设置可被覆盖 |

### 1. **按聊天设置：**

- **说明**：按聊天设置是指针对某个具体聊天实例配置的 system prompt 和 advanced parameters。这些设置只对当前对话生效，不会影响后续新聊天。
- **如何设置**：用户可在 Open WebUI 右侧边栏的 **Chat Controls** 中修改某个具体聊天实例的 system prompt 和 advanced parameters。
- **覆盖能力**：如果管理员已在模型级（**#2**）设置了 **System Prompt** 或特定 **Advanced Parameters**，用户将不能在聊天级覆盖它们。这可确保一致性并遵守模型级配置。

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>示例用例</summary>

:::tip

**按聊天设置：**  
例如某位用户想为某个特定对话设置自定义 system prompt，他可以进入 **Chat Controls** 并修改 **System Prompt** 字段。这些改动只会影响当前聊天会话。

:::
</details>

### 2. **按账号设置：**

- **说明**：按账号设置是指为某个用户账号配置默认 system prompt 和 advanced parameters。当更低层级没有定义相关设置时，这些用户级设置可作为回退值使用。
- **如何设置**：用户可在 Open WebUI 的 **Settings** 菜单中的 **General** 部分为自己的账号设置 system prompt 和 advanced parameters。
- **覆盖能力**：用户可以为自己的账号设置 system prompt，但也要注意：如果管理员已经针对正在使用的特定模型，在模型级设置了 **System Prompt** 或特定 **Advanced Parameters**，这些账号级参数仍然可能被覆盖。

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>示例用例</summary>

:::tip

**按账号设置：**  
例如某位用户想为自己的账号设置默认 system prompt，他可以进入 **Settings** 菜单并修改 **System Prompt** 字段。

:::
</details>

### 3. **按模型设置：**

- **说明**：按模型设置是指为某个模型配置默认 system prompt 和 advanced parameters。这些设置会应用于所有使用该模型的聊天实例。
- **如何设置**：管理员可在 Open WebUI 的 **Workspace** 中的 **Models** 部分，为某个模型设置默认 system prompt 和 advanced parameters。
- **覆盖能力**：**User** 账号不能在模型级（**#3**）修改 **System Prompt** 或特定 **Advanced Parameters**。这一限制可防止用户不恰当地更改默认设置。
- **上下文长度保持：** 当管理员在 **Workspace** 中手动为模型设置 **System Prompt** 或特定 **Advanced Parameters** 后，**User** 账号便无法再在 **General** 设置或 **Chat Controls** 中按账号或按聊天覆盖这些手动设置。这可确保一致性，并避免用户修改上下文长度时频繁导致模型重新加载。
- **模型优先级：** 如果管理员已在 Workspace 中为某模型预设了 **System Prompt** 或特定 **Advanced Parameters**，那么 **User** 账号在 **General** 设置或 **Chat Controls** 中做出的上下文长度变更将被忽略，以保持该模型的预配置值。需要注意的是，凡是管理员**未触及**的参数，用户仍可按账号或按聊天自行调整。

<!-- markdownlint-disable-next-line MD033 -->
<details>
<!-- markdownlint-disable-next-line MD033 -->
<summary>示例用例</summary>

:::tip

**按模型设置：**  
例如管理员想为某个特定模型设置默认 system prompt，他可以进入 **Models** 部分并修改相应模型的 **System Prompt** 字段。任何使用该模型的聊天实例都会自动继承该模型的 system prompt 和 advanced parameters。

:::
</details>

## **最大化灵活性的 System Prompt 优化建议**

:::tip

**额外建议**  
**以下建议同时适用于管理员和普通用户。若想最大化 system prompt 的灵活性，可考虑如下方式：**

- 将你的主要 System Prompt（**例如赋予 LLM 一个明确人格**）放在 **General** 设置中的 **System Prompt** 字段。这会在账号级生效，让它在所有 LLM 上都可作为基础 system prompt，而无需在 **Workspace** 的模型设置里逐个调整。

- 对于次级 System Prompt（**例如让 LLM 执行某个具体任务**），你可以根据需要将其放在 **Chat Controls** 侧边栏的 **System Prompt** 字段（按聊天），或对于管理员放到 **Workspace** 的 **Models** 部分（按模型）。这样账号级 system prompt 就能与 **Chat Controls** 提供的聊天级 prompt，或 **Models** 提供的模型级 prompt 叠加工作。

- 作为管理员，建议你通过 **Models** 部分按模型设置 LLM 参数，以获得最佳灵活性。对于这些次级 System Prompt，请尽量采用既能提高灵活性、又能减少跨账号 / 跨聊天重复调整的设置方式。管理员和所有用户都应清楚了解：**Chat Controls** 与 **Models** 中的 system prompt 最终会按怎样的优先顺序应用到 **LLM**。

:::
