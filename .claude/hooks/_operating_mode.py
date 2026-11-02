#!/usr/bin/env python3
"""Shared operating-mode reader for grc's mode-reading hooks (3b781).

AUTHORITY ORDER. The fleet's canonical, root-owned mode file
``/opt/orch-operator/operating-mode`` (JSON: ``mode``, ``set_at``) is the authority.
A lease ``Operating-mode`` value is subordinate: it can only ADD unattendedness, and
only through a DATED swap record ``<mode>@<YYYY-MM-DDTHH:MM:SSZ>`` written by the
orchestrator on a #5(b) timeout swap, honoured only while its stamp is strictly
newer than the fleet file's ``set_at``. An undated (legacy) lease value is treated
as dated at the epoch: any readable fleet file supersedes it, and the supersession
is named in the returned source, never silently dropped.

FAIL CLOSED. ``read_fleet`` returns ``(None, None, "absent")`` only when the fleet
path genuinely does not exist (lstat ENOENT or ENOTDIR); that is the ONE case that
falls back to the lease. Every other defect fails closed to ``"unattended"``: any
other lstat error, a symlink at the final component (lstat S_ISLNK, plus O_NOFOLLOW
against the race), a non-regular file (FIFO, device, directory; rejected on the
open descriptor before any read, so nothing can block), a wrong owner
(``fstat st_uid != require_owner_uid``; uid 0 in production), an unreadable,
oversized (over 65536 bytes) or undecodable file, malformed or duplicate-key JSON,
a non-dict document, a missing or non-string ``mode``, an unrecognized mode value,
and a missing or unparseable ``set_at``. ``set_at`` is load-bearing for the swap
comparison (the fleet writer orch-set-mode always writes it), so an unusable
``set_at`` makes the whole file unusable. Ignorance never permits.

ABSENT-FLEET FALLBACK (grc divergence, deliberate). lab_infra's readers treat an
absent fleet file as attended; grc's stop guard must keep its arming coverage on a
fleet-less checkout, so with the fleet file ABSENT the lease decides exactly as it
did before this module existed: a dated swap record yields its mode, and ANY other
nonempty value is returned RAW (unparsed, case preserved) so each consumer applies
its own pre-3b781 legacy rule to it (the stop guard maps the WHOLE leading token
via its _grc_map_mode; the AskUserQuestion hook blocks on any value that mentions
"unattended", stricter-is-safer). No value at all yields ``(None, "absent")`` so
each consumer takes its own indeterminate path (the AskUserQuestion hook allows,
the stop guard fails open).

NO TIME-OF-DAY MAPPING. A fleet ``"unattended"`` is returned verbatim; both
consumers already handle the bare word, so no hand mapping exists here. The fleet
path and owner uid are parameters for the hermetic self-test only; there is
deliberately no environment override, so no configuration can switch the fleet
file off.

Residuals (documented, not detectable here): the ownership check trusts fstat uid
0, so a root-owned but wrongly written file passes (R1); a parent-directory swap
between lstat and open is narrowed, not excluded, and the fail-closed default
bounds the harm to over-blocking (R2); clock skew between the swap stamp and
``set_at`` can mis-order the comparison, remedied by rerunning orchmod (R3); a
hand-forged dated swap can ADD unattendedness, by design never weaken the fleet
mode (R4); lease reads take no flock, and a torn read lands on the None or
fail-closed paths (R5); fleet ``phase`` is read past, not interpreted (R6).

Self-test: ``python3 .claude/hooks/_operating_mode.py --self-test``.
"""

import errno
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone

CANONICAL_MODE_FILE = "/opt/orch-operator/operating-mode"
UNATTENDED = frozenset({"unattended", "daytime-unattended", "overnight-unattended"})
ATTENDED = frozenset({"attended", "attended-autonomous", "fully-attended", "decisions"})
# A dated lease swap may only ADD unattendedness (#5(b) is direction-limited).
SWAP_MODES = frozenset({"daytime-unattended", "overnight-unattended"})
# The lease vocabulary the pre-3b781 readers recognized ("decisions" is the fleet's
# operator-present mode, which the AskUserQuestion hook recognized as attended).
LEGACY_MODES = frozenset({"unattended", "attended", "fully-attended",
                          "attended-autonomous", "daytime-unattended",
                          "overnight-unattended", "decisions"})

