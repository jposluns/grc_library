#!/usr/bin/env python3
"""Gate blind-spot map: which repo surfaces does each audit gate scan, and which
markdown surfaces does NO gate scan.

WHAT THIS IS (and is NOT). This is an orchestrator dev-AID for the deep-assessment
skill's audit-programme phase, not an audit gate. It always exits 0 after printing
its report (2 on an internal or usage error, an empty or missing --root,
or a refused runner entry); its output is a coverage report, not a
defect list. It derives, per gate wired into ``tools/run_all_audits.sh``, the
gate's effective scan scope by static inspection of the gate's module source, then
inverts the union: the markdown files no scope-derivable gate scans at all. Every
fully-unscanned surface is a candidate for the deep-assessment run's manual review
list.

Scope-derivation classes, reported separately so an inferred scope is never shown
as a measured one:

- ``common-discovery``: the module uses the shared ``lint_common`` discovery
  helpers (``iter_targets`` / ``iter_markdown_targets`` / ``is_target`` /
  ``is_markdown_target``) or references ``DEFAULT_EXEMPT_DIRS``. Its scope is
  approximated as: all tracked ``.md`` files, minus the shared exempt dirs, minus
  the module's own statically-collected exemption constants (module-level names
  containing ``EXEMPT``, holding strings or collections of strings, interpreted
  as path prefixes or exact relative paths).
- ``target-scoped``: no common-discovery signal, but the module carries
  module-level path-shaped constants (names containing ``TARGET`` / ``FILE`` /
  ``PATH`` / ``SURFACE`` / ``DIR`` / ``ROOT`` / ``SCAN``); its scope is those
  explicit paths, further filtered to path-shaped values (containing ``/`` or
  ending ``.md`` / ``.yml`` / ``.yaml`` / ``.py`` / ``.sh``).
- ``not-derivable``: neither signal. The gate is listed and excluded from the
  coverage inversion, and the report says so.

Runner entries: a line that holds the word ``run_gate`` and is neither a comment nor
the ``run_gate() {`` definition must be, from column 0,
``run_gate "LABEL" python3 [-I] tools/X.py [plain arguments]`` (gate 35's closed
allowlist, the same patterns); any other shape is a refused runner entry. The
allowlist does not cover runner shell code outside run_gate lines (the function
body, a redefinition of python3 or run_gate, PATH or BASH_ENV, and whether bash
reaches a run_gate line inside a conditional, heredoc, loop or backslash
continuation), which python3 is found on PATH, or what a gate script does. This map
reads no YAML: gate 35 alone checks the workflow and pre-commit gate surfaces against
the fixed skeleton of each file (3b646 round 6: only the keys the current files use at
each level, each nested value two columns deeper than its key, no repeated key, no
quoted value, and a gate hook's run-deciding key pinned to the values the gate hooks
use), and that gate's module docstring states their residuals: the values of the
excluded steps and hooks, the values the skeletons leave free (the workflow and job
names and the step and hook names and ids), YAML a real reader takes differently in ways
those rules do not exclude (the check does not validate YAML), and whether GitHub
Actions or pre-commit runs at all.

Honest limits: static inspection cannot see dynamically-computed scopes, so both
the per-gate scope and the unscanned-file list are APPROXIMATE by construction.
The report's purpose is triage (where to point manual review), never proof of
coverage; a file listed as unscanned may be reached by a not-derivable gate, and
the adjudication belongs to the deep-assessment run.

Usage:
    python3 tools/audit-gate-blindspots.py [--root PATH] [--format md|tsv]
    python3 tools/audit-gate-blindspots.py --unscanned-only

Stdlib-only Python 3.11. This script requires the adjacent lint_common.py
module for shared path-containment checks. The runner and the lint_common.py
source inspected under ``--root`` must resolve within that root.
This point-in-time check cannot stop a symlink swapped after resolution or a hard-link alias.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from lint_common import PathContainmentError, is_containment_refusal, join_under  # noqa: E402

TOOL_ROOT = Path(__file__).resolve().parent.parent

# Runner lines are matched against gate 35's closed allowlist (3b646 round 4, maintainer
# option A), with the same pattern strings (a test keeps them equal): every line that is
# not a comment and holds the word run_gate is the `run_gate() {` definition or, from
# column 0, `run_gate "LABEL" python3 [-I] tools/X.py [plain arguments]`. Anything else is
# refused (exit 2). See tools/lint-audit-gate-parity.py's GATE_COMMAND comment for the
# grammar and for what it does not cover.
GATE_COMMAND = (r"python3(?: -I)? (?P<script>tools/[a-z0-9][a-z0-9_-]*\.py)"
                r"(?P<args>(?: [A-Za-z0-9_./=,+-]+)*)")
RUNNER_LABEL = r"[A-Za-z0-9][A-Za-z0-9 ./-]*"
RUNNER_LINE_RE = re.compile(rf'run_gate "(?P<name>{RUNNER_LABEL})" +{GATE_COMMAND}')
RUN_GATE_WORD_RE = re.compile(r"\brun_gate\b")
RUNNER_NON_GATE_LINES = frozenset({"run_gate() {"})


COMMON_DISCOVERY_TOKENS = (
    "iter_targets",
    "iter_markdown_targets",
    "is_target",
    "is_markdown_target",
    "DEFAULT_EXEMPT_DIRS",
)
EXEMPT_NAME_RE = re.compile(r"EXEMPT", re.IGNORECASE)
TARGET_NAME_RE = re.compile(r"TARGET|FILE|PATH|SURFACE|DIR|ROOT|SCAN", re.IGNORECASE)


@dataclass
class GateScope:
    name: str
    script: str
    scope_class: str = "not-derivable"
    exempt_values: list[str] = field(default_factory=list)
    target_values: list[str] = field(default_factory=list)
    note: str = ""


def _const_strings(node: ast.AST) -> list[str]:
    """Collect constant strings from a str / tuple / list / set / frozenset node."""
    out: list[str] = []
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        out.append(node.value)
    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        for elt in node.elts:
            out.extend(_const_strings(elt))
    elif isinstance(node, ast.Call):
        # frozenset({...}) / set([...]) wrappers
        for arg in node.args:
            out.extend(_const_strings(arg))
    return out


def derive_scope(root: Path, name: str, script: str) -> GateScope:
    gate = GateScope(name=name, script=script)
    try:
        path = join_under(root, script)
    except PathContainmentError as exc:
        if is_containment_refusal(exc):
            raise
        path = root / script
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError as exc:
        gate.note = f"unreadable: {exc}"
        return gate
    # Any other read error (a locked script, a link into a locked directory) propagates to main()'s
    # refusal: classifying it not-derivable let the run succeed on evidence it never read (3b50b2e1 r3).

    uses_common = any(tok in source for tok in COMMON_DISCOVERY_TOKENS)
    walk_based = 'rglob("*.md")' in source or "rglob('*.md')" in source

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        gate.note = f"unparseable: {exc}"
        gate.scope_class = "common-discovery" if uses_common else "not-derivable"
        return gate

    exempts: list[str] = []
    targets: list[str] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            value = node.value
        else:
            names = [node.target.id] if isinstance(node.target, ast.Name) else []
            value = node.value
        if not names or value is None:
            continue
        strings = _const_strings(value)
        if not strings:
            continue
        for nm in names:
            if EXEMPT_NAME_RE.search(nm):
                exempts.extend(strings)
            elif TARGET_NAME_RE.search(nm):
                # keep only path-shaped strings (contain a slash or a known suffix)
                targets.extend(
                    s for s in strings
                    if ("/" in s or s.endswith((".md", ".yml", ".yaml", ".py", ".sh")))
                )

    gate.exempt_values = sorted(set(exempts))
    gate.target_values = sorted(set(targets))
    if uses_common:
        gate.scope_class = "common-discovery"
    elif gate.target_values:
        gate.scope_class = "target-scoped"
        if walk_based:
            gate.note = "walk-based (rglob) over the listed roots"
    elif walk_based:
        gate.scope_class = "not-derivable"
        gate.note = "walk-based (rglob) but roots not statically derivable"
    else:
        gate.scope_class = "not-derivable"
    return gate


def load_gates(root: Path) -> list[GateScope]:
    try:
        runner = join_under(root, "tools/run_all_audits.sh")
    except PathContainmentError as exc:
        if is_containment_refusal(exc):
            raise
        runner = root / "tools/run_all_audits.sh"
    if not runner.is_file():
        raise RuntimeError(f"runner not found: {runner}")
    gates: list[GateScope] = []
    # Split at LF only, as bash does: a universal-newline read would also split at CR.
    for raw in runner.read_bytes().decode("utf-8", errors="replace").split("\n"):
        line = raw.rstrip(" \t")
        if (line.lstrip().startswith("#") or not RUN_GATE_WORD_RE.search(line)
                or line in RUNNER_NON_GATE_LINES):
            continue
        m = RUNNER_LINE_RE.fullmatch(line)
        if not m:
            raise RuntimeError(f"runner line {line!r} is not an accepted gate line; only "
                               f'`run_gate "LABEL" python3 [-I] tools/X.py [plain arguments]` '
                               f"at column 0 is accepted")
        gates.append(derive_scope(root, m.group("name"), m.group("script")))
    return gates


def default_exempt_dirs(root: Path) -> frozenset[str]:
    """Read DEFAULT_EXEMPT_DIRS from lint_common by importing its source safely."""
    try:
        path = join_under(root, "tools/lint_common.py")
    except PathContainmentError as exc:
        if is_containment_refusal(exc):
            raise
        path = root / "tools/lint_common.py"
    src = path.read_text(
        encoding="utf-8", errors="replace"
    )
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            names = (
                [t.id for t in node.targets if isinstance(t, ast.Name)]
                if isinstance(node, ast.Assign)
                else ([node.target.id] if isinstance(node.target, ast.Name) else [])
            )
            if "DEFAULT_EXEMPT_DIRS" in names and node.value is not None:
                return frozenset(_const_strings(node.value))
    return frozenset()


def tracked_markdown(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "*.md"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln]


def file_scanned_by(rel: str, gate: GateScope, shared_exempt: frozenset[str]) -> bool:
    parts = rel.split("/")
    if gate.scope_class == "common-discovery":
        if any(p in shared_exempt for p in parts):
            return False
        for ex in gate.exempt_values:
            ex_norm = ex.rstrip("/")
            if rel == ex_norm or rel.startswith(ex_norm + "/") or ex_norm in parts:
                return False
        return True
    if gate.scope_class == "target-scoped":
        return any(rel == t or rel.startswith(t.rstrip("/") + "/") for t in gate.target_values)
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report per-gate scan scope and the markdown surfaces no gate scans."
    )
    parser.add_argument("--root", type=str, default=str(TOOL_ROOT))
    parser.add_argument("--format", choices=("md", "tsv"), default="md")
    parser.add_argument(
        "--unscanned-only",
        action="store_true",
        help="Print only the unscanned-surface list.",
    )
    args = parser.parse_args(argv)
    # 3b50b2e1: an empty --root used to become '.', so the current directory was audited. Checked
    # inline to preserve this tool's existing root-argument diagnostics.
    try:
        root_is_dir = bool(str(args.root).strip()) and Path(args.root).is_dir()
    except OSError as exc:
        # Python 3.11's is_dir() raises on EACCES where newer versions return False.
        print(f"ERROR: --root {args.root!r}: unreadable ({exc.strerror}); nothing would be audited.",
              file=sys.stderr)
        return 2
    if not root_is_dir:
        print(f"ERROR: --root {args.root!r}: not a directory; nothing would be audited.",
              file=sys.stderr)
        return 2
    root = Path(args.root).resolve()

    try:
        gates = load_gates(root)
        shared_exempt = default_exempt_dirs(root)
        md_files = tracked_markdown(root)
    except (PathContainmentError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    derivable = [g for g in gates if g.scope_class != "not-derivable"]
    coverage: dict[str, int] = {}
    for rel in md_files:
        coverage[rel] = sum(
            1 for g in derivable if file_scanned_by(rel, g, shared_exempt)
        )
    unscanned_all = sorted(rel for rel, n in coverage.items() if n == 0)
    def in_exempt_tree(rel: str) -> bool:
        return any(p in shared_exempt for p in rel.split("/"))
    unscanned = [r for r in unscanned_all if not in_exempt_tree(r)]
    exempt_counts: dict[str, int] = {}
    for r in unscanned_all:
        if in_exempt_tree(r):
            top = r.split("/")[0]
            exempt_counts[top] = exempt_counts.get(top, 0) + 1

    if not args.unscanned_only:
        classes = {"common-discovery": 0, "target-scoped": 0, "not-derivable": 0}
        for g in gates:
            classes[g.scope_class] += 1
        print(f"# Gate blind-spot report (root: {root})")
        print(
            f"\nGates in runner: {len(gates)} "
            f"(common-discovery {classes['common-discovery']}, "
            f"target-scoped {classes['target-scoped']}, "
            f"not-derivable {classes['not-derivable']}). "
            f"Tracked .md files: {len(md_files)}. Shared exempt dirs: "
            f"{', '.join(sorted(shared_exempt))}."
        )
        print(
            "\nAPPROXIMATE by construction (static derivation; see module "
            "docstring). Not-derivable gates are excluded from the inversion."
        )
        sep = "\t" if args.format == "tsv" else " | "
        print(f"\n## Per-gate scope\n")
        if args.format == "md":
            print("| Gate | Script | Class | Own exemptions / targets |")
            print("| --- | --- | --- | --- |")
        for g in gates:
            detail = (
                "; ".join(g.exempt_values)
                if g.scope_class == "common-discovery"
                else "; ".join(g.target_values)
            ) or g.note or "-"
            if args.format == "md":
                print(f"| {g.name} | `{g.script}` | {g.scope_class} | {detail} |")
            else:
                print(sep.join((g.name, g.script, g.scope_class, detail)))

    print(
        f"\n## Non-exempt markdown files scanned by ZERO scope-derivable gates "
        f"({len(unscanned)})\n"
    )
    for rel in unscanned:
        print(f"- {rel}")
    if not unscanned:
        print("(none)")
    if exempt_counts:
        summary = ", ".join(f"{k}/ {v}" for k, v in sorted(exempt_counts.items()))
        print(
            f"\nKnown-by-design gate-blind trees (shared exempt dirs): {summary} "
            f"file(s). These are exempt by convention; the deep-assessment run "
            f"reviews them manually rather than via gates."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
