const monthFormatter = new Intl.DateTimeFormat("en", { month: "short" });
const fullDateFormatter = new Intl.DateTimeFormat("en", {
  month: "short",
  day: "numeric",
  year: "numeric",
});
const REPO_URL = "https://github.com/arif-js/leetcode";
const searchInput = document.querySelector("#problem-search");
const languageFilter = document.querySelector("#language-filter");
const problemList = document.querySelector("#problem-list");
const emptyState = document.querySelector("#empty-state");
let problems = [];

function parseDate(value) {
  if (!value) return null;
  const [year, month, day] = value.split("-").map(Number);
  return new Date(year, month - 1, day);
}

function formatDate(value) {
  const parsed = parseDate(value);
  return parsed ? fullDateFormatter.format(parsed) : "Date unavailable";
}

function monthsInRange(endDate, count) {
  return Array.from({ length: count }, (_, index) => {
    const month = new Date(endDate.getFullYear(), endDate.getMonth() - count + index + 1, 1);
    return {
      date: month,
      key: `${month.getFullYear()}-${String(month.getMonth() + 1).padStart(2, "0")}`,
    };
  });
}

function renderActivity(calendar) {
  const today = new Date();
  const months = monthsInRange(today, 6);
  const counts = new Map(months.map(({ key }) => [key, 0]));

  if (calendar) {
    for (const [key, count] of Object.entries(calendar)) {
      if (counts.has(key)) counts.set(key, count);
    }
  } else {
    for (const problem of problems) {
      const solvedAt = parseDate(problem.solvedAt);
      if (!solvedAt) continue;
      const key = `${solvedAt.getFullYear()}-${String(solvedAt.getMonth() + 1).padStart(2, "0")}`;
      if (counts.has(key)) counts.set(key, counts.get(key) + 1);
    }
  }

  const maxCount = Math.max(1, ...counts.values());
  const activityChart = document.querySelector("#activity-chart");
  activityChart.replaceChildren();

  for (const { date, key } of months) {
    const count = counts.get(key);
    const column = document.createElement("div");
    column.className = `chart-column${key === months.at(-1).key ? " current" : ""}`;
    const track = document.createElement("div");
    track.className = "chart-bar-track";
    const bar = document.createElement("div");
    bar.className = `chart-bar${count === 0 ? " zero" : ""}`;
    bar.style.height = `${count === 0 ? 3 : Math.max(10, (count / maxCount) * 100)}%`;
    bar.title = calendar
      ? `${count} ${count === 1 ? "submission" : "submissions"}`
      : `${count} ${count === 1 ? "solution" : "solutions"} added`;
    track.append(bar);
    const countLabel = document.createElement("span");
    countLabel.className = "chart-count";
    countLabel.textContent = count ? String(count) : "";
    const monthLabel = document.createElement("span");
    monthLabel.className = "chart-month";
    monthLabel.textContent = monthFormatter.format(date);
    column.append(track, countLabel, monthLabel);
    activityChart.append(column);
  }

  document.querySelector("#activity-total").textContent = String(
    [...counts.values()].reduce((sum, count) => sum + count, 0),
  );
  document.querySelector("#activity-period").textContent =
    `${monthFormatter.format(months[0].date)} – ${monthFormatter.format(months.at(-1).date)}`;
}

function renderLanguages() {
  const counts = new Map();
  for (const problem of problems) {
    counts.set(problem.language, (counts.get(problem.language) || 0) + 1);
  }
  const sortedLanguages = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const bars = document.querySelector("#language-bars");
  bars.replaceChildren();
  const maxCount = Math.max(1, ...counts.values());

  for (const [language, count] of sortedLanguages) {
    const row = document.createElement("div");
    row.className = "language-row";
    const name = document.createElement("span");
    name.className = "language-name";
    name.textContent = language;
    const track = document.createElement("div");
    track.className = "language-track";
    track.setAttribute("aria-label", `${language}: ${count} solutions`);
    const fill = document.createElement("div");
    fill.className = "language-fill";
    fill.style.width = `${(count / maxCount) * 100}%`;
    track.append(fill);
    const countLabel = document.createElement("span");
    countLabel.className = "language-count";
    countLabel.textContent = String(count);
    row.append(name, track, countLabel);
    bars.append(row);
  }

  document.querySelector("#language-problem-total").textContent = String(problems.length);
}