_MAX_BYTES = 65536
# The dated-swap stamp grammar is exactly gate 63's heartbeat grammar.
SWAP_STAMP_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
_SWAP_STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class _Unusable(Exception):
    pass


def _no_duplicate_keys(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise _Unusable("duplicate key")
    return dict(pairs)


def _reject_constant(name):
    # 3b781 r4 (codex E1): json.loads accepts NaN, Infinity and -Infinity unless
    # parse_constant refuses them; none of the three is JSON, so a fleet file
    # carrying one is unusable and fails closed.
    raise _Unusable("non-JSON constant %s" % name)


def parse_swap_stamp(stamp):
    """A lease swap stamp as an aware UTC datetime: exactly the heartbeat grammar
    ``YYYY-MM-DDTHH:MM:SSZ`` and a real UTC time, else None."""
    if not isinstance(stamp, str) or not SWAP_STAMP_RE.fullmatch(stamp):
        return None
    try:
        return datetime.strptime(stamp, _SWAP_STAMP_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_fleet_stamp(value):
    """The fleet ``set_at`` as an aware UTC datetime, or None. The strict heartbeat
    grammar is accepted first; any other ISO 8601 form is accepted through
    ``datetime.fromisoformat`` (a trailing Z is normalized; a naive stamp is UTC)."""
    strict = parse_swap_stamp(value)
    if strict is not None:
        return strict
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def read_fleet(path=CANONICAL_MODE_FILE, require_owner_uid=0):
    """Return (mode, set_at, note) from the fleet's canonical mode file.

    (None, None, "absent") only when the path genuinely does not exist; everything
    else that cannot yield a recognized mode WITH a parseable ``set_at`` fails
    closed to ("unattended", None, reason). See the module docstring."""
    try:
        if stat.S_ISLNK(os.lstat(path).st_mode):
            raise _Unusable("symlink at the final component")
    except (FileNotFoundError, NotADirectoryError):
        return None, None, "absent"
    except _Unusable as exc:
        return "unattended", None, f"unusable fleet mode file ({exc})"
    except Exception as exc:  # noqa: BLE001 (e.g. PermissionError on a parent directory)
        return "unattended", None, f"unusable fleet mode file ({type(exc).__name__})"
    try:
        try:
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC)
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise _Unusable("symlink at the final component") from exc
            raise
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                raise _Unusable("not a regular file")
            if info.st_uid != require_owner_uid:
                raise _Unusable("wrong owner uid %d" % info.st_uid)
            raw = os.read(fd, _MAX_BYTES + 1)
        finally:
            os.close(fd)
        if len(raw) > _MAX_BYTES:
            raise _Unusable("oversized")  # a prefix is not the file
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_reject_constant)
        mode = data.get("mode") if isinstance(data, dict) else None
        if not isinstance(mode, str):
            raise _Unusable("no string mode")
        mode = mode.strip().lower()
        if mode not in UNATTENDED and mode not in ATTENDED:
            return "unattended", None, f"unrecognized fleet mode {mode!r}"
        set_at = _parse_fleet_stamp(data.get("set_at"))
        if set_at is None:
            raise _Unusable("missing or unparseable set_at")
    except _Unusable as exc:
        return "unattended", None, f"unusable fleet mode file ({exc})"
    except Exception as exc:  # noqa: BLE001 (any unusable authority fails closed)
        return "unattended", None, f"unusable fleet mode file ({type(exc).__name__})"
    return mode, set_at, "fleet mode file"


