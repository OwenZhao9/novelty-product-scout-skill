#!/usr/bin/env node

const { execFileSync } = require("node:child_process");

const args = parseArgs(process.argv.slice(2));
const keyword = args.keyword || "";
const targetUrl = args.url || "";
const negativeWords = splitWords(args.negative || args["negative-words"] || "");
const includeWords = splitWords(args.include || args["include-words"] || "");
const authorWords = splitWords(args.author || args["author-words"] || "");
const installPanel = args.panel !== "false";
const jsonOutput = Boolean(args.json);

main().catch((error) => {
  const message = error && error.stack ? error.stack : String(error);
  if (jsonOutput) {
    console.log(JSON.stringify({ ok: false, error: message }));
  } else {
    console.error(message);
  }
  process.exit(1);
});

async function main() {
  let currentUrl = "NOT_FOUND";
  if (targetUrl) {
    if (!isTikTokUrl(targetUrl)) {
      throw new Error(`Refusing to inject TikTok panel into non-TikTok URL: ${targetUrl}`);
    }
    openTikTokUrl(targetUrl);
    sleep(4600);
    currentUrl = activeTikTokUrl(false);
  } else {
    currentUrl = activeTikTokUrl(false);
  }
  if (currentUrl === "NOT_FOUND" && keyword) {
    openTikTokSearch(keyword);
    sleep(4200);
    currentUrl = activeTikTokUrl(false);
  }
  if (currentUrl === "NOT_FOUND") {
    throw new Error("No TikTok tab found in Google Chrome. Open TikTok in Chrome first, then run this again.");
  }
  if (!/tiktok\.com/.test(currentUrl)) {
    throw new Error(`Active Chrome tab is not TikTok: ${currentUrl}`);
  }

  if (!installPanel) {
    throw new Error("Only --panel mode is supported for TikTok page injection.");
  }

  const result = JSON.parse(runChromeJs(panelJs({ negativeWords, includeWords, authorWords })));
  const payload = {
    ok: true,
    url: currentUrl,
    hidden: result.hidden,
    visible: result.visible,
    words: result.words,
    include: result.include,
    authors: result.authors,
  };
  if (jsonOutput) {
    console.log(JSON.stringify(payload));
    return;
  }
  console.log("TikTok filter panel installed");
  console.log(`URL: ${currentUrl}`);
  console.log(`Hidden on page: ${payload.hidden}`);
  console.log(`Visible on page: ${payload.visible}`);
}

function activeTikTokUrl(failIfMissing = true) {
  const script = `
tell application "Google Chrome"
  if (count of windows) is not 0 then
    if (URL of active tab of front window) contains "tiktok.com" then
      return URL of active tab of front window
    end if
  end if
  repeat with wi from 1 to count of windows
    repeat with ti from 1 to count of tabs of window wi
      if (URL of tab ti of window wi) contains "tiktok.com" then
        set active tab index of window wi to ti
        set index of window wi to 1
        return URL of active tab of front window
      end if
    end repeat
  end repeat
  return "NOT_FOUND"
end tell
`;
  const result = runAppleScript(script);
  if (failIfMissing && result === "NOT_FOUND") {
    throw new Error("No TikTok tab found in Google Chrome. Open TikTok and log in first.");
  }
  return result;
}

function openTikTokUrl(url) {
  const script = `
tell application "Google Chrome"
  activate
  if (count of windows) is 0 then
    make new window
  end if
  set newTab to make new tab at end of tabs of front window with properties {URL:${JSON.stringify(url)}}
  set active tab index of front window to (count of tabs of front window)
  return URL of newTab
end tell
`;
  return runAppleScript(script);
}

function openTikTokSearch(term) {
  const url = `https://www.tiktok.com/search?q=${encodeURIComponent(term)}`;
  const script = `
tell application "Google Chrome"
  activate
  if (count of windows) is 0 then
    make new window
  end if
  set newTab to make new tab at end of tabs of front window with properties {URL:${JSON.stringify(url)}}
  set active tab index of front window to (count of tabs of front window)
  return URL of newTab
end tell
`;
  return runAppleScript(script);
}

