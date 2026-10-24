/* API kapalıyken panelin çalışması için yedek veri. Sahip: k4. */
const MOCK_DB = {
  incidents: [
    {
      id: "mock-1",
      title: "Baretsiz çalışan",
      description: "Üretim Alanı · Hat 2",
      category: "kke",
      principle_6s: "safety",
      priority: "high",
      status: "open",
      confidence: 0.94,
      ai_explanation: "YZ baret eksikliğini buldu. 6S Güvenlik ilkesine aykırı.",
      action_plan: ["Baret temini", "Saha eğitimi", "Hat girişinde KKE kontrolü"],
      assignee: null,
      council: null,
    },
  ],
  scores: {
    seiri: 92,
    seiton: 88,
    seiso: 90,
    seiketsu: 86,
    shitsuke: 91,
    safety: 74,
    overall: 86.8,
  },
};

function mockClone(value) {
  return JSON.parse(JSON.stringify(value));
}

function mockApi(path, opts) {
  const method = (opts && opts.method) || "GET";
  if (path === "/api/incidents" && method === "GET") {
    return Promise.resolve(mockClone(MOCK_DB.incidents));
  }
  if (path === "/api/scores/6s") {
    return Promise.resolve(mockClone(MOCK_DB.scores));
  }
  const detail = path.match(/^\/api\/incidents\/([^/]+)$/);
  if (detail && method === "GET") {
    const item = MOCK_DB.incidents.find((row) => row.id === detail[1]);
    if (!item) return Promise.reject(new Error("not found"));
    return Promise.resolve(mockClone(item));
  }
  if (path === "/api/demo/spawn" && method === "POST") {
    const created = {
      id: "mock-" + Date.now(),
      title: "Baretsiz çalışan",
      description: "Demo tespit",
      category: "kke",
      principle_6s: "safety",
      priority: "high",
      status: "open",
      confidence: 0.94,
      ai_explanation: "Demo: baret eksik. Son karar insanda.",
      action_plan: ["Baret temini", "Hat kontrolü"],
      assignee: null,
      council: {
        mode: "fake",
        synthesis: "Öneri: ihlal var. Son karar İSG uzmanındadır.",
        dissent: "Muhalif görüş — gemini-family-sim (ihlal yok): açı hatası olabilir.",
        votes: [
          {
            model_name: "gpt-family-sim",
            provider: "openai-sim",
            is_violation: true,
            priority: "high",
            confidence: 0.96,
            rationale: "KKE sinyali güçlü.",
          },
          {
            model_name: "claude-family-sim",
            provider: "anthropic-sim",
            is_violation: true,
            priority: "high",
            confidence: 0.9,
            rationale: "6S Güvenlik ilkesine aykırı.",
          },
          {
            model_name: "gemini-family-sim",
            provider: "google-sim",
            is_violation: false,
            priority: "medium",
            confidence: 0.62,
            rationale: "Açı hatası olabilir.",
          },
        ],
      },
    };
    MOCK_DB.incidents.unshift(created);
    MOCK_DB.scores.safety = Math.max(40, MOCK_DB.scores.safety - 4);
    return Promise.resolve(mockClone(created));
  }
  const action = path.match(/^\/api\/incidents\/([^/]+)\/(confirm|false-alarm|assign|council)$/);
  if (action && method === "POST") {
    const item = MOCK_DB.incidents.find((row) => row.id === action[1]);
    if (!item) return Promise.reject(new Error("not found"));
    if (action[2] === "confirm") item.status = "open";
    if (action[2] === "false-alarm") item.status = "false_alarm";
    if (action[2] === "assign") {
      item.status = "resolved";
      item.assignee = "İSG Uzmanı";
    }
    if (action[2] === "council" && !item.council) {
      item.council = mockClone(MOCK_DB.incidents[0].council || {
        mode: "fake",
        synthesis: "Öneri hazır. Son karar İSG uzmanındadır.",
        dissent: "",
        votes: [],
      });
    }
    return Promise.resolve(mockClone(item));
  }
  return Promise.reject(new Error("mock path unsupported: " + path));
}
