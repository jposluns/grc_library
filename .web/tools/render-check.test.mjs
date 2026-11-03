/* Self-contained unit tests for render-check.mjs's pure logic (no browser,
 * no server, no network). Run by hand with Node 22:
 *
 *     node --test .web/tools/render-check.test.mjs
 *
 * NEVER RUN IN CI, like the tool itself. These test the page enumeration, the
 * check matrix, the viewport assertions and the rail-mark assertions; driving
 * a real Chrome is the tool's manual job.
 */

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  WIDTHS, SCHEMES, RAIL_WIDTHS, LANDING_MAX_HEIGHT,
  draftPagesFromRels, renderMatrix,
  evaluateViewportChecks, evaluateRailChecks,
} from "./render-check.mjs";

const CLEAN = {
  scrollWidth: 1180, scrollHeight: 1500, innerWidth: 1180,
  invertocatsVisible: 1, blankTiles: 0, navRows: 1, statementLines: null,
};

test("draftPagesFromRels keeps draft HTML only, as URL paths", () => {
  const pages = draftPagesFromRels([
    "index.html", "404.html", "robots.txt",
    "draft/index.html", "draft/404.html", "draft/browse/index.html",
    "draft/governance/index.html", "draft/assets/baseline/baseline.css",
    "v3/search/index.html",
  ]);
  assert.deepEqual(pages, [
    "/draft/", "/draft/404.html", "/draft/browse/", "/draft/governance/",
  ]);
});

test("renderMatrix is every page by width by scheme", () => {
  const rows = renderMatrix(["/draft/", "/draft/browse/"]);
  assert.equal(rows.length, 2 * WIDTHS.length * SCHEMES.length);
  assert.deepEqual(rows[0], { page: "/draft/", width: 390, scheme: "light" });
  assert.ok(RAIL_WIDTHS.every((w) => WIDTHS.includes(w)),
    "the rail runs reuse matrix widths");
});

test("a clean measurement passes", () => {
  assert.deepEqual(
    evaluateViewportChecks(CLEAN, { page: "/draft/browse/", width: 1180 }),
    []);
});

test("horizontal scroll fails", () => {
  const bad = evaluateViewportChecks(
    { ...CLEAN, scrollWidth: 1300 }, { page: "/draft/browse/", width: 1180 });
  assert.equal(bad.length, 1);
  assert.match(bad[0], /horizontal scroll/);
});

test("Invertocat count and blank tiles fail", () => {
  const bad = evaluateViewportChecks(
    { ...CLEAN, invertocatsVisible: 2, blankTiles: 1 },
    { page: "/draft/browse/", width: 1180 });
  assert.equal(bad.length, 2);
  assert.match(bad[0], /Invertocats/);
  assert.match(bad[1], /blank footer tile/);
});

test("a wrapped top bar fails", () => {
  const bad = evaluateViewportChecks(
    { ...CLEAN, navRows: 2 }, { page: "/draft/404.html", width: 390 });
  assert.equal(bad.length, 1);
  assert.match(bad[0], /top bar/);
});

test("the landing 2-screen cap applies at 1180 only", () => {
  const tall = { ...CLEAN, scrollHeight: LANDING_MAX_HEIGHT + 1 };
  assert.match(
    evaluateViewportChecks(tall, { page: "/draft/", width: 1180 })[0],
    /landing/);
  assert.deepEqual(
    evaluateViewportChecks(tall, { page: "/draft/", width: 390 }), []);
  assert.deepEqual(
    evaluateViewportChecks(tall, { page: "/draft/browse/", width: 1180 }), []);
});

test("the statement must sit on 1 line at 1440 px and above", () => {
  const two = { ...CLEAN, statementLines: 2 };
  assert.match(
    evaluateViewportChecks(two, { page: "/draft/", width: 1512 })[0],
    /statement/);
  assert.deepEqual(
    evaluateViewportChecks(two, { page: "/draft/", width: 1180 }), []);
  assert.deepEqual(
    evaluateViewportChecks(
      { ...CLEAN, statementLines: 1 }, { page: "/draft/", width: 2000 }), []);
});

const SECTIONS = ["d-1", "d-2", "d-3"];
const GOOD_SAMPLES = [
  { at: "scrolled-to-second", marked: ["#d-2"] },
  { at: "page-end", marked: ["#d-3"] },
  { at: "rail-click-first", marked: ["#d-1"] },
  { at: "opened-at-hash", marked: ["#d-2"] },
  { at: "javascript-off", marked: [] },
];

test("a correct rail-mark run passes", () => {
  assert.deepEqual(evaluateRailChecks(GOOD_SAMPLES, SECTIONS), []);
});

test("the mark must follow scrolling", () => {
  const samples = GOOD_SAMPLES.map((s) =>
    s.at === "scrolled-to-second" ? { ...s, marked: ["#d-1"] } : s);
  const bad = evaluateRailChecks(samples, SECTIONS);
  assert.equal(bad.length, 1);
  assert.match(bad[0], /follows scrolling/);
});

test("the last section is marked at the end of the page", () => {
  const samples = GOOD_SAMPLES.map((s) =>
    s.at === "page-end" ? { ...s, marked: ["#d-2"] } : s);
  assert.match(evaluateRailChecks(samples, SECTIONS)[0], /last section/);
});

test("the mark follows a rail click and an opening hash", () => {
  let samples = GOOD_SAMPLES.map((s) =>
    s.at === "rail-click-first" ? { ...s, marked: [] } : s);
  assert.match(evaluateRailChecks(samples, SECTIONS)[0], /rail click/);
  samples = GOOD_SAMPLES.map((s) =>
    s.at === "opened-at-hash" ? { ...s, marked: ["#d-1"] } : s);
  assert.match(evaluateRailChecks(samples, SECTIONS)[0], /opened at #id/);
});

test("more than 1 marked link fails, wherever it happens", () => {
  const samples = GOOD_SAMPLES.map((s) =>
    s.at === "page-end" ? { ...s, marked: ["#d-2", "#d-3"] } : s);
  const bad = evaluateRailChecks(samples, SECTIONS);
  assert.ok(bad.some((b) => /max 1/.test(b)));
});

test("with JavaScript off no link may be marked", () => {
  const samples = GOOD_SAMPLES.map((s) =>
    s.at === "javascript-off" ? { ...s, marked: ["#d-1"] } : s);
  assert.match(
    evaluateRailChecks(samples, SECTIONS).pop(), /want none/);
});

test("a missing sample is a failure, never a silent pass", () => {
  const bad = evaluateRailChecks([], SECTIONS);
  assert.equal(bad.length, 5);
  for (const line of bad) assert.match(line, /no sample recorded/);
});
