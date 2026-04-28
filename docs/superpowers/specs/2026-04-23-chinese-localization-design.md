# Open WebUI Docs 原地中文化设计

## 背景

本仓库是一个 Docusaurus 3 文档站，主要内容位于 `docs/`，当前约有 272 个 Markdown/MDX 文档、35 个 `_category_.json` 分类文件，文档正文总量约 2.35 MB。站点配置中已有 `i18n` 字段，但当前只启用了英文 `en`，没有中文 locale 目录。

本项目目标是将仓库中的用户可见内容原地中文化。用户已确认不新增 `zh-Hans` 多语言目录，不保留英文站点副本，不按核心路径拆分多轮交付，而是在单轮工作中持续完成全站翻译。

当前工作树中 `README.md` 存在用户已有未提交修改。实施时必须保护该修改，不得覆盖或回滚。

## 目标

1. 将站点所有主要用户可见文案翻译为发布质量的简体中文。
2. 原地替换英文内容，保持现有文件路径、URL 结构、侧边栏自动生成机制和 Docusaurus 站点形态。
3. 保持技术准确、表达自然、术语一致，并避免破坏 MDX、代码块、导入语句、链接、环境变量和配置示例。
4. 在完成翻译后通过格式、类型、MDX 和 Docusaurus 构建验证。
5. 提供可重复执行的翻译残留检查方式，帮助发现明显英文残留和结构风险。

## 非目标

1. 不新增或维护英文/中文双语站点。
2. 不引入外部翻译平台、CMS 或运行时语言切换。
3. 不改造信息架构、视觉设计、路由结构或部署方式。
4. 不对截图进行像素级改图。截图应反映真实产品或第三方界面状态；若截图中存在英文 UI，会保留原图，同时翻译周边说明和图片 alt 文案。
5. 不翻译品牌名、产品名、命令名、包名、路径、API 字段、环境变量、类名、函数名等需要保持原样才能准确或可运行的内容。

## 翻译原则

### 语言风格

使用简体中文，语气清晰、专业、直接。面向技术用户时避免过度口语化，面向新用户教程时允许更友好的引导语。保留原文的安全提示、警告强度和操作顺序，不因润色弱化风险提示。

### 术语策略

常见技术名词和产品名保留英文，不额外解释。例如 Open WebUI、Docker、Ollama、API、GitHub、Discord、Kubernetes、Helm、Podman、OpenAI、Anthropic、vLLM、Redis、PostgreSQL、SQLite、OAuth、OIDC、SSO、LDAP、RAG、MCP、OpenAPI。

可自然翻译的通用概念使用中文。例如 installation 翻译为安装，configuration 翻译为配置，troubleshooting 翻译为故障排查，provider 翻译为提供商，workspace 翻译为工作区，model 翻译为模型，pipeline 翻译为流水线或 Pipeline，具体按上下文选择。

### 代码和配置

代码块、命令、配置键、环境变量、API 路径、文件路径、包名、镜像名、服务名、类名、函数名和参数名必须保持可运行。代码块中的注释、示例字符串、示例提示文本、输出说明等可读文本应尽量翻译，但不得改变语法或命令语义。

示例：

```yaml
# 可翻译注释
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      # 不翻译环境变量名，只翻译解释性注释
      - WEBUI_SECRET_KEY=change-me
```

### 链接和锚点

内部链接路径保持不变。链接显示文字可翻译。Markdown 标题翻译后可能改变自动生成锚点；如果同页或跨页链接依赖英文标题锚点，应显式添加或保留可工作的锚点，避免构建和导航断链。

### Frontmatter 和分类文件

`title`、`sidebar_label`、`description`、`label` 等用户可见字段应翻译。`slug`、`sidebar_position`、`id`、`customProps`、导入路径等结构性字段保持不变，除非有明确证据表明字段值只用于展示。

### MDX 和 JSX

MDX 导入语句、组件名、属性名、`value`、`className`、`href`、`src`、`target`、`rel` 等结构性内容保持不变。`label`、`title`、`aria-label`、按钮文案、警告框标题、表格标题和 JSX 文本节点应翻译。

## 范围

### 文档内容

翻译 `docs/` 下所有 `.md`、`.mdx` 和 `_category_.json` 文件中的用户可见内容。包含首页、Getting Started、Features、Tutorials、Troubleshooting、Reference、Enterprise、FAQ、Contributing、License、Security、Roadmap 等现有路径。

### 站点配置

