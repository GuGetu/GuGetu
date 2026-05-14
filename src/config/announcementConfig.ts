import type { AnnouncementConfig } from "../types/config";

export const announcementConfig: AnnouncementConfig = {
	// 公告标题
	title: "招生公告",

	// 公告内容
	content: "诚招优秀本科生和研究生加入课题组！一起从事高性能计算、数据挖掘等领域研究，长期与国内外多所高校保持良好合作。",

	// 是否允许用户关闭公告
	closable: true,

	link: {
		// 启用链接
		enable: true,
		// 链接文本
		text: "了解更多",
		// 链接 URL
		url: "/about/",
		// 内部链接
		external: false,
	},
};
