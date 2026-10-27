# -*- coding: utf-8 -*-
"""
生成课题组成员的头像与封面图（图片内不含任何文字）。

用法：
    python scripts/gen-team-assets.py

规则：
  · 若 src/content/posts/images/students/<拼音>.jpg|jpeg|png 存在 → 用这张真实照片，
    照片会铺满整个画框（cover 裁切），不加渐变色块、不加姓名文字。
  · 若没有照片 → 生成同色系的渐变占位图（人形剪影），同样不含文字，
    所有人名一律由页面上的文字承担，避免图片里的字形出错。
  · 色系按 tags 里的研究方向取色：容错计算=蓝、故障诊断=青、网络优化=紫、
    数据挖掘/复杂网络=橙粉、其他=灰。

输出：
  public/assets/images/students/<拼音>.webp   640x640   头像（名单卡片、侧边栏）
  public/assets/images/covers/<拼音>.webp     1400x538  封面（文章列表、文章页横幅）

新增成员或补上照片后重跑本脚本即可，无需改动其它文件。
"""
import hashlib
import glob
import io
import os
import re

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "src", "content", "posts")
PHOTO_DIR = os.path.join(POSTS, "images", "students")
AVATAR_OUT = os.path.join(ROOT, "public", "assets", "images", "students")
COVER_OUT = os.path.join(ROOT, "public", "assets", "images", "covers")

AVATAR_SIZE = 640
COVER_W, COVER_H = 1400, 788  # 16:9

# 研究方向 -> 渐变配色
PALETTE = {
    "fault": ((37, 99, 235), (79, 70, 229)),    # 容错计算
    "diag": ((13, 148, 136), (5, 150, 105)),    # 故障诊断
    "net": ((124, 58, 237), (168, 85, 247)),    # 网络优化
    "data": ((234, 88, 12), (219, 39, 119)),    # 数据挖掘 / 复杂网络
    "none": ((71, 85, 105), (100, 116, 139)),   # 其他
}

TAG_TO_COLOR = [
    ("容错计算", "fault"),
    ("故障诊断", "diag"),
    ("网络优化", "net"),
    ("网络可靠性", "net"),
    ("数据挖掘", "data"),
    ("复杂网络", "data"),
]

# 每张照片的裁切参数：fx/fy 是 0~1 的重心（0=左/上, 1=右/下），zoom 是放大倍数
# （1.0 = 用满画幅，<1 表示向人物脸部收紧）
PHOTO_CROP = {
    "guocheng": {"cover": {"fx": 0.5, "fy": 0.62, "zoom": 1.0},
                 "avatar": {"fx": 0.5, "fy": 1.0, "zoom": 1.0}},
    "liaofuxing": {"cover": {"fx": 0.5, "fy": 0.55, "zoom": 1.0},
                   "avatar": {"fx": 0.5, "fy": 0.5, "zoom": 1.0}},
    "liangchunjian": {"cover": {"fx": 0.5, "fy": 0.22, "zoom": 1.0},
                      "avatar": {"fx": 0.5, "fy": 0.18, "zoom": 1.0}},
    "chengxinbang": {"cover": {"fx": 0.5, "fy": 0.37, "zoom": 1.0},
                     "avatar": {"fx": 0.5, "fy": 0.5, "zoom": 1.0}},
    # 竖构图、人物偏左：头像收紧缩到脸部，封面保留讲话场景
    "liuwenfei": {"cover": {"fx": 0.5, "fy": 0.07, "zoom": 1.0},
                  "avatar": {"fx": 0.0, "fy": 0.12, "zoom": 0.50}},
    # 漫展合影：他在右边，头像向右收紧对准本人，封面保留两个人
    "xieyanzhen": {"cover": {"fx": 0.5, "fy": 0.0, "zoom": 1.0},
                   "avatar": {"fx": 0.74, "fy": 0.03, "zoom": 0.62}},
}
DEFAULT_COVER_CROP = {"fx": 0.5, "fy": 0.40, "zoom": 1.0}
DEFAULT_AVATAR_CROP = {"fx": 0.5, "fy": 0.35, "zoom": 1.0}

# 这些成员的照片不做任何裁剪：封面按原图比例、头像用模糊背景 + 完整等比放入
NO_CROP = {"xieyanzhen", "lijiaqi"}

PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def read_posts():
    people = []
    # 递归扫描：成员档案按 研究生/2026级 这类分类文件夹存放
    for path in sorted(glob.glob(os.path.join(POSTS, "**", "*.md"), recursive=True)):
        fn = os.path.basename(path)
        if not fn.endswith(".md"):
            continue
        with io.open(path, encoding="utf-8") as f:
            text = f.read()
        m = re.search(r"(?m)^title:\s*(.+?)\s+-\s+(\S.*)$", text)
        if not m:
            continue
        name = m.group(1).strip()
        role = m.group(2).strip()
        tags = re.search(r"(?m)^tags:\s*\[(.+?)\]", text)
        tag_text = tags.group(1) if tags else ""
        key = "none"
        for tag, k in TAG_TO_COLOR:
            if tag in tag_text:
                key = k
                break
        people.append(
            {
                "slug": os.path.splitext(fn)[0],
                "name": name,
                "role": role,
                "color": key,
                "photo": find_photo(os.path.splitext(fn)[0]),
            }
        )
    return people