function renderProblemRows() {
  const query = searchInput.value.trim().toLocaleLowerCase();
  const language = languageFilter.value;
  const visibleProblems = problems
    .filter((problem) => {
      const matchesQuery =
        problem.title.toLocaleLowerCase().includes(query) ||
        problem.filename.toLocaleLowerCase().includes(query);
      return matchesQuery && (language === "all" || problem.language === language);
    })
    .sort((a, b) => {
      if (a.solvedAt && b.solvedAt) return b.solvedAt.localeCompare(a.solvedAt) || a.title.localeCompare(b.title);
      if (a.solvedAt) return -1;
      if (b.solvedAt) return 1;
      return a.title.localeCompare(b.title);
    });

  problemList.replaceChildren();
  for (const problem of visibleProblems) {
    const row = document.createElement("tr");
    const titleCell = document.createElement("td");
    const solutionLink = document.createElement("a");
    solutionLink.className = "problem-title file-link";
    solutionLink.href = `/solutions/${encodeURIComponent(problem.filename)}`;
    solutionLink.target = "_blank";
    solutionLink.rel = "noreferrer";
    const icon = document.createElement("span");
    icon.className = "file-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = problem.language === "PY" ? "PY" : "JS";
    solutionLink.append(icon, document.createTextNode(problem.title));
    solutionLink.addEventListener("click", (event) => {
      // Let modified clicks fall through to the raw file in a new tab.
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      openSolution(problem);
    });
    titleCell.append(solutionLink);

    const languageCell = document.createElement("td");
    const languagePill = document.createElement("span");
    languagePill.className = "language-pill";
    languagePill.textContent = problem.language;
    languageCell.append(languagePill);

    const dateCell = document.createElement("td");
    dateCell.className = "date-cell";
    dateCell.textContent = formatDate(problem.solvedAt);

    const actionsCell = document.createElement("td");
    actionsCell.className = "row-actions";
    const leetcodeLink = document.createElement("a");
    leetcodeLink.className = "leetcode-link";
    leetcodeLink.href = problem.leetcodeUrl;
    leetcodeLink.target = "_blank";
    leetcodeLink.rel = "noreferrer";
    leetcodeLink.textContent = "LeetCode ↗";
    actionsCell.append(leetcodeLink);
    row.append(titleCell, languageCell, dateCell, actionsCell);
    problemList.append(row);
  }

  emptyState.hidden = visibleProblems.length !== 0;
  document.querySelector("#problem-count").textContent =
    visibleProblems.length === problems.length
      ? String(problems.length)
      : `${visibleProblems.length} / ${problems.length}`;
}

function renderSummary() {
  document.querySelector("#repo-solved").textContent = String(problems.length);
  const mostRecent = problems
    .filter((problem) => problem.solvedAt)
    .sort((a, b) => b.solvedAt.localeCompare(a.solvedAt))[0];

  if (mostRecent) {
    document.querySelector("#last-solved").textContent = formatDate(mostRecent.solvedAt);
    document.querySelector("#last-solved-title").textContent = mostRecent.title;
  } else {
    document.querySelector("#last-solved").textContent = "—";
    document.querySelector("#last-solved-title").textContent = "No Git history available";
  }
}

async function loadProfileSummary() {
  const response = await fetch("/api/profile");
  if (!response.ok) throw new Error(`Could not load LeetCode profile stats (${response.status})`);
  const stats = await response.json();
  document.querySelector("#leetcode-solved").textContent = String(stats.all);
  document.querySelector("#profile-breakdown").textContent =
    `${stats.easy} Easy · ${stats.medium} Medium · ${stats.hard} Hard`;
  // The 2026 card carries this year's rhythm; the all-time card carries the 65.
  const thisYear = [
    `${problems.length} published here`,
    stats.activeDays && `${stats.activeDays} active days`,
    stats.streak && `${stats.streak}-day streak`,
  ].filter(Boolean);
  document.querySelector("#repo-breakdown").textContent = thisYear.join(" · ");

  if (stats.languages?.length) renderProfileLanguages(stats.languages);
  if (stats.calendar && Object.keys(stats.calendar).length) {
    renderActivity(stats.calendar);
    document.querySelector("#activity-title").textContent = "Practice activity";
    document.querySelector("#activity-unit").textContent = "submissions";
    document.querySelector("#chart-caption").textContent =
      "Submissions per month, from the LeetCode submission calendar.";
  }
  if (stats.recent?.length) renderRecent(stats.recent);
}

