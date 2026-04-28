---
sidebar_position: 3
title: "聊天分享"
---

### 启用社区分享

要启用社区分享，请按以下步骤操作：

1. 以 **Admin** 身份进入 **Admin Panel**
2. 点击 **Settings** 标签
3. 在 **General** 设置标签中开启 **Enable Community Sharing**

:::note

**注意：** 只有管理员可以切换 **Enable Community Sharing**。如果该选项关闭，用户和管理员都不会看到 **Share to Open WebUI Community** 这个聊天分享选项。只有管理员启用社区分享后，用户才能把聊天分享到 Open WebUI 社区。

:::

这样一来，你的 Open WebUI 实例中的所有用户都可以使用社区分享。

### 分享聊天

要分享聊天：

1. 选中你想分享的聊天对话
2. 将鼠标悬停在目标聊天上方，点击出现的 3 点菜单
3. 点击 **Share**
4. 选择 **Share to Open WebUI Community**（如果管理员已开启 **Enable Community Sharing**）或 **Copy Link**

#### 分享到 Open WebUI Community

当你选择 `Share to Open WebUI Community` 时：

- 会打开一个新标签页，让你把聊天以快照形式上传到 Open WebUI 社区网站（https://openwebui.com/chats/upload）
- 你可通过以下权限设置控制谁可以查看已上传的聊天：
  - **Private**：只有你自己可以访问
  - **Public**：互联网中的任何人都可以查看该聊天快照中展示的消息
  - **Public, Full History**：互联网中的任何人都可以查看该聊天的完整重生成历史

:::note

注意：你可以随时在社区平台上的 openwebui.com 账号中修改已分享聊天的权限级别。

**当前，社区网站上的已分享聊天还不能通过搜索发现。不过后续更新计划支持：当权限为 `Public` 或 `Public, Full History` 时，公开聊天可被公众发现。**

:::

#### 复制分享链接

当你选择 `Copy Link` 时，系统会生成一个唯一的分享链接，你可以把它发送给其他人。

**重要说明：**

- 被分享的聊天只会包含创建链接当时已有的消息。生成链接后，如果聊天里新增了消息，这些新消息不会自动包含进去，除非你删除旧链接并重新生成新链接
- 生成的分享链接本质上是该聊天在生成时刻的静态快照
- 若要查看已分享聊天，用户必须：
  1. 在生成该链接的 Open WebUI 实例上拥有账号
  2. 已在该实例中登录自己的账号
- 如果用户未登录就访问该分享链接，会先被重定向到登录页，登录后才能查看该聊天

### 查看已分享聊天

要查看已分享聊天：

1. 确保你已登录到生成该分享链接的 Open WebUI 实例账号
2. 点击分享给你的链接
3. 聊天会以只读形式显示
4. 如果生成该分享链接的 Open WebUI 实例管理员已配置 Text-to-Speech，则消息旁可能会显示朗读按钮（视具体情况而定）

### 更新已分享聊天

要更新已分享聊天：

1. 选中你想分享的聊天对话
2. 将鼠标悬停在目标聊天上方，点击出现的 3 点菜单
3. 点击 **Share**
4. 如果你之前分享过该聊天，**Share Chat** Modal 的显示会有所不同

**Share Chat** Modal 包含以下选项：

- **before**：在新标签页打开此前通过分享链接分享出去的聊天
- **delete this link**：删除该聊天当前的分享链接，并恢复到初始分享弹窗
- **Share to Open WebUI Community**：打开新标签页进入 https://openwebui.com/chats/upload，并自动带上当前聊天快照
- **Update and Copy Link**：更新此前分享链接对应的聊天快照，并将该链接复制到设备剪贴板

### 删除已分享聊天 {#deleting-shared-chats}

要删除分享链接：

1. 选中你想删除分享链接的聊天对话
2. 将鼠标悬停在目标聊天上方，点击出现的 3 点菜单
3. 点击 **Share**
4. 如果你之前分享过该聊天，**Share Chat** Modal 的显示会有所不同
5. 点击 **delete this link**

删除后，该分享链接将立即失效，其他用户将无法再查看该聊天。

:::note

**注意：** 分享到社区平台的聊天无法删除。如需修改社区平台上某个聊天的访问权限：

:::

1. 登录你在 openwebui.com 上的 Open WebUI 账号
2. 点击网站右上角的账号用户名
3. 点击 **Chats**
4. 打开你要修改权限的聊天
5. 滚动到聊天底部并更新其权限级别
6. 点击 **Update Chat**

### 管理已分享聊天

Open WebUI 提供了一个集中式面板，用于管理你分享过的所有聊天对话。你可以在其中搜索分享历史、重新复制链接，或立即撤销访问权限。

有关该管理面板的详细说明，请参阅 [Shared Chats Management](/features/chat-conversations/data-controls/shared-chats)。
