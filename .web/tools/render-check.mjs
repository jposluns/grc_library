#!/usr/bin/env node
/* render-check.mjs: the /draft tree's render acceptance check (PR 2b).
 *
 * NEVER RUN IN CI. A development-machine tool for Node 22 with a local
 * Chrome; it is run by hand after a build and its one-line-per-combination
 * output goes into the review notes. Exact command, from the repository root
 * after `python3 .web/build.py`:
 *
 *     node .web/tools/render-check.mjs
 *
 * Options: --dist <dir> (default .web/dist), --chrome <binary> (default
 * google-chrome), --port <http port> (default 8799).
 *
 * No dependencies: the global fetch and WebSocket of Node 22,
 * node:child_process for the servers, node:fs to list the pages. It serves
 * the dist tree with `python3 -m http.server`, drives a headless Chrome over
 * the DevTools protocol, and checks, per draft page, per width in 390, 820,
 * 1180, 1512 and 2000 px, per scheme light and dark:
 *
 *   - no horizontal scroll (scrollWidth <= innerWidth);
 *   - exactly 1 footer Invertocat displayed and no blank footer tile;
 *   - the top bar's links on 1 row;
 *   - the landing page within 2 screens at 1180 by 820 (scrollHeight <= 1640);
 *   - the hero statement on 1 line at 1440 px and above (light and dark).
 *
 * And, on pages whose rail lists in-page sections, at 1180 and 390 px in
 * light and dark, the rail mark (rail.js, aria-current="location"):
 *
 *   - follows scrolling (a section scrolled past the reading line is marked);
 *   - moves to the last section at the end of the page;
 *   - follows a rail click;
 *   - marks the target section on a page opened at #id;
 *   - marks at most 1 link at every sampled moment;
 *   - with JavaScript off, marks none.
 *
 * One row per combination; non-zero exit on any failure.
 */

import { spawn } from "node:child_process";
import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import process from "node:process";

export const WIDTHS = [390, 820, 1180, 1512, 2000];
export const SCHEMES = ["light", "dark"];
export const RAIL_WIDTHS = [390, 1180];
export const VIEW_HEIGHT = 820;
export const LANDING_MAX_HEIGHT = 1640;
export const STATEMENT_ONE_LINE_MIN_WIDTH = 1440;

/* ---------------------------------------------------------------- pure -- */

/** The draft page URLs under a dist tree, from its relative HTML paths. */
export function draftPagesFromRels(rels) {
  const pages = [];
  for (const rel of rels) {
    if (!rel.startsWith("draft/") || !rel.endsWith(".html")) continue;
    if (rel.endsWith("/index.html")) {
      pages.push("/" + rel.slice(0, -"index.html".length));
    } else if (rel === "draft/index.html") {
      pages.push("/draft/");
    } else {
      pages.push("/" + rel);
    }
  }
  return pages.sort();
}

/** Every (page, width, scheme) combination the viewport checks run on. */
export function renderMatrix(pages) {
  const rows = [];
  for (const page of pages) {
    for (const width of WIDTHS) {
      for (const scheme of SCHEMES) {
        rows.push({ page, width, scheme });
      }
    }
  }
  return rows;
}

/**
 * Evaluate one combination's measurements. `m` is the object the in-page
 * probe returns; returns the failure strings (empty = pass).
 */
export function evaluateViewportChecks(m, { page, width }) {
  const failures = [];
  if (m.scrollWidth > m.innerWidth) {
    failures.push(`horizontal scroll (${m.scrollWidth} > ${m.innerWidth})`);
  }
  if (m.invertocatsVisible !== 1) {
    failures.push(`${m.invertocatsVisible} Invertocats displayed (want 1)`);
  }
  if (m.blankTiles > 0) {
    failures.push(`${m.blankTiles} blank footer tile(s)`);
  }
  if (m.navRows !== 1) {
    failures.push(`top bar links on ${m.navRows} rows (want 1)`);
  }
  if (page === "/draft/" && width === 1180
      && m.scrollHeight > LANDING_MAX_HEIGHT) {
    failures.push(
      `landing is ${m.scrollHeight}px tall (max ${LANDING_MAX_HEIGHT})`);
  }
  if (m.statementLines !== null && width >= STATEMENT_ONE_LINE_MIN_WIDTH
      && m.statementLines !== 1) {
    failures.push(`statement on ${m.statementLines} lines at ${width}px`);
  }
  return failures;
}

/**
 * Evaluate one rail-mark run. `samples` is the ordered list of states the
 * driver records; each has `at` (a label) and `marked` (the marked rail-link
 * hrefs at that moment). `sections` is the rail's section ids in page order.
 */
