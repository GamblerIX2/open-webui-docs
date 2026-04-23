import React from "react";
import DocItemFooter from "@theme-original/DocItem/Footer";

const DISCLAIMER_TEXT =
	"本内容仅供参考，不构成任何保证、担保或合同承诺。Open WebUI 按“现状”提供。请参阅您的";

export default function DocItemFooterWrapper(props) {
	return (
		<>
			<div className="disclaimer-bar">
				{DISCLAIMER_TEXT}
				<a href="/license">许可协议</a> 以了解适用条款。
			</div>
			<DocItemFooter {...props} />
		</>
	);
}