// LeetCode knows about every language solved, not just the ones published here.
function renderProfileLanguages(languages) {
  const bars = document.querySelector("#language-bars");
  bars.replaceChildren();
  const maxCount = Math.max(1, ...languages.map((entry) => entry.solved));

  for (const { name, solved } of languages) {
    const row = document.createElement("div");
    row.className = "language-row";
    const label = document.createElement("span");
    label.className = "language-name";
    label.textContent = name;
    const track = document.createElement("div");
    track.className = "language-track";
    track.setAttribute("aria-label", `${name}: ${solved} solved`);
    const fill = document.createElement("div");
    fill.className = "language-fill";
    fill.style.width = `${(solved / maxCount) * 100}%`;
    track.append(fill);
    const count = document.createElement("span");
    count.className = "language-count";
    count.textContent = String(solved);
    row.append(label, track, count);
    bars.append(row);
  }

  document.querySelector("#language-problem-total").textContent = String(languages.length);
  document.querySelector("#language-total-unit").textContent = "languages used";
  document.querySelector("#language-caption").hidden = false;
}

function renderRecent(recent) {
  const strip = document.querySelector("#recent-strip");
  const published = new Set(problems.map((problem) => problem.title.toLocaleLowerCase()));
  strip.replaceChildren();

  for (const entry of recent) {
    const card = document.createElement("a");
    card.className = "recent-card";
    card.href = entry.url;
    card.target = "_blank";
    card.rel = "noreferrer";

    const title = document.createElement("strong");
    title.textContent = entry.title;
    const meta = document.createElement("span");
    meta.className = "recent-meta";
    meta.textContent = [entry.lang, entry.solvedAt && formatDate(entry.solvedAt)]
      .filter(Boolean)
      .join(" · ");
    card.append(title, meta);

    if (published.has(entry.title.toLocaleLowerCase())) {
      const tag = document.createElement("span");
      tag.className = "in-repo-tag";
      tag.textContent = "IN REPO";
      card.append(tag);
    }
    strip.append(card);
  }

  document.querySelector("#recent-panel").hidden = false;
}

function populateLanguageFilter() {
  const languages = [...new Set(problems.map((problem) => problem.language))].sort();
  for (const language of languages) {
    const option = document.createElement("option");
    option.value = language;
    option.textContent = language;
    languageFilter.append(option);
  }
}

async function initialize() {
  const response = await fetch("/api/problems");
  if (!response.ok) throw new Error(`Could not load problems (${response.status})`);
  const data = await response.json();
  problems = data.problems;

  renderSummary();
  renderActivity();
  renderLanguages();
  populateLanguageFilter();
  renderProblemRows();
  document.querySelector("#updated-at").textContent =
    `Updated ${fullDateFormatter.format(parseDate(data.generatedAt))}`;
  loadProfileSummary().catch((error) => {
    console.error(error);
    document.querySelector("#leetcode-solved").textContent = "—";
    document.querySelector("#profile-breakdown").textContent =
      "Could not load the live LeetCode total.";
  });
}

searchInput.addEventListener("input", renderProblemRows);
languageFilter.addEventListener("change", renderProblemRows);

function setUpNavigation() {
  const navLinks = [...document.querySelectorAll(".nav-link")];
  const crumbLabel = document.querySelector(".breadcrumb .crumb-current");

  function labelOf(link) {
    return link.querySelector(".nav-label-text").textContent.trim();
  }

  function activate(id) {
    for (const link of navLinks) {
      const isActive = link.getAttribute("href") === `#${id}`;
      link.classList.toggle("active", isActive);
      if (isActive && crumbLabel) crumbLabel.textContent = labelOf(link);
    }
  }

  // A click scrolls past the sections in between, so pause the scroll spy until
  // the page settles — otherwise those sections light up on the way through.
  let spyPaused = false;
  let resumeTimer;

  function pauseSpy() {
    spyPaused = true;
    clearTimeout(resumeTimer);
    const resume = () => {
      clearTimeout(resumeTimer);
      spyPaused = false;
    };
    if ("onscrollend" in window) window.addEventListener("scrollend", resume, { once: true });
    resumeTimer = setTimeout(resume, 1200);
  }

  for (const link of navLinks) {
    link.addEventListener("click", () => {
      pauseSpy();
      activate(link.getAttribute("href").slice(1));
    });
  }

  // Keep the sidebar in sync with the lowest section that has reached the top band.
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean)
    .sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));
  const inView = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) inView.add(entry.target);
        else inView.delete(entry.target);
      }
      if (spyPaused) return;
      const current = sections.filter((section) => inView.has(section)).at(-1);
      if (current) activate(current.id);
    },
    { rootMargin: "-80px 0px -70% 0px" },
  );
  for (const section of sections) observer.observe(section);
}

