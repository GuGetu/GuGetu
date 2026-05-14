import {
	LinkPreset,
	type NavBarConfig,
	type NavBarLink,
	type NavBarSearchConfig,
	NavBarSearchMethod,
} from "../types/config";

// 学术主页导航栏配置
const getDynamicNavBarConfig = (): NavBarConfig => {
	const links: (NavBarLink | LinkPreset)[] = [
		// 主页
		LinkPreset.Home,

		// 研究方向
		{
			name: "研究方向",
			url: "/about/",
			icon: "material-symbols:biotech",
		},

		// 归档（论文成果、论文代码、课题组成员、博文归档）
		{
			name: "归档",
			url: "/archive/",
			icon: "material-symbols:archive",
			children: [
				{
					name: "论文成果归档",
					url: "/publications/",
					icon: "material-symbols:description",
				},
				{
					name: "论文代码归档",
					url: "/code/",
					icon: "material-symbols:code",
				},
				{
					name: "课题组成员",
					url: "/team/",
					icon: "material-symbols:group",
				},
				LinkPreset.Archive,
			],
		},

		// 关于
		LinkPreset.About,

		// 友链
		LinkPreset.Friends,

		// 留言板
		LinkPreset.Guestbook,
	];

	return { links } as NavBarConfig;
};

// 导航搜索配置
export const navBarSearchConfig: NavBarSearchConfig = {
	method: NavBarSearchMethod.PageFind,
};

export const navBarConfig: NavBarConfig = getDynamicNavBarConfig();
