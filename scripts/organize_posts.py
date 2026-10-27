# -*- coding: utf-8 -*-
"""
把 src/content/posts 下的成员档案按「研究生 / 本科生 + 年级」整理进分类文件夹。

规则来自每个文件 frontmatter 的 title：`姓名 - 2026级硕士研究生`
  · 含「硕士研究生」-> 研究生/<年级>级/
  · 含「本科生」    -> 本科生/<年级>级/
  · 没有年级标题的（如 welcome.md）保持不动

文件夹只用于组织内容，URL 由 src/utils/url-utils.ts 的 getPostSlug() 只取文件名，
所以移动文件不会改变任何已有链接。
"""
import io
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "src", "content", "posts")


def classify(title):
    """返回 (分类目录, 年级目录)；无法判断时返回 None。"""
    m = re.match(r"^(?P<grade>\d{4})级(?P<role>.*)$", title.strip())
    if not m:
        return None
    grade = m.group("grade")
    role = m.group("role")
    if "研究生" in role:
        return ("研究生", grade + "级")
    if "本科" in role:
        return ("本科生", grade + "级")
    return None


def main():
    moved = []
    kept = []
    for fn in sorted(os.listdir(POSTS)):
        if not fn.endswith(".md"):
            continue
        src = os.path.join(POSTS, fn)
        with io.open(src, encoding="utf-8") as f:
            head = f.read(1200)
        t = re.search(r"(?m)^title:\s*(.+?)\s+-\s+(\S.*)$", head)
        if not t:
            kept.append((fn, "(无分类)"))
            continue
        target = classify(t.group(2))
        if not target:
            kept.append((fn, "(无分类)"))
            continue
        folder = os.path.join(POSTS, *target)
        os.makedirs(folder, exist_ok=True)
        dst = os.path.join(folder, fn)
        shutil.move(src, dst)
        moved.append((fn, "/".join(target)))

    from collections import Counter

    print("=== 移动统计 ===")
    for k, v in sorted(Counter(m[1] for m in moved).items()):
        print("  %-14s %d 人" % (k, v))
    print("  合计移动 %d 个文件" % len(moved))
    if kept:
        print("=== 未移动 ===")
        for fn, why in kept:
            print("  %-16s %s" % (fn, why))


if __name__ == "__main__":
    main()
