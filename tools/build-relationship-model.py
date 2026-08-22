#!/usr/bin/env python3
"""Generate `governance/relationship-model.generated.json` from the relationship source records.

The relationship model is a derived, machine-readable projection of the
hand-maintained records in `governance/relationship-model-source.json`,
validated against the controlled vocabulary of
`governance/framework-governance-relationship-and-flow-modelling.md`:
the controlled verb registry (the 18 structural verbs plus the 5
assessed-outcome verbs), the node-class taxonomy, the nature
vocabulary, and the field shape of that framework's illustrative
machine-readable record. The generated file is not the source of
truth: edit the source records and regenerate.

Every record is validated before anything is written. A validation
failure names the failing record id and the rule, and the tool exits
non-zero without writing.

Usage:
    python3 tools/build-relationship-model.py
    python3 tools/build-relationship-model.py --check    # validate without writing

`--check` exits non-zero if any record fails validation or if the
committed generated file differs from the regenerated content,
suitable for CI integration. Exit codes: 0 written or in sync, 1 on a
validation failure or drift, 2 on an environmental error (the source
file missing or unparseable).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "governance" / "relationship-model-source.json"
GENERATED = REPO_ROOT / "governance" / "relationship-model.generated.json"

# The 7 node-category short names from the framework's node-class taxonomy.
CATEGORY_TOKENS = frozenset((
    "authority", "sources", "governance", "context",
    "implementation", "risk", "assurance",
))

# The framework's 6 declared viewpoints. The record field is the viewpoint
# under which the record was validated, so it is held to this closed set.
VIEWPOINTS = frozenset((
    "authority", "applicability", "governance",
    "implementation", "assurance", "risk",
))

LAYOUT_ROLES = frozenset(("primary", "associative"))
INVERSE_STORAGE = frozenset(("inferred", "stored"))

# Principle 6: a relationship carries at least 1 of these 5 natures.
VALID_NATURES = frozenset((
    "structural", "inferred", "assessed", "temporal", "evidence-dependent",
))

# Contradictory nature combinations (validation test 4: a relationship that
# depends on assessment, time, or evidence must not also pose as an enduring
# structural fact). structural+inferred is deliberately NOT contradictory:
# an inferred edge can assert a structural fact. Multi-nature records such
# as assessed+temporal+evidence-dependent are valid.
CONTRADICTORY_NATURE_PAIRS = (
    frozenset(("structural", "assessed")),
    frozenset(("structural", "temporal")),
    frozenset(("structural", "evidence-dependent")),
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

RECORD_FIELDS = (
    "id", "source", "verb", "destination", "relationship_class",
    "layout_role", "nature", "viewpoint", "direction_rule", "inverse",
    "validity", "authority_level", "evidence_refs", "provenance",
    "scope", "status",
)
ENDPOINT_FIELDS = frozenset(("id", "class"))
INVERSE_FIELDS = frozenset(("verb", "storage", "justification"))
VALIDITY_FIELDS = frozenset(("from", "to"))


def _verb(relationship_class: str,
          source_categories: tuple[str, ...] | None,
          destination_categories: tuple[str, ...] | None,
          layout_role: str,
          inverse: str) -> dict:
    return {
        "relationship_class": relationship_class,
        "source_categories": (frozenset(source_categories)
                              if source_categories is not None else None),
        "destination_categories": (frozenset(destination_categories)
                                   if destination_categories is not None else None),
        "layout_role": layout_role,
        "inverse": inverse,
    }


# The controlled verb registry, transcribed from the framework's controlled
# verb set table (the 18 structural verbs) and its assessed-outcomes
# subsection (the 5 assessed-outcome verbs): 23 controlled verbs, exactly
# one registry entry per verb. Category sets are the TYPICAL source and
# destination categories; a multi-category node fits if ANY of its
# categories is in the verb's set. A None set means unrestricted
# (`references` is "any category to any category"). `layout_role` records
# the TYPICAL role only; the operative role is decided per view, so records
# are not validated against it. `contains` is same-category composition and
# is checked as a non-empty category intersection (SAME_CATEGORY_VERBS)
# rather than as fixed source and destination sets.
VERB_REGISTRY: dict[str, dict] = {
    "issues": _verb("authority", ("authority",), ("authority", "sources"),
                    "primary", "is issued by"),
    "mandates": _verb("authority", ("authority", "governance"), ("sources",),
                      "primary", "is mandated by"),
    "requires": _verb("requirement", ("authority", "governance"),
                      ("governance", "implementation"), "primary", "is required by"),
    "applies to": _verb("applicability",
                        ("authority", "sources", "governance", "risk"),
                        ("context",), "primary", "is subject to"),
    "contains": _verb("containment", None, None, "primary", "is contained in"),
    "defines": _verb("definition", ("sources", "governance"), ("governance",),
                     "primary", "is defined by"),
    "specifies": _verb("specification", ("sources", "governance"),
                       ("governance", "implementation"), "primary", "is specified by"),
    "implements": _verb("implementation", ("implementation",), ("governance",),
                        "primary", "is implemented by"),
    "enforces": _verb("implementation", ("implementation",), ("governance",),
                      "primary", "is enforced by"),
    "produces": _verb("evidence generation", ("implementation", "assurance"),
                      ("assurance",), "primary", "is produced by"),
    "demonstrates": _verb("assurance", ("assurance",),
                          ("implementation", "assurance"), "primary",
                          "is demonstrated by"),
    "assesses": _verb("assurance", ("assurance",),
                      ("implementation", "risk", "assurance"), "primary",
                      "is assessed by"),
    "determines": _verb("assurance", ("assurance",), ("assurance", "risk"),
                        "primary", "is determined by"),
    "mitigates": _verb("risk treatment", ("implementation",), ("risk",),
                       "primary", "is mitigated by"),
    "informs": _verb("influence", ("sources", "assurance"),
                     ("governance", "assurance"), "associative", "is informed by"),
    "references": _verb("citation", None, None, "associative", "is referenced by"),
    "adopts": _verb("commitment", ("governance", "context"), ("sources",),
                    "associative", "is adopted by"),
    "maps to": _verb("correspondence", ("sources",), ("authority", "sources"),
                     "associative", "is mapped from"),
}

# The assessed-outcome group shares one controlled contract: relationship
# class "assessed outcome", typically an implementation- or
# governance-category source and a governance- or authority-category
# destination, typically associative (the illustrative record's layout
# role), inverses inferred by default (principle 5). Principle 7's support
# requirements are enforced in validation, not here.
for _verb_token, _inverse_reading in (
    ("satisfies", "is satisfied by"),
    ("fulfils", "is fulfilled by"),
    ("conforms to", "is conformed to by"),
    ("complies with", "is complied with by"),
    ("meets", "is met by"),
):
    VERB_REGISTRY[_verb_token] = _verb(
        "assessed outcome", ("implementation", "governance"),
        ("governance", "authority"), "associative", _inverse_reading)

# Verbs whose compatibility rule is same-category composition: the source
# and destination must share at least one category.
SAME_CATEGORY_VERBS = frozenset(("contains",))

# Closed-world node-class-to-category map, transcribed from the framework's
# node-class taxonomy table. A class not in this map is a validation error,
# so the source file and this map stay in lockstep. "organizational
# standard" and "procedure" additionally carry the implementation category:
# the framework's implements/enforces distinction cluster records that a
# governance document which operationalizes a higher instrument acts in an
# implementation capacity (a multi-category reading).
CLASS_TO_CATEGORY: dict[str, frozenset[str]] = {
    # 1. Authority (external authority and obligation)
    "authority": frozenset(("authority",)),
    "regulator": frozenset(("authority",)),
    "standards body": frozenset(("authority",)),
    "regulation or law": frozenset(("authority",)),
    "contractual requirement": frozenset(("authority",)),
    "regulatory guidance": frozenset(("authority",)),
    # 2. Sources (interpretive and normative sources)
    "framework": frozenset(("sources",)),
    "standard": frozenset(("sources",)),
    "benchmark": frozenset(("sources",)),
    "guideline": frozenset(("sources",)),
    "control catalogue": frozenset(("sources",)),
    # 3. Governance (organizational governance)
    "policy": frozenset(("governance",)),
    "organizational standard": frozenset(("governance", "implementation")),
    "procedure": frozenset(("governance", "implementation")),
    "control objective": frozenset(("governance",)),
    "risk appetite": frozenset(("governance",)),
    "exception": frozenset(("governance",)),
    # 4. Context (scope and operating context)
    "macro-domain": frozenset(("context",)),
    "sector": frozenset(("context",)),
    "organization": frozenset(("context",)),
    "business process": frozenset(("context",)),
    "asset": frozenset(("context",)),
    "application": frozenset(("context",)),
    "workload": frozenset(("context",)),
    "data": frozenset(("context",)),
    # 5. Implementation
    "administrative control": frozenset(("implementation",)),
    "technical control": frozenset(("implementation",)),
    "physical control": frozenset(("implementation",)),
    "process": frozenset(("implementation",)),
    "configuration": frozenset(("implementation",)),
    "safeguard": frozenset(("implementation",)),
    # 6. Risk
    "threat": frozenset(("risk",)),
    "vulnerability": frozenset(("risk",)),
    "risk": frozenset(("risk",)),
    "residual risk": frozenset(("risk",)),
    # 7. Assurance (assurance and outcome)
    "evidence": frozenset(("assurance",)),
    "assessment": frozenset(("assurance",)),
    "finding": frozenset(("assurance",)),
    "compliance status": frozenset(("assurance",)),
}


def _registry_integrity() -> None:
    """Guard the constants at import time. A duplicated key in a dict
    literal silently keeps the last entry, so the 23-verb count and the
    category spellings are checked mechanically rather than trusted."""
    if len(VERB_REGISTRY) != 23:
        raise RuntimeError(
            f"VERB_REGISTRY must carry exactly 23 controlled verbs "
            f"(18 structural + 5 assessed outcome); found {len(VERB_REGISTRY)}")
    for verb, entry in VERB_REGISTRY.items():
        for side in ("source_categories", "destination_categories"):
            cats = entry[side]
            if cats is not None and not cats <= CATEGORY_TOKENS:
                raise RuntimeError(f"verb {verb!r} names unknown categories in {side}")
        if not entry["inverse"]:
            raise RuntimeError(f"verb {verb!r} has no inverse reading")
    for cls, cats in CLASS_TO_CATEGORY.items():
        if not cats or not cats <= CATEGORY_TOKENS:
            raise RuntimeError(f"node class {cls!r} maps to unknown or empty categories")


_registry_integrity()


def _is_nonempty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def validate_record(rec: object, position: int) -> list[str]:
    """Validate one record; return error strings (empty when valid).

    Each error names the record (its id, or its list position when the id
    itself is unusable) and a bracketed rule token, so a failure is
    traceable to the specific record and rule.
    """
    label = f"records[{position}]"
    if not isinstance(rec, dict):
        return [f"{label}: [shape] record must be a JSON object"]
    errors: list[str] = []
    rid = rec.get("id")
    if _is_nonempty_str(rid):
        label = rid
    else:
        errors.append(f"{label}: [shape] id must be a non-empty string")

    unknown = sorted(set(rec) - set(RECORD_FIELDS))
    if unknown:
        errors.append(f"{label}: [shape] unknown field(s): {', '.join(unknown)}")
    missing = sorted(set(RECORD_FIELDS) - set(rec))
    if missing:
        errors.append(f"{label}: [shape] missing field(s): {', '.join(missing)}")
        return errors  # a partial record cannot be validated meaningfully

    # Endpoints and their taxonomy categories (closed world: an unmapped
    # class is an error, so the source file and CLASS_TO_CATEGORY stay in
    # lockstep).
    endpoint_cats: dict[str, frozenset[str] | None] = {"source": None,
                                                       "destination": None}
    endpoint_cls = {"source": "", "destination": ""}
    for role in ("source", "destination"):
        endpoint = rec[role]
        if not isinstance(endpoint, dict):
            errors.append(f"{label}: [shape] {role} must be an object with id and class")
            continue
        unknown_ep = sorted(set(endpoint) - ENDPOINT_FIELDS)
        if unknown_ep:
            errors.append(f"{label}: [shape] unknown {role} field(s): "
                          f"{', '.join(unknown_ep)}")
        if not _is_nonempty_str(endpoint.get("id")):
            errors.append(f"{label}: [shape] {role}.id must be a non-empty string")
        cls = endpoint.get("class")
        if not _is_nonempty_str(cls):
            errors.append(f"{label}: [shape] {role}.class must be a non-empty string")
        else:
            endpoint_cls[role] = cls
            cats = CLASS_TO_CATEGORY.get(cls)
            if cats is None:
                errors.append(
                    f"{label}: [unmapped-node-class] {role}.class {cls!r} is not in "
                    f"the closed-world CLASS_TO_CATEGORY map; add the class with its "
                    f"taxonomy category in the same change that first uses it")
            else:
                endpoint_cats[role] = cats

    # Rule 1: verb allow-list (validation test 5: an out-of-set verb fails
    # until registered through the lifecycle process).
    verb = rec["verb"]
    entry = None
    if not _is_nonempty_str(verb):
        errors.append(f"{label}: [shape] verb must be a non-empty string")
    else:
        entry = VERB_REGISTRY.get(verb)
        if entry is None:
            errors.append(
                f"{label}: [verb-allow-list] verb {verb!r} is not one of the 23 "
                f"controlled verbs (validation test 5)")

    # relationship_class is derivable from the verb, so a stated class that
    # contradicts the registry is an error.
    if entry is not None and rec["relationship_class"] != entry["relationship_class"]:
        errors.append(
            f"{label}: [relationship-class-mismatch] relationship_class "
            f"{rec['relationship_class']!r} does not match the registry class "
            f"{entry['relationship_class']!r} for verb {verb!r}")

    # Rule 2: source and destination category compatibility. A
    # multi-category node fits if ANY of its categories is in the verb's
    # typical set.
    src_cats = endpoint_cats["source"]
    dst_cats = endpoint_cats["destination"]
    if entry is not None and src_cats is not None and dst_cats is not None:
        if verb in SAME_CATEGORY_VERBS:
            if not (src_cats & dst_cats):
                errors.append(
                    f"{label}: [category-compatibility] {verb!r} asserts "
                    f"same-category composition, but source class "
                    f"{endpoint_cls['source']!r} (categories {sorted(src_cats)}) "
                    f"shares no category with destination class "
                    f"{endpoint_cls['destination']!r} (categories {sorted(dst_cats)})")
        else:
            allowed_src = entry["source_categories"]
            if allowed_src is not None and not (src_cats & allowed_src):
                errors.append(
                    f"{label}: [category-compatibility] source class "
                    f"{endpoint_cls['source']!r} (categories {sorted(src_cats)}) does "
                    f"not fit verb {verb!r} (typical source categories "
                    f"{sorted(allowed_src)})")
            allowed_dst = entry["destination_categories"]
            if allowed_dst is not None and not (dst_cats & allowed_dst):
                errors.append(
                    f"{label}: [category-compatibility] destination class "
                    f"{endpoint_cls['destination']!r} (categories {sorted(dst_cats)}) "
                    f"does not fit verb {verb!r} (typical destination categories "
                    f"{sorted(allowed_dst)})")

    if rec["layout_role"] not in LAYOUT_ROLES:
        errors.append(f"{label}: [shape] layout_role must be one of "
                      f"{sorted(LAYOUT_ROLES)}")

    # Rule 3: nature vocabulary and contradiction checks (principle 6;
    # validation test 4).
    natures = rec["nature"]
    nature_set: set[str] = set()
    if (not isinstance(natures, list) or not natures
            or not all(isinstance(n, str) for n in natures)):
        errors.append(
            f"{label}: [shape] nature must be a non-empty list of strings "
            f"(principle 6)")
    else:
        bad = sorted(set(natures) - VALID_NATURES)
        if bad:
            errors.append(f"{label}: [nature-vocabulary] unknown nature token(s): "
                          f"{', '.join(bad)}")
        if len(set(natures)) != len(natures):
            errors.append(f"{label}: [shape] nature carries duplicate tokens")
        nature_set = set(natures) & VALID_NATURES
        for pair in CONTRADICTORY_NATURE_PAIRS:
            if pair <= set(natures):
                other = sorted(pair - frozenset(("structural",)))[0]
                errors.append(
                    f"{label}: [nature-contradiction] natures {sorted(pair)} "
                    f"contradict each other: an edge that is {other} must not also "
                    f"pose as an enduring structural fact (validation test 4)")

    if rec["viewpoint"] not in VIEWPOINTS:
        errors.append(
            f"{label}: [shape] viewpoint must be one of the framework's declared "
            f"viewpoints {sorted(VIEWPOINTS)}")

    for field in ("direction_rule", "authority_level", "status"):
        if not _is_nonempty_str(rec[field]):
            errors.append(f"{label}: [shape] {field} must be a non-empty string")

    for field in ("provenance", "scope"):
        if rec[field] is not None and not _is_nonempty_str(rec[field]):
            errors.append(f"{label}: [shape] {field} must be null or a "
                          f"non-empty string")

    evidence = rec["evidence_refs"]
    if not isinstance(evidence, list) or not all(_is_nonempty_str(x) for x in evidence):
        errors.append(f"{label}: [shape] evidence_refs must be a list of "
                      f"non-empty strings")
        evidence = []

    # Rule 7: date well-formedness. ISO-8601 dates or null, never an empty
    # string; from must not be after to.
    validity = rec["validity"]
    parsed_dates: dict[str, date | None] = {"from": None, "to": None}
    if not isinstance(validity, dict):
        errors.append(f"{label}: [shape] validity must be an object with from and to")
    else:
        unknown_v = sorted(set(validity) - VALIDITY_FIELDS)
        if unknown_v:
            errors.append(f"{label}: [shape] unknown validity field(s): "
                          f"{', '.join(unknown_v)}")
        missing_v = sorted(VALIDITY_FIELDS - set(validity))
        if missing_v:
            errors.append(f"{label}: [shape] missing validity field(s): "
                          f"{', '.join(missing_v)}")
        for key in ("from", "to"):
            value = validity.get(key)
            if value is None:
                continue
            if not isinstance(value, str) or not DATE_RE.match(value):
                errors.append(
                    f"{label}: [date-well-formedness] validity.{key} must be an "
                    f"ISO-8601 date (YYYY-MM-DD) or null, never an empty string; "
                    f"got {value!r}")
                continue
            try:
                parsed_dates[key] = date.fromisoformat(value)
            except ValueError:
                errors.append(
                    f"{label}: [date-well-formedness] validity.{key} {value!r} is "
                    f"not a real calendar date")
        d_from, d_to = parsed_dates["from"], parsed_dates["to"]
        if d_from is not None and d_to is not None and d_from > d_to:
            errors.append(
                f"{label}: [date-well-formedness] validity.from "
                f"{validity.get('from')!r} is after validity.to "
                f"{validity.get('to')!r}")

    # Rule 5 and the principle-5 inverse contract: inferred is the default;
    # a stored inverse requires a recorded justification; a stated inverse
    # verb must match the registry's inverse reading.
    inverse = rec["inverse"]
    if not isinstance(inverse, dict):
        errors.append(f"{label}: [shape] inverse must be an object with verb "
                      f"and storage")
    else:
        unknown_i = sorted(set(inverse) - INVERSE_FIELDS)
        if unknown_i:
            errors.append(f"{label}: [shape] unknown inverse field(s): "
                          f"{', '.join(unknown_i)}")
        storage = inverse.get("storage")
        if storage not in INVERSE_STORAGE:
            errors.append(f"{label}: [shape] inverse.storage must be one of "
                          f"{sorted(INVERSE_STORAGE)}")
        if storage == "stored" and not _is_nonempty_str(inverse.get("justification")):
            errors.append(
                f"{label}: [stored-inverse-justification] a stored inverse requires "
                f"a recorded inverse.justification (principle 5); inferred is the "
                f"default and needs none")
        inverse_verb = inverse.get("verb")
        if inverse_verb is not None:
            if not _is_nonempty_str(inverse_verb):
                errors.append(f"{label}: [shape] inverse.verb must be null or a "
                              f"non-empty string")
            elif entry is not None and inverse_verb != entry["inverse"]:
                errors.append(
                    f"{label}: [inverse-verb-mismatch] inverse.verb {inverse_verb!r} "
                    f"does not match the registry inverse reading "
                    f"{entry['inverse']!r} for verb {verb!r}")

    # Rule 4: assessed outcomes require support (principle 7): the assessed
    # nature itself, at least 1 evidence reference, a validity period, a
    # provenance, and a scope.
    is_assessed_class = rec["relationship_class"] == "assessed outcome"
    if is_assessed_class and "assessed" not in nature_set:
        errors.append(
            f"{label}: [assessed-support] an assessed-outcome relationship must "
            f"carry the assessed nature")
    if is_assessed_class or "assessed" in nature_set:
        if not evidence:
            errors.append(
                f"{label}: [assessed-support] an assessed relationship requires at "
                f"least 1 evidence reference (principle 7)")
        if parsed_dates["from"] is None:
            errors.append(
                f"{label}: [assessed-support] an assessed relationship requires a "
                f"validity period (a non-null validity.from; principle 7)")
        if not _is_nonempty_str(rec["provenance"]):
            errors.append(
                f"{label}: [assessed-support] an assessed relationship requires a "
                f"provenance (the assessment that established it; principle 7)")
        if not _is_nonempty_str(rec["scope"]):
            errors.append(
                f"{label}: [assessed-support] an assessed relationship requires a "
                f"scope (principle 7)")

    return errors


def _find_cycle(adjacency: dict[str, list[str]]) -> list[str] | None:
    """Return one directed cycle as a node list (first node repeated at the
    end), or None. Iterative three-colour depth-first search; iteration
    order is sorted, so the reported cycle is deterministic."""
    white, grey, black = 0, 1, 2
    colour = {node: white for node in adjacency}
    for start in sorted(adjacency):
        if colour[start] != white:
            continue
        colour[start] = grey
        stack = [(start, iter(sorted(adjacency[start])))]
        path = [start]
        while stack:
            node, successors = stack[-1]
            nxt = next(successors, None)
            if nxt is None:
                colour[node] = black
                stack.pop()
                path.pop()
                continue
            if colour[nxt] == grey:
                idx = path.index(nxt)
                return path[idx:] + [nxt]
            if colour[nxt] == white:
                colour[nxt] = grey
                stack.append((nxt, iter(sorted(adjacency[nxt]))))
                path.append(nxt)
    return None


def detect_primary_cycles(records: list) -> list[str]:
    """Rule 6 (validation test 3): a directed cycle among the PRIMARY edges
    of one viewpoint slice is an error. The check runs per viewpoint, so a
    cycle formed only across viewpoints, or only when associative edges are
    included, is never flagged. Records too malformed to place in a graph
    are skipped here; the shape checks report them separately."""
    by_viewpoint: dict[str, dict[str, list[str]]] = {}
    for rec in records:
        if not isinstance(rec, dict) or rec.get("layout_role") != "primary":
            continue
        viewpoint = rec.get("viewpoint")
        source = rec.get("source")
        destination = rec.get("destination")
        if not (isinstance(viewpoint, str) and isinstance(source, dict)
                and isinstance(destination, dict)):
            continue
        src_id = source.get("id")
        dst_id = destination.get("id")
        if not (_is_nonempty_str(src_id) and _is_nonempty_str(dst_id)):
            continue
        adjacency = by_viewpoint.setdefault(viewpoint, {})
        adjacency.setdefault(src_id, []).append(dst_id)
        adjacency.setdefault(dst_id, [])
    errors: list[str] = []
    for viewpoint in sorted(by_viewpoint):
        cycle = _find_cycle(by_viewpoint[viewpoint])
        if cycle is not None:
            errors.append(
                f"[primary-cycle] viewpoint {viewpoint!r}: directed cycle among "
                f"primary edges: {' -> '.join(cycle)} (validation test 3; the check "
                f"runs per viewpoint slice, so associative edges and cross-viewpoint "
                f"edges never trigger it)")
    return errors


def validate_records(records: list) -> list[str]:
    """All validation: per-record rules, duplicate ids, and per-viewpoint
    primary-edge cycle detection. Returns every error, not only the first."""
    errors: list[str] = []
    for position, rec in enumerate(records):
        errors.extend(validate_record(rec, position))
    counts: dict[str, int] = {}
    for rec in records:
        if isinstance(rec, dict) and _is_nonempty_str(rec.get("id")):
            counts[rec["id"]] = counts.get(rec["id"], 0) + 1
    for rid in sorted(rid for rid, n in counts.items() if n > 1):
        errors.append(f"{rid}: [duplicate-id] record id appears {counts[rid]} "
                      f"times; ids must be unique")
    errors.extend(detect_primary_cycles(records))
    return errors


def normalize_record(rec: dict) -> dict:
    """Canonical projection of a validated record: the inverse verb is
    filled from the registry when the source leaves it null (principle 5:
    inverses are inferred by default), and set-valued fields (nature,
    evidence_refs) are sorted so the output is deterministic."""
    entry = VERB_REGISTRY[rec["verb"]]
    inverse: dict = {
        "storage": rec["inverse"]["storage"],
        "verb": rec["inverse"].get("verb") or entry["inverse"],
    }
    if "justification" in rec["inverse"]:
        inverse["justification"] = rec["inverse"]["justification"]
    return {
        "id": rec["id"],
        "source": {"id": rec["source"]["id"], "class": rec["source"]["class"]},
        "verb": rec["verb"],
        "destination": {"id": rec["destination"]["id"],
                        "class": rec["destination"]["class"]},
        "relationship_class": rec["relationship_class"],
        "layout_role": rec["layout_role"],
        "nature": sorted(rec["nature"]),
        "viewpoint": rec["viewpoint"],
        "direction_rule": rec["direction_rule"],
        "inverse": inverse,
        "validity": {"from": rec["validity"]["from"], "to": rec["validity"]["to"]},
        "authority_level": rec["authority_level"],
        "evidence_refs": sorted(rec["evidence_refs"]),
        "provenance": rec["provenance"],
        "scope": rec["scope"],
        "status": rec["status"],
    }


def build(records: list) -> str:
    """Serialize the model: normalized records sorted by id, plus a summary
    of counts by relationship class. `json.dumps` with sorted keys and a
    trailing newline keeps the output byte-deterministic for --check."""
    normalized = sorted((normalize_record(rec) for rec in records),
                        key=lambda rec: rec["id"])
    counts: dict[str, int] = {}
    for rec in normalized:
        counts[rec["relationship_class"]] = counts.get(rec["relationship_class"], 0) + 1
    model = {
        "_notice": ("Auto-generated relationship model for the GRC Documentation "
                    "Library. Source of truth: "
                    "governance/relationship-model-source.json. Regenerate with "
                    "python3 tools/build-relationship-model.py. Do not edit this "
                    "file by hand."),
        "schema_version": 1,
        "generated_by": "tools/build-relationship-model.py",
        "source": "governance/relationship-model-source.json",
        "framework": "governance/framework-governance-relationship-and-flow-modelling.md",
        "summary": {
            "record_count": len(normalized),
            "records_by_relationship_class": counts,
        },
        "records": normalized,
    }
    return json.dumps(model, indent=2, sort_keys=True) + "\n"


def load_records(payload: object) -> tuple[list, list[str]]:
    """Unwrap the source envelope: a JSON object holding an optional
    _comment and the records list. Returns (records, errors)."""
    if not isinstance(payload, dict):
        return [], [f"{SOURCE.name}: [shape] top level must be a JSON object "
                    f"holding a records list"]
    errors: list[str] = []
    unknown = sorted(set(payload) - {"_comment", "records"})
    if unknown:
        errors.append(f"{SOURCE.name}: [shape] unknown top-level field(s): "
                      f"{', '.join(unknown)}")
    records = payload.get("records")
    if not isinstance(records, list):
        errors.append(f"{SOURCE.name}: [shape] records must be a list")
        return [], errors
    return records, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the relationship model from the relationship "
                    "source records.")
    parser.add_argument("--check", action="store_true",
                        help="Validate the source records and confirm the generated "
                             "file is in sync; do not write. Exits non-zero on a "
                             "validation failure or drift.")
    args = parser.parse_args()

    if not SOURCE.exists():
        print(f"ERROR: {SOURCE.name} is missing; the relationship model cannot "
              f"be built.")
        return 2
    try:
        payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {SOURCE.name} is not valid JSON: {exc}")
        return 2

    records, errors = load_records(payload)
    errors.extend(validate_records(records))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"{len(errors)} validation error(s); nothing written.")
        return 1

    new_content = build(records)

    if args.check:
        if not GENERATED.exists():
            print(f"FAIL: {GENERATED.name} does not exist; run without --check "
                  f"to generate.")
            return 1
        current = GENERATED.read_text(encoding="utf-8")
        if current != new_content:
            print(f"FAIL: {GENERATED.name} is out of sync with {SOURCE.name}.")
            print("Run `python3 tools/build-relationship-model.py` to regenerate.")
            return 1
        print(f"OK: {GENERATED.name} is in sync ({len(records)} records validated).")
        return 0

    GENERATED.write_text(new_content, encoding="utf-8")
    print(f"Wrote {GENERATED.name} ({len(records)} records, "
          f"{len(new_content.splitlines())} lines).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