export function evaluateRailChecks(samples, sections) {
  const failures = [];
  const byAt = new Map(samples.map((s) => [s.at, s]));
  for (const s of samples) {
    if (s.marked.length > 1) {
      failures.push(`${s.at}: ${s.marked.length} links marked (max 1)`);
    }
  }
  const last = sections[sections.length - 1];
  const expect = (at, id, why) => {
    const s = byAt.get(at);
    if (!s) {
      failures.push(`${at}: no sample recorded`);
    } else if (!(s.marked.length === 1 && s.marked[0] === `#${id}`)) {
      failures.push(`${at}: marked ${JSON.stringify(s.marked)}, want #${id} (${why})`);
    }
  };
  expect("scrolled-to-second", sections[1],
         "the mark follows scrolling");
  expect("page-end", last, "the last section is marked at the end");
  expect("rail-click-first", sections[0], "the mark follows a rail click");
  expect("opened-at-hash", sections[1],
         "a page opened at #id marks that section");
  const noScript = byAt.get("javascript-off");
  if (!noScript) {
    failures.push("javascript-off: no sample recorded");
  } else if (noScript.marked.length !== 0) {
    failures.push(
      `javascript-off: ${JSON.stringify(noScript.marked)} marked (want none)`);
  }
  return failures;
}

/* ------------------------------------------------------------- driving -- */

function listHtmlRels(dist) {
  const rels = [];
  const walk = (dir, prefix) => {
    for (const name of readdirSync(dir)) {
      const full = join(dir, name);
      const rel = prefix ? `${prefix}/${name}` : name;
      if (statSync(full).isDirectory()) walk(full, rel);
      else if (name.endsWith(".html")) rels.push(rel);
    }
  };
  walk(dist, "");
  return rels;
}

const PROBE = `(() => {
  const doc = document.documentElement;
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).display !== "none";
  };
  const invertocats = [...document.querySelectorAll(
    'footer .tail img[src*="github-invertocat"]')].filter(visible).length;
  const tiles = [...document.querySelectorAll("footer .bar a.card")];
  const blankTiles = tiles.filter((t) => !t.querySelector("img") || !visible(t)).length;
  const navLinks = [...document.querySelectorAll("nav.nav a")];
  const navRows = new Set(navLinks.map(
    (a) => Math.round(a.getBoundingClientRect().top))).size;
  const statement = document.querySelector(".statement");
  let statementLines = null;
  if (statement) {
    const style = getComputedStyle(statement);
    statementLines = Math.round(
      statement.getBoundingClientRect().height / parseFloat(style.lineHeight));
  }
  return JSON.stringify({
    scrollWidth: doc.scrollWidth,
    scrollHeight: doc.scrollHeight,
    innerWidth: window.innerWidth,
    invertocatsVisible: invertocats,
    blankTiles,
    navRows,
    statementLines,
  });
})()`;

const MARKED = `JSON.stringify([...document.querySelectorAll(
  'nav.rail a[aria-current="location"]')].map((a) => a.getAttribute("href")))`;

const RAIL_SECTIONS = `JSON.stringify([...document.querySelectorAll(
  'nav.rail ol a[href^="#"]')].map((a) => a.getAttribute("href").slice(1)))`;

class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    ws.addEventListener("message", (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      }
    });
  }

  send(method, params = {}, sessionId = undefined) {
    this.id += 1;
    const id = this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function evaluate(cdp, sessionId, expression) {
  const result = await cdp.send(
    "Runtime.evaluate", { expression, returnByValue: true }, sessionId);
  if (result.exceptionDetails) {
    throw new Error(`in-page probe failed: ${result.exceptionDetails.text}`);
  }
  return JSON.parse(result.result.value);
}

async function configure(cdp, sessionId, width, scheme, scriptOff = false) {
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width, height: VIEW_HEIGHT, deviceScaleFactor: 1, mobile: width < 600,
  }, sessionId);
  await cdp.send("Emulation.setEmulatedMedia", {
    features: [{ name: "prefers-color-scheme", value: scheme }],
  }, sessionId);
  await cdp.send(
    "Emulation.setScriptExecutionDisabled", { value: scriptOff }, sessionId);
}

async function navigate(cdp, sessionId, url) {
  await cdp.send("Page.navigate", { url }, sessionId);
  await sleep(350);
}

