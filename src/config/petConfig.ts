/**
 * 网页桌宠配置
 *
 * 形象来自老师本人的全身像素立绘（scripts/assets/pet-fullbody.png），
 * 由 scripts/gen_pet_sprite.py 抠底并切成三个可以独立摆动的部件：
 *   pet-body.webp    头 + 上身 + 手臂
 *   pet-leg-l.webp   左腿（含鞋）
 *   pet-leg-r.webp   右腿（含鞋）
 *   pet-face.webp    头部方图（菜单图标、收起后的圆形按钮）
 *
 * 换了新的立绘后，重跑 `python scripts/gen_pet_sprite.py`，
 * 把脚本打印出来的几何数字填到下面的 parts 里即可。
 */

export type TeacherPetConfig = {
	enable: boolean;
	name: string;
	/** 头部图，用于菜单与收起状态 */
	face: string;
	/** 身体部件 */
	parts: {
		body: string;
		legL: string;
		legR: string;
	};
	/** 整体高宽比（高 / 宽） */
	aspect: number;
	/** 两个腿部件相对整体画布的位置与宽度（百分比） */
	legs: {
		left: { x: number; y: number; w: number };
		right: { x: number; y: number; w: number };
	};
	/** 桌面端 / 移动端显示宽度（px） */
	width: number;
	mobileWidth: number;
	/** 跑动速度（px/s） */
	speed: number;
	/** 跑动范围：以落脚点为中心，左右各多少（占视口宽度的比例，0~0.5） */
	range: number;
	zIndex: number;
	/** 进入页面后延迟出现（毫秒） */
	appearDelay: number;
	/** 点击时随机切换的台词 */
	messages: string[];
	greeting: string;
	greetingDuration: number;
	/** 长时间无操作后进入睡眠（毫秒），0 表示不睡 */
	sleepAfter: number;
	/** 夜间自动睡觉的起止小时 */
	nightHours: [number, number];
	sleepMessage: string;
	quickLinks: { label: string; href: string }[];
};

export const teacherPetConfig: TeacherPetConfig = {
	enable: true,
	name: "刘老师",
	face: "/assets/images/pet/pet-face.webp",
	parts: {
		body: "/assets/images/pet/pet-body.webp",
		legL: "/assets/images/pet/pet-leg-l.webp",
		legR: "/assets/images/pet/pet-leg-r.webp",
	},
	// 立绘 300x893（原图像素）→ 显示 76x227.5，高宽比 2.9933
	aspect: 2.9933,
	legs: {
		left: { x: 11.75, y: 65.13, w: 37.25 },
		right: { x: 50.34, y: 65.13, w: 35.91 },
	},
	width: 76,
	mobileWidth: 58,
	speed: 62,
	range: 0.34,
	zIndex: 999,
	appearDelay: 800,
	messages: [
		"你好呀！我是刘老师 👋",
		"欢迎来到课题组主页～",
		"今天也要好好搞科研哦！✨",
		"容错计算 · 故障诊断 · 网络优化 · 复杂网络，四大方向等你来",
		"有问题随时邮件找我：liujiafei@gxnu.edu.cn",
		"最好的输入是输出，多写多思考 ✍️",
		"组会记得带上你的新进展！",
		"累了就休息一下，身体是科研的本钱 🌿",
		"欢迎 2027 级同学加入课题组！🚀",
		"点我一下就好，别一直戳啦 😆",
		"多读好文章，也多发好文章 📄",
		"做研究要有耐心，也要有好奇心 🔍",
		"跑两步活动一下，久坐伤身 🏃",
		"这个实验，要不要再复现一遍？",
	],
	greeting: "你好呀，我是刘老师～ 有事随时叫我！",
	greetingDuration: 4200,
	sleepAfter: 120000,
	nightHours: [23, 7],
	sleepMessage: "Zzz… 有事点我一下 💤",
	quickLinks: [
		{ label: "关于我", href: "/about/" },
		{ label: "论文成果", href: "/publications/" },
		{ label: "课题组成员", href: "/team/" },
		{ label: "友情链接", href: "/friends/" },
	],
};
