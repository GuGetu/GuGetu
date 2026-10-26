# -*- coding: utf-8 -*-
"""
把老师的全身像素立绘（scripts/assets/pet-fullbody.png）切成可以独立摆动的部件。

输出到 public/assets/images/pet/：
  pet-body.webp   头 + 上身 + 手臂（不含腿）
  pet-leg-l.webp  左腿（含鞋）
  pet-leg-r.webp  右腿（含鞋）
  pet-face.webp   头部方图（菜单图标、收起后的圆形按钮）

切分点自动检测：找到两腿之间出现背景空隙的那一行作为胯线，
空隙的左右居中位置作为左右腿的分界。
"""
import io
import json
import os

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "scripts", "assets", "pet-fullbody.png")
OUT_DIR = os.path.join(ROOT, "public", "assets", "images", "pet")
os.makedirs(OUT_DIR, exist_ok=True)

BG = (16, 174, 253)          # 立绘的蓝色背景
BG_TOL = 52                  # 蓝色容差
DISPLAY_W = 76               # 页面里的显示宽度（px），导出 2 倍


def keyed():
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    px = img.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    br, bg_, bb = BG
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = max(abs(r - br), abs(g - bg_), abs(b - bb))
            if d <= BG_TOL:
                ap[x, y] = 0
            elif d <= BG_TOL + 40:
                ap[x, y] = int(255 * (d - BG_TOL) / 40)
    # 去蓝边：只处理半透明边缘像素，避免皮鞋/头发边上残留蓝色
    for y in range(h):
        for x in range(w):
            a = ap[x, y]
            if 0 < a < 250:
                r, g, b = px[x, y]
                if b - max(r, g) > 16:
                    ap[x, y] = 0

    alpha = alpha.filter(ImageFilter.MedianFilter(3))
    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out


def find_crotch(im):
    """自上而下找到两腿之间第一次出现背景空隙的行。"""
    w, h = im.size
    a = im.split()[-1].load()
    for y in range(int(h * 0.45), h):
        # 只看中间 1/3 区域，避免两侧空隙干扰
        x0, x1 = int(w * 0.36), int(w * 0.64)
        gap = sum(1 for x in range(x0, x1) if a[x, y] < 40)
        if gap >= 5:
            return y
    return int(h * 0.66)


def gap_center(im, crotch):
    """取腿部中段一行，返回两腿空隙的中心 x。"""
    w, h = im.size
    a = im.split()[-1].load()
    y = min(h - 20, crotch + (h - crotch) // 2)
    x0, x1 = int(w * 0.30), int(w * 0.70)
    gaps = [x for x in range(x0, x1) if a[x, y] < 40]
    if not gaps:
        return w // 2
    return (gaps[0] + gaps[-1]) // 2


def main():
    im = keyed()
    bbox = im.split()[-1].getbbox()
    fig = im.crop(bbox)
    fx, fy = bbox[0], bbox[1]
    fw, fh = fig.size
    print("figure bbox:", bbox, "size:", fig.size)

    crotch = find_crotch(fig)
    split = gap_center(fig, crotch)
    print("crotch y (rel):", crotch, " leg split x (rel):", split)

    overlap = 16                      # 腿的切片向上多留一点，藏到上身后面
    body = fig.crop((0, 0, fw, crotch + overlap))
    leg_l = fig.crop((0, crotch - overlap, split, fh))
    leg_r = fig.crop((split, crotch - overlap, fw, fh))

    s = (DISPLAY_W * 2) / fw          # 导出 2 倍显示尺寸

    def dump(part, name, ox, oy):
        """ox/oy 是这块部件在上身原图里的左上角坐标（原图像素）。"""
        bb = part.split()[-1].getbbox()
        part = part.crop(bb)
        w = max(1, int(round(part.width * s)))
        h = max(1, int(round(part.height * s)))
        res = part.resize((w, h), Image.LANCZOS)
        res.save(os.path.join(OUT_DIR, name + ".webp"), "WEBP", quality=92, method=6)
        disp = DISPLAY_W / fw          # 原图像素 -> 页面像素
        return {"x": round((ox + bb[0]) * disp, 2), "y": round((oy + bb[1]) * disp, 2),
                "w": round(part.width * disp, 2), "h": round(part.height * disp, 2)}

    geo = {
        "figure": {"w": DISPLAY_W, "h": round(fh * DISPLAY_W / fw, 2)},
        "body": dump(body, "pet-body", 0, 0),
        "legL": dump(leg_l, "pet-leg-l", 0, crotch - overlap),
        "legR": dump(leg_r, "pet-leg-r", split, crotch - overlap),
    }

    # 头部方图（菜单 / 收起按钮）
    head_h = int(fw * 0.92)
    head = fig.crop((int(fw * 0.12), 0, int(fw * 0.88), head_h))
    head = head.crop(head.split()[-1].getbbox())
    side = max(head.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(head, ((side - head.width) // 2, (side - head.height) // 2), head)
    canvas = canvas.resize((160, 160), Image.LANCZOS)
    canvas.save(os.path.join(OUT_DIR, "pet-face.webp"), "WEBP", quality=92, method=6)

    print(json.dumps(geo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
