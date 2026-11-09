#!/usr/bin/env node
/* check_overflow.js: the sideways-scroll check for a site's pages (baseline 1.8.0 and later).

   Loads each page in headless Chromium at each width (default 320, 360, 390 and 1512 px), in the light and the
   dark colour scheme, and fails a page that scrolls sideways: the document is wider than the window, or a
   .tablewrap box (whose table may scroll inside it, by design) is itself wider than the window. It also fails a
   page that throws a script error or answers with an HTTP error. Requests to any origin other than --base are
   refused and counted, so the check never reaches the network and no outside service can change its answer.

   Requires Node.js 18 or later and the playwright package with its Chromium (npm install playwright, then
   npx playwright install chromium); it is a development tool, not served. Serve the built site locally first:
     python3 -m http.server 8000 --directory site &
     node .baseline/check_overflow.js --base http://127.0.0.1:8000 / /method/ /references/
   or list the pages in a file, 1 path per line (# starts a comment):
     node .baseline/check_overflow.js --base http://127.0.0.1:8000 --pages .baseline/pages.txt
   --widths 320,360,390,1512 sets the widths; --schemes light,dark sets the schemes.

   Exit status: 0 when every page passes at every width and scheme; 1 when any case fails or a page cannot be
   loaded (the check fails closed); 2 for a usage error. */
"use strict";
const fs = require("fs");

function usage(msg) {
  if (msg) { console.error("usage error: " + msg); }
  console.error("usage: node check_overflow.js --base <url> [--pages <file>] [--widths 320,360,390,1512] [--schemes light,dark] [path ...]");
  process.exit(2);
}

function parse(argv) {
  const o = { base: null, pages: [], widths: [320, 360, 390, 1512], schemes: ["light", "dark"] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => { if (i + 1 >= argv.length) { usage(a + " needs a value"); } return argv[++i]; };
    if (a === "--base") { o.base = val().replace(/\/+$/, ""); }
    else if (a === "--pages") {
      let text;
      const f = val();
      try { text = fs.readFileSync(f, "utf8"); } catch (e) { usage("cannot read " + f + ": " + e.message); }
      text.split(/\r?\n/).map((l) => l.replace(/#.*/, "").trim()).filter(Boolean).forEach((l) => o.pages.push(l));
    }
    else if (a === "--widths") { o.widths = val().split(",").map((x) => parseInt(x, 10)); if (o.widths.some((x) => !(x > 0))) { usage("--widths takes whole numbers"); } }
    else if (a === "--schemes") { o.schemes = val().split(","); if (o.schemes.some((x) => x !== "light" && x !== "dark")) { usage("--schemes takes light, dark or both"); } }
    else if (a.startsWith("--")) { usage("unknown option " + a); }
    else { o.pages.push(a); }
  }
  if (!o.base || !/^https?:\/\//.test(o.base)) { usage("--base must be an http or https URL"); }
  if (!o.pages.length) { usage("name at least 1 page"); }
  return o;
}

(async () => {
  const o = parse(process.argv.slice(2));
  let chromium;
  try { ({ chromium } = require("playwright")); } catch (e) { console.error("check_overflow.js needs the playwright package: " + e.message); process.exit(1); }
  const origin = new URL(o.base).origin;
  const browser = await chromium.launch();
  let cases = 0, failing = 0;
  for (const path of o.pages) {
    const url = o.base + (path.startsWith("/") ? path : "/" + path);
    for (const scheme of o.schemes) {
      for (const w of o.widths) {
        cases++;
        const page = await browser.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
        const errors = [];
        let refused = 0;
        await page.route("**/*", (r) => { if (new URL(r.request().url()).origin === origin) { r.continue(); } else { refused++; r.abort(); } });
        page.on("pageerror", (e) => errors.push("script error: " + String(e.message || e)));
        let res = null;
        try { res = await page.goto(url, { waitUntil: "load", timeout: 30000 }); } catch (e) { errors.push("load failed: " + e.message.split("\n")[0]); }
        if (res && res.status() >= 400) { errors.push("HTTP " + res.status()); }
        let m = null;
        if (res) {
          m = await page.evaluate(() => {
            const vw = document.documentElement.clientWidth;
            const boxes = [...document.querySelectorAll(".tablewrap")].map((b) => Math.round(b.getBoundingClientRect().right - vw)).filter((d) => d > 0);
            return { doc: document.documentElement.scrollWidth, vw, boxes };
          });
        }
        const over = m ? m.doc - m.vw : 0;
        const bad = errors.length > 0 || over > 0 || (m && m.boxes.length > 0);
        if (bad) {
          failing++;
          const what = [];
          if (over > 0) { what.push("page " + m.doc + " px wide in a " + m.vw + " px window"); }
          if (m && m.boxes.length) { what.push(m.boxes.length + " table box(es) past the window edge by " + m.boxes.join(", ") + " px"); }
          what.push(...errors);
          console.log("FAIL " + path + " " + w + " px " + scheme + ": " + what.join("; "));
        }
        if (refused) { console.log("note " + path + " " + w + " px " + scheme + ": refused " + refused + " request(s) to other origins"); }
        await page.close();
      }
    }
  }
  await browser.close();
  console.log("RESULT: " + (failing ? "fail" : "pass") + " (" + o.pages.length + " page" + (o.pages.length === 1 ? "" : "s") + ", " + cases + " cases, " + failing + " failing)");
  process.exit(failing ? 1 : 0);
})().catch((e) => { console.error("ERROR: " + (e && e.message ? e.message : e)); console.log("RESULT: fail (the check could not run)"); process.exit(1); });
