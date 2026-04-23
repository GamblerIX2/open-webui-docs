import { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

import rehypeShiki, { type RehypeShikiOptions } from "@shikijs/rehype";
import { type BundledLanguage, bundledLanguages } from "shiki";

const shikiPlugin: [typeof rehypeShiki, RehypeShikiOptions] = [
	rehypeShiki,
	{
		themes: {
			light: "github-light",
			dark: "github-dark",
		},
		defaultColor: false,
		langs: Object.keys(bundledLanguages) as BundledLanguage[],
	},
];

const config: Config = {
	title: "Open WebUI",
	titleDelimiter: "/",
	tagline: "致力于打造最佳 AI 界面",
	favicon: "images/favicon.png",

	// Set the production url of your site here
	url: "https://openwebui.com",
	// Set the /<baseUrl>/ pathname under which your site is served
	// For GitHub pages deployment, it is often '/<projectName>/'
	baseUrl: "/",

	// GitHub pages deployment config.
	// If you aren't using GitHub pages, you don't need these.
	organizationName: "open-webui", // Usually your GitHub org/user name.
	projectName: "docs", // Usually your repo name.

	onBrokenLinks: "throw",

	// Even if you don't use internationalization, you can use this field to set
	// useful metadata like html lang. For example, if your site is Chinese, you
	// may want to replace "en" with "zh-Hans".
	i18n: {
		defaultLocale: "zh-Hans",
		locales: ["zh-Hans"],
	},

	// Enable Mermaid for diagrams
	markdown: {
		mermaid: true,
	},
	themes: ["@docusaurus/theme-mermaid"],

	presets: [
		[
			"classic",
			{
				gtag: {
					trackingID: "G-522JSJVWTB",
					anonymizeIP: false,
				},
				docs: {
					sidebarPath: "./sidebars.ts",
					routeBasePath: "/",
					// Please change this to your repo.
					// Remove this to remove the "edit this page" links.
					editUrl: "https://github.com/open-webui/docs/blob/main",
					exclude: ["**/tab-**/**"],
					beforeDefaultRehypePlugins: [shikiPlugin],
				},
				// blog: false,
				blog: {
					showReadingTime: true,
					onUntruncatedBlogPosts: "ignore",
					// Please change this to your repo.
					// Remove this to remove the "edit this page" links.
					// editUrl:
					// "https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/",
					beforeDefaultRehypePlugins: [shikiPlugin],
				},
				theme: {
					customCss: "./src/css/custom.css",
				},
			} satisfies Preset.Options,
		],
	],

	themeConfig: {
		// Replace with your project's social card
		// image: "images/docusaurus-social-card.jpg",
		navbar: {
			title: "Open WebUI",
			logo: {
				src: "images/logo.png",
				srcDark: "images/logo-dark.png",
			},
			items: [
				{
					href: "https://openwebui.com/blog",
					label: "博客",
					position: "left",
				},
				{
					label: "GitHub",
					href: "https://github.com/open-webui/open-webui",
					position: "right",
					className: "header-github-link",
					"aria-label": "GitHub 仓库",
				},
				{
					label: "Discord",
					href: "https://discord.com/invite/5rJgQTnV4s",
					position: "right",
					className: "header-discord-link",
					"aria-label": "Discord 服务器",
				},
			],
		},
		footer: {
			style: "light",
			links: [
				{
					title: "文档",
					items: [
						{
							label: "快速开始",
							to: "getting-started",
						},
						{
							label: "常见问题",
							to: "faq",
						},
						{
							label: "帮助改进文档",
							to: "https://github.com/open-webui/docs",
						},
					],
				},
				{
					title: "社区",
					items: [
						{
							label: "GitHub",
							href: "https://github.com/open-webui/open-webui",
						},
						{
							label: "Discord",
							href: "https://discord.gg/5rJgQTnV4s",
						},
						{
							label: "Reddit",
							href: "https://www.reddit.com/r/OpenWebUI/",
						},
						{
							label: "𝕏",
							href: "https://x.com/OpenWebUI",
						},
					],
				},
				{
					title: "更多",
					items: [
						{
							label: "发布说明",
							to: "https://github.com/open-webui/open-webui/blob/main/CHANGELOG.md",
						},
						{
							label: "关于",
							to: "https://openwebui.com",
						},
						{
							label: "报告漏洞 / 负责任披露",
							to: "https://github.com/open-webui/open-webui/security",
						},
					],
				},
			],
			// copyright: `Copyright © ${new Date().getFullYear()} OpenWebUI`,
		},
		prism: {
			theme: {
				plain: { color: "#333", backgroundColor: "#f3f3f3" },
				styles: [],
			},
			darkTheme: {
				plain: { color: "#ccc", backgroundColor: "#1a1a1a" },
				styles: [],
			},
		},
	} satisfies Preset.ThemeConfig,
	plugins: [require.resolve("docusaurus-lunr-search")],
};

export default config;
