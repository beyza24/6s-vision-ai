/* k4 owns this file — bootstrap by coordinator for demo wiring */
const API = "";
let selectedId = null;

async function api(path, opts) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function renderList(items) {
  const ul = document.getElementById("incident-list");
  ul.innerHTML = "";
  if (!items.length) {
    ul.innerHTML = '<li class="mute">Henüz olay yok. Demo butonunu kullanın.</li>';
    return;
  }
  for (const it of items) {
    const li = document.createElement("li");
    li.dataset.id = it.id;
    if (it.id === selectedId) li.classList.add("sel");
    li.innerHTML = `<b>${it.title}</b><div class="mute">${it.priority} · ${it.status} · güven ${(it.confidence * 100).toFixed(0)}%</div>`;
    li.onclick = () => selectIncident(it.id);
    ul.appendChild(li);
  }
}

async function selectIncident(id) {
  selectedId = id;
  const it = await api(`/api/incidents/${id}`);
  document.getElementById("detail-empty").hidden = true;
  document.getElementById("detail-body").hidden = false;
  document.getElementById("d-title").textContent = it.title;
  document.getElementById("d-meta").textContent = `${it.principle_6s} · ${it.category} · ${it.description}`;
  document.getElementById("d-explain").textContent = it.ai_explanation || "—";
  const plan = document.getElementById("d-plan");
  plan.innerHTML = "";
  for (const step of it.action_plan || []) {
    const li = document.createElement("li");
    li.textContent = step;
    plan.appendChild(li);
  }
  const box = document.getElementById("council-box");
  const votesUl = document.getElementById("d-council-votes");
  votesUl.innerHTML = "";
  if (it.council) {
    box.hidden = false;
    document.getElementById("d-council-syn").textContent =
      `[${it.council.mode}] ${it.council.synthesis || ""}`;
    document.getElementById("d-council-dissent").textContent = it.council.dissent
      ? `Muhalefet: ${it.council.dissent}`
      : "Muhalefet yok.";
    for (const v of it.council.votes || []) {
      const li = document.createElement("li");
      li.textContent = `${v.model_name} (${v.provider}): ${
        v.is_violation ? "ihlal" : "ihlal yok"
      } · ${v.priority} · ${(v.confidence * 100).toFixed(0)}% — ${v.rationale}`;
      votesUl.appendChild(li);
    }
  } else {
    box.hidden = true;
  }
  refreshList();
}

async function refreshList() {
  const items = await api("/api/incidents");
  renderList(items);
}

async function refreshScores() {
  const s = await api("/api/scores/6s");
  document.getElementById("scores").textContent = JSON.stringify(s, null, 2);
}

document.getElementById("btn-demo").onclick = async () => {
  const it = await api("/api/demo/spawn", { method: "POST" });
  await refreshList();
  await refreshScores();
  await selectIncident(it.id);
};

document.getElementById("btn-council").onclick = async () => {
  if (!selectedId) return;
  await api(`/api/incidents/${selectedId}/council`, { method: "POST" });
  await selectIncident(selectedId);
};

document.getElementById("btn-confirm").onclick = async () => {
  if (!selectedId) return;
  await api(`/api/incidents/${selectedId}/confirm`, { method: "POST" });
  await selectIncident(selectedId);
};

document.getElementById("btn-false").onclick = async () => {
  if (!selectedId) return;
  await api(`/api/incidents/${selectedId}/false-alarm`, { method: "POST" });
  await selectIncident(selectedId);
  await refreshScores();
};

document.getElementById("btn-assign").onclick = async () => {
  if (!selectedId) return;
  await api(`/api/incidents/${selectedId}/assign`, {
    method: "POST",
    body: JSON.stringify({ assignee: "İSG Uzmanı", note: "Baret temini" }),
  });
  await selectIncident(selectedId);
  await refreshScores();
};

refreshList().catch(console.error);
refreshScores().catch(console.error);
