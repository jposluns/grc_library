/* matrix.js: column presets for a matrix table (from 1.5.0), column toggles and a column highlight (from 1.7.0).
   Markup: presets anywhere on the page, as buttons or links, each with data-preset (the column keys it shows,
           space-separated) and data-preset-id (its name in the address): <a href="..." data-preset="iso27001 csf soc2"
           data-preset-id="security">Security</a>; the All preset has data-preset="" and shows every column.
           <p class="matrix-status" role="status" aria-live="polite" data-matrix-status></p>
           <table class="matrix sticky sticky-col" data-matrix> with data-col="<key>" on every th and td of a preset
           column; the row-header column carries no data-col and always shows. 1 matrix per page, 1 header row.
   Choosing a preset hides the other columns with the hidden attribute and writes the status ("View: Security.
   Showing 3 of 8 columns."). The chosen preset carries aria-pressed="true" when it is a button (the others "false"),
   and aria-current="true" when it is a link (the others none): a link keeps its link role and leads to a page that
   resolves. A modified click (new tab, new window) is left to the browser. ?view=<preset-id> chooses a preset on
   load (an unknown id is ignored); a choice is written back with history.replaceState, and All removes the parameter.
   Without this script every column shows and each preset is a plain link. No colspan handling: by design the
   matrix has a single header row.
   From 1.7.0, each opt-in by markup:
   - Column toggles: <div class="matrix-toggles" data-col-toggles hidden> holding <button type="button"
     data-col="<key>" aria-pressed="true"> per column (in labelled groups if wanted). The script reveals the
     container; a press shows or hides that column (hidden on its th, td and any col[data-col]), keeps focus on the
     button, and writes the status ("Showing 4 of 20 columns.", or the preset's wording when the columns shown are
     exactly a preset's). Toggles and presets stay in sync. The address carries ?cols=<key>+<key> for a set that is
     no preset and ?view= for a set that is one; ?cols= is read on load only where toggles exist.
   - Column highlight: data-col-highlight on the table. Hovering or focusing a cell adds the class colhl to every
     cell sharing its data-col, and removes it on leaving; it never moves focus.
   From 1.8.0: while every visible column header carries the same data-grp, the table gets data-one-grp and the
   group tags (.grp) are not shown, since they would repeat 1 name on every column and only add width; they return
   as soon as a second group is visible. The coloured group accent under each header stays. */
