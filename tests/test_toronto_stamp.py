"""Console stamp in Toronto local time only (maintainer and Architect directive 2026-11-04; the UTC
form refused, maintainer decision 2026-11-04): the shared _session_clock helper,
block-unstamped-turn-end.py and inject-session-timestamp.py. The clock-inject.py check is skipped
until that guardrails-owned hook is re-adopted (see its skip reason).

The hooks are loaded as modules (the TEST-ONLY SEAM of _load_sibling), so the helper loaded here is
the one they use; the instant is pinned by patching _session_clock._now."""

import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude/hooks"
UTC = timezone.utc
TORONTO = ZoneInfo("America/Toronto")

# (instant, expected stamp): both DST changes of 2026 and the directive itself (21:01Z).
BOUNDARIES = (
    (datetime(2026, 3, 8, 6, 59, tzinfo=UTC), "[2026-03-08 01:59 EST]"),
    (datetime(2026, 3, 8, 7, 0, tzinfo=UTC), "[2026-03-08 03:00 EDT]"),
    (datetime(2026, 11, 1, 5, 59, tzinfo=UTC), "[2026-11-01 01:59 EDT]"),
    (datetime(2026, 11, 1, 6, 0, tzinfo=UTC), "[2026-11-01 01:00 EST]"),
    (datetime(2026, 11, 4, 21, 1, tzinfo=UTC), "[2026-11-04 16:01 EST]"),
)
WINTER = datetime(2026, 1, 15, 17, 0, tzinfo=UTC)
SUMMER = datetime(2026, 7, 15, 16, 0, tzinfo=UTC)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TorontoStampTests(unittest.TestCase):
    def setUp(self):
        saved = sys.modules.get("_session_clock")
        self.addCleanup(lambda: sys.modules.__setitem__("_session_clock", saved) if saved
                        else sys.modules.pop("_session_clock", None))
        self.clock = _load(HOOKS / "_session_clock.py", "_session_clock")
        sys.modules["_session_clock"] = self.clock
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)

    def at(self, now):
        patcher = mock.patch.object(self.clock, "_now", lambda: now)
        patcher.start()
        self.addCleanup(patcher.stop)

    def transcript(self, start):
        path = self.tmp / "t.jsonl"
        path.write_text(json.dumps({"type": "user", "timestamp": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                    "message": {}}) + "\n", encoding="utf-8")
        return str(path)

    def hook(self, filename, modname):
        module = _load(HOOKS / filename, modname)
        module._is_worker = lambda: False
        module.maintainer_env = lambda: True
        return module

    def run_hook(self, module, payload):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(payload))), \
                mock.patch.object(sys, "argv", [module.__file__]), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = module.main()
        return rc, out.getvalue(), err.getvalue()

    def test_abbreviation_from_zoneinfo_at_dst_boundaries(self):
        for now, want in BOUNDARIES:
            with self.subTest(now=now):
                self.assertEqual(self.clock.format_stamp(now), want)
                self.assertTrue(want.endswith(" " + now.astimezone(TORONTO).tzname() + "]"))

    def test_stamp_ignores_process_zone(self):
        old = os.environ.get("TZ")
        self.addCleanup(time.tzset)
        self.addCleanup(lambda: os.environ.__setitem__("TZ", old) if old is not None
                        else os.environ.pop("TZ", None))
        for tz in ("UTC", "Asia/Tokyo"):
            os.environ["TZ"] = tz
            time.tzset()
            for now, want in BOUNDARIES:
                self.assertEqual(self.clock.format_stamp(now), want, tz)

    def test_winter_and_summer_stamps_conform_and_are_current(self):
        for now, stamp in ((WINTER, "[2026-01-15 12:00 EST]"), (SUMMER, "[2026-07-15 12:00 EDT]")):
            text = stamp + " done (session: 1h 0m)"
            tp = self.transcript(now - timedelta(hours=1))
            self.assertTrue(self.clock.conforms(text), text)
            self.assertTrue(self.clock.values_current(text, tp, now), text)
            self.assertEqual(self.clock.stamp_and_duration(tp, now), (stamp, "(session: 1h 0m)"))

    def test_wrong_or_skipped_abbreviation_rejected(self):
        for text in ("[2026-01-15 12:00 EDT] x (session: 1h 0m)",   # EDT in winter
                     "[2026-07-15 12:00 EST] x (session: 1h 0m)",   # EST in summer
                     "[2026-07-15 12:00 UTC] x (session: 1h 0m)",   # another zone
                     "[2026-03-08 02:30 EST] x (session: 1h 0m)",   # skipped by the spring change
                     "[2026-03-08 02:30 EDT] x (session: 1h 0m)"):
            self.assertFalse(self.clock.conforms(text), text)

    def test_repeated_autumn_hour_both_folds(self):
        edt, est = datetime(2026, 11, 1, 5, 30, tzinfo=UTC), datetime(2026, 11, 1, 6, 30, tzinfo=UTC)
        self.assertTrue(self.clock.values_current("[2026-11-01 01:30 EDT] x (session: 0h 0m)", None, edt))
        self.assertTrue(self.clock.values_current("[2026-11-01 01:30 EST] x (session: 0h 0m)", None, est))
        self.assertFalse(self.clock.values_current("[2026-11-01 01:30 EST] x (session: 0h 0m)", None, edt))
        self.assertFalse(self.clock.values_current("[2026-11-01 01:30 EDT] x (session: 0h 0m)", None, est))

    def test_legacy_utc_form_refused(self):
        # Toronto only (maintainer decision 2026-11-04): a current, otherwise correct UTC stamp
        # no longer conforms, and the Stop hook blocks it with the Toronto value for the re-send.
        text = "[2026-07-15 16:00Z] x (session: 1h 0m)"
        self.assertFalse(self.clock.conforms(text))
        self.assertFalse(self.clock.conforms("[2026-07-15 16:00:00Z] x (session: 1h 0m)"))
        self.assertFalse(hasattr(self.clock, "ACCEPT_LEGACY_UTC"))
        hook = self.hook("block-unstamped-turn-end.py", "block_unstamped_turn_end")
        self.at(SUMMER)
        tp = self.transcript(SUMMER - timedelta(hours=1))
        rc, _, err = self.run_hook(hook, {"transcript_path": tp, "last_assistant_message": text})
        self.assertEqual(rc, 2)
        self.assertIn("`[2026-07-15 12:00 EDT]`", err)
        self.assertIn("no longer conforms", err)

    def test_stop_hook_accepts_toronto_winter_and_summer(self):
        hook = self.hook("block-unstamped-turn-end.py", "block_unstamped_turn_end")
        for now, stamp, wrong in ((WINTER, "[2026-01-15 12:00 EST]", "[2026-01-15 12:00 EDT]"),
                                  (SUMMER, "[2026-07-15 12:00 EDT]", "[2026-07-15 12:00 EST]")):
            with self.subTest(stamp=stamp), mock.patch.object(self.clock, "_now", lambda now=now: now):
                tp = self.transcript(now - timedelta(hours=1))
                rc, _, err = self.run_hook(hook, {"transcript_path": tp,
                                                  "last_assistant_message": stamp + " ok (session: 1h 0m)"})
                self.assertEqual(rc, 0, err)
                rc, _, err = self.run_hook(hook, {"transcript_path": tp,
                                                  "last_assistant_message": wrong + " ok (session: 1h 0m)"})
                self.assertEqual(rc, 2)
                self.assertIn("Toronto", err)
                self.assertIn(f"`{stamp}`", err)
                self.assertIn("`(session: 1h 0m)`", err)

    def test_stop_hook_fails_open_without_zone(self):
        hook = self.hook("block-unstamped-turn-end.py", "block_unstamped_turn_end")
        self.at(SUMMER)
        tp = self.transcript(SUMMER - timedelta(hours=1))
        with mock.patch.object(self.clock, "STAMP_ZONE", "Nowhere/Missing"):
            self.assertEqual(self.clock.stamp_and_duration(tp), (None, None))
            rc, _, err = self.run_hook(hook, {"transcript_path": tp, "last_assistant_message": "no stamp"})
        self.assertEqual(rc, 0, err)

    def test_injected_instruction_names_toronto_form(self):
        hook = self.hook("inject-session-timestamp.py", "inject_session_timestamp")
        self.at(SUMMER)
        rc, out, err = self.run_hook(hook, {"transcript_path": self.transcript(SUMMER - timedelta(hours=1))})
        self.assertEqual(rc, 0, err)
        msg = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("start with `[2026-07-15 12:00 EDT]`", msg)
        self.assertIn("end with `(session: 1h 0m)`", msg)
        self.assertIn("Toronto", msg)
        self.assertIn("`[YYYY-MM-DD HH:MM EST]` (EDT in summer)", msg)
        self.assertNotIn("HH:MMZ", msg)
        self.assertNotIn("current UTC timestamp", msg)

    @unittest.skip("clock-inject.py is a guardrails-owned byte-identical copy, changed only by "
                   "re-adoption from the guardrails share; its Toronto local segment goes upstream "
                   "separately, so no grc test may require it. Remove this skip after re-adoption.")
    def test_clock_inject_local_segment_is_toronto(self):
        clock_inject = _load(HOOKS / "clock-inject.py", "clock_inject")
        for now, want in BOUNDARIES:
            line = clock_inject.clock_line(now)
            self.assertIn(": " + want[1:17] + ":00 " + want[18:21] + " | ", line)
            self.assertIn(now.strftime("| %Y-%m-%dT%H:%M:%SZ"), line)


if __name__ == "__main__":
    unittest.main()
