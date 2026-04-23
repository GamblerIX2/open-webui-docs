# Podman Quadlet（systemd）

Podman Quadlet 允许你把容器作为原生 systemd 服务进行管理。这是在使用 systemd 的 Linux 发行版（如 Fedora、RHEL、Ubuntu 等）上运行生产容器的推荐方式。

## 🛠️ 配置

1. **创建配置目录：**
   如果是 rootless 用户部署：
   ```bash
   mkdir -p ~/.config/containers/systemd/
   ```

2. **创建容器文件：**
   新建 `~/.config/containers/systemd/open-webui.container`，内容如下：

   ```ini title="open-webui.container"
   [Unit]
   Description=Open WebUI Container
   After=network-online.target

   [Container]
   Image=ghcr.io/open-webui/open-webui:main
   ContainerName=open-webui
   PublishPort=3000:8080
   Volume=open-webui:/app/backend/data
   
   # 网络：Podman 5+ 默认使用 Pasta
   # 如果需要访问宿主机服务（例如宿主机上的 Ollama）：
   AddHost=host.containers.internal:host-gateway

   [Service]
   Restart=always

   [Install]
   WantedBy=default.target
   ```

3. **重新加载 systemd 并启动服务：**
   ```bash
   systemctl --user daemon-reload
   systemctl --user start open-webui
   ```

4. **设置开机自启：**
   ```bash
   systemctl --user enable open-webui
   ```

## 📊 管理

- **查看状态：**
  ```bash
  systemctl --user status open-webui
  ```

- **查看日志：**
  ```bash
  journalctl --user -u open-webui -f
  ```

- **停止服务：**
  ```bash
  systemctl --user stop open-webui
  ```

:::tip 更新
更新镜像时，只需拉取新版本（`podman pull ghcr.io/open-webui/open-webui:main`），然后重启服务（`systemctl --user restart open-webui`）。
:::