def find_photo(slug):
    for ext in PHOTO_EXTS:
        p = os.path.join(PHOTO_DIR, slug + ext)
        if os.path.exists(p):
            return p
    return None


def shift_hue(rgb, deg):
    r, g, b = [c / 255.0 for c in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    v = mx
    s = 0 if mx == 0 else (mx - mn) / mx
    if mx == mn:
        h = 0.0
    elif mx == r:
        h = (60 * ((g - b) / (mx - mn))) % 360
    elif mx == g:
        h = 60 * ((b - r) / (mx - mn)) + 120
    else:
        h = 60 * ((r - g) / (mx - mn)) + 240
    h = (h + deg) % 360
    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m_ = v - c
    if h < 60:
        rp, gp, bp = c, x, 0
    elif h < 120:
        rp, gp, bp = x, c, 0
    elif h < 180:
        rp, gp, bp = 0, c, x
    elif h < 240:
        rp, gp, bp = 0, x, c
    elif h < 300:
        rp, gp, bp = x, 0, c
    else:
        rp, gp, bp = c, 0, x
    return tuple(int(round((v_ + m_) * 255)) for v_ in (rp, gp, bp))


def person_hue(name):
    """每个人一个稳定的色相偏移，让没有照片的成员也能靠颜色区分。"""
    h = int(hashlib.md5(name.encode("utf-8")).hexdigest()[:6], 16)
    return (h % 41) - 20


def gradient(size, c1, c2):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line(
            [(0, y), (w, y)],
            fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)),
        )
    return img


def person_mask(size_wh, alpha=255):
    """人形剪影遮罩：头 + 圆润的肩身，整体完整落在画布内。"""
    w, h = size_wh
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    cx = w / 2
    r = min(w, h) * 0.155
    d.ellipse((cx - r, h * 0.205, cx + r, h * 0.515), fill=alpha)          # 头
    d.ellipse((w * 0.19, h * 0.50, w * 0.81, h * 0.985), fill=alpha)       # 肩身
    return m.filter(ImageFilter.GaussianBlur(min(w, h) * 0.008))


def person_glyph(side, alpha):
    """裁到内容边界后的人形图标，返回 RGBA。"""
    mask = person_mask((side, side), 255)
    bbox = mask.point(lambda v: 255 if v > 6 else 0).getbbox()
    if bbox:
        mask = mask.crop(bbox)
    glyph = Image.new("RGBA", mask.size, (255, 255, 255, 255))
    glyph.putalpha(mask.point(lambda v: int(v * alpha)))
    return glyph


def placeholder(size_wh, c1, c2, compact=False):
    """没有照片时用的渐变占位图（无文字）。"""
    w, h = size_wh
    base = gradient((w, h), c1, c2).convert("RGBA")

    deco = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deco)
    dd.ellipse((-w * 0.22, -h * 0.42, w * 0.34, h * 0.58), fill=(255, 255, 255, 24))
    dd.ellipse((w * 0.72, h * 0.5, w * 1.2, h * 1.5), fill=(255, 255, 255, 18))
    if not compact:
        for gy in range(56, h - 28, 30):
            for gx in range(int(w * 0.60), w - 24, 30):
                dd.ellipse((gx, gy, gx + 3, gy + 3), fill=(255, 255, 255, 28))
    base = Image.alpha_composite(base, deco.filter(ImageFilter.GaussianBlur(6)))

    cx, cy = w / 2, h / 2

    if compact:
        # 头像本身就是圆的，直接放人物剪影
        side = int(min(w, h) * 0.62)
        glyph = person_glyph(side, 0.34)
        gx = int(cx - glyph.width / 2)
        gy = int(cy - glyph.height / 2 + min(w, h) * 0.02)
        base.paste(glyph, (gx, gy), glyph)
        return base

    # 封面：中间一个淡淡的圆形徽标，里面是人物剪影
    R = min(w, h) * 0.255
    ring = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(255, 255, 255, 22))
    rd.ellipse(
        (cx - R, cy - R, cx + R, cy + R),
        outline=(255, 255, 255, 62),
        width=max(2, int(R * 0.022)),
    )
    base = Image.alpha_composite(base, ring)

    side = int(R * 1.02)
    glyph = person_glyph(side, 0.32)
    gx = int(cx - glyph.width / 2)
    gy = int(cy - glyph.height / 2 + R * 0.05)
    base.paste(glyph, (gx, gy), glyph)
    return base


