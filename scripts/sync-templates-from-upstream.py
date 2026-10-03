#!/usr/bin/env python3
"""把技能模板重组为「上游 DESIGN.md 正文 + 保留本地 Notes 头」。

模板格式: `# Design System: <Name>` + Hermes Notes 块 + 上游正文(逐字)。
本脚本从上游克隆重建每个文件，Notes 块原样保留，因此产出可与上游 diff。

用法:
  DESIGN_MD_UPSTREAM=/path/to/awesome-design-md/design-md \
      python3 sync-templates-from-upstream.py [--apply]

不传 --apply 时为 dry-run，只报告会改哪些文件。
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.environ.get("DESIGN_MD_TEMPLATES", os.path.join(HERE, "..", "templates"))
UP = os.environ.get("DESIGN_MD_UPSTREAM",
                    os.path.join(HERE, "..", "..", "..", "awesome-design-md-upstream", "design-md"))
APPLY = "--apply" in sys.argv


def split_upstream(t):
    """返回 (frontmatter, body)；旧格式丢掉首行 h1。"""
    fm = ""
    if t.startswith("---\n"):
        i = t.find("\n---", 4)
        fm, body = t[:i + 4], t[i + 4:].lstrip("\n")
    else:
        body = t
    if body.startswith("# "):
        body = body.split("\n", 1)[1].lstrip("\n")
    return fm, body.rstrip("\n") + "\n"


def notes_of(txt):
    i = txt.find("> **Hermes Agent")
    if i < 0:
        return None
    j = txt.find("> Verify visual accuracy", i)
    if j < 0:
        return None
    return txt[i:txt.find("\n", j) + 1]


def title_of(txt):
    """第一个 '# ' 行。含 frontmatter 时必须先跳过，否则会取到 '---'。"""
    if txt.startswith("---\n"):
        i = txt.find("\n---", 4)
        rest = txt[i + 4:]
    else:
        rest = txt
    for line in rest.splitlines():
        if line.startswith("# "):
            return line
    return None


def main():
    if not os.path.isdir(TPL) or not os.path.isdir(UP):
        sys.exit(f"missing dir: TPL={TPL} UP={UP}")
    changed, skipped, same = [], [], []
    for f in sorted(os.listdir(TPL)):
        if not f.endswith(".md"):
            continue
        slug = f[:-3]
        tpl_path = os.path.join(TPL, f)
        up_path = os.path.join(UP, slug, "DESIGN.md")
        if not os.path.exists(up_path):
            skipped.append((slug, "no upstream entry"))
            continue
        txt = open(tpl_path).read()
        notes = notes_of(txt)
        if notes is None:
            skipped.append((slug, "no Hermes notes block"))
            continue
        title = title_of(txt)
        if title is None:
            skipped.append((slug, "no title line"))
            continue
        fm, body = split_upstream(open(up_path).read())
        new = (fm + "\n" if fm else "") + title + "\n\n\n" + notes + "\n" + body
        if new == txt:
            same.append(slug)
        else:
            changed.append((slug, len(txt), len(new), "fm" if fm else "--"))
            if APPLY:
                open(tpl_path, "w").write(new)
    print(f"mode={'APPLY' if APPLY else 'DRY-RUN'}")
    print(f"identical: {len(same)}  would-change: {len(changed)}  skipped: {len(skipped)}")
    for s, a, b, tag in changed:
        print(f"  {s:16s} {tag} {a:6d} -> {b:6d} bytes")
    for s, why in skipped:
        print(f"  SKIP {s}: {why}")


if __name__ == "__main__":
    main()
