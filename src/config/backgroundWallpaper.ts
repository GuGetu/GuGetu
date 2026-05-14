import type { BackgroundWallpaperConfig } from "@/types/config";

export const backgroundWallpaper: BackgroundWallpaperConfig = {
	mode: "fullscreen",
	switchable: false,
	src: {
		desktop: "assets/images/beijingtu.jpg",
		mobile: "assets/images/beijingtu.jpg",
	},
	common: {
		dimOpacity: 0.2,
		homeText: {
			enable: true,
			switchable: false,
			title: "刘佳飞",
			titleSize: "3.5rem",
			subtitle: [
				"博士，副教授 / 硕士生导师",
				"广西师范大学 计算机科学与工程学院",
				"容错计算 · 故障诊断 · 网络优化",
			],
			subtitleSize: "1.4rem",
			typewriter: {
				enable: true,
				speed: 80,
				deleteSpeed: 40,
				pauseTime: 2500,
			},
		},
		navbar: {
			transparentMode: "semi",
			enableBlur: true,
			blur: 5,
		},
		waves: {
			enable: { desktop: true, mobile: true },
			switchable: false,
		},
		gradient: {
			enable: { desktop: true, mobile: true },
			height: "15vh",
			switchable: false,
		},
	},
	banner: {
		position: "0% 20%",
		carousel: {
			enable: false,
			interval: 5000,
			switchable: false,
		},
	},
	overlay: {
		switchable: { opacity: true, blur: true, cardOpacity: true },
		zIndex: -1,
		opacity: 0.8,
		blur: 10,
		cardOpacity: 0.5,
	},
	fullscreen: {
		position: "center",
	},
};
