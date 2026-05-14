import type { MusicPlayerConfig } from "../types/config";

// 音乐播放器配置
export const musicPlayerConfig: MusicPlayerConfig = {
    // 是否在导航栏显示音乐播放器入口
    showInNavbar: true,

    // 使用方式："meting" 使用 Meting API，"local" 使用本地音乐列表
    mode: "local",

    // 默认音量 (0-1)
    volume: 0.7,

    // 播放模式：'list'=列表循环, 'one'=单曲循环, 'random'=随机播放
    playMode: "list",

    // 是否显启用歌词
    showLyrics: false,

    // 本地音乐配置
    local: {
        playlist: [
            {
                name: "",
                artist: "",
                url: "/assets/music/music.mp3",
                cover: "/assets/music/cover/109951169585655912.webp",
                lrc: "",
            },
        ],
    },
};
