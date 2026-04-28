---
sidebar_position: 2
title: "Artifacts"
---

## 什么是 Artifacts？如何在 Open WebUI 中使用它们？

Open WebUI 中的 Artifacts 是一项受 Claude.AI Artifacts 启发的创新功能，它允许你在聊天中直接与 LLM 生成的、较大且独立的内容进行交互。通过 Artifacts，你可以将重要内容与主对话分离地查看、修改、迭代、构建或引用，从而更容易处理复杂输出，也能在之后再次访问关键信息。

## Open WebUI 何时会使用 Artifacts？

当生成内容满足本平台特定条件时，Open WebUI 就会创建 Artifact：

1. **可渲染**：要作为 Artifact 显示，内容必须是 Open WebUI 支持渲染的格式，包括：

- 单页 HTML 网站
- 可缩放矢量图（SVG）
- 完整网页，即同一个 Artifact 中同时包含 HTML、JavaScript 和 CSS。若要生成完整网页，必须包含 HTML
- ThreeJS 可视化，以及 D3.js 等其他 JavaScript 可视化库

其他内容类型，例如文档（Markdown 或纯文本）、代码片段和 React 组件，不会在 Open WebUI 中被渲染为 Artifact。

## Open WebUI 的模型如何创建 Artifacts？

若要在 Open WebUI 中使用 Artifacts，模型必须生成会触发渲染流程的内容。这通常意味着模型要生成有效的 HTML、SVG 或其他受支持的 Artifact 渲染格式。当生成内容满足上述条件时，Open WebUI 就会将其显示为可交互的 Artifact。

## 如何在 Open WebUI 中使用 Artifacts？

当 Open WebUI 创建 Artifact 后，你会在主聊天右侧看到一个专门的 Artifacts 窗口。你可以这样与它交互：

- **编辑与迭代**：直接在聊天中要求 LLM 修改或迭代该内容，更新结果会立即显示在 Artifact 窗口中。你可通过 Artifact 左下角的版本选择器切换不同版本。每次编辑都会生成一个新版本，方便追踪变化
- **自动更新**：Open WebUI 可能会根据你的后续消息更新现有 Artifact，窗口会显示最新内容
- **操作按钮**：在 Artifact 右下角可以使用更多操作，例如复制内容或全屏打开 Artifact

## 编辑 Artifacts

1. **定向更新**：描述你想改什么以及改哪里。例如：

- “请把图表中柱子的颜色从蓝色改成红色。”
- “请将 SVG 图像的标题更新为 'New Title'。”

2. **整体重写**：如果变更涉及大部分内容、结构调整较大或需要同时修改多个区域，可以要求整体重写。例如：

- “请把这个单页 HTML 网站重写成一个落地页。”
- “请重新设计这个 SVG，让它用 ThreeJS 动画化。”

**最佳实践：**

- 明确指出你想修改 Artifact 的哪一部分
- 对于定向更新，可引用目标附近的唯一文本作为定位依据
- 根据你的需求判断：是小范围修改更合适，还是整体重写更合适

## 使用场景

Open WebUI 中的 Artifacts 能帮助不同团队快速高效地产出高质量工作成果。以下是一些适合本平台的例子：

- **设计师**：
  - 创建用于 UI/UX 设计的交互式 SVG 图形
  - 设计单页 HTML 网站或落地页
- **开发者**：创建简单 HTML 原型，或为项目生成 SVG 图标
- **市场团队**：
  - 设计带效果指标的活动落地页
  - 创建用于广告创意或社交媒体发布的 SVG 图形

## 你可以用 Open WebUI Artifacts 创建哪些项目

Open WebUI 中的 Artifacts 让不同团队和个人能够快速高效地创建高质量成果。以下示例展示了它的多样性，也希望能激发你探索其潜力：

1. **交互式可视化**

- 组件：ThreeJS、D3.js、SVG
- 优势：可创建沉浸式数据叙事与交互式可视化。Open WebUI 的 Artifacts 支持版本切换，因此你可以更容易测试不同可视化方案并跟踪修改

示例项目：用 ThreeJS 构建一个展示股价时间变化的交互式折线图。通过不同版本分别调整颜色和坐标轴比例，以比较不同可视化策略。

2. **单页 Web 应用**

- 组件：HTML、CSS、JavaScript
- 优势：可直接在 Open WebUI 中开发单页 Web 应用，并通过定向更新或整体重写不断迭代内容

示例项目：设计一个基于 HTML 和 CSS 的待办事项应用，并用 JavaScript 增加交互功能。随后通过定向更新和整体重写，持续改进布局与 UI/UX。

3. **动画 SVG 图形**

- 组件：SVG、ThreeJS
- 优势：为营销活动、社交媒体或网页设计创建吸引人的动画 SVG 图形。Open WebUI 的 Artifacts 允许你在同一个窗口中持续编辑和迭代

示例项目：为某公司品牌设计一个带动画效果的 SVG Logo。使用 ThreeJS 添加动画，再利用 Open WebUI 的定向更新优化配色和设计。

4. **网页原型**

- 组件：HTML、CSS、JavaScript
- 优势：可直接在 Open WebUI 中构建并测试网页原型，并通过版本切换对比不同设计方案，不断打磨原型

示例项目：用 HTML、CSS 和 JavaScript 为一个新的电商网站制作原型，并通过 Open WebUI 的定向更新不断优化导航、布局和 UI/UX。

5. **交互式叙事**

- 组件：HTML、CSS、JavaScript
- 优势：可创建带滚动效果、动画及其他交互元素的互动故事。Open WebUI 的 Artifacts 支持你持续优化故事内容，并测试不同版本

示例项目：制作一个讲述公司发展历史的交互式故事，使用滚动效果和动画增强阅读体验，并通过定向更新优化叙事内容，再利用版本选择器测试不同故事版本。

## 故障排查

### Artifacts 预览无法工作（Uncaught SecurityError）

如果你遇到聊天界面中代码预览不显示，并在浏览器控制台中看到类似 `Artifacts.svelte:40 Uncaught SecurityError` 的报错，这通常是某些环境配置下的跨域 iframe 限制造成的。

**解决方案：**

1. 前往 **Settings > Interface**
2. 开启 **Allow Iframe Sandbox Same-Origin Access**
3. 保存设置