setUpNavigation();

initialize().catch((error) => {
  console.error(error);
  document.querySelector("#repo-solved").textContent = "!";
  document.querySelector("#last-solved-title").textContent =
    "Could not load the README solution list.";
  document.querySelector("#empty-state").hidden = false;
  document.querySelector("#empty-state").textContent =
    "Unable to load dashboard data. Check the README and Git history, then refresh.";
});


/* ---------- Solution viewer ---------- */

// Small, dependency-free highlighter. Sub-patterns stay non-capturing so the
// matched group index lines up with the rule that produced it.
const SYNTAX = {
  PY: [
    ["comment", /#[^\n]*/],
    ["string", /"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/],
    [
      "keyword",
      /\b(?:def|class|return|if|elif|else|for|while|in|not|and|or|import|from|as|with|try|except|finally|raise|lambda|yield|global|nonlocal|pass|break|continue|assert|del|is|None|True|False|self)\b/,
    ],
    ["number", /\b\d[\d_]*(?:\.\d+)?\b/],
  ],
  JS: [
    ["comment", /\/\/[^\n]*|\/\*[\s\S]*?\*\//],
    ["string", /`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'/],
    [
      "keyword",
      /\b(?:const|let|var|function|return|if|else|for|while|of|in|new|class|extends|this|null|undefined|true|false|typeof|instanceof|try|catch|finally|throw|async|await|break|continue|switch|case|default|delete|yield)\b/,
    ],
    ["number", /\b\d[\d_]*(?:\.\d+)?\b/],
  ],
};

function highlight(source, language) {
  const fragment = document.createDocumentFragment();
  const rules = SYNTAX[language];
  if (!rules) {
    fragment.append(source);
    return fragment;
  }

  const pattern = new RegExp(rules.map(([, rule]) => `(${rule.source})`).join("|"), "g");
  let index = 0;
  for (const match of source.matchAll(pattern)) {
    if (match.index > index) fragment.append(source.slice(index, match.index));
    const rule = rules[match.slice(1).findIndex((group) => group !== undefined)];
    const token = document.createElement("span");
    token.className = `tok-${rule[0]}`;
    token.textContent = match[0];
    fragment.append(token);
    index = match.index + match[0].length;
  }
  if (index < source.length) fragment.append(source.slice(index));
  return fragment;
}

const drawer = document.querySelector("#code-drawer");
const drawerCode = document.querySelector("#drawer-code");
let lastFocused = null;

async function openSolution(problem) {
  lastFocused = document.activeElement;
  document.querySelector("#drawer-title").textContent = problem.title;
  document.querySelector("#drawer-lang").textContent = problem.language;
  document.querySelector("#drawer-date").textContent = `Added ${formatDate(problem.solvedAt)}`;
  document.querySelector("#drawer-leetcode").href = problem.leetcodeUrl;
  const rawUrl = `/solutions/${encodeURIComponent(problem.filename)}`;
  document.querySelector("#drawer-raw").href = rawUrl;
  document.querySelector("#drawer-github").href =
    `${REPO_URL}/blob/main/${encodeURIComponent(problem.filename)}`;

  drawer.hidden = false;
  document.body.classList.add("drawer-open");
  drawer.querySelector(".drawer-close").focus();
  drawerCode.textContent = "Loading…";

  try {
    const response = await fetch(rawUrl);
    if (!response.ok) throw new Error(String(response.status));
    drawerCode.replaceChildren(highlight(await response.text(), problem.language));
  } catch (error) {
    console.error(error);
    drawerCode.textContent = "Could not load this solution file.";
  }
}

function closeDrawer() {
  if (drawer.hidden) return;
  drawer.hidden = true;
  document.body.classList.remove("drawer-open");
  lastFocused?.focus();
}

for (const element of drawer.querySelectorAll("[data-drawer-close]")) {
  element.addEventListener("click", closeDrawer);
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeDrawer();
});
