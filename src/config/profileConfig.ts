import type { ProfileConfig } from "../types/config";

export const profileConfig: ProfileConfig = {
	// 头像
	avatar: "assets/images/avatar.avif",

	// 名字
	name: "刘佳飞",

	// 个人签名
	bio: "博士，副教授 / 教研室主任、硕士生导师",

	// 链接配置
	links: [
		{
			name: "Email",
			icon: "fa7-solid:envelope",
			url: "mailto:liujiafei@gxnu.edu.cn",
			showName: false,
		},
		{
			name: "广西师范大学",
			icon: "fa7-solid:school",
			url: "http://www.cs.gxnu.edu.cn",
			showName: false,
		},
		{
			name: "RSS",
			icon: "fa7-solid:rss",
			url: "/rss/",
			showName: false,
		},
	],
};