翻译 `docusaurus.config.ts` 中的用户可见站点文案，包括导航栏、页脚、标签、标题、aria 文案和说明性字符串。保留站点 `url`、`baseUrl`、GitHub 仓库配置、插件配置和路由配置。

对于 `i18n`，因为本项目是原地中文化，最终应将 `defaultLocale` 调整为适合简体中文站点的值，例如 `zh-Hans`，并将 `locales` 调整为只包含该默认语言。该调整只改变站点语言元数据，不创建多语言内容目录。

### 组件和主题

翻译 `src/` 下组件和主题覆写中的用户可见字符串，例如赞助商说明、客户证言、复制按钮 aria 文案、免责声明和链接文字。保留 React 组件结构和样式。

### README

翻译 `README.md` 中的用户可见说明，同时必须保留用户已有未提交改动。实施时需先读取当前文件内容，再基于当前内容最小化编辑，不得恢复已删除段落。

### 静态资源

图片、GIF、图标和截图不做像素级编辑。翻译引用这些资源的周边文字、图片替代文本和说明。如果后续需要中文截图，应单独采集真实中文界面截图，而不是直接改图。

## 架构

本项目不改变 Docusaurus 架构。中文化工作以内容层和配置层为主：

1. 内容层：`docs/` 文档和分类文件原地翻译。
2. 配置层：`docusaurus.config.ts` 和站点级可见字符串翻译。
3. 组件层：`src/` 中少量可见字符串翻译。
4. 质量层：新增或使用脚本检查英文残留、MDX 结构、构建结果和可疑变更。

文件路径和 URL 不随标题翻译而改变，避免破坏外部链接、现有书签和搜索索引。

## 工作流

### 1. 建立中文化规范和术语表

新增仓库内中文化规范文档，记录术语表、保留规则、代码块翻译规则、MDX 注意事项和审查清单。该规范作为整轮翻译的统一依据。

### 2. 生成翻译清单

从 `docs/`、`docusaurus.config.ts`、`src/` 和 `README.md` 生成待翻译文件清单。清单应标记文件类型、大小、是否包含 MDX/JSX、是否包含代码块、是否包含表格、是否包含特殊语法。

### 3. 连续原地翻译

按清单逐文件翻译。优先处理结构复杂文件时保持小步验证，尤其是大型参考页、包含大量代码块的插件文档、数据库文档和环境变量文档。

### 4. 结构和残留检查

翻译过程中持续检查以下风险：

1. Markdown frontmatter 是否闭合。
2. MDX import 是否仍位于合法位置。
3. JSX 标签是否配对。
4. 代码围栏数量是否成对。
5. 表格列数是否保持一致。
6. 内部链接路径是否被误翻译。
7. 环境变量、API 路径、命令和配置键是否被误翻译。
8. 可疑英文残留是否需要保留或继续翻译。

### 5. 全站验证

完成翻译后运行项目已有验证命令：

```bash
npm run typecheck
npm run lint
npm run prettier:check
npm run mdx-check
npm run build
```

根据失败信息修复语法、链接、MDX 或类型问题。若某个命令因环境问题无法运行，应记录原因和已完成的替代检查。

## 数据流

输入是现有英文文档、配置和组件字符串。处理过程是根据术语表和翻译规则进行原地替换。输出是同一路径下的中文文档站源码。Docusaurus 构建流程保持不变，仍从 `docs/`、`sidebars.ts`、`docusaurus.config.ts` 和 `src/` 生成静态站点。

## 错误处理

### MDX 构建错误

若构建或 MDX 检查失败，优先定位最近翻译文件，检查未闭合标签、误翻译属性、代码围栏错位、表格格式损坏和 `{}` 表达式被误改。

### 链接错误

若出现 broken link，优先确认路径是否被翻译、标题锚点是否变化、文件名是否保持原样。必要时使用显式锚点或恢复原路径。

### 命令或配置被误翻译

若发现命令、环境变量、配置键、API 字段或路径被误翻译，应立即恢复原样，并在术语表或保留规则中补充该模式，避免后续重复。

### 英文残留

英文残留不一定都是错误。品牌名、产品名、命令、变量、路径、API 字段、协议名、专有名词、代码内容和外部引用可保留。检查时应区分“应保留英文”和“漏翻的说明性英文”。

## 测试与验收

### 自动化验证

1. `npm run typecheck` 通过。
2. `npm run lint` 通过。
3. `npm run prettier:check` 通过。
4. `npm run mdx-check` 通过。
5. `npm run build` 通过。
6. 英文残留扫描完成，明显漏翻说明性文本已处理或记录为合理保留。
7. Git diff 中未出现大规模路径重命名、无关格式化或用户未要求的结构改造。

