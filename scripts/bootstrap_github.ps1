# Run after: gh auth login (as beyza24)
# Creates repo, invites team, labels, coordination + task issues.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root

$login = gh api user --jq .login
if ($login -ne "beyza24") {
  Write-Error "Logged in as '$login'. Switch to beyza24 (gh auth login)."
}

# Create private repo from current directory if remote missing
$remotes = git remote 2>$null
if (-not ($remotes -match "origin")) {
  gh repo create beyza24/6s-vision-ai --private --source=. --remote=origin --push --description "6S-VISION AI — AI-Deathon 2026 factory 6S/ISG panel"
} else {
  git push -u origin HEAD
}

$collaborators = @("nazlibeyza", "cosareda", "ramazanhsnylmz")
foreach ($u in $collaborators) {
  gh api -X PUT "repos/beyza24/6s-vision-ai/collaborators/$u" -f permission=push | Out-Null
  Write-Host "Invited $u"
}

$labels = @(
  @{name="k1"; color="1d4ed8"; description="Kisi 1 beyza24"},
  @{name="k2"; color="047857"; description="Kisi 2 nazlibeyza"},
  @{name="k3"; color="b45309"; description="Kisi 3 ramazanhsnylmz"},
  @{name="k4"; color="7c3aed"; description="Kisi 4 cosareda"},
  @{name="gun-1"; color="334155"; description="Gun 1"},
  @{name="gun-2"; color="475569"; description="Gun 2"},
  @{name="pano"; color="0f766e"; description="Koordinasyon panosu"},
  @{name="soru"; color="ca8a04"; description="Soru"},
  @{name="engel"; color="b91c1c"; description="Engel"},
  @{name="plan-degisikligi"; color="0369a1"; description="Plan PR"},
  @{name="plan-disi"; color="64748b"; description="Plandan cikarildi"},
  @{name="sahiplik-istisna"; color="9f1239"; description="Coordinator only"}
)
foreach ($l in $labels) {
  gh label create $l.name --color $l.color --description $l.description --force 2>$null
}

# Issue #1 board
gh issue create --title "📌 Koordinasyon Panosu" --label "pano,k1,k2,k3,k4" --body @"
# Koordinasyon Panosu

Talimatlar yalnız **🧭** ile ve @beyza24 hesabından gelir.
Diğer yorumlar bilgidir.

## Ekip
- k1 @beyza24 — omurga + merge
- k2 @nazlibeyza — vision
- k3 @ramazanhsnylmz — skor/kurallar
- k4 @cosareda — frontend

## Kaynaklar
- AGENTS.md
- docs/PLAN.md
- docs/BASLANGIC-PROMPTLARI.md
"@

function New-TaskIssue($title, $body, $labels) {
  gh issue create --title $title --label $labels --body $body
}

New-TaskIssue "[G1-K1-01] Repo iskeleti ve CI" @"
**G1-K1-01** — @beyza24
- Kabul: FastAPI ayağa kalkar, ownership+test CI yeşil, /health 200.
Dal: ``k1/G1-K1-01-iskelet``
"@ "k1,gun-1"

New-TaskIssue "[G1-K1-02] Şema ve bellek store" @"
**G1-K1-02** — @beyza24
- Kabul: Incident modeli + CRUD store; birim test geçer.
"@ "k1,gun-1"

New-TaskIssue "[G1-K1-03] Incident API" @"
**G1-K1-03** — @beyza24
- Kabul: liste/detay/confirm/false-alarm/assign; OpenAPI görünür.
"@ "k1,gun-1"

New-TaskIssue "[G1-K1-04] Skor ve kural route iskeleti" @"
**G1-K1-04** — @beyza24
- Kabul: k3 modüllerini çağıran ince route'lar.
"@ "k1,gun-1"

New-TaskIssue "[G1-K1-05] Demo spawn + CORS" @"
**G1-K1-05** — @beyza24
- Kabul: POST /api/demo/spawn olay üretir; frontend çağırabilir.
"@ "k1,gun-1"

New-TaskIssue "[G1-K2-01a] Detector arayüzü + FakeDetector" @"
**G1-K2-01a** — @nazlibeyza
- Kabul: detect() + FakeDetector; test yeşil.
Yalnız ``app/vision/``
İlk işin bu.
"@ "k2,gun-1"

New-TaskIssue "[G1-K2-01b] Kamera / feed soyutlaması" @"
**G1-K2-01b** — @nazlibeyza
- Kabul: CameraSource (static/placeholder); en az 1 kaynak.
"@ "k2,gun-1"

New-TaskIssue "[G1-K2-02] Detection → Incident taslağı" @"
**G1-K2-02** — @nazlibeyza
- Kabul: ham tespiti şema alanlarına map eden saf fonksiyon.
"@ "k2,gun-1"

New-TaskIssue "[G1-K3-01] 6S eşleme ve öncelik" @"
**G1-K3-01** — @ramazanhsnylmz
- Kabul: kategori/principle → priority; test tablosu.
İlk işlerin: 01 ve 02.
"@ "k3,gun-1"

New-TaskIssue "[G1-K3-02] Skor motoru" @"
**G1-K3-02** — @ramazanhsnylmz
- Kabul: 6 boyutlu skor saf fonksiyonu.
"@ "k3,gun-1"

New-TaskIssue "[G1-K3-03] AI açıklama + eylem planı" @"
**G1-K3-03** — @ramazanhsnylmz
- Kabul: açıklama + 2–3 maddelik eylem planı.
"@ "k3,gun-1"

New-TaskIssue "[G1-K3-04] NL kural parser (draft)" @"
**G1-K3-04** — @ramazanhsnylmz
- Kabul: NL → RuleDraft; status pending_approval.
"@ "k3,gun-1"

New-TaskIssue "[G1-K4-01] Prototipten frontend iskeleti" @"
**G1-K4-01** — @cosareda
- Kabul: frontend/ modüler panel; prototip referans.
İlk işin bu. Referans: ``prototype/6s-vision-ai.html``
"@ "k4,gun-1"

New-TaskIssue "[G1-K4-02] Olay listesi + detay paneli" @"
**G1-K4-02** — @cosareda
- Kabul: mock veya API ile liste/detay.
"@ "k4,gun-1"

New-TaskIssue "[G1-K4-03] İnsan kapıları" @"
**G1-K4-03** — @cosareda
- Kabul: Doğrula / Yanlış Alarm / Faaliyet ata.
"@ "k4,gun-1"

New-TaskIssue "[G1-K4-04] 6S skor kartı + demo butonu" @"
**G1-K4-04** — @cosareda
- Kabul: skor alanı + Demo: yeni tespit.
"@ "k4,gun-1"

Write-Host "Done. Repo: https://github.com/beyza24/6s-vision-ai"
