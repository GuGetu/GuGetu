import type { FriendLink, FriendsPageConfig } from "../types/config";

// 可以在src/content/spec/friends.md中编写友链页面下方的自定义内容

// 友链页面配置
export const friendsPageConfig: FriendsPageConfig = {
	// 页面标题，如果留空则使用 i18n 中的翻译
	title: "",

	// 页面描述文本，如果留空则使用 i18n 中的翻译
	description: "",

	// 是否显示底部自定义内容（friends.mdx 中的内容）
	showCustomContent: true,

	// 是否显示评论区，需要先在commentConfig.ts启用评论系统
	showComment: true,

	// 是否开启随机排序配置，如果开启，就会忽略权重，构建时进行一次随机排序
	randomizeSort: false,
};

// 友链配置
export const friendsConfig: FriendLink[] = [
	{
		title: "周书明 · 福建师范大学",
		imgurl: "/assets/images/friends/zhoushuming.webp",
		desc: "福建师范大学数学与统计学院教授、博士生导师，图论与理论计算机科学、网络容错与故障诊断方向专家。",
		siteurl: "https://math.fjnu.edu.cn/6f/14/c15118a290580/page.htm",
		tags: ["导师", "高校学者", "容错计算", "图论"],
		weight: 100,
		enabled: true,
	},
];

export const getEnabledFriends = (): FriendLink[] => {
	return friendsConfig.filter((f) => f.enabled);
};
