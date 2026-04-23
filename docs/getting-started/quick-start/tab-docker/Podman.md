# 使用 Podman

Podman 是一个无守护进程的容器引擎，可用于开发、管理和运行 OCI 容器。

## 基础命令

- **运行容器：**

  ```bash
  podman run -d --name openwebui -p 3000:8080 -v open-webui:/app/backend/data ghcr.io/open-webui/open-webui:main
  ```

- **查看运行中的容器：**

  ```bash
  podman ps
  ```

## Podman 网络

如果出现网络问题（尤其是在 rootless Podman 下），你可能需要调整网络桥接设置。

:::warning Slirp4netns 已逐步弃用
较早的 Podman 教程常建议使用 `slirp4netns`。不过，`slirp4netns` 正在**被弃用**，并将在 **Podman 6** 中移除。

现代替代方案是 **[pasta](https://passt.top/passt/about/)**，它已成为 Podman 5.0+ 的默认方案。
:::

### 访问宿主机（本地服务）

如果你把 Ollama 或其他服务直接运行在宿主机上，请使用特殊 DNS 名称 **`host.containers.internal`** 指向你的电脑。

#### 现代方式（Pasta - Podman 5+ 默认）
通常无需额外参数，就可以通过 `host.containers.internal` 访问宿主机。

#### 旧方式（Slirp4netns）
如果你的 Podman 版本较旧，且不支持 `pasta`：
1. 请先确认已安装 [slirp4netns](https://github.com/rootless-containers/slirp4netns)。
2. 使用以下参数启动容器，以允许访问宿主回环地址：

```bash
podman run -d --network=slirp4netns:allow_host_loopback=true --name openwebui -p 3000:8080 -v open-webui:/app/backend/data ghcr.io/open-webui/open-webui:main
```

### 连接配置
进入 Open WebUI 后，打开 **Settings > Admin Settings > Connections**，将你的 Ollama API 连接设为：
`http://host.containers.internal:11434`

更多高级配置请参阅 Podman [官方文档](https://podman.io/)。

## 卸载

如需卸载通过 Podman 运行的 Open WebUI，请执行以下步骤：

1.  **停止并删除容器：**
    ```bash
    podman rm -f openwebui
    ```

2.  **删除镜像（可选）：**
    ```bash
    podman rmi ghcr.io/open-webui/open-webui:main
    ```

3.  **删除数据卷（可选，警告：会删除所有数据）：**
    如果你希望彻底清除数据（聊天、设置等）：
    ```bash
    podman volume rm open-webui
    ```