def parse_lease_record(value):
    """Parse a raw lease ``Operating-mode`` token.

    Returns ("dated", mode, stamp) for ``<swap-mode>@<YYYY-MM-DDTHH:MM:SSZ>``
    (mode restricted to SWAP_MODES: a swap may only add unattendedness),
    ("legacy", word, None) for a recognized plain word, or None for anything else
    (a dated attended value, a bad stamp, an unknown word)."""
    if not isinstance(value, str) or not value:
        return None
    if "@" in value:
        mode, _sep, stamp = value.partition("@")
        mode = mode.strip().lower()
        parsed = parse_swap_stamp(stamp)
        if mode in SWAP_MODES and parsed is not None:
            return "dated", mode, parsed
        return None
    word = value.strip().lower()
    if word in LEGACY_MODES:
        return "legacy", word, None
    return None


def _lease_mentions_unattended(value):
    """Stricter-is-safer: any lease value containing "unattended" counts as an
    unattendedness claim, however malformed."""
    return isinstance(value, str) and "unattended" in value.lower()


def effective_mode(fleet_path=CANONICAL_MODE_FILE, lease_value=None, require_owner_uid=0):
    """Combine the fleet file and the lease value into (mode, source).

    1. A fleet reading in UNATTENDED (a genuine value or the fail-closed default)
       is returned as is; no lease reading can weaken it.
    2. A fleet attended-family reading wins over the lease, EXCEPT a dated swap
       whose stamp is strictly newer than the fleet ``set_at``: that swap's mode is
       returned. A superseded or ignored lease value is named in the source.
    3. An absent fleet file leaves the decision to the lease exactly as the
       pre-3b781 readers took it: a dated swap yields its mode, and ANY other
       nonempty value is returned RAW so each consumer applies its own legacy
       rule to it; with no lease value either, (None, "absent")."""
    fleet, set_at, note = read_fleet(fleet_path, require_owner_uid)
    record = parse_lease_record(lease_value)
    if fleet in UNATTENDED:
        return fleet, note
    if fleet is not None:
        if record is not None and record[0] == "dated":
            _kind, swap_mode, stamp = record
            if stamp > set_at:
                return swap_mode, (f"lease dated swap {lease_value!r} "
                                   f"(newer than the fleet set_at)")
            return fleet, (f"{note} (supersedes lease swap {lease_value!r}: "
                           f"its stamp is not newer than set_at)")
        if _lease_mentions_unattended(lease_value):
            return fleet, f"{note} (supersedes undated lease {lease_value!r})"
        if record is None and lease_value:
            return fleet, f"{note} (ignored unrecognized lease value {lease_value!r})"
        return fleet, note
    if record is not None and record[0] == "dated":
        return record[1], f"lease Operating-mode {lease_value!r} (fleet mode file absent)"
    if lease_value:
        # RAW, never normalized or mapped here: each consumer applies its own
        # pre-3b781 legacy rule (the stop guard its leading-token _grc_map_mode,
        # the AskUserQuestion hook its mentions-unattended rule).
        return lease_value, "lease Operating-mode (fleet mode file absent; raw value)"
    return None, "absent"