### 人工抽检

至少抽检以下类型页面：

1. 首页和导航入口。
2. Quick Start 及其嵌套 tabs。
3. FAQ。
4. 环境变量参考页。
5. 插件或扩展性长文档。
6. 故障排查页面。
7. 包含 Mermaid、表格、admonition、JSX 和代码块的页面。

### 发布质量标准

中文表达应自然、准确、统一。警告和安全说明必须清晰。操作步骤必须可执行。代码示例必须保持语法有效。产品名、生态名和命令必须不被误译。站点应能完整构建。

## 实施注意事项

1. 保护现有未提交修改，尤其是 `README.md`。
2. 每次编辑前读取当前文件内容，避免覆盖用户或其他进程的改动。
3. 对大型文件分块处理，避免一次性修改导致难以定位错误。
4. 不运行破坏性 git 命令，不回滚用户改动。
5. 翻译完成前不声称全站已完成；必须以验证命令输出为准。

## 待进入实施计划的任务边界

设计获批后，下一步应创建详细实施计划，至少包含：

1. 中文化规范和术语表文件。
2. 翻译清单生成方式。
3. 文档、配置、组件、README 的翻译顺序。
4. 残留英文和结构检查脚本。
5. 验证命令和修复循环。
6. 最终审查和提交策略。

## 实施进度

*最后更新：2026-04-28*

### 当前进度快照

当前翻译进度以仓库根目录中的 `all_docs.txt`、`modified_docs.txt` 和 `untranslated_docs.txt` 为准。

- 翻译范围内总文件数：308
- 已完成翻译：98
- 剩余待翻译：210
- 当前完成率：31.8%

`modified_docs.txt` 中另有 1 个额外文件 `.github/agents/docs-manager.agent.md`，它不在原始 `all_docs.txt` 统计范围内，因此不计入上述完成率。

### 已完成的主要区域

截至本次更新，以下区域已完成或基本完成中文化：

- `docs/features/open-terminal/**`
- `docs/features/extensibility/**` 的已翻译子集
- `docs/features/authentication-access/**` 的已翻译子集
- `docs/features/administration/**` 的已翻译子集
- `docs/tutorials/auth-sso/**`
- `docs/tutorials/integrations/**` 的已翻译子集
- `docs/tutorials/maintenance/**`
- `docs/features/workspace/**`
- `docs/reference/` 下的部分页面

详细文件清单以仓库根目录 `modified_docs.txt` 为准。

### 仍需推进的主要区域

当前剩余工作主要集中在以下目录：

- `docs/features/chat-conversations/**`（剩余 79 个）
- `docs/getting-started/quick-start/**`（剩余 31 个）
- `docs/features/extensibility/**`（剩余 11 个）
- `docs/features/open-terminal/**`（剩余 8 个）
- `docs/reference/https/**`（剩余 7 个）
- `docs/tutorials/integrations/**`（剩余 7 个）
- `docs/getting-started/advanced-topics/**`（剩余 5 个）
- `docs/reference/tab-nginx/**`（剩余 5 个）
- `docs/enterprise/**`
- 根级页面与分类文件，如 `docs/brand.mdx`、`docs/contributing.mdx`、`docs/faq.mdx` 以及各目录下的 `_category_.json`

详细待翻译文件清单以仓库根目录 `untranslated_docs.txt` 为准。

### 进度记录与合并前要求

在继续翻译或准备合并 PR 前，应保持以下记录与验证习惯：

1. 每完成一批翻译后，同步更新 `modified_docs.txt` 与 `untranslated_docs.txt`。
2. 若翻译范围发生变化，重新生成 `all_docs.txt`，确保基数一致。
3. 合并前至少运行：
   - `npm run prettier:check`
   - `npm run mdx-check`
   - `npm run build`
4. 如环境允许，继续补跑：
   - `npm run typecheck`
   - `npm run lint`
5. 对于保留英文的品牌名、命令、环境变量、路径、API 字段和代码块内容，需在审查时明确标注为“合理保留”，避免被误判为漏翻。

### 下一阶段建议

为尽快逼近全站 100% 中文化，建议优先按以下顺序推进：

1. `docs/features/chat-conversations/**`
2. `docs/getting-started/**`
3. `docs/reference/**`
4. `docs/enterprise/**`
5. 全量 `_category_.json` 与根级零散页面收尾