(function () {
  "use strict";
  var table = document.querySelector("table[data-matrix]");
  if (!table) { return; }
  var slice = function (list) { return Array.prototype.slice.call(list); };
  var presets = slice(document.querySelectorAll("[data-preset]"));
  var toggles = slice(document.querySelectorAll("[data-col-toggles] button[data-col]"));
  var highlight = table.hasAttribute("data-col-highlight");
  if (!presets.length && !toggles.length && !highlight) { return; }
  var status = document.querySelector("[data-matrix-status]");
  var heads = slice(table.querySelectorAll("thead th[data-col]"));
  var cells = slice(table.querySelectorAll("th[data-col], td[data-col], col[data-col]"));
  var urlOK = !!(window.URLSearchParams && window.history && window.history.replaceState);

  function col(el) { return (el.getAttribute("data-col") || "").toLowerCase(); }
  function keys(p) { return (p.getAttribute("data-preset") || "").toLowerCase().split(/\s+/).filter(Boolean); }
  function label(p) {
    var text = p.textContent;
    Array.prototype.forEach.call(p.querySelectorAll(".vh, .n"), function (v) { text = text.replace(v.textContent, ""); });
    return text.replace(/\s+/g, " ").trim();
  }
  function shownKeys() { return heads.filter(function (h) { return !h.hidden; }).map(col); }
  function sameSet(a, b) { return a.length === b.length && a.every(function (k) { return b.indexOf(k) >= 0; }); }
  function syncToggles() {
    var shown = shownKeys();
    toggles.forEach(function (t) { t.setAttribute("aria-pressed", shown.indexOf(col(t)) >= 0 ? "true" : "false"); });
  }
  function groupTags() {
    var grps = heads.filter(function (h) { return !h.hidden; }).map(function (h) { return h.getAttribute("data-grp") || ""; });
    var one = grps.length > 0 && grps[0] !== "" && grps.every(function (g) { return g === grps[0]; });
    if (one) { table.setAttribute("data-one-grp", ""); } else { table.removeAttribute("data-one-grp"); }
  }
  function writeAddress(set) {
    if (!urlOK) { return; }
    var s = new URLSearchParams(window.location.search);
    Object.keys(set).forEach(function (k) { if (set[k]) { s.set(k, set[k]); } else { s.delete(k); } });
    var qs = s.toString();
    window.history.replaceState(window.history.state, "", window.location.pathname + (qs ? "?" + qs : "") + window.location.hash);
  }

  function choose(p, write) {
    var k = keys(p);
    cells.forEach(function (c) {
      c.hidden = k.length > 0 && k.indexOf(col(c)) < 0;
    });
    presets.forEach(function (q) {
      var mine = q === p;
      if (q.tagName === "A") {
        if (mine) { q.setAttribute("aria-current", "true"); } else { q.removeAttribute("aria-current"); }
      } else {
        q.setAttribute("aria-pressed", mine ? "true" : "false");
      }
    });
    var shown = heads.filter(function (h) { return !h.hidden; }).length;
    if (status) { status.textContent = "View: " + label(p) + ". Showing " + shown + " of " + heads.length + " columns."; }
    syncToggles();
    groupTags();
    if (write) {
      var id = p.getAttribute("data-preset-id");
      writeAddress(toggles.length ? { view: k.length && id ? id : "", cols: "" } : { view: k.length && id ? id : "" });
    }
  }

  /* Show exactly the columns in `shown` (from the toggles or ?cols=). A set that is a preset's is that preset. */
  function showSet(shown, write) {
    var all = heads.map(col);
    var match = presets.filter(function (p) { var k = keys(p); return sameSet(k.length ? k : all, shown); })[0];
    if (match) { choose(match, write); return; }
    cells.forEach(function (c) { c.hidden = shown.indexOf(col(c)) < 0; });
    presets.forEach(function (q) {
      if (q.tagName === "A") { q.removeAttribute("aria-current"); } else { q.setAttribute("aria-pressed", "false"); }
    });
    if (status) { status.textContent = "Showing " + shown.length + " of " + heads.length + " columns."; }
    syncToggles();
    groupTags();
    if (write) { writeAddress({ view: "", cols: sameSet(shown, all) ? "" : shown.join(" ") }); }
  }

  presets.forEach(function (p) {
    p.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) { return; }
      e.preventDefault();
      choose(p, true);
    });
  });
  toggles.forEach(function (t) {
    t.addEventListener("click", function () {
      var k = col(t), shown = shownKeys();
      var i = shown.indexOf(k);
      if (i >= 0) { shown.splice(i, 1); } else { shown.push(k); }
      showSet(heads.map(col).filter(function (h) { return shown.indexOf(h) >= 0; }), true);
    });
  });
  slice(document.querySelectorAll("[data-col-toggles]")).forEach(function (g) { g.hidden = false; });
  groupTags();

  var done = false;
  if (urlOK && toggles.length) {
    var all = heads.map(col);
    var want = (new URLSearchParams(window.location.search).get("cols") || "").toLowerCase().split(/[\s,]+/)
      .filter(function (k) { return all.indexOf(k) >= 0; });
    if (want.length) { showSet(all.filter(function (k) { return want.indexOf(k) >= 0; }), false); done = true; }
  }
  if (!done && presets.length) {
    var start = null;
    if (urlOK) {
      var view = new URLSearchParams(window.location.search).get("view");
      if (view) { start = presets.filter(function (p) { return p.getAttribute("data-preset-id") === view; })[0] || null; }
    }
    if (!start) { start = presets.filter(function (p) { return !keys(p).length; })[0] || null; }
    if (start) { choose(start, false); }
  }

  if (highlight) {
    var byCol = {};
    slice(table.querySelectorAll("th[data-col], td[data-col]")).forEach(function (c) { (byCol[col(c)] = byCol[col(c)] || []).push(c); });
    var hoverKey = null, focusKey = null, lit = null;
    var keyOf = function (el) {
      var c = el && el.closest ? el.closest("th[data-col], td[data-col]") : null;
      return c && table.contains(c) ? col(c) : null;
    };
    var render = function () {
      var k = hoverKey || focusKey;
      if (k === lit) { return; }
      if (lit && byCol[lit]) { byCol[lit].forEach(function (c) { c.classList.remove("colhl"); }); }
      lit = k;
      if (lit && byCol[lit]) { byCol[lit].forEach(function (c) { c.classList.add("colhl"); }); }
    };
    table.addEventListener("mouseover", function (e) { hoverKey = keyOf(e.target); render(); });
    table.addEventListener("mouseleave", function () { hoverKey = null; render(); });
    table.addEventListener("focusin", function (e) { focusKey = keyOf(e.target); render(); });
    table.addEventListener("focusout", function (e) { focusKey = table.contains(e.relatedTarget) ? keyOf(e.relatedTarget) : null; render(); });
  }
})();
