// Scroll progress bar: accent while reading, green when the page is finished,
// with a confetti burst on first arrival at the bottom.
const progressBar = document.createElement("div");
progressBar.className = "progress-bar";
progressBar.setAttribute("aria-hidden", "true");
document.body.appendChild(progressBar);

const DONE_THRESHOLD = 0.99;
const REARM_THRESHOLD = 0.9;
let done = false;

function updateProgress() {
const doc = document.documentElement;
const max = doc.scrollHeight - window.innerHeight;
const progress = max > 0 ? window.scrollY / max : 0;
progressBar.style.transform = `scaleX(${progress})`;
progressBar.classList.toggle("done", progress >= DONE_THRESHOLD);
if (progress >= DONE_THRESHOLD && !done) {
done = true;
confetti();
} else if (progress < REARM_THRESHOLD) {
done = false;
}
}

window.addEventListener("scroll", updateProgress, { passive: true });
window.addEventListener("resize", updateProgress);
updateProgress();

// Lightweight dependency-free confetti
function confetti() {
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
const style = getComputedStyle(document.body);
const colors = [
style.getPropertyValue("--odd").trim(),
style.getPropertyValue("--even").trim(),
style.getPropertyValue("--accent").trim(),
style.getPropertyValue("--text").trim()
];

const canvas = document.createElement("canvas");
canvas.style.cssText = "position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:999";
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");
const dpr = window.devicePixelRatio || 1;
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;
ctx.scale(dpr, dpr);

const W = window.innerWidth;
const H = window.innerHeight;
const pieces = Array.from({ length: 160 }, () => ({
x: Math.random() * W,
y: -20 - Math.random() * H * 0.3,
w: 6 + Math.random() * 6,
h: 8 + Math.random() * 8,
color: colors[Math.floor(Math.random() * colors.length)],
vx: -1.5 + Math.random() * 3,
vy: 2 + Math.random() * 3.5,
rot: Math.random() * Math.PI * 2,
vr: -0.1 + Math.random() * 0.2
}));

const start = performance.now();
const duration = 3200;

function tick(now) {
const elapsed = now - start;
ctx.clearRect(0, 0, W, H);
const fade = elapsed > duration - 600 ? Math.max(0, (duration - elapsed) / 600) : 1;
ctx.globalAlpha = fade;
pieces.forEach(p => {
p.x += p.vx;
p.y += p.vy;
p.rot += p.vr;
ctx.save();
ctx.translate(p.x, p.y);
ctx.rotate(p.rot);
ctx.fillStyle = p.color;
ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
ctx.restore();
});
if (elapsed < duration) {
requestAnimationFrame(tick);
} else {
canvas.remove();
}
}
requestAnimationFrame(tick);
}

// Scroll-reveal animations
const revealTargets = document.querySelectorAll(
".stat, .card, .flow-step, .finding, .quote-block, .models, .cta, .terminal, .love-card"
);
revealTargets.forEach(el => el.classList.add("reveal"));

