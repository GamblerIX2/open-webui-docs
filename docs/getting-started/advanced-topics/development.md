---
sidebar_position: 10
title: "开发 Open WebUI"
---

# 开发 Open WebUI

**从源码运行 Open WebUI，用于开发与测试。**

本指南介绍如何搭建本地开发环境，让前端（SvelteKit）和后端（Python/FastAPI）并行运行。你需要两个终端会话，各负责一端。

:::tip 不需要完整开发环境？
如果你只是想体验最新改动，也可以直接运行 [dev Docker 镜像](/getting-started/quick-start)：`docker run -d -p 3000:8080 -v open-webui-dev:/app/backend/data --name open-webui-dev ghcr.io/open-webui/open-webui:dev`
:::

---

## 前置要求

| 要求 | 版本 |
|-------------|---------|
| **Python** | 3.11+ |
| **Node.js** | 22.10+ |
| **Git** | 任意较新版本 |

:::warning 将开发数据与生产数据分开
不要在开发环境与生产环境之间共享数据库或数据目录。开发构建可能包含向后不兼容的数据库迁移。
:::

---

## 1. 克隆仓库

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
```

---

## 2. 前端环境配置

在你的**第一个终端**中，于项目根目录执行：

```bash
cp -RPp .env.example .env
npm install
npm run build
npm run dev
```

`npm run build` 会先编译前端并尽早发现构建期错误；随后 `npm run dev` 会在 [http://localhost:5173](http://localhost:5173) 启动开发服务器。在后端启动之前，它会显示等待画面。

:::tip
如果 `npm install` 因兼容性警告失败，可尝试运行 `npm install --force`。
:::

---

## 3. 后端环境配置

在你的**第二个终端**中执行：

```bash
cd backend
```

创建并激活虚拟环境（Conda 或 venv）：

```bash
# 方案 A：Conda
conda create --name open-webui python=3.11
conda activate open-webui

# 方案 B：venv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

安装依赖并启动服务：

```bash
pip install -r requirements.txt -U
sh dev.sh
```

后端会在 [http://localhost:8080](http://localhost:8080) 启动，API 文档可在 [http://localhost:8080/docs](http://localhost:8080/docs) 查看。

刷新前端页面 [http://localhost:5173](http://localhost:5173)，你应该就能看到完整应用了。

---

## 从其他设备测试

如果你想在手机或同一网络中的另一台电脑上访问开发实例：

1. 找到你机器的局域网 IP（例如 `192.168.1.42`）
2. 将该来源加入 `backend/dev.sh` 中的 CORS：

```bash
export CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080;http://192.168.1.42:5173"
```

3. 重启后端，然后访问 `http://192.168.1.42:5173`

---

## 故障排查

### “FATAL ERROR: Reached Heap Limit”

说明 Node.js 在构建时内存不足。执行前端命令前先增大堆内存：

```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run dev
```

请确认系统至少有 4 GB 可用内存。

### 端口冲突

如果端口 `5173` 或 `8080` 已被占用，请先找出冲突进程：

```bash
# macOS/Linux
lsof -i :5173

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess
```

结束对应进程，或在 `vite.config.js`（前端）或 `dev.sh`（后端）中修改端口。

### 图标未加载（CORS）

如果静态资源加载失败，请在 `backend/dev.sh` 中配置 `CORS_ALLOW_ORIGIN`，使其包含你的前端 URL。详情参见 [CORS 配置](/reference/env-configuration#cors_allow_origin)。

### 热重载不工作

1. 确认两个开发服务器都已启动且没有报错
2. 强制刷新浏览器（Ctrl+Shift+R / Cmd+Shift+R）
3. 重新安装前端依赖：`rm -rf node_modules && npm install`
4. 后端改动可能需要手动重启 `sh dev.sh`

---

## 贡献流程

1. 在开始写代码前，先到 [GitHub Discussions](https://github.com/open-webui/open-webui/discussions/new/choose) **发起讨论**
2. 从 `dev` 分支**创建你自己的分支**。不要直接向 `dev` 提交

```bash
git checkout dev
git pull origin dev
git checkout -b my-feature-branch
```

3. **保持分支同步**，定期从 `dev` 合并更新
4. 以清晰的标题和描述向 `dev` 分支**提交 pull request**

贡献规范请参见 [Contributing](/contributing)。