def _self_test():
    import tempfile
    import unittest
    from pathlib import Path

    OWNER = os.geteuid()
    SET_AT = "2026-11-01T12:00:00Z"

    def fleet_file(d, body):
        path = Path(d) / "operating-mode"
        path.write_text(body, encoding="utf-8")
        return str(path)

    class TestParseLeaseRecord(unittest.TestCase):
        def test_dated_swap_forms(self):
            for mode in ("daytime-unattended", "overnight-unattended"):
                kind, parsed, stamp = parse_lease_record(mode + "@2026-11-01T13:00:00Z")
                self.assertEqual((kind, parsed), ("dated", mode))
                self.assertEqual(stamp, datetime(2026, 11, 1, 13, tzinfo=timezone.utc))

        def test_dated_attended_and_bad_stamps_parse_as_none(self):
            for value in ("attended-autonomous@2026-11-01T13:00:00Z",
                          "fully-attended@2026-11-01T13:00:00Z",
                          "unattended@2026-11-01T13:00:00Z",
                          "daytime-unattended@tomorrow",
                          "daytime-unattended@2026-11-01T13:00:00",
                          "daytime-unattended@2026-13-01T13:00:00Z",
                          # 3b781 r2 (codex W4): strptime accepts these three; the
                          # required YYYY-MM-DDTHH:MM:SSZ grammar must reject them.
                          "daytime-unattended@2026-11-1T13:00:00Z",
                          "daytime-unattended@2026-1-01T13:00:00Z",
                          "daytime-unattended@2026-11-01T3:00:00Z",
                          "daytime-unattended@"):
                self.assertIsNone(parse_lease_record(value), value)

        def test_legacy_words(self):
            for word in sorted(LEGACY_MODES):
                self.assertEqual(parse_lease_record(word), ("legacy", word, None))
            # agy1 N6: the fleet's operator-present mode is a recognized legacy word,
            # pinned explicitly so dropping it from LEGACY_MODES fails here.
            self.assertEqual(parse_lease_record("decisions"), ("legacy", "decisions", None))
            for value in ("casual", "", None, "unattended-overnight"):
                self.assertIsNone(parse_lease_record(value), value)

    class TestReadFleet(unittest.TestCase):
        def test_valid_file_with_set_at(self):
            with tempfile.TemporaryDirectory() as d:
                path = fleet_file(d, '{"mode":"attended-autonomous","set_at":"%s"}' % SET_AT)
                mode, set_at, note = read_fleet(path, OWNER)
                self.assertEqual(mode, "attended-autonomous")
                self.assertEqual(set_at, datetime(2026, 11, 1, 12, tzinfo=timezone.utc))
                self.assertEqual(note, "fleet mode file")

        def test_absent_is_the_one_fallback(self):
            with tempfile.TemporaryDirectory() as d:
                self.assertEqual(read_fleet(str(Path(d) / "missing"), OWNER),
                                 (None, None, "absent"))
                # ENOTDIR: a path component that is not a directory is absent too.
                reg = fleet_file(d, "x")
                self.assertEqual(read_fleet(os.path.join(reg, "below"), OWNER)[0], None)

        def test_defects_fail_closed(self):
            bodies = ['{"mode":"unattended"',  # malformed JSON
                      '{"mode":"unattended","mode":"attended"}',  # duplicate key
                      '{"set_by":"x","set_at":"%s"}' % SET_AT,  # missing mode
                      '{"mode":["unattended"],"set_at":"%s"}' % SET_AT,
                      '{"mode":"bananas","set_at":"%s"}' % SET_AT,
                      '{"mode":"attended"}',  # missing set_at (load-bearing)
                      '{"mode":"attended","set_at":"not-a-time"}',
                      '{"mode":"attended","set_at":42}',
                      "", "[]"]
            with tempfile.TemporaryDirectory() as d:
                for body in bodies:
                    path = fleet_file(d, body)
                    self.assertEqual(read_fleet(path, OWNER)[0], "unattended", body)
                undecodable = Path(d) / "operating-mode"
                undecodable.write_bytes(b"\xff\xfe{")
                self.assertEqual(read_fleet(str(undecodable), OWNER)[0], "unattended")
                oversized = Path(d) / "big"
                oversized.write_bytes(
                    ('{"mode":"attended","set_at":"%s"}' % SET_AT).encode()
                    .ljust(_MAX_BYTES, b" ") + b"X")
                self.assertEqual(read_fleet(str(oversized), OWNER)[0], "unattended")

        def test_each_defect_isolated_in_a_valid_attended_fixture(self):
            # 3b781 r2 (codex W4): each defect alone in an otherwise valid ATTENDED
            # fixture, with its own named reason, so removing one rejection cannot
            # hide behind another defect or behind the fail-closed default.
            with tempfile.TemporaryDirectory() as d:
                dup = fleet_file(
                    d, '{"mode":"attended","set_at":"%s","mode":"attended"}' % SET_AT)
                mode, _at, note = read_fleet(dup, OWNER)
                self.assertEqual((mode, note),
                                 ("unattended", "unusable fleet mode file (duplicate key)"))
                oversized = Path(d) / "big"
                oversized.write_bytes(  # valid JSON end to end: only the bound rejects it
                    ('{"mode":"attended","set_at":"%s"}' % SET_AT).encode()
                    .ljust(_MAX_BYTES + 1, b" "))
                mode, _at, note = read_fleet(str(oversized), OWNER)
                self.assertEqual((mode, note),
                                 ("unattended", "unusable fleet mode file (oversized)"))

        def test_nonjson_constants_fail_closed(self):
            # 3b781 r4 (codex E1): json.loads accepts NaN, Infinity and -Infinity
            # unless parse_constant refuses them; each constant alone in an
            # otherwise valid ATTENDED fixture must fail closed with its own named
            # reason, never read as attended.
            with tempfile.TemporaryDirectory() as d:
                control = fleet_file(d, '{"mode":"attended","set_at":"%s"}' % SET_AT)
                self.assertEqual(read_fleet(control, OWNER)[0], "attended")
                for constant in ("NaN", "Infinity", "-Infinity"):
                    path = fleet_file(d, '{"mode":"attended","set_at":"%s","phase":%s}'
                                      % (SET_AT, constant))
                    mode, _at, note = read_fleet(path, OWNER)
                    self.assertEqual(
                        (mode, note),
                        ("unattended",
                         "unusable fleet mode file (non-JSON constant %s)" % constant),
                        constant)

        def test_non_regular_symlink_and_unreadable_fail_closed(self):
            with tempfile.TemporaryDirectory() as d:
                target = fleet_file(d, '{"mode":"attended","set_at":"%s"}' % SET_AT)
                link = str(Path(d) / "link")
                os.symlink(target, link)
                mode, _at, note = read_fleet(link, OWNER)
                self.assertEqual(mode, "unattended")
                self.assertIn("symlink", note)
                dangling = str(Path(d) / "dangling")
                os.symlink(str(Path(d) / "missing"), dangling)
                self.assertEqual(read_fleet(dangling, OWNER)[0], "unattended")
                # 3b781 r4 (codex W2): the S_ISREG check itself must reject a
                # directory and a writerless FIFO, named in the reason and with no
                # read attempted on the descriptor; the other fail-closed paths (a
                # read error, empty input) must not mask the check's removal.
                from unittest import mock
                directory = str(Path(d) / "dir")
                os.mkdir(directory)
                fifo = str(Path(d) / "fifo")
                os.mkfifo(fifo)  # must fail closed without blocking
                for nonregular in (directory, fifo):
                    with mock.patch("os.read", side_effect=AssertionError(
                            "os.read on a non-regular file")) as reads:
                        mode, _at, note = read_fleet(nonregular, OWNER)
                    self.assertEqual(
                        (mode, note),
                        ("unattended", "unusable fleet mode file (not a regular file)"),
                        nonregular)
                    self.assertEqual(reads.call_count, 0, nonregular)
                if os.geteuid() != 0:  # an inaccessible parent fails closed
                    locked = Path(d) / "locked"
                    locked.mkdir()
                    inner = fleet_file(str(locked), '{"mode":"attended","set_at":"%s"}' % SET_AT)
                    locked.chmod(0)
                    try:
                        self.assertEqual(read_fleet(inner, OWNER)[0], "unattended")
                    finally:
                        locked.chmod(0o700)

        def test_wrong_owner_fails_closed(self):
            # Portable only in the FAIL direction: an unprivileged test cannot make
            # a root-owned fixture, so the pass direction is untestable here (R1).
            with tempfile.TemporaryDirectory() as d:
                path = fleet_file(d, '{"mode":"attended","set_at":"%s"}' % SET_AT)
                mode, _at, note = read_fleet(path, OWNER + 1)
                self.assertEqual(mode, "unattended")
                self.assertIn("wrong owner", note)

        def test_bom_case_and_whitespace_are_read(self):
            # 3b781 r2 (codex W4): an ATTENDED fixture read to full success, so a lost
            # BOM decode or lost case normalization cannot pass as fail-closed.
            with tempfile.TemporaryDirectory() as d:
                path = fleet_file(d, '﻿{"mode":" Attended ","set_at":"%s"}' % SET_AT)
                self.assertEqual(read_fleet(path, OWNER),
                                 ("attended", datetime(2026, 11, 1, 12, tzinfo=timezone.utc),
                                  "fleet mode file"))

    class TestEffectiveMode(unittest.TestCase):
        def effective(self, d, body, lease):
            path = (fleet_file(d, body) if body is not None
                    else str(Path(d) / "missing"))
            return effective_mode(path, lease, OWNER)

        def test_fleet_unattended_beats_attended_lease(self):
            with tempfile.TemporaryDirectory() as d:
                mode, source = self.effective(
                    d, '{"mode":"unattended","set_at":"%s"}' % SET_AT, "attended-autonomous")
                self.assertEqual((mode, source), ("unattended", "fleet mode file"))

        def test_fleet_attended_supersedes_stale_undated_lease(self):
            # NEW behaviour (3b781): fails at 430da42ef, where an undated
            # daytime-unattended lease value blocked over an attended fleet file.
            with tempfile.TemporaryDirectory() as d:
                mode, source = self.effective(
                    d, '{"mode":"attended-autonomous","set_at":"%s"}' % SET_AT,
                    "daytime-unattended")
                self.assertEqual(mode, "attended-autonomous")
                self.assertIn("supersedes undated lease", source)

        def test_dated_swap_newer_than_set_at_wins(self):
            with tempfile.TemporaryDirectory() as d:
                mode, source = self.effective(
                    d, '{"mode":"attended-autonomous","set_at":"%s"}' % SET_AT,
                    "daytime-unattended@2026-11-01T12:00:01Z")
                self.assertEqual(mode, "daytime-unattended")
                self.assertIn("newer than the fleet set_at", source)

        def test_dated_swap_not_newer_is_superseded_and_named(self):
            with tempfile.TemporaryDirectory() as d:
                for stamp in ("2026-11-01T12:00:00Z", "2026-10-31T12:00:00Z"):
                    mode, source = self.effective(
                        d, '{"mode":"attended-autonomous","set_at":"%s"}' % SET_AT,
                        "daytime-unattended@" + stamp)
                    self.assertEqual(mode, "attended-autonomous", stamp)
                    self.assertIn("supersedes lease swap", source)

        def test_dated_attended_value_is_ignored(self):
            with tempfile.TemporaryDirectory() as d:
                mode, source = self.effective(
                    d, '{"mode":"attended-autonomous","set_at":"%s"}' % SET_AT,
                    "attended@2026-11-02T00:00:00Z")
                self.assertEqual(mode, "attended-autonomous")
                self.assertIn("ignored unrecognized lease value", source)

        def test_unusable_fleet_file_fails_closed_whatever_the_lease(self):
            with tempfile.TemporaryDirectory() as d:
                for body in ('{"mode":"attended"}', '{"mode":"unattended"',
                             '{"mode":"attended","set_at":"soon"}'):
                    mode, _source = self.effective(d, body, "attended-autonomous")
                    self.assertEqual(mode, "unattended", body)

        def test_absent_fleet_leaves_the_lease_deciding(self):
            # 3b781 r2 (codex E2): an undated value is returned RAW with the fleet
            # file absent; each consumer applies its own pre-3b781 legacy rule.
            with tempfile.TemporaryDirectory() as d:
                cases = (("daytime-unattended", "daytime-unattended"),
                         ("daytime-unattended@2026-11-01T13:00:00Z", "daytime-unattended"),
                         ("unattended-overnight", "unattended-overnight"),
                         ("attended; was overnight-unattended",
                          "attended; was overnight-unattended"),
                         ("attended-autonomous", "attended-autonomous"),
                         ("fully-attended", "fully-attended"))
                for lease, want in cases:
                    mode, source = self.effective(d, None, lease)
                    self.assertEqual(mode, want, lease)
                    self.assertIn("fleet mode file absent", source, lease)
                self.assertEqual(self.effective(d, None, None), (None, "absent"))

    loader = unittest.TestLoader()
    suite = unittest.TestSuite(
        loader.loadTestsFromTestCase(cls)
        for cls in (TestParseLeaseRecord, TestReadFleet, TestEffectiveMode))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(_self_test())
    print("usage: _operating_mode.py --self-test (a library for the mode-reading hooks)",
          file=sys.stderr)
    sys.exit(2)