function runChromeJs(js) {
  const script = `
tell application "Google Chrome"
  if (count of windows) is not 0 then
    if (URL of active tab of front window) contains "tiktok.com" then
      return execute active tab of front window javascript ${JSON.stringify(js)}
    end if
  end if
  repeat with wi from 1 to count of windows
    repeat with ti from 1 to count of tabs of window wi
      if (URL of tab ti of window wi) contains "tiktok.com" then
        return execute tab ti of window wi javascript ${JSON.stringify(js)}
      end if
    end repeat
  end repeat
  return "NO_TIKTOK_TAB"
end tell
`;
  return runAppleScript(script);
}

function isTikTokUrl(url) {
  try {
    const parsed = new URL(url);
    return /(^|\.)tiktok\.com$/i.test(parsed.hostname);
  } catch {
    return false;
  }
}

function runAppleScript(script) {
  return execFileSync("osascript", ["-e", script], {
    encoding: "utf8",
    maxBuffer: 30 * 1024 * 1024,
  }).trim();
}

function panelJs(config) {
  return `(() => {
    const initialNegativeWords = ${JSON.stringify(config.negativeWords)};
    const initialIncludeWords = ${JSON.stringify(config.includeWords)};
    const initialAuthorWords = ${JSON.stringify(config.authorWords)};
    const panelId = "tk-scout-filter-panel";
    const styleId = "tk-scout-filter-style";
    const hiddenAttr = "data-tk-scout-hidden";
    const hitAttr = "data-tk-scout-hits";
    const negativeKey = "tk-scout-negative-words";
    const includeKey = "tk-scout-include-words";
    const authorKey = "tk-scout-author-words";
    const dateFromKey = "tk-scout-date-from";
    const dateToKey = "tk-scout-date-to";
    const hideUnknownDateKey = "tk-scout-hide-unknown-date";
    const positionKey = "tk-scout-panel-position";

    const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim().toLocaleLowerCase();
    const splitWords = (value) => String(value || "")
      .split(/[,，\\n]/)
      .map((word) => word.trim())
      .filter(Boolean);
    const unique = (items) => Array.from(new Set(items.filter(Boolean)));

    const bestCardForAnchor = (anchor) => {
      const semantic = anchor.closest('div[data-e2e*="search"], div[data-e2e*="video"], div[data-e2e*="recommend"], div[data-e2e*="item"], article, section');
      if (semantic && semantic !== document.body && semantic !== document.documentElement) return semantic;
      let node = anchor;
      for (let i = 0; i < 5 && node && node.parentElement; i += 1) {
        node = node.parentElement;
        const rect = node.getBoundingClientRect();
        const text = normalize(node.innerText || "");
        if (rect.width > 120 && rect.height > 80 && text.length > 8 && text.length < 2200) return node;
      }
      return null;
    };

    const getCards = () => {
      const cards = new Set();
      [
        'div[data-e2e="search_video-item"]',
        'div[data-e2e="search_top-item"]',
        'div[data-e2e="user-post-item"]',
        'div[data-e2e="recommend-list-item-container"]',
        'div[data-e2e="feed-video"]',
        'article',
      ].forEach((selector) => {
        document.querySelectorAll(selector).forEach((node) => {
          const text = normalize(node.innerText || "");
          if (text.length > 3) cards.add(node);
        });
      });
      document.querySelectorAll('a[href*="/video/"], a[href*="/@"]').forEach((anchor) => {
        const card = bestCardForAnchor(anchor);
        if (card) cards.add(card);
      });
      return Array.from(cards).filter((card) => {
        if (!card || card === document.body || card === document.documentElement) return false;
        const rect = card.getBoundingClientRect();
        const text = normalize(card.innerText || "");
        if (rect.width < 80 || rect.height < 40 || text.length < 2) return false;
        return Boolean(card.querySelector('a[href*="/video/"], a[href*="/@"]')) || /video|search|item|feed/i.test(card.getAttribute("data-e2e") || "");
      });
    };

    const extractAuthor = (card) => {
      const explicit = card.querySelector('[data-e2e*="author"], [data-e2e*="user"], a[href^="/@"], a[href*="tiktok.com/@"]');
      const href = explicit?.getAttribute("href") || "";
      const hrefAuthor = href.match(/@([^/?#]+)/)?.[1] || "";
      return normalize(explicit?.innerText || explicit?.textContent || hrefAuthor);
    };

    const parseDate = (text) => {
      const now = new Date();
      const normalized = String(text || "").replace(/\\s+/g, " ");
      const full = normalized.match(/(20\\d{2})[.\\/-](\\d{1,2})[.\\/-](\\d{1,2})/);
      if (full) return new Date(Number(full[1]), Number(full[2]) - 1, Number(full[3]));
      const monthDay = normalized.match(/(?:^|[^\\d])(\\d{1,2})[.\\/-](\\d{1,2})(?:[^\\d]|$)/);
      if (monthDay) return new Date(now.getFullYear(), Number(monthDay[1]) - 1, Number(monthDay[2]));
      if (/today|今天/i.test(normalized)) return new Date(now.getFullYear(), now.getMonth(), now.getDate());
      if (/yesterday|昨天/i.test(normalized)) return new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);
      const daysAgo = normalized.match(/(\\d+)\\s*(d|day|days|天)\\s*(ago|前)?/i);
      if (daysAgo) return new Date(now.getFullYear(), now.getMonth(), now.getDate() - Number(daysAgo[1]));
      const weeksAgo = normalized.match(/(\\d+)\\s*(w|week|weeks|周)\\s*(ago|前)?/i);
      if (weeksAgo) return new Date(now.getFullYear(), now.getMonth(), now.getDate() - Number(weeksAgo[1]) * 7);
      const monthsAgo = normalized.match(/(\\d+)\\s*(mo|month|months|月)\\s*(ago|前)?/i);
      if (monthsAgo) return new Date(now.getFullYear(), now.getMonth() - Number(monthsAgo[1]), now.getDate());
      return null;
    };

    const parseInputDate = (value, endOfDay) => {
      if (!value) return null;
      const date = new Date(value + (endOfDay ? "T23:59:59" : "T00:00:00"));
      return Number.isNaN(date.getTime()) ? null : date;
    };

    const triggerLayout = () => {
      window.dispatchEvent(new Event("resize"));
      window.dispatchEvent(new Event("scroll"));
      requestAnimationFrame(() => {
        window.dispatchEvent(new Event("resize"));
        window.dispatchEvent(new Event("scroll"));
      });
    };

    const clearHidden = () => {
      for (const card of document.querySelectorAll("[" + hiddenAttr + "]")) {
        card.removeAttribute(hiddenAttr);
        card.removeAttribute(hitAttr);
      }
      triggerLayout();
    };

    const applyFilters = (filters) => {
      clearHidden();
      const stats = { hidden: 0, visible: 0, word: 0, include: 0, author: 0, date: 0, unknownDate: 0 };
      const fromDate = parseInputDate(filters.dateFrom, false);
      const toDate = parseInputDate(filters.dateTo, true);
      for (const card of getCards()) {
        const text = normalize(card.innerText || "");
        const author = extractAuthor(card);
        const hits = [];
        const wordHits = filters.words.filter((word) => text.includes(String(word).toLocaleLowerCase()));
        const includeHits = filters.include.filter((word) => text.includes(String(word).toLocaleLowerCase()));
        const authorHits = filters.authors.filter((word) => author.includes(String(word).toLocaleLowerCase()));
        for (const hit of wordHits) hits.push("exclude:" + hit);
        for (const hit of authorHits) hits.push("author:" + hit);
        if (filters.include.length && !includeHits.length) hits.push("missing-required-word");

        if (fromDate || toDate || filters.hideUnknownDate) {
          const cardDate = parseDate(card.innerText || "");
          if (!cardDate) {
            stats.unknownDate += 1;
            if (filters.hideUnknownDate) hits.push("date:unknown");
          } else if ((fromDate && cardDate < fromDate) || (toDate && cardDate > toDate)) {
            hits.push("date:out-of-range");
            stats.date += 1;
          }
        }

        if (hits.length) {
          card.setAttribute(hiddenAttr, "true");
          card.setAttribute(hitAttr, hits.join(","));
          stats.hidden += 1;
          if (wordHits.length) stats.word += 1;
          if (filters.include.length && !includeHits.length) stats.include += 1;
          if (authorHits.length) stats.author += 1;
        } else {
          stats.visible += 1;
        }
      }
      triggerLayout();
      return stats;
    };

    const saveConfig = (filters) => {
      localStorage.setItem(negativeKey, filters.words.join(","));
      localStorage.setItem(includeKey, filters.include.join(","));
      localStorage.setItem(authorKey, filters.authors.join(","));
      localStorage.setItem(dateFromKey, filters.dateFrom || "");
      localStorage.setItem(dateToKey, filters.dateTo || "");
      localStorage.setItem(hideUnknownDateKey, filters.hideUnknownDate ? "1" : "0");
    };
    const loadInitial = (key, initial) => {
      if (initial.length) return initial;
      const stored = localStorage.getItem(key);
      return stored ? splitWords(stored) : [];
    };

    let style = document.getElementById(styleId);
    if (!style) {
      style = document.createElement("style");
      style.id = styleId;
      document.documentElement.appendChild(style);
    }
    style.textContent = [
      '[' + hiddenAttr + '="true"]{display:none!important;}',
      '#' + panelId + '{position:fixed;right:16px;top:96px;z-index:2147483647;width:324px;background:#fff;color:#111;border:1px solid rgba(0,0,0,.12);box-shadow:0 10px 30px rgba(0,0,0,.18);border-radius:8px;font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden;transform:none;}',
      '#' + panelId + ' *{box-sizing:border-box;}',
      '#' + panelId + ' .tk-scout-head{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;background:#111;color:#fff;font-weight:700;cursor:move;user-select:none;}',
      '#' + panelId + ' .tk-scout-title{display:grid;gap:2px;min-width:0;}',
      '#' + panelId + ' .tk-scout-title strong{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
      '#' + panelId + ' .tk-scout-title span{color:#7af0bd;font-size:10px;text-transform:uppercase;letter-spacing:.08em;}',
      '#' + panelId + ' .tk-scout-close{border:0;background:transparent;color:#fff;font-size:18px;line-height:1;cursor:pointer;}',
      '#' + panelId + ' .tk-scout-body{display:block;max-height:calc(100vh - 154px);overflow:auto;padding:12px;background:#fff;}',
      '#' + panelId + ' label{display:block;margin:8px 0 4px;color:#444;font-size:12px;font-weight:700;}',
      '#' + panelId + ' textarea{box-sizing:border-box;width:100%;height:58px;resize:vertical;border:1px solid #ddd;border-radius:6px;padding:8px;color:#111;background:#fff;font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}',
      '#' + panelId + ' input[type="date"]{box-sizing:border-box;width:100%;height:30px;border:1px solid #ddd;border-radius:6px;padding:0 8px;color:#111;background:#fff;}',
      '#' + panelId + ' .tk-scout-date-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;}',
      '#' + panelId + ' .tk-scout-check{display:flex;align-items:center;gap:6px;margin-top:6px;color:#555;font-size:12px;white-space:nowrap;}',
      '#' + panelId + ' .tk-scout-actions{display:flex;gap:8px;margin-top:10px;}',
      '#' + panelId + ' button{height:30px;border-radius:6px;border:1px solid #ddd;background:#f7f7f7;color:#111;padding:0 10px;cursor:pointer;font-weight:700;}',
      '#' + panelId + ' .tk-scout-apply{background:#111;border-color:#111;color:#fff;}',
      '#' + panelId + ' .tk-scout-status{margin-top:10px;color:#555;font-size:12px;white-space:pre-line;max-height:112px;overflow:auto;border:1px solid #eee;border-radius:6px;padding:8px;background:#fafafa;}',
      '#' + panelId + ' .tk-scout-note{margin-top:8px;color:#777;font-size:11px;line-height:1.45;}'
    ].join("");

    let panel = document.getElementById(panelId);
    if (!panel) {
      panel = document.createElement("div");
      panel.id = panelId;
      document.body.appendChild(panel);
    }
    if (!panel.querySelector(".tk-scout-panel-v1")) {
      panel.innerHTML = [
        '<div class="tk-scout-panel-v1"></div>',
        '<div class="tk-scout-head"><div class="tk-scout-title"><span>TikTok Filter</span><strong>TikTok 线索过滤浮窗</strong></div><button class="tk-scout-close" title="Close">×</button></div>',
        '<div class="tk-scout-body">',
        '<div><label>内容排除词</label><textarea class="tk-scout-negative" placeholder="广告, 招募, 代理, 私信"></textarea></div>',
        '<div><label>必须包含词</label><textarea class="tk-scout-include" placeholder="review, demo, shop"></textarea></div>',
        '<div><label>账号/作者排除词</label><textarea class="tk-scout-authors" placeholder="agency, official, seller"></textarea></div>',
        '<div class="tk-scout-date-row">',
        '<div><label>开始日期</label><input class="tk-scout-date-from" type="date"></div>',
        '<div><label>结束日期</label><input class="tk-scout-date-to" type="date"></div>',
        '</div>',
        '<label class="tk-scout-check"><input class="tk-scout-hide-unknown-date" type="checkbox">日期未知也隐藏</label>',
        '<div class="tk-scout-actions">',
        '<button class="tk-scout-apply">Apply</button>',
        '<button class="tk-scout-reset">Reset</button>',
        '</div>',
        '<div class="tk-scout-status">Ready</div>',
        '<div class="tk-scout-note">滚动加载新内容后会自动重新过滤。若页面结构变化，优先以当前可见视频卡片文本为准。</div>',
        '</div>'
      ].join("");
    }

    const header = panel.querySelector(".tk-scout-head");
    const negativeInput = panel.querySelector(".tk-scout-negative");
    const includeInput = panel.querySelector(".tk-scout-include");
    const authorsInput = panel.querySelector(".tk-scout-authors");
    const dateFromInput = panel.querySelector(".tk-scout-date-from");
    const dateToInput = panel.querySelector(".tk-scout-date-to");
    const hideUnknownDateInput = panel.querySelector(".tk-scout-hide-unknown-date");
    const status = panel.querySelector(".tk-scout-status");
    const applyButton = panel.querySelector(".tk-scout-apply");
    const resetButton = panel.querySelector(".tk-scout-reset");
    const closeButton = panel.querySelector(".tk-scout-close");

    negativeInput.value = loadInitial(negativeKey, initialNegativeWords).join(", ");
    includeInput.value = loadInitial(includeKey, initialIncludeWords).join(", ");
    authorsInput.value = loadInitial(authorKey, initialAuthorWords).join(", ");
    dateFromInput.value = localStorage.getItem(dateFromKey) || "";
    dateToInput.value = localStorage.getItem(dateToKey) || "";
    hideUnknownDateInput.checked = localStorage.getItem(hideUnknownDateKey) === "1";

    const readFilters = () => ({
      words: splitWords(negativeInput.value),
      include: splitWords(includeInput.value),
      authors: splitWords(authorsInput.value),
      dateFrom: dateFromInput.value,
      dateTo: dateToInput.value,
      hideUnknownDate: hideUnknownDateInput.checked,
    });

    const savedPosition = (() => {
      try { return JSON.parse(localStorage.getItem(positionKey) || "null"); } catch (_) { return null; }
    })();
    if (savedPosition && Number.isFinite(savedPosition.left) && Number.isFinite(savedPosition.top)) {
      panel.style.left = savedPosition.left + "px";
      panel.style.top = savedPosition.top + "px";
      panel.style.right = "auto";
      panel.style.transform = "none";
    }

    const refresh = () => {
      const filters = readFilters();
      saveConfig(filters);
      const stats = applyFilters(filters);
      const active = [];
      if (filters.words.length) active.push("exclude: " + filters.words.join(", "));
      if (filters.include.length) active.push("required: " + filters.include.join(", "));
      if (filters.authors.length) active.push("authors: " + filters.authors.join(", "));
      if (filters.dateFrom || filters.dateTo) active.push("date: " + (filters.dateFrom || "...") + " to " + (filters.dateTo || "..."));
      status.textContent = [
        "Hidden " + stats.hidden + " videos; visible " + stats.visible,
        "By exclude " + stats.word + ", required " + stats.include + ", author " + stats.author + ", date " + stats.date,
        stats.unknownDate ? "Unknown date cards: " + stats.unknownDate : "",
        active.length ? active.join("\\n") : "No filters set"
      ].filter(Boolean).join("\\n");
      return { words: filters.words, include: filters.include, authors: filters.authors, hidden: stats.hidden, visible: stats.visible };
    };

    applyButton.onclick = refresh;
    resetButton.onclick = () => {
      negativeInput.value = "";
      includeInput.value = "";
      authorsInput.value = "";
      dateFromInput.value = "";
      dateToInput.value = "";
      hideUnknownDateInput.checked = false;
      saveConfig({ words: [], include: [], authors: [], dateFrom: "", dateTo: "", hideUnknownDate: false });
      clearHidden();
      status.textContent = "Reset: all loaded TikTok cards visible";
    };
    closeButton.onclick = () => panel.remove();
    panel.addEventListener("keydown", (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") refresh();
    });
    for (const el of [dateFromInput, dateToInput, hideUnknownDateInput]) {
      el.addEventListener("change", refresh);
    }

    let dragState = null;
    header.addEventListener("pointerdown", (event) => {
      if (event.target.closest("button")) return;
      const rect = panel.getBoundingClientRect();
      dragState = { dx: event.clientX - rect.left, dy: event.clientY - rect.top };
      header.setPointerCapture(event.pointerId);
    });
    header.addEventListener("pointermove", (event) => {
      if (!dragState) return;
      const left = Math.max(8, Math.min(window.innerWidth - panel.offsetWidth - 8, event.clientX - dragState.dx));
      const top = Math.max(8, Math.min(window.innerHeight - panel.offsetHeight - 8, event.clientY - dragState.dy));
      panel.style.left = left + "px";
      panel.style.top = top + "px";
      panel.style.right = "auto";
      panel.style.transform = "none";
    });
    header.addEventListener("pointerup", () => {
      if (!dragState) return;
      dragState = null;
      const rect = panel.getBoundingClientRect();
      localStorage.setItem(positionKey, JSON.stringify({ left: Math.round(rect.left), top: Math.round(rect.top) }));
    });

    if (window.__tkScoutPanelObserver) {
      window.__tkScoutPanelObserver.disconnect();
    }
    const observer = new MutationObserver(() => {
      clearTimeout(window.__tkScoutPanelTimer);
      window.__tkScoutPanelTimer = setTimeout(refresh, 350);
    });
    observer.observe(document.body, { childList: true, subtree: true });
    window.__tkScoutPanelObserver = observer;
    window.__tkScoutPanel = { refresh, clearHidden };

    const result = refresh();
    return JSON.stringify(result);
  })()`;
}

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      parsed[key] = "true";
    } else {
      parsed[key] = next;
      i += 1;
    }
  }
  return parsed;
}

function splitWords(value) {
  return String(value || "")
    .split(/[,，\n]/)
    .map((word) => word.trim())
    .filter(Boolean);
}

function sleep(ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {}
}
