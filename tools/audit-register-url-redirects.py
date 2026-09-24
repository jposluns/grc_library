#!/usr/bin/env python3
"""Advisory network audit of the canonical-citations register's upstream URLs.

WHAT THIS IS (and is NOT). An orchestrator dev-AID, not an audit gate. The
citation-verification specification's fetch rule forbids an upstream check that
redirects to a domain outside the publisher allow-list, but CI has no network
egress, so no gate can follow a URL. This tool follows every URL in the
``Upstream check location`` column of
[`governance/register-canonical-citations.md`] and reports:

  UNLISTED      the URL's own host is not on the allow-list
  OFF-LIST      a redirect hop lands on a host that is not on the allow-list
  NON-200       the chain ends on a final HTTP status other than 200
  UNKNOWN       the URL could not be fetched (timeout, TLS or DNS error, too
                many redirects); ignorance is reported, never read as a pass
  cross-domain  (note, not a finding) a redirect between two DIFFERENT
                allow-listed hosts, listed so a reviewer can see it

It is named ``audit-*`` (not ``lint-*``) so the gate machinery does not discover
it, and it is NOT wired into ``run_all_audits.sh``, ``quality.yml`` or
``.pre-commit-config.yaml``. Run it after a register edit and on the currency
cadence. It exits 0 by default; ``--strict`` exits 1 when any finding (UNKNOWN
included) is reported. The self-test lives behind ``--self-test``.

Residue, stated at the point of use:
- The allow-list read here is the external-link gate's ``ALLOW_LIST`` (with the
  gate's own suffix matcher), used as the proxy for the specification's
  section 7.1 publisher table. The two surfaces are reconciled by hand today; a
  mechanical parity check is a separate backlog item.
- A NON-200 can be a publisher's bot protection (a 403 to an unrecognized
  client) rather than a dead page; the tool reports the status and a human
  decides.
- A redirect performed by page script or a meta refresh is invisible here;
  only HTTP 3xx redirects are followed.

Exit codes:
  0   report printed (default), or --strict with no findings
  1   --strict and at least one finding
  2   usage or input error (register unreadable)
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import unittest
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = REPO_ROOT / "governance" / "register-canonical-citations.md"
URL_RE = re.compile(r"https?://[^\s)|>\]]+")
MAX_REDIRECTS = 10
USER_AGENT = "Mozilla/5.0 (compatible; grc-library-register-url-audit)"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    tools_dir = str(REPO_ROOT / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    spec.loader.exec_module(mod)
    return mod


def register_urls(text: str) -> list[tuple[str, str]]:
    """Return (standard_id, url) for every URL in each row's upstream cell."""
    currency = _load("audit_register_currency_mod", "tools/audit-register-currency.py")
    pairs: list[tuple[str, str]] = []
    for row in currency.parse_register(text):
        for url in URL_RE.findall(row["upstream"]):
            pairs.append((row["standard_id"], url.rstrip(".,;")))
    return pairs


def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower().rstrip(".")


def classify(chain: list[str], status: int | None, error: str | None,
             is_allowed) -> tuple[list[str], list[str]]:
    """Pure decision: (findings, notes) for one fetched chain.

    ``chain`` is the start URL followed by each redirect target in order;
    ``status`` the final HTTP status (None when unknown); ``error`` a fetch error
    text (None on success); ``is_allowed`` a host -> bool predicate.
    """
    findings: list[str] = []
    notes: list[str] = []
    start = host_of(chain[0])
    if not is_allowed(start):
        findings.append(f"UNLISTED host {start}")
    prev = start
    for hop in chain[1:]:
        h = host_of(hop)
        if not is_allowed(h):
            findings.append(f"OFF-LIST redirect {prev} -> {h} ({hop})")
        elif h != prev:
            notes.append(f"cross-domain redirect {prev} -> {h}")
        prev = h
    if error is not None:
        findings.append(f"UNKNOWN ({error})")
    elif status != 200:
        findings.append(f"NON-200 final status {status}")
    return findings, notes


