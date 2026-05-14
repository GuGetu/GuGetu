import {
	LinkPreset,
	type NavBarConfig,
	type NavBarLink,
	type NavBarSearchConfig,
	NavBarSearchMethod,
} from "../types/config";

// 根据页面开关动态生成导航栏配置
const getDynamicNavBarConfig = (): NavBarConfig => {
	const links: (NavBarLink | LinkPreset)[] = [
		// 主页
		LinkPreset.Home,

		// 归档（新闻 / 学术动态）
		LinkPreset.Archive,

		// 关于（学术简历）
		LinkPreset.About,
	];

	// 学术相关外链
	links.push({
		name: "学术链接",
		url: "/links/",
		icon: "material-symbols:link",
		children: [
			{
				name: "广西师范大学",
				url: "https://www.gxnu.edu.cn",
				external: true,
				icon: "fa7-solid:school",
			},
			{
				name: "计算机学院",
				url: "http://www.cs.gxnu.edu.cn",
				external: true,
				icon: "material-symbols:computer",
			},
			{
				name: "中国计算机学会",
				url: "https://www.ccf.org.cn",
				external: true,
				icon: "material-symbols:group",
			},
		],
	});

	return { links } as NavBarConfig;
};

// 导航搜索配置
export const navBarSearchConfig: NavBarSearchConfig = {
	method: NavBarSearchMethod.PageFind,
};

export const navBarConfig: NavBarConfig = getDynamicNavBarConfig();
