"""Fail on any comment block longer than 2 lines, or any comment carrying a date. Usage: py tools/comment_cap.py [--staged] [paths...]"""
import ast
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

CAP = 2
ROOT = Path(__file__).resolve().parent.parent
C_LIKE = {".cpp", ".hpp", ".h", ".c", ".slang", ".js", ".mjs", ".ts", ".glsl", ".wgsl"}
DATE = re.compile(r"\b(19|20)\d\d-\d\d\b")
DIRECTIVE = re.compile(r"clang-format|NOLINT|NOSONAR|noqa|type:|pragma|pylint:")


def lex_c(text):
    """Returns (code with comments removed, per-line [has_code, comment_text])."""
    lines = [[False, ""] for _ in range(text.count("\n") + 1)]
    out, i, ln, n = [], 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == "\n":
            ln += 1; out.append(c); i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            lines[ln][1] += text[i:j]; i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k, part in enumerate(text[i:j].split("\n")):
                lines[ln + k][1] += part
            ln += text.count("\n", i, j); out.append("\n" * text.count("\n", i, j)); i = j
        elif c == "R" and text.startswith('R"', i) and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")):
            p = text.find("(", i)
            end = ")" + text[i + 2:p] + '"'
            j = text.find(end, p)
            j = n if j < 0 else j + len(end)
            for k in range(text.count("\n", i, j) + 1):
                lines[ln + k][0] = True
            ln += text.count("\n", i, j); out.append(text[i:j]); i = j
        elif c in "\"'" and not (c == "'" and i > 0 and text[i - 1].isalnum() and i + 1 < n and text[i + 1].isalnum()):
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            j = min(j + 1, n)
            lines[ln][0] = True; out.append(text[i:j]); i = j
        else:
            if not c.isspace():
                lines[ln][0] = True
            out.append(c); i += 1
    return "".join(out), lines


def lex_py(text):
    lines = [[False, ""] for _ in range(text.count("\n") + 1)]
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.COMMENT:
            lines[tok.start[0] - 1][1] += tok.string
        elif tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
            for r in range(tok.start[0], tok.end[0] + 1):
                lines[r - 1][0] = True
    for node in ast.walk(ast.parse(text)):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) \
                and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
            for r in range(body[0].lineno, body[0].end_lineno + 1):
                lines[r - 1] = [False, "docstring"]
    if lines and lines[0][1].startswith("#!"):
        lines[0][1] = ""
    return lines


def lex_cmake(text):
    lines = []
    for raw in text.split("\n"):
        s = raw.strip()
        lines.append([bool(s) and not s.startswith("#"), s if s.startswith("#") else ""])
    return lines


def lex(path, text):
    if path.suffix in C_LIKE:
        return lex_c(text)[1]
    if path.suffix == ".py":
        return lex_py(text)
    return lex_cmake(text)


def blocks(lines):
    """Consecutive comment-only lines, blank lines included, form one block; a trailing comment starts one."""
    start, size = None, 0
    for i, (code, comment) in enumerate(lines):
        if comment and DIRECTIVE.search(comment) and len(comment) < 60:
            comment = ""
        if not code and comment:
            if size == 0:
                start = i
            size += 1
        elif code:
            if size > CAP:
                yield start, size
            start, size = (i, 1) if comment else (None, 0)
    if size > CAP:
        yield start, size


def wanted(p):
    return p.suffix in C_LIKE | {".py", ".cmake"} or p.name == "CMakeLists.txt"


def main(argv):
    staged = "--staged" in argv
    args = [a for a in argv if a != "--staged"]
    if args:
        files = [Path(a) for a in args]
    else:
        cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged else ["git", "ls-files"]
        files = [Path(f) for f in subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()]
    bad = 0
    for rel in filter(wanted, files):
        path = rel if rel.is_absolute() else ROOT / rel
        if staged:
            text = subprocess.run(["git", "show", f":{rel.as_posix()}"], cwd=ROOT, capture_output=True,
                                  encoding="utf-8", check=True).stdout
        elif path.exists():
            text = path.read_text(encoding="utf-8")
        else:
            continue
        lines = lex(path, text)
        for i, (_, comment) in enumerate(lines):
            if DATE.search(comment):
                print(f"{rel.as_posix()}:{i + 1}: a date in a comment")
                bad += 1
        for start, size in blocks(lines):
            print(f"{rel.as_posix()}:{start + 1}: {size}-line comment block (cap {CAP})")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
