#!/usr/bin/env python3
"""Print numbered sections of DECISIONS.md or ENGINE.md instead of the whole file.
py tools/sec.py DECISIONS|ENGINE [nums or ranges, e.g. 9 16 7-11]"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Both files number their sections, but not at a consistent heading level: ENGINE.md
# opens with "## 1." and then switches to "# 2.". Match the number, not the depth.
HEADING = re.compile(r"^(#{1,6})\s+(\d+)\.\s*(.*?)\s*$")


def resolve(name):
    stem = name.removesuffix(".md").upper()
    path = ROOT / f"{stem}.md"
    if not path.is_file():
        sys.exit(f"sec: no such document: {path.name}")
    return path


def sections(path):
    """[(number, title, start_line, end_line)], 1-based inclusive; a section runs to
    the next numbered heading, so an unnumbered sub-heading stays with it."""
    lines = path.read_text(encoding="utf-8").splitlines()
    found = []
    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if m:
            found.append((int(m.group(2)), m.group(3), i))
    out = []
    for n, (num, title, start) in enumerate(found):
        end = found[n + 1][2] if n + 1 < len(found) else len(lines)
        out.append((num, title, start + 1, end))
    return lines, out


def expand(args):
    wanted = []
    for arg in args:
        if "-" in arg[1:]:
            lo, _, hi = arg.partition("-")
            try:
                wanted.extend(range(int(lo), int(hi) + 1))
            except ValueError:
                sys.exit(f"sec: not a section range: {arg}")
        else:
            try:
                wanted.append(int(arg))
            except ValueError:
                sys.exit(f"sec: not a section number: {arg}")
    return wanted


def main(argv):
    # Windows' cp1252 stdout can't encode the arrows/em dashes these documents use,
    # raising UnicodeEncodeError mid-section after the header already printed.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    if not argv:
        sys.exit(__doc__)
    path = resolve(argv[0])
    lines, found = sections(path)

    if len(argv) == 1:
        print(f"{path.name} - {len(found)} sections, {len(lines)} lines")
        for num, title, start, end in found:
            print(f"  {num:>3}. {title}  ({end - start + 1} lines)")
        return 0

    by_num = {num: (title, start, end) for num, title, start, end in found}
    status = 0
    for num in expand(argv[1:]):
        if num not in by_num:
            print(f"sec: {path.name} has no section {num}", file=sys.stderr)
            status = 1
            continue
        _, start, end = by_num[num]
        print(f"===== {path.name} §{num}  (lines {start}-{end}) =====")
        print("\n".join(lines[start - 1 : end]).rstrip())
        print()
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