const revealObserver = new IntersectionObserver(entries => {
entries.forEach(entry => {
if (!entry.isIntersecting) return;
entry.target.classList.add("visible");
revealObserver.unobserve(entry.target);
});
}, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

revealTargets.forEach(el => revealObserver.observe(el));

// Animated stat counters
const counters = document.querySelectorAll(".stat-num");
const observer = new IntersectionObserver(entries => {
entries.forEach(entry => {
if (!entry.isIntersecting) return;
animate(entry.target);
observer.unobserve(entry.target);
});
}, { threshold: 0.5 });

counters.forEach(counter => observer.observe(counter));

function animate(el) {
const target = Number(el.dataset.count);
const suffix = el.dataset.suffix || "";
const start = performance.now();
const duration = 1200;
requestAnimationFrame(tick);

function tick(now) {
const progress = Math.min((now - start) / duration, 1);
const eased = 1 - Math.pow(1 - progress, 3);
el.textContent = Math.round(target * eased) + suffix;
if (progress < 1) requestAnimationFrame(tick);
}
}

// Logs browser: fetches raw experiment JSONs from GitHub.
const REPO = "theamankumarsingh/odd-number-forensics";
const BRANCH = "main";
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/results/`;
const API_RESULTS_URL = `https://api.github.com/repos/${REPO}/contents/results?ref=${BRANCH}`;
const FALLBACK_EXPERIMENTS = Array.from({ length: 21 }, (_, i) =>
`experiment_${String(i + 1).padStart(3, "0")}.json`);

const expList = document.getElementById("exp-list");
const expCount = document.getElementById("exp-count");
const logTitle = document.getElementById("log-title");
const logRaw = document.getElementById("log-raw");
const logSummary = document.getElementById("log-summary");
const logFilters = document.getElementById("log-filters");
const logRecords = document.getElementById("log-records");

const jsonCache = new Map();
let currentRecords = [];
let currentFilter = "all";

async function listExperiments() {
try {
const res = await fetch(API_RESULTS_URL);
if (!res.ok) throw new Error(`GitHub API ${res.status}`);
const entries = await res.json();
const names = entries.filter(e => e.type === "file" && e.name.endsWith(".json"))
.map(e => e.name).sort();
if (!names.length) throw new Error("no JSON files listed");
return names;
} catch (err) {
// Rate-limited or offline: fall back to the known list
return FALLBACK_EXPERIMENTS;
}
}

async function fetchExperiment(name) {
if (jsonCache.has(name)) return jsonCache.get(name);
const res = await fetch(RAW_BASE + name);
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const data = await res.json();
jsonCache.set(name, data);
return data;
}

function el(tag, className, text) {
const node = document.createElement(tag);
if (className) node.className = className;
if (text !== undefined) node.textContent = text;
return node;
}

function classify(rec) {
const ev = rec.evaluation || {};
if (ev.valid === false) return "invalid";
return ev.correct ? "compliant" : "gamed";
}

function makeRecord(rec, idx) {
const status = classify(rec);
const card = el("div", "log-record");
const head = el("div", "record-head");
head.setAttribute("role", "button");
head.setAttribute("tabindex", "0");
head.setAttribute("aria-expanded", "false");
head.append(
el("span", "record-idx", String(idx + 1).padStart(2, "0")),
el("span", "record-run", rec.run || "run"),
el("span", "record-model", (rec.config && rec.config.model) || "")
);
const output = el("span", "record-output");
const numText = rec.response && typeof rec.response.text === "string"
? rec.response.text.trim() : "";
output.append(
el("span", "record-num", numText || "—"),
el("span", `badge badge-${status}`,
status === "gamed" ? "odd / gamed"
: status === "compliant" ? "even / compliant" : "invalid"));
head.appendChild(output);

const body = el("div", "record-body");
const inputBlock = el("div", "record-block");
inputBlock.append(el("div", "record-block-label", "Prompt sent"), el("pre", null, rec.input || ""));
const textBlock = el("div", "record-block");
textBlock.append(el("div", "record-block-label", "Final answer"), el("pre", null, numText || "—"));
const thinkBlock = el("div", "record-block");
thinkBlock.append(el("div", "record-block-label", "Chain of thought"),
el("pre", null, (rec.response && rec.response.thinking) || "(no chain of thought recorded)"));
body.append(inputBlock, textBlock, thinkBlock);

function toggle() {
const open = body.classList.toggle("open");
head.setAttribute("aria-expanded", String(open));
}
head.addEventListener("click", toggle);
head.addEventListener("keydown", e => {
if (e.key === "Enter" || e.key === " ") {
e.preventDefault();
toggle();
}
});

card.append(head, body);
return card;
}

function renderRecords() {
const visible = currentRecords.filter(rec => {
if (currentFilter === "all") return true;
return classify(rec) === currentFilter;
});
logRecords.textContent = "";
if (!visible.length) {
logRecords.appendChild(el("div", "log-empty", "No runs match this filter."));
return;
}
visible.forEach((rec, i) => logRecords.appendChild(makeRecord(rec, i)));
}

function renderExperiment(data, name) {
logTitle.textContent = name.replace(".json", "");
logRaw.href = RAW_BASE + name;
logRaw.hidden = false;

const recs = Array.isArray(data.results) ? data.results : [];
currentRecords = recs;
const valid = recs.filter(r => r.evaluation && r.evaluation.valid !== false);
const gamed = valid.filter(r => !r.evaluation.correct).length;

logSummary.hidden = false;
logSummary.textContent = "";
const total = el("span");
total.append(el("strong", null, String(recs.length)), document.createTextNode(" runs"));
const gamedSpan = el("span");
gamedSpan.append(el("strong", null, String(gamed)), document.createTextNode(" gamed"));
const models = [...new Set(recs.map(r => r.config && r.config.model).filter(Boolean))];
const modelSpan = el("span");
modelSpan.append(el("strong", null, models.join(", ") || "—"), document.createTextNode(" model"));
logSummary.append(total, gamedSpan, modelSpan);

logFilters.hidden = false;
renderRecords();
}

async function selectExperiment(name, btn) {
expList.querySelectorAll(".exp-item").forEach(b => b.classList.remove("active"));
btn.classList.add("active");
currentFilter = "all";
logFilters.querySelectorAll(".log-filter").forEach(b =>
b.classList.toggle("active", b.dataset.filter === "all"));
logTitle.textContent = `Loading ${name.replace(".json", "")}…`;
logRaw.hidden = true;
logSummary.hidden = true;
logFilters.hidden = true;
logRecords.textContent = "";
logRecords.appendChild(el("div", "log-empty", "Fetching log from GitHub…"));
try {
const data = await fetchExperiment(name);
renderExperiment(data, name);
} catch (err) {
logTitle.textContent = "Could not load this log";
logRecords.textContent = "";
const msg = el("div", "log-error",
`Failed to fetch ${name} (${err.message}). If you are viewing this page locally, `);
msg.appendChild(Object.assign(document.createElement("a"), {
href: `https://github.com/${REPO}/tree/main/results`,
target: "_blank",
rel: "noopener",
textContent: "browse the logs on GitHub"
}));
logRecords.appendChild(msg);
}
}

expFiltersInit();
function expFiltersInit() {
logFilters.addEventListener("click", e => {
const btn = e.target.closest(".log-filter");
if (!btn) return;
currentFilter = btn.dataset.filter;
logFilters.querySelectorAll(".log-filter").forEach(b =>
b.classList.toggle("active", b === btn));
renderRecords();
});
}

async function initLogs() {
const names = await listExperiments();
expCount.textContent = String(names.length);
expList.textContent = "";
names.forEach(name => {
const item = el("button", "exp-item", name.replace(".json", ""));
item.setAttribute("role", "option");
item.setAttribute("aria-selected", "false");
item.addEventListener("click", () => {
expList.querySelectorAll(".exp-item").forEach(b => b.setAttribute("aria-selected", "false"));
item.setAttribute("aria-selected", "true");
selectExperiment(name, item);
});
expList.appendChild(item);
});
logRecords.textContent = "";
logRecords.appendChild(el("div", "log-empty", "Pick an experiment on the left to browse its runs."));
}

initLogs();

// Live star count from the GitHub API
async function initStars() {
const navCount = document.getElementById("star-count-nav");
const loveCount = document.getElementById("star-count-love");
try {
const res = await fetch(`https://api.github.com/repos/${REPO}`);
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const data = await res.json();
const n = data.stargazers_count || 0;
const label = n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, "") + "k" : String(n);
if (navCount) navCount.textContent = n === 0 ? "Star" : label;
// A bare "0" reads as a dead repo — turn it into an invitation instead
if (loveCount) loveCount.textContent = n === 0 ? "be the first" : label;
} catch (err) {
// API unavailable (rate limit / offline): keep the buttons usable without a count
if (navCount) navCount.textContent = "Star";
if (loveCount) loveCount.textContent = "★";
}
}

initStars();
