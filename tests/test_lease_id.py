"""The shared lease-id grammar, tools/lease_id.py (3b793, D-0502-LEASE-ID-GRAMMAR)."""
import importlib.util
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "lease_id.py"


def _load():
    spec = importlib.util.spec_from_file_location("_lease_id_under_test", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _utc(*parts):
    return datetime(*parts, tzinfo=timezone.utc)


# Accepted with a start: value -> (start, precision, form).
STAMPED = {
    # The live session id (compact minutes, hyphenated label).
    "grc-orch1-20261102T1310Z": (_utc(2026, 11, 2, 13, 10), 60, "compact-minutes"),
    # The plan elides the date of "sess-/S88-...T141710Z"; 20260916 is assumed here.
    "sess-20260916T141710Z": (_utc(2026, 9, 16, 14, 17, 10), 1, "compact-seconds"),
    "S88-20260916T141710Z": (_utc(2026, 9, 16, 14, 17, 10), 1, "compact-seconds"),
    "orch-2026-10-04T13:36:00Z": (_utc(2026, 10, 4, 13, 36), 1, "extended-seconds"),
    "orch-20261004T133600Z": (_utc(2026, 10, 4, 13, 36), 1, "compact-seconds"),
    "sess-20260916T230059Z": (_utc(2026, 9, 16, 23, 0, 59), 1, "compact-seconds"),
    "2026-20261102T1310Z": (_utc(2026, 11, 2, 13, 10), 60, "compact-minutes"),
    "x-20240229T235959Z": (_utc(2024, 2, 29, 23, 59, 59), 1, "compact-seconds"),
    # A 32-character label with hyphens is the longest accepted label.
    "abcdefghij-abcdefghij-abcdefghij-20261102T1310Z":
        (_utc(2026, 11, 2, 13, 10), 60, "compact-minutes"),
}

# Valid ids with no start (kind ID), from the plan's section 2 lists.
NO_START = (
    "claude/example-branch", "69556d8c", "orch-x", "sess-2026-09-23-opus55-r1",
    "hex-id", "nonee",
)

# Refused as stamped, still a valid ID: start UNKNOWN (kind ID).
UNSTAMPED_REFUSALS = {
    "extended minutes": "orch-2026-10-04T13:36Z",
    "impossible day": "orch-2026-02-30T13:36:00Z",
    "not a leap year": "x-20250229T0000Z",
    "month 13": "grc-orch1-20261302T1310Z",
    "hour 24": "grc-orch1-20261102T2400Z",
    "minute 60": "grc-orch1-20261102T1360Z",
    "second 60": "orch-20261004T133660Z",
    "year zero": "orch-00001004T133600Z",
    "33-character label": "abcdefghij-abcdefghij-abcdefghijk-20261102T1310Z",
    "33-character single run": "a" * 33 + "-20261102T1310Z",
    "empty label": "-20261102T1310Z",
    "no label": "20261102T1310Z",
    "empty segment": "grc--orch1-20261102T1310Z",
    "leading hyphen": "-grc-orch1-20261102T1310Z",
    "underscore": "grc_orch1-20261102T1310Z",
    "trailing text": "grc-orch1-20261102T1310Z-extra",
    "trailing extended text": "orch-2026-10-04T13:36:00Z-extra",
    "trailing character": "grc-orch1-20261102T1310Zx",
    "missing Z": "grc-orch1-20261102T1310",
    "lowercase z": "grc-orch1-20261102T1310z",
    "lowercase t": "grc-orch1-20261102t1310Z",
    "seven-digit date": "grc-orch1-2026110T1310Z",
    "offset": "orch-2026-10-04T13:36:00+00:00",
}

# Not 1 to 128 printable ASCII characters (kind INVALID).
INVALID = {
    "non-string None": None,
    "non-string int": 20261102,
    "non-string bytes": b"grc-orch1-20261102T1310Z",
    "empty": "",
    "129 characters": "a" * 129,
    "space": "grc orch1-20261102T1310Z",
    "trailing space": "none ",
    "tab": "grc-orch1-20261102T1310Z\t",
    "NBSP": "grc" + chr(0xA0) + "orch1-20261102T1310Z",
    "fullwidth digit": "grc-orch1-" + chr(0xFF12) + "0261102T1310Z",
    "non-ASCII letter": "orch-" + chr(0xE9),
    "DEL": "orch\x7f",
}


class LeaseIdGrammarTests(unittest.TestCase):
    def setUp(self):
        self.mod = _load()

    def test_stamped_values_give_start_and_precision(self):
        for value, (start, precision, form) in STAMPED.items():
            with self.subTest(value=value):
                self.assertEqual(self.mod.parse(value),
                                 (self.mod.STAMPED, start, precision, form))
                self.assertEqual(self.mod.parse(value).start.tzinfo, timezone.utc)

    def test_live_id_minute_precision(self):
        parsed = self.mod.parse("grc-orch1-20261102T1310Z")
        self.assertEqual(parsed.kind, "STAMPED")
        self.assertEqual(parsed.start.strftime("%Y-%m-%dT%H:%M:%SZ"), "2026-11-02T13:10:00Z")
        self.assertEqual(parsed.precision, 60)

    def test_valid_ids_without_a_stamp(self):
        for value in NO_START:
            with self.subTest(value=value):
                self.assertEqual(self.mod.parse(value), (self.mod.ID, None, None, None))

    def test_refused_stamps_stay_valid_ids(self):
        for name, value in UNSTAMPED_REFUSALS.items():
            with self.subTest(name=name, value=value):
                self.assertEqual(self.mod.parse(value), (self.mod.ID, None, None, None))
                self.assertTrue(self.mod.ID_RE.fullmatch(value))

    def test_invalid_values(self):
        for name, value in INVALID.items():
            with self.subTest(name=name):
                self.assertEqual(self.mod.parse(value), (self.mod.INVALID, None, None, None))

    def test_none_in_any_case(self):
        for value in ("none", "NONE", "None", "nOnE"):
            with self.subTest(value=value):
                self.assertEqual(self.mod.parse(value).kind, self.mod.NONE)

    def test_kinds_are_distinct(self):
        kinds = {self.mod.parse(value).kind
                 for value in ("none", "grc-orch1-20261102T1310Z", "69556d8c", "")}
        self.assertEqual(kinds, {"NONE", "STAMPED", "ID", "INVALID"})

    def test_id_length_boundaries(self):
        self.assertEqual(self.mod.parse("a").kind, "ID")
        self.assertEqual(self.mod.parse("a" * 128).kind, "ID")
        self.assertEqual(self.mod.parse("a" * 129).kind, "INVALID")
        self.assertEqual(self.mod.parse("!~").kind, "ID")

    def test_id_rule_is_gate_63_rule(self):
        # The ID layer keeps gate 63's earlier pattern, so no previously valid id is refused.
        import re
        old = re.compile(r"[!-~]{1,128}")
        self.assertEqual(self.mod.ID_RE.pattern, old.pattern)
        samples = [chr(code) for code in range(0x110)] + ["a" * 128, "a" * 129, ""]
        samples += list(STAMPED) + list(NO_START) + list(UNSTAMPED_REFUSALS.values())
        samples += [value for value in INVALID.values() if isinstance(value, str)]
        for value in samples:
            with self.subTest(value=value):
                self.assertEqual(bool(self.mod.ID_RE.fullmatch(value)),
                                 bool(old.fullmatch(value)))

    def test_never_raises_for_hostile_str_subclass(self):
        # Review N4: parse() calls no method of the value, so a str subclass whose
        # methods raise is classified like the equal plain str.
        def boom(*_args, **_kwargs):
            raise RuntimeError("hostile str method called")

        hostile = type("HostileStr", (str,), {name: boom for name in (
            "lower", "upper", "casefold", "__str__", "__eq__", "__len__", "__getitem__",
            "__iter__", "__contains__", "startswith", "endswith")})
        for value in ("grc-orch1-20261102T1310Z", "orch-2026-10-04T13:36:00Z", "none", "NONE",
                      "69556d8c", "orch-2026-10-04T13:36Z", "", "a b"):
            with self.subTest(value=value):
                self.assertEqual(self.mod.parse(hostile(value)), self.mod.parse(value))

    def test_never_raises_when_class_lookup_raises(self):
        # isinstance() reads __class__, which an object may make raise; parse() reads
        # type(value) instead and classifies the object as INVALID.
        class Pretender:
            @property
            def __class__(self):
                raise RuntimeError("__class__ looked up")

        self.assertEqual(self.mod.parse(Pretender()), (self.mod.INVALID, None, None, None))

    def test_stamp_forms_have_distinct_lengths(self):
        self.assertEqual(sorted(self.mod.FORMS), [14, 16, 20])
        self.assertEqual({precision for _, _, precision in self.mod.FORMS.values()}, {1, 60})

    def test_pure_and_stdlib_only(self):
        # Loads and parses under python3 -I with no repository path on sys.path.
        proc = subprocess.run(
            [sys.executable, "-I", "-c",
             "import runpy,sys; m=runpy.run_path(sys.argv[1]); "
             "print(m['parse']('grc-orch1-20261102T1310Z'))", str(TOOL)],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("kind='STAMPED'", proc.stdout)
        self.assertIn("precision=60", proc.stdout)


if __name__ == "__main__":
    unittest.main()
