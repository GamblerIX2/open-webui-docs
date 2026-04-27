import { useState } from "react";

export const Testimonals = ({
	bannerClassName = "h-18",
	label = true,
	description = true,
	mobile = true,
}) => {
	const items = [
		{
			imgSrc: "https://avatars.githubusercontent.com/u/5860369?v=4",
			url: "https://github.com/Ithanil/",
			name: "Jan Kessler, AI Architect",
			company: "JGU Mainz",
			content:
				"像约翰内斯·古腾堡大学美因茨分校这样的大型高校，在部署自托管 AI 聊天技术栈时，需要既可扩展又能无缝集成的解决方案。作为学校数据中心的 AI 架构师，我选择 Open WebUI 作为我们的聊天前端，因为它开箱即具备面向企业环境的成熟度，同时又保持着高节奏、社区驱动的开发速度。如今，我们这套完全开源的技术栈——由 LLM、代理/负载均衡器和前端组成——已经稳定服务于超过 30,000 名学生和 5,000 名教职员工，并收获了非常积极的反馈。Open WebUI 以用户为中心的设计、丰富的功能集合以及出色的适应性，使它成为我们机构的优秀选择。",
		},
	];

	return (
		<>
			{items.map((item, index) => (
				<div key={index} className="flex items-center gap-6 py-6 text-center">
					<div className="flex shrink-0 basis-1/4 flex-col items-center">
						<a href={item.url} target="_blank" rel="noopener noreferrer">
							<div>
								<img
									src={item.imgSrc}
									alt={item.name}
									className="mb-2 size-20 rounded-full"
								/>
							</div>

							<div className="text-sm font-medium no-underline hover:underline">
								{item.name}
							</div>
							<div className="text-sm font-medium no-underline hover:underline">
								@ {item.company}
							</div>
						</a>
					</div>
					<p className="text-sm italic">{item.content}</p>
				</div>
			))}
		</>
	);
};
