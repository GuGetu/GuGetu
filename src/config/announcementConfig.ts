import type { AnnouncementConfig } from "../types/config";

export const announcementConfig: AnnouncementConfig = {
	// 公告标题
	title: "招生公告",

	// 公告内容
	content:
		"诚招优秀本科生和研究生加入课题组！方向覆盖容错计算、故障诊断、网络优化与复杂网络数据挖掘，欢迎 2027 级同学联系 liujiafei@gxnu.edu.cn。",

	// 是否允许用户关闭公告
	closable: true,

	link: {
		// 启用链接
		enable: true,
		// 链接文本
		text: "课题组介绍",
		// 链接 URL
		url: "/team/",
		// 内部链接
		external: false,
	},
};
