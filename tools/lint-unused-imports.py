#!/usr/bin/env python3
"""FP-safe static unused-import gate for grc_library tooling (Fable-planned, #1698 follow-up).

WHY THIS EXISTS. PRs #1697/#1698 removed unused imports by hand; #1698's AST pass
initially over-removed three DELIBERATE back-compat re-exports in `residual-scan.py`
(`FROZEN_RECORD_RE`, `LEDGER_PATHS`, `LEDGER_RE`), which a codex `/validate-pr` HOLD caught
and restored. This tool detects the recurrence CLASS, but is built so it can NEVER repeat
that over-removal: it is deliberately ASYMMETRIC (false negatives acceptable, false
positives are not). It shipped report-only (#1702), soaked to an empty report (#1703 removed the
last five findings), and now runs as ENFORCING gate 94 (exit 1 on findings by default; --report is
the advisory opt-out), wired into the four gate surfaces.

SCOPE. `tools/*.py` and `.claude/hooks/*.py` only (`tests/`, `.web/`, corpus are non-goals).

VERDICT. A name is flagged ONLY when a semantic (AST) pass finds no Load reference AND a
conservative textual backstop finds no bare token AND no exclusion applies. Every ambiguity
resolves to DO NOT FLAG.

EXCLUSIONS (each with its detection mechanism):
  1. `from __future__ import ...`     -> never a candidate (excluded at collection).
  2. names in a module `__all__`      -> re-export by declaration; if `__all__` is present but
                                         not statically a literal list/tuple of str, the WHOLE
                                         FILE is SKIPped (ignorance refuses to flag).
  3. the #1250 back-compat re-export  -> an inline `# re-export` marker on the import statement
                                         (head line = statement-wide) or on an alias's own
                                         continuation line (that alias only). A bare
                                         imported-but-unused name is statically indistinguishable
                                         from a re-export, so the marker is the control; residue
                                         stated: a marker-less future re-export reads as dead.
  4. `# noqa: F401` / bare `# noqa`    -> exempt (unused-import suppression). A `# noqa: E402`
                                         that does NOT list F401 is NOT exempt (E402 suppresses an
                                         import-POSITION complaint, not an unused one; it is the
                                         single most common import shape here, `from lint_common
                                         import ... # noqa: E402`, and treating it as exempting
                                         would blind the gate).
  5. `if TYPE_CHECKING:` imports       -> exempt (annotation-only; usage undetectable in general).
  6. star imports (`from x import *`)  -> SKIP the whole file (namespace unresolvable).
  7. imports in a `try` BODY          -> exempt (the try/except-ImportError fallback idiom; ANY
                                         try-body import is treated as a probe regardless of the
                                         handler, covering aliased/broad exceptions and `except*`).
  8. conditional / function-local      -> NOT class-exempt: flagged, but usage is checked
                                         FILE-WIDE (scope-blind), so a locally-imported name used
                                         anywhere in the file is never flagged.

RESIDUES (stated so nobody trusts the gate past its reach): a marker-less deliberate re-export is
indistinguishable from dead code; a name used only via `getattr`/`globals()` is invisible unless a
string literal names it; a name mentioned only in a comment or docstring suppresses a real finding
(the accepted false-negative direction, the PR #1697 shape); a file that does not PARSE is SKIPped whole (printed as a SKIP line, not a finding), so gate 94 does not syntax-check the toolchain (that coverage for `.claude/hooks/` is a separate routed gap).

Usage:
    python3 tools/lint-unused-imports.py                 # ENFORCE (default): exit 1 on any finding (gate 94)
    python3 tools/lint-unused-imports.py --report        # report-only opt-out: print worklist, exit 0
    python3 tools/lint-unused-imports.py --ignore-markers # debug: ignore `# re-export` markers (control)
    python3 tools/lint-unused-imports.py --paths a.py b.py   # explicit files (default: the two dirs)
    python3 tools/lint-unused-imports.py --self-test
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIRS = ("tools", ".claude/hooks")
_MARKER_RE = re.compile(r"#\s*re-export", re.IGNORECASE)
_NOQA_RE = re.compile(r"#\s*noqa(?::\s*(?P<codes>[A-Z0-9,\t ]+))?", re.IGNORECASE)


class Finding:
    __slots__ = ("path", "lineno", "name", "statement")

    def __init__(self, path: str, lineno: int, name: str, statement: str):
        self.path = path
        self.lineno = lineno
        self.name = name
        self.statement = statement

    def render(self) -> str:
        return f"{self.path}:{self.lineno}: unused import {self.name!r} ({self.statement})"


class Binding:
    __slots__ = ("name", "lineno", "end_lineno", "alias_line", "type_checking", "import_error")

    def __init__(self, name, lineno, end_lineno, alias_line, type_checking, import_error):
        self.name = name
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.alias_line = alias_line
        self.type_checking = type_checking
        self.import_error = import_error


def collect(tree: ast.AST):
    """Return (bindings, has_star, all_names_or_None, unresolved_all).

    all_names is the set of `__all__` string entries; unresolved_all is True if an `__all__`
    statement exists but is not a static literal list/tuple of strings (=> caller SKIPs the file).
    """
    bindings: list[Binding] = []
    has_star = False
    all_names: set[str] = set()
    unresolved_all = False

    # Names bound to typing.TYPE_CHECKING, including aliases (`from typing import
    # TYPE_CHECKING as TC`), so `if TC:` is recognized as a type-only guard. Collected
    # in a pre-pass because a guard may be written before or after the import statement.
    tc_aliases = {"TYPE_CHECKING"}
    for _n in ast.walk(tree):
        if isinstance(_n, ast.ImportFrom):
            for _alias in _n.names:
                if _alias.name == "TYPE_CHECKING":
                    tc_aliases.add(_alias.asname or "TYPE_CHECKING")
        # A dynamic `__all__` mutation/access (`__all__.append(...)`, `.extend(...)`,
        # `__all__[i] = ...`) is not a static literal assign, so the membership set is
        # unresolvable; skip the file rather than risk flagging a name it re-exports.
        elif isinstance(_n, ast.Attribute) and isinstance(_n.value, ast.Name) and _n.value.id == "__all__":
            unresolved_all = True
        elif isinstance(_n, ast.Subscript) and isinstance(_n.value, ast.Name) and _n.value.id == "__all__":
            unresolved_all = True

    def visit(node, type_checking, import_error):
        nonlocal has_star, unresolved_all
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.Import):
                for alias in child.names:
                    bound = alias.asname or alias.name.split(".")[0]
                    bindings.append(Binding(bound, child.lineno, child.end_lineno or child.lineno,
                                            alias.lineno if hasattr(alias, "lineno") else child.lineno,
                                            type_checking, import_error))
            elif isinstance(child, ast.ImportFrom):
                if child.module == "__future__":
                    continue
                for alias in child.names:
                    if alias.name == "*":
                        has_star = True
                        continue
                    bound = alias.asname or alias.name
                    bindings.append(Binding(bound, child.lineno, child.end_lineno or child.lineno,
                                            alias.lineno if hasattr(alias, "lineno") else child.lineno,
                                            type_checking, import_error))
            elif isinstance(child, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                if any(isinstance(t, ast.Name) and t.id == "__all__" for t in targets):
                    val = child.value
                    if isinstance(val, (ast.List, ast.Tuple)) and all(
                        isinstance(e, ast.Constant) and isinstance(e.value, str) for e in val.elts
                    ):
                        all_names.update(e.value for e in val.elts)
                    else:
                        unresolved_all = True
                # recurse into value anyway (harmless)
                visit(child, type_checking, import_error)
            elif isinstance(child, ast.If):
                # TYPE_CHECKING may appear compounded (`if TYPE_CHECKING and FEATURE:`),
                # so walk the whole test rather than matching only a bare name/attribute.
                is_tc = any(
                    (isinstance(n, ast.Name) and n.id in tc_aliases)
                    or (isinstance(n, ast.Attribute) and n.attr == "TYPE_CHECKING")
                    for n in ast.walk(child.test)
                )
                visit(child, type_checking or is_tc, import_error)
            elif isinstance(child, (ast.Try, ast.TryStar)):
                # Any import in a try BODY is treated as a probe (the try/except-ImportError
                # fallback idiom), regardless of the handler's exception type. This is the
                # conservative choice: it covers ImportError, ModuleNotFoundError, aliased or
                # qualified exception names, broad `except Exception`, and `except*` (TryStar),
                # without having to resolve exception identity. The false-negative cost (a
                # genuinely dead import sitting in a try body) is accepted.
                for sub in child.body:
                    visit_stmt(sub, type_checking, True)
                for h in child.handlers:
                    visit(h, type_checking, import_error)
                for sub in child.orelse + child.finalbody:
                    visit_stmt(sub, type_checking, import_error)
            else:
                visit(child, type_checking, import_error)

    def visit_stmt(stmt, type_checking, import_error):
        # wrap a single statement so it is processed like a child of a synthetic parent
        holder = ast.Module(body=[stmt], type_ignores=[])
        visit(holder, type_checking, import_error)

    visit(tree, False, False)
    return bindings, has_star, all_names, unresolved_all


def collect_references(tree: ast.AST) -> set[str]:
    refs: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            refs.add(node.id)
        elif isinstance(node, ast.Attribute):
            # covered by the Name of the root, but harmless to be explicit for `a.b.c`
            pass
    # string (forward-ref) annotations
    for node in ast.walk(tree):
        ann = None
        if isinstance(node, ast.AnnAssign):
            ann = node.annotation
        elif isinstance(node, ast.arg):
            ann = node.annotation
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ann = node.returns
        if isinstance(ann, ast.Constant) and isinstance(ann.value, str):
            try:
                sub = ast.parse(ann.value, mode="eval")
                for n in ast.walk(sub):
                    if isinstance(n, ast.Name):
                        refs.add(n.id)
            except SyntaxError:
                pass
    return refs


def _statement_lines(lines: list[str], lineno: int, end_lineno: int) -> list[str]:
    return lines[lineno - 1 : end_lineno]


def _has_marker(lines: list[str], binding: Binding) -> bool:
    head = lines[binding.lineno - 1]
    if _MARKER_RE.search(head):
        return True
    if 0 < binding.alias_line <= len(lines):
        if _MARKER_RE.search(lines[binding.alias_line - 1]):
            return True
    return False


def _noqa_exempts_unused(lines: list[str], binding: Binding) -> bool:
    for raw in _statement_lines(lines, binding.lineno, binding.end_lineno):
        m = _NOQA_RE.search(raw)
        if not m:
            continue
        codes = m.group("codes")
        if codes is None:
            return True  # bare `# noqa`
        code_set = {c.strip().upper() for c in re.split(r"[,\s]+", codes) if c.strip()}
        if "F401" in code_set:
            return True
    return False


def layer2_used(name: str, source: str, spans: list[tuple[int, int]]) -> bool:
    lines = source.splitlines()
    kept = []
    blanked = set()
    for lo, hi in spans:
        for ln in range(lo, hi + 1):
            blanked.add(ln)
    for i, line in enumerate(lines, start=1):
        if i in blanked:
            continue
        kept.append(line)
    text = "\n".join(kept)
    return re.search(r"\b" + re.escape(name) + r"\b", text) is not None


def scan_file(path: Path, *, ignore_markers: bool = False):
    """Return (findings, skip_reason_or_None)."""
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [], f"syntax error: {e}"
    bindings, has_star, all_names, unresolved_all = collect(tree)
    if has_star:
        return [], "star import"
    if unresolved_all:
        return [], "dynamic __all__"
    refs = collect_references(tree)
    lines = source.splitlines()
    spans = [(b.lineno, b.end_lineno) for b in bindings]
    rel = str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path)
    findings = []
    for b in bindings:
        if b.type_checking or b.import_error:
            continue
        if b.name in all_names:
            continue
        if b.name in refs:
            continue
        if not ignore_markers and _has_marker(lines, b):
            continue
        if _noqa_exempts_unused(lines, b):
            continue
        if layer2_used(b.name, source, spans):
            continue
        stmt = lines[b.lineno - 1].strip()
        findings.append(Finding(rel, b.lineno, b.name, stmt))
    return findings, None


def iter_targets(paths):
    if paths:
        for p in paths:
            yield Path(p).resolve()
        return
    for d in DEFAULT_DIRS:
        base = REPO_ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.glob("*.py")):
            yield p


def run(paths=None, *, enforce=False, ignore_markers=False, out=sys.stdout):
    all_findings = []
    skips = []
    for target in iter_targets(paths):
        findings, skip = scan_file(target, ignore_markers=ignore_markers)
        if skip:
            rel = str(target.relative_to(REPO_ROOT)) if target.is_relative_to(REPO_ROOT) else str(target)
            skips.append((rel, skip))
        all_findings.extend(findings)
    banner = "" if enforce else "REPORT-ONLY (opt-out; the wired gate enforces). "
    for f in all_findings:
        print(f.render(), file=out)
    for path, reason in skips:
        print(f"SKIP {path}: {reason}", file=out)
    print(f"{banner}{len(all_findings)} unused-import finding(s), {len(skips)} file(s) skipped.", file=out)
    if enforce and all_findings:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Self-test (stdlib-only, tmp fixtures)
# ---------------------------------------------------------------------------
def _self_test() -> int:
    import tempfile
    import textwrap

    cases = []

    def check(desc, src, *, expect_names, ignore_markers=False):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "m.py"
            p.write_text(textwrap.dedent(src), encoding="utf-8")
            findings, skip = scan_file(p, ignore_markers=ignore_markers)
            got = sorted(f.name for f in findings)
            ok = got == sorted(expect_names) and skip is None
            cases.append((desc, ok, f"expected {sorted(expect_names)}, got {got}, skip={skip}"))

    def check_skip(desc, src, *, expect_skip_substr):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "m.py"
            p.write_text(textwrap.dedent(src), encoding="utf-8")
            findings, skip = scan_file(p)
            ok = skip is not None and expect_skip_substr in skip and not findings
            cases.append((desc, ok, f"expected skip~{expect_skip_substr!r}, got skip={skip}, findings={[f.name for f in findings]}"))

    # positives
    check("module-level unused", "import os\nx = 1\n", expect_names=["os"])
    check("alias unused", "from pathlib import Path as P\nx = 1\n", expect_names=["P"])
    check("function-local unused", "def f():\n    import json\n    return 1\n", expect_names=["json"])
    check("marker positive control (ignore-markers flags it)",
          "from a import b  # re-export\nx = 1\n", expect_names=["b"], ignore_markers=True)
    # negatives
    check("used module-level", "import os\nprint(os.getcwd())\n", expect_names=[])
    check("__all__ re-export", "from a import y\n__all__ = ['y']\n", expect_names=[])
    check("re-export marker (statement)", "from a import b  # re-export\nx = 1\n", expect_names=[])
    check("re-export marker (per-alias continuation)",
          "from a import (\n    b,  # re-export: back-compat\n)\nx = 1\n", expect_names=[])
    check("noqa F401", "import os  # noqa: F401\nx = 1\n", expect_names=[])
    check("bare noqa", "import os  # noqa\nx = 1\n", expect_names=[])
    check("noqa E402 only, used -> not flagged (used)", "import os  # noqa: E402\nprint(os)\n", expect_names=[])
    check("noqa E402 only, unused -> STILL flagged", "import os  # noqa: E402\nx = 1\n", expect_names=["os"])
    check("TYPE_CHECKING import (exempt purely by the TC block, used nowhere)",
          "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from a import T\nx = 1\n",
          expect_names=[])
    check("compound TYPE_CHECKING (if TYPE_CHECKING and FEATURE)",
          "from typing import TYPE_CHECKING\nFEATURE = True\nif TYPE_CHECKING and FEATURE:\n    from a import T\nx = 1\n",
          expect_names=[])
    check("string annotation forward-ref exempts a module-level import (no TYPE_CHECKING)",
          "from a import T\ndef f(x: 'T'):\n    return x\n", expect_names=[])
    check("submodule import a.b used as a.b.c",
          "import os.path\nprint(os.path.join('a', 'b'))\n", expect_names=[])
    check("try/except ImportError probe (fallback does NOT reuse the name)",
          "try:\n    import ujson\nexcept ImportError:\n    pass\nx = 1\n", expect_names=[])
    check("try/except Exception (broad) probe",
          "try:\n    import ujson\nexcept Exception:\n    pass\nx = 1\n", expect_names=[])
    check("try/except qualified ImportError probe",
          "import builtins\ntry:\n    import ujson\nexcept builtins.ImportError:\n    pass\nprint(builtins)\n",
          expect_names=[])
    check("noqa F401 whitespace-separated code list",
          "import os  # noqa: F401 E402\nx = 1\n", expect_names=[])
    check("noqa F401 TAB-separated code list",
          "import os  # noqa: E402\tF401\nx = 1\n", expect_names=[])
    check("TYPE_CHECKING alias (imported as TC)",
          "from typing import TYPE_CHECKING as TC\nif TC:\n    from a import T\nx = 1\n", expect_names=[])
    check("except* ImportError probe (TryStar, blanket try-body exemption)",
          "try:\n    import ujson\nexcept* ImportError:\n    pass\nx = 1\n", expect_names=[])
    check("qualified except in try body (blanket exemption)",
          "import builtins\ntry:\n    import ujson\nexcept builtins.ImportError:\n    pass\nprint(builtins)\n",
          expect_names=[])
    check("future import never flagged", "from __future__ import annotations\nimport os\nprint(os)\n", expect_names=[])
    check("comment mention suppresses (accepted FN)", "import os\n# os is used elsewhere\nx = 1\n", expect_names=[])
    check_skip("star import skips file", "from a import *\nimport os\nx = 1\n", expect_skip_substr="star import")
    check_skip("dynamic __all__ (call) skips file", "import os\n__all__ = sorted(['os'])\n", expect_skip_substr="dynamic __all__")
    check_skip("annotated dynamic __all__ skips file",
               "from p import Public\n__all__: list = make_exports()\n", expect_skip_substr="dynamic __all__")
    check_skip("__all__.extend mutation skips file",
               "from p import Public\n__all__ = []\n__all__.extend(['Public'])\n", expect_skip_substr="dynamic __all__")
    check_skip("__all__.append mutation skips file",
               "from p import Public\n__all__ = []\n__all__.append('Public')\n", expect_skip_substr="dynamic __all__")

    # Direct collector assertions (discriminating): layer 2 also silences `__all__` names via the
    # string literal, so scan_file alone cannot isolate the `__all__` mechanism; assert it directly.
    _b, _star, _alln, _unres = collect(ast.parse("from a import y\n__all__ = ['y']\n"))
    cases.append(("__all__ collector captures static membership", "y" in _alln and not _unres,
                  f"all_names={_alln}, unresolved={_unres}"))
    _b2, _s2, _a2, _unres2 = collect(ast.parse("from p import Public\n__all__: list = make_exports()\n"))
    cases.append(("annotated dynamic __all__ marks unresolved", _unres2 is True, f"unresolved={_unres2}"))

    passed = sum(1 for _, ok, _ in cases if ok)
    for desc, ok, detail in cases:
        if not ok:
            print(f"FAIL: {desc}: {detail}", file=sys.stderr)
    print(f"self-test: {passed}/{len(cases)} passed", file=sys.stderr)
    return 0 if passed == len(cases) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="FP-safe static unused-import gate (enforce-mode default).")
    ap.add_argument("--enforce", action="store_true",
                    help="exit 1 on any finding (the default; kept as the explicit gate-invocation form)")
    ap.add_argument("--report", action="store_true",
                    help="report-only opt-out: print the worklist and exit 0")
    ap.add_argument("--ignore-markers", action="store_true", help="debug/control: ignore `# re-export` markers")
    ap.add_argument("--paths", nargs="+", help="explicit files to scan (default: tools/ + .claude/hooks/)")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return _self_test()
    enforce = not args.report
    return run(args.paths, enforce=enforce, ignore_markers=args.ignore_markers)


if __name__ == "__main__":
    raise SystemExit(main())
