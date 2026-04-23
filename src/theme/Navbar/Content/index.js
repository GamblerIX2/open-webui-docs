import React from "react";
import Content from "@theme-original/Navbar/Content";
export default function ContentWrapper(props) {
    return (<>
			<div className="flex h-full w-full items-center">
				<div className="flex w-full flex-col">
					<div>
						<Content {...props}/>
					</div>
				</div>
			</div>
		</>);
}