def crop_to(img, size_wh, fx=0.5, fy=0.5, zoom=1.0):
    """按 cover 方式裁切到目标比例。

    fx / fy   裁切窗口的重心（0 = 左/上，1 = 右/下）
    zoom      1.0 用满可用画幅；小于 1 表示向画面中心收紧（放大人物）
    """
    tw, th = size_wh
    w, h = img.size
    ratio = tw / th
    if w / h > ratio:
        bw, bh = h * ratio, float(h)
    else:
        bw, bh = float(w), w / ratio
    zoom = max(0.05, min(1.0, zoom))
    bw *= zoom
    bh *= zoom
    bw, bh = int(round(bw)), int(round(bh))
    left = int(round((w - bw) * max(0.0, min(1.0, fx))))
    top = int(round((h - bh) * max(0.0, min(1.0, fy))))
    return img.crop((left, top, left + bw, top + bh)).resize((tw, th), Image.LANCZOS)


def uncropped_cover(im, width=COVER_W, max_h=1400):
    """原图不裁剪：只等比缩放，保持照片原本的比例与全部内容。"""
    w, h = im.size
    if w > width:
        im = im.resize((width, max(1, round(h * width / w))), Image.LANCZOS)
    # 竖构图封顶高度，避免整页被一张超高图撑开
    if im.height > max_h:
        im = im.resize((max(1, round(im.width * max_h / im.height)), max_h), Image.LANCZOS)
    return im


def uncropped_avatar(im, size=AVATAR_SIZE):
    """原图不裁剪地放进方形头像：背景用自身模糊放大填充，前景完整等比放入。"""
    side = size
    # 背景：cover 缩放到方形后模糊压暗
    w, h = im.size
    scale = max(side / w, side / h)
    bg = im.resize((max(side, round(w * scale)), max(side, round(h * scale))), Image.LANCZOS)
    left = (bg.width - side) // 2
    top = (bg.height - side) // 2
    bg = bg.crop((left, top, left + side, top + side))
    bg = bg.filter(ImageFilter.GaussianBlur(side * 0.045))
    bg = Image.eval(bg, lambda v: int(v * 0.62))
    # 前景：contain 等比放入
    fs = min(side / w, side / h)
    fg = im.resize((max(1, round(w * fs)), max(1, round(h * fs))), Image.LANCZOS)
    canvas = bg.convert("RGBA")
    canvas.paste(fg, ((side - fg.width) // 2, (side - fg.height) // 2))
    return canvas


def make_avatar(person):
    c1, c2 = PALETTE[person["color"]]
    hue = person_hue(person["name"])
    c1 = shift_hue(c1, hue)
    c2 = shift_hue(c2, hue)
    size = (AVATAR_SIZE, AVATAR_SIZE)
    if person["photo"]:
        im = Image.open(person["photo"]).convert("RGB")
        if person["slug"] in NO_CROP:
            return uncropped_avatar(im)
        spec = PHOTO_CROP.get(person["slug"], {}).get("avatar", DEFAULT_AVATAR_CROP)
        out = crop_to(im, size, **spec)
        # 圆形
        mask = Image.new("L", (AVATAR_SIZE * 4, AVATAR_SIZE * 4), 0)
        ImageDraw.Draw(mask).ellipse(
            (0, 0, AVATAR_SIZE * 4 - 1, AVATAR_SIZE * 4 - 1), fill=255
        )
        mask = mask.resize(size, Image.LANCZOS)
        rgba = out.convert("RGBA")
        rgba.putalpha(mask)
        return rgba
    # 无照片：圆形渐变 + 人形剪影
    return placeholder(size, c1, c2, compact=True)


def make_cover(person):
    c1, c2 = PALETTE[person["color"]]
    hue = person_hue(person["name"])
    c1 = shift_hue(c1, hue)
    c2 = shift_hue(c2, hue)
    size = (COVER_W, COVER_H)
    if person["photo"]:
        im = Image.open(person["photo"]).convert("RGB")
        if person["slug"] in NO_CROP:
            return uncropped_cover(im).convert("RGBA")
        spec = PHOTO_CROP.get(person["slug"], {}).get("cover", DEFAULT_COVER_CROP)
        return crop_to(im, size, **spec).convert("RGBA")
    return placeholder(size, c1, c2)


def main():
    os.makedirs(AVATAR_OUT, exist_ok=True)
    os.makedirs(COVER_OUT, exist_ok=True)
    people = read_posts()
    with_photo = 0
    for p in people:
        if p["photo"]:
            with_photo += 1
        make_avatar(p).convert("RGB").save(
            os.path.join(AVATAR_OUT, p["slug"] + ".webp"), "WEBP", quality=90, method=6
        )
        make_cover(p).convert("RGB").save(
            os.path.join(COVER_OUT, p["slug"] + ".webp"), "WEBP", quality=86, method=6
        )
    print("成员 %d 人：真实照片 %d 人，渐变占位 %d 人" % (len(people), with_photo, len(people) - with_photo))
    print("头像 ->", AVATAR_OUT)
    print("封面 ->", COVER_OUT)


if __name__ == "__main__":
    main()
