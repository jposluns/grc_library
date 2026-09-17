#!/usr/bin/env python3
"""Document metadata-block check (grc gate): pack-owned engine (source of record).

The pure validation of a document's metadata block against a corpus's metadata
model: required fields present, the Document Type in the allowed set, the Version
semver, the Date ISO-8601, the Owner / Approving Authority role-based, the License
the canonical value, the Repository Path a self-referential link, and the filename
prefix matching the Document Type. It also verifies the backslash-newline hard-break
markers on the metadata block.

Engine/wrapper split (Group-A content-generic lane, Pattern A): this engine carries
the PURE check (``extract_metadata``, ``check_line_break_markers``,
``looks_role_based``, ``normalize_link_value``, ``check_file``) plus the GENERIC
metadata-parsing regexes (field, raw-field, link, semver, ISO-date). The corpus's
METADATA MODEL is project configuration and is supplied by the wrapper
(``tools/lint-metadata.py``): the allowed Document Types, the type-to-filename-prefix
map, the required-field list, the exempt files / directory prefixes / prefix-exempt
basenames, the role-suffix and role-stem vocabularies, the canonical license value,
and the exempt-root predicate. Keeping the model wrapper-side also preserves the
project's cross-surface doctype-enumeration parity check, which reads the allowed
types from the wrapper.

Exit codes (the wrapper returns these): 0 clean; 1 one or more findings.
"""

from __future__ import annotations

import re
from pathlib import Path

# Generic metadata-parsing patterns (not corpus-model config): the field shape,
# the raw-field shape (with its on-disk line ending, for the hard-break check),
# the code-span markdown link, semver, and ISO date.
FIELD_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$")
FIELD_RAW_PATTERN = re.compile(r"^\*\*([^*]+):\*\*\s+.+$")
LINK_RE = re.compile(r"\[`([^`]+)`\]\(([^)]+)\)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def extract_metadata(text: str) -> dict[str, str]:
    """Return the metadata block parsed as a field-name -> value dict.

    Strips the CommonMark backslash-newline hard-line-break marker when present,
    so the captured value is the user-facing content only.
    """
    fields: dict[str, str] = {}
    seen_field = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("---") and seen_field:
            break
        if not stripped and seen_field:
            break
        m = FIELD_PATTERN.match(line)
        if m:
            name, value = m.groups()
            value = value.strip()
            if value.endswith("\\"):
                value = value[:-1].rstrip()
            fields[name.strip()] = value
            seen_field = True
    return fields


def check_line_break_markers(text: str) -> list[str]:
    """Verify metadata block line breaks use the backslash-newline convention.

    Each metadata line except the last must end with a literal ``\\`` so GitHub
    renders the field as a hard line break (CommonMark §6.7).
    """
    findings: list[str] = []
    lines = text.splitlines()
    metadata_indices: list[int] = []
    started = False
    for i, line in enumerate(lines):
        if FIELD_RAW_PATTERN.match(line):
            metadata_indices.append(i)
            started = True
        elif started:
            break
        elif i > 10:
            break
    if not metadata_indices:
        return findings
    for idx_in_block, line_idx in enumerate(metadata_indices):
        line = lines[line_idx]
        is_last = idx_in_block == len(metadata_indices) - 1
        stripped = line.rstrip()
        ends_with_backslash = stripped.endswith("\\")
        if is_last:
            continue
        if not ends_with_backslash:
            findings.append(
                f"L{line_idx + 1}: metadata line missing backslash-newline "
                f"marker (expected line to end with '\\\\' per CommonMark "
                f"§6.7 hard line-break convention)"
            )
    return findings


def looks_role_based(value: str, role_suffixes: set[str], role_stems: set[str]) -> bool:
    """Heuristic: a role-based value ends in a known role suffix or role stem."""
    if not value:
        return True
    cleaned = re.sub(r"\(.*?\)", "", value).strip()
    parts = [p.strip() for p in re.split(r"[,/]", cleaned) if p.strip()]
    for part in parts:
        words = part.split()
        if any(w in role_suffixes for w in words):
            continue
        if any(w in role_stems for w in words):
            continue
        return False
    return True


def normalize_link_value(value: str) -> str:
    """If the field value is a markdown link, return the target; otherwise the value."""
    m = LINK_RE.search(value)
    if m:
        return m.group(2)
    return value.strip()


def check_file(
    path: Path,
    repo_root: Path,
    *,
    is_exempt_root,
    exempt: set[str],
    exempt_prefixes: tuple[str, ...],
    required_fields: list[str],
    allowed_types: set[str],
    type_to_prefix: dict[str, list[str]],
    prefix_exempt_basenames: set[str],
    role_suffixes: set[str],
    role_stems: set[str],
    license_value: str,
) -> list[str]:
    """Return metadata-block findings for one markdown file, per the supplied model."""
    findings: list[str] = []
    if is_exempt_root(path, repo_root=repo_root):
        return findings
    rel = path.relative_to(repo_root).as_posix()
    basename = path.name

    if rel in exempt:
        return findings

    if any(rel.startswith(p) for p in exempt_prefixes):
        return findings

    # Domain README files: enforce only the basic metadata header (loose check).
    if basename == "README.md" and rel != "README.md":
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append("file not utf-8")
            return findings
        meta = extract_metadata(text)
        for required in ("Document Title", "License"):
            if required not in meta:
                findings.append(f"domain README missing field: {required}")
        findings.extend(check_line_break_markers(text))
        return findings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append("file not utf-8")
        return findings

    meta = extract_metadata(text)

    # 0. Backslash-newline line-break markers on metadata block.
    findings.extend(check_line_break_markers(text))

    # 1. All required fields present.
    for f in required_fields:
        if f not in meta:
            findings.append(f"missing required metadata field: {f}")

    # 2. Document Type allowed.
    dtype = meta.get("Document Type", "").strip()
    if dtype and dtype not in allowed_types:
        findings.append(f"invalid Document Type: {dtype!r}")

    # 3. Version semver.
    version = meta.get("Version", "").strip()
    if version and not VERSION_RE.match(version):
        findings.append(f"invalid Version (expected x.y.z): {version!r}")

    # 4. Date ISO 8601.
    date_val = meta.get("Date", "").strip()
    if date_val and not DATE_RE.match(date_val):
        findings.append(f"invalid Date (expected YYYY-MM-DD): {date_val!r}")

    # 5. Owner / Approving Authority role-based.
    for role_field in ("Owner", "Approving Authority"):
        v = meta.get(role_field, "")
        if v and not looks_role_based(v, role_suffixes, role_stems):
            findings.append(f"{role_field} does not look role-based: {v!r}")

    # 6. License is the canonical value.
    lic = meta.get("License", "").strip()
    if lic and lic != license_value:
        findings.append(f"License is not {license_value!r}: {lic!r}")

    # 7. Repository Path matches actual path (after link normalization).
    repo_path_field = meta.get("Repository Path", "")
    if repo_path_field:
        link = LINK_RE.search(repo_path_field)
        if link:
            display = link.group(1)
            if display != rel:
                findings.append(f"Repository Path display does not match actual path: "
                                f"{display!r} vs {rel!r}")
        else:
            findings.append(f"Repository Path is not a markdown link: {repo_path_field!r}")

    # 8. Filename prefix matches Document Type.
    if basename not in prefix_exempt_basenames and dtype in type_to_prefix:
        prefixes = type_to_prefix[dtype]
        if not any(basename.startswith(p) for p in prefixes):
            findings.append(f"filename prefix does not match Document Type "
                            f"{dtype!r}: expected one of {prefixes}")

    return findings