class _Recorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append(newurl)
        if len(self.chain) > MAX_REDIRECTS:
            raise urllib.error.URLError(f"more than {MAX_REDIRECTS} redirects")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_chain(url: str, timeout: float) -> tuple[list[str], int | None, str | None]:
    """Thin observer: follow HTTP redirects; return (chain, final status, error)."""
    rec = _Recorder()
    opener = urllib.request.build_opener(rec)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(req, timeout=timeout) as resp:
            return [url] + rec.chain, resp.status, None
    except urllib.error.HTTPError as exc:  # a final non-2xx is a status, not ignorance
        return [url] + rec.chain, exc.code, None
    except Exception as exc:  # noqa: BLE001 (any fetch failure is reported as UNKNOWN)
        return [url] + rec.chain, None, f"{type(exc).__name__}: {exc}"[:160]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Advisory register upstream-URL redirect audit.")
    ap.add_argument("--register", default=str(DEFAULT_REGISTER))
    ap.add_argument("--only", help="only URLs whose standard id or URL contains this text")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--strict", action="store_true", help="exit 1 when any finding is reported")
    ap.add_argument("--self-test", action="store_true", help="run inline unit tests")
    args = ap.parse_args(argv)
    if args.self_test:
        return _run_self_test()
    try:
        text = Path(args.register).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read register: {exc}", file=sys.stderr)
        return 2
    gate = _load("lint_external_link_domains_mod", "tools/lint-external-link-domains.py")
    engine = gate._engine()

    def allowed(h: str) -> bool:
        return engine.is_allowed(h, allow_list=gate.ALLOW_LIST)

    pairs = register_urls(text)
    if args.only:
        pairs = [p for p in pairs if args.only.lower() in (p[0] + " " + p[1]).lower()]
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        results = list(pool.map(lambda p: fetch_chain(p[1], args.timeout), pairs))
    n_find = n_unknown = 0
    for (sid, url), (chain, status, error) in zip(pairs, results):
        findings, notes = classify(chain, status, error, allowed)
        n_find += bool(findings)
        n_unknown += error is not None
        for f in findings:
            print(f"FINDING {sid} | {url} | {f}")
        for n in notes:
            print(f"note    {sid} | {url} | {n}")
    print(f"SUMMARY: {len(pairs)} URLs checked; {n_find} with findings "
          f"({n_unknown} UNKNOWN, not verified either way)")
    return 1 if (args.strict and n_find) else 0


class _SelfTest(unittest.TestCase):
    ALLOW = {"slsa.dev", "spdx.dev", "iso.org"}

    def ok(self, h: str) -> bool:
        return h in self.ALLOW or any(h.endswith("." + a) for a in self.ALLOW)

    def test_clean_same_domain_redirect(self):
        f, n = classify(["https://slsa.dev/spec", "https://slsa.dev/spec/v1.2/"], 200, None, self.ok)
        self.assertEqual((f, n), ([], []))

    def test_off_list_redirect(self):
        f, _ = classify(["https://spdx.dev/x", "https://evil.example/x"], 200, None, self.ok)
        self.assertEqual(len(f), 1)
        self.assertTrue(f[0].startswith("OFF-LIST"))

    def test_unlisted_start(self):
        f, _ = classify(["https://spdx.org/specifications"], 200, None, self.ok)
        self.assertTrue(f[0].startswith("UNLISTED"))

    def test_cross_domain_between_allowed_is_note(self):
        f, n = classify(["https://iso.org/a", "https://www.spdx.dev/b"], 200, None, self.ok)
        self.assertEqual(f, [])
        self.assertEqual(len(n), 1)

    def test_non_200(self):
        f, _ = classify(["https://iso.org/a"], 403, None, self.ok)
        self.assertEqual(f, ["NON-200 final status 403"])

    def test_error_is_unknown_not_pass(self):
        f, _ = classify(["https://iso.org/a"], None, "URLError: timed out", self.ok)
        self.assertEqual(f, ["UNKNOWN (URLError: timed out)"])

    def test_register_urls_parses_live_register(self):
        pairs = register_urls(DEFAULT_REGISTER.read_text(encoding="utf-8"))
        self.assertGreater(len(pairs), 100)
        self.assertTrue(all(u.startswith("http") for _, u in pairs))


def _run_self_test() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_SelfTest)
    ok = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