async function main() {
  const args = process.argv.slice(2);
  const opt = (name, fallback) => {
    const i = args.indexOf(name);
    return i >= 0 ? args[i + 1] : fallback;
  };
  const dist = opt("--dist", ".web/dist");
  const chromeBin = opt("--chrome", "google-chrome");
  const port = Number(opt("--port", "8799"));

  const pages = draftPagesFromRels(listHtmlRels(dist));
  if (pages.length === 0) {
    console.error(`no draft pages under ${dist}; run python3 .web/build.py first`);
    return 2;
  }

  const server = spawn(
    "python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"],
    { cwd: dist, stdio: "ignore" });
  const chrome = spawn(chromeBin, [
    "--headless=new", "--remote-debugging-port=0",
    `--user-data-dir=${process.env.TMPDIR || "/tmp"}/render-check-profile`,
    "--no-first-run",
  ], { stdio: ["ignore", "ignore", "pipe"] });
  let failures = 0;
  try {
    let devtools = "";
    chrome.stderr.on("data", (chunk) => { devtools += chunk; });
    for (let i = 0; i < 100 && !/ws:\/\/\S+/.test(devtools); i += 1) {
      await sleep(100);
    }
    const match = devtools.match(/ws:\/\/\S+/);
    if (!match) throw new Error("Chrome's DevTools endpoint did not appear");
    const browserWs = new WebSocket(match[0]);
    await new Promise((resolve, reject) => {
      browserWs.addEventListener("open", resolve);
      browserWs.addEventListener("error", reject);
    });
    const cdp = new Cdp(browserWs);
    const { targetId } = await cdp.send(
      "Target.createTarget", { url: "about:blank" });
    const { sessionId } = await cdp.send(
      "Target.attachToTarget", { targetId, flatten: true });
    await cdp.send("Page.enable", {}, sessionId);
    await cdp.send("Runtime.enable", {}, sessionId);
    const base = `http://127.0.0.1:${port}`;

    for (const row of renderMatrix(pages)) {
      await configure(cdp, sessionId, row.width, row.scheme);
      await navigate(cdp, sessionId, base + row.page);
      const metrics = await evaluate(cdp, sessionId, PROBE);
      const bad = evaluateViewportChecks(metrics, row);
      const status = bad.length === 0 ? "ok" : `FAIL ${bad.join("; ")}`;
      console.log(`${row.page} ${row.width}px ${row.scheme}: ${status}`);
      failures += bad.length;
    }

    for (const page of pages) {
      await configure(cdp, sessionId, 1180, "light");
      await navigate(cdp, sessionId, base + page);
      const sections = await evaluate(cdp, sessionId, RAIL_SECTIONS);
      if (sections.length < 2) continue; // no section rail on this page
      for (const width of RAIL_WIDTHS) {
        for (const scheme of SCHEMES) {
          const samples = [];
          const record = async (at) => samples.push(
            { at, marked: await evaluate(cdp, sessionId, MARKED) });
          await configure(cdp, sessionId, width, scheme);
          await navigate(cdp, sessionId, base + page);
          await evaluate(cdp, sessionId, `(document.getElementById(
            ${JSON.stringify(sections[1])}).scrollIntoView(), "[]")`);
          await sleep(250);
          await record("scrolled-to-second");
          await evaluate(cdp, sessionId,
            '(window.scrollTo(0, document.documentElement.scrollHeight), "[]")');
          await sleep(250);
          await record("page-end");
          await evaluate(cdp, sessionId, `(document.querySelector(
            'nav.rail ol a[href="#' + ${JSON.stringify(sections[0])} + '"]'
          ).click(), "[]")`);
          await sleep(250);
          await record("rail-click-first");
          await navigate(cdp, sessionId,
            `${base}${page}#${sections[1]}`);
          await sleep(250);
          await record("opened-at-hash");
          await configure(cdp, sessionId, width, scheme, true);
          await navigate(cdp, sessionId, base + page);
          await record("javascript-off");
          await configure(cdp, sessionId, width, scheme, false);
          const bad = evaluateRailChecks(samples, sections);
          const status = bad.length === 0 ? "ok" : `FAIL ${bad.join("; ")}`;
          console.log(`${page} rail ${width}px ${scheme}: ${status}`);
          failures += bad.length;
        }
      }
    }
  } finally {
    chrome.kill();
    server.kill();
  }
  if (failures > 0) {
    console.error(`render-check: ${failures} failure(s)`);
    return 1;
  }
  console.log("render-check: every combination passed");
  return 0;
}

const invokedDirectly = process.argv[1]
  && import.meta.url.endsWith(process.argv[1].split("/").pop());
if (invokedDirectly && !process.env.RENDER_CHECK_NO_MAIN) {
  main().then(
    (code) => process.exit(code),
    (error) => { console.error(error.message); process.exit(2); },
  );
}
