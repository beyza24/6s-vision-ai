/* Denetim paneli. Sahip: k4. API varsa ona bağlanır, yoksa mock.js kullanır. */
const STATUS_TR = {
  open: "Açık",
  review: "İnceleme",
  resolved: "Çözüldü",
  false_alarm: "Yanlış alarm",
};
const PRIORITY_TR = { high: "Yüksek", medium: "Orta", low: "Düşük" };
const PRINCIPLE_TR = {
  seiri: "Ayıklama",
  seiton: "Düzen",
  seiso: "Temizlik",
  seiketsu: "Standartlaştırma",
  shitsuke: "Disiplin",
  safety: "Güvenlik",
};

let selectedId = null;
let useMock = false;

function notice(text) {
  const el = document.getElementById("notice");
  if (!text) {
    el.hidden = true;
    el.textContent = "";
    return;
  }
  el.hidden = false;
  el.textContent = text;
}

function chip(className, label) {
  const span = document.createElement("span");
  span.className = "chip " + className;
  span.textContent = label;
  return span;
}

async function api(path, opts) {
  if (useMock) return mockApi(path, opts);
  try {
    const res = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  } catch (err) {
    if (path === "/api/incidents" || path === "/api/scores/6s") {
      useMock = true;
      notice("API yok. Panel örnek veriyle çalışıyor.");
      return mockApi(path, opts);
    }
    throw err;
  }
}

function renderList(items) {
  const ul = document.getElementById("incident-list");
  ul.innerHTML = "";
  if (!items.length) {
    const li = document.createElement("li");
    li.className = "mute";
    li.textContent = "Henüz olay yok. Demo butonunu kullanın.";
    ul.appendChild(li);
    return;
  }
  for (const it of items) {
    const li = document.createElement("li");
    li.dataset.id = it.id;
    if (it.id === selectedId) li.classList.add("sel");
    const title = document.createElement("b");
    title.textContent = it.title;
    const row = document.createElement("div");
    row.className = "chips";
    row.append(
      chip(it.priority, PRIORITY_TR[it.priority] || it.priority),
      chip(it.status, STATUS_TR[it.status] || it.status),
      chip("conf", "güven " + Math.round(it.confidence * 100) + "%")
    );
    li.append(title, row);
    li.onclick = () => selectIncident(it.id);
    ul.appendChild(li);
  }
}

function renderCouncil(council) {
  const box = document.getElementById("council-box");
  const votesUl = document.getElementById("d-council-votes");
  votesUl.innerHTML = "";
  if (!council) {
    box.hidden = true;
    return;
  }
  box.hidden = false;
  document.getElementById("d-council-syn").textContent =
    (council.mode === "live" ? "Canlı konsey. " : "Sahte konsey. ") + (council.synthesis || "");
  const dissent = document.getElementById("d-council-dissent");
  dissent.textContent = council.dissent ? council.dissent : "Muhalif görüş yok.";
  for (const vote of council.votes || []) {
    const li = document.createElement("li");
    li.className = "vote";
    const head = document.createElement("div");
    head.className = "vote-head";
    const name = document.createElement("b");
    name.textContent = vote.model_name + " · " + vote.provider;
    head.append(
      name,
      chip(vote.is_violation ? "high" : "resolved", vote.is_violation ? "ihlal" : "ihlal yok"),
      chip(vote.priority, PRIORITY_TR[vote.priority] || vote.priority)
    );
    const bar = document.createElement("div");
    bar.className = "bar";
    const fill = document.createElement("i");
    fill.style.width = Math.round(vote.confidence * 100) + "%";
    bar.appendChild(fill);
    const why = document.createElement("p");
    why.textContent = vote.rationale || "";
    li.append(head, bar, why);
    votesUl.appendChild(li);
  }
}

async function selectIncident(id) {
  selectedId = id;
  const it = await api("/api/incidents/" + id);
  document.getElementById("detail-empty").hidden = true;
  document.getElementById("detail-body").hidden = false;
  document.getElementById("d-title").textContent = it.title;
  const status = document.getElementById("d-status");
  status.className = "chip " + it.status;
  status.textContent = STATUS_TR[it.status] || it.status;
  document.getElementById("d-meta").textContent =
    (PRINCIPLE_TR[it.principle_6s] || it.principle_6s) +
    " · " +
    it.category +
    (it.description ? " · " + it.description : "") +
    (it.assignee ? " · " + it.assignee : "");
  document.getElementById("d-explain").textContent = it.ai_explanation || "Açıklama yok.";
  const plan = document.getElementById("d-plan");
  plan.innerHTML = "";
  for (const step of it.action_plan || []) {
    const li = document.createElement("li");
    li.textContent = step;
    plan.appendChild(li);
  }
  renderCouncil(it.council);
  refreshList();
}

async function refreshList() {
  const items = await api("/api/incidents");
  renderList(items);
}

async function refreshScores() {
  const scores = await api("/api/scores/6s");
  const root = document.getElementById("scores");
  root.innerHTML = "";
  const order = ["seiri", "seiton", "seiso", "seiketsu", "shitsuke", "safety"];
  for (const key of order) {
    const value = Number(scores[key] ?? 0);
    const card = document.createElement("div");
    card.className = "score";
    const label = document.createElement("span");
    label.textContent = PRINCIPLE_TR[key];
    const num = document.createElement("b");
    num.textContent = String(Math.round(value));
    const bar = document.createElement("div");
    bar.className = "bar";
    const fill = document.createElement("i");
    fill.style.width = Math.max(0, Math.min(100, value)) + "%";
    bar.appendChild(fill);
    card.append(label, num, bar);
    root.appendChild(card);
  }
  const overall = document.createElement("div");
  overall.className = "score overall";
  const label = document.createElement("span");
  label.textContent = "Genel";
  const num = document.createElement("b");
  num.textContent = String(Math.round(Number(scores.overall ?? 0)));
  overall.append(label, num);
  root.appendChild(overall);
}

async function runAction(work) {
  notice("");
  try {
    await work();
  } catch (err) {
    notice("İşlem tamamlanamadı. " + (err && err.message ? err.message : ""));
  }
}

document.getElementById("btn-demo").onclick = () =>
  runAction(async () => {
    const it = await api("/api/demo/spawn", { method: "POST" });
    await refreshList();
    await refreshScores();
    await selectIncident(it.id);
  });

document.getElementById("btn-council").onclick = () =>
  runAction(async () => {
    await api("/api/incidents/" + selectedId + "/council", { method: "POST" });
    await selectIncident(selectedId);
  });

document.getElementById("btn-confirm").onclick = () =>
  runAction(async () => {
    await api("/api/incidents/" + selectedId + "/confirm", { method: "POST" });
    await selectIncident(selectedId);
  });

document.getElementById("btn-false").onclick = () =>
  runAction(async () => {
    await api("/api/incidents/" + selectedId + "/false-alarm", { method: "POST" });
    await selectIncident(selectedId);
    await refreshScores();
  });

document.getElementById("btn-assign").onclick = () =>
  runAction(async () => {
    await api("/api/incidents/" + selectedId + "/assign", {
      method: "POST",
      body: JSON.stringify({ assignee: "İSG Uzmanı", note: "Faaliyet atandı" }),
    });
    await selectIncident(selectedId);
    await refreshScores();
  });

refreshList().catch((err) => notice(err.message));
refreshScores().catch((err) => notice(err.message));
