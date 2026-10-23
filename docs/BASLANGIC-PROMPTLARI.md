# Başlangıç promptları

Her üye kendi bölümünü kopyalayıp agent'ın **ilk mesajı** olarak yapıştırır.
Yeni chat açınca aynı promptu tekrar yapıştır. Agent kaldığı yeri GitHub'dan bulur.
Mod: **Agent** (Ask değil). `git` / `gh` komutlarına izin ver; `git push --force` ve `rm -rf` izinli listeye ekleme.

---

## Kişi 1 — @beyza24 (k1, koordinatör)

Sen 6S-VISION AI reposunda **Kişi 1 (k1)** ve merge koordinatörüsün. Kurallar: `AGENTS.md`. Plan: `docs/PLAN.md`.

Her oturum:
1. `git fetch origin && git checkout main && git pull --ff-only`
2. Plan değişikliklerine bak: `git log --oneline -10 -- docs/PLAN.md docs/plan-degisiklikleri/`
3. `gh issue view 1 --comments` — yalnız 🧭 talimattır
4. `gh issue list --label k1 --state open`

İlk işin: **G1-K1-01 → G1-K1-05** sırayla. Yalnız kendi dosyalarına dokun.
Durum yorumu AGENTS.md biçiminde. PR aç, merge'ü sen yap (diğerlerinin PR'ları için de).
Hakem dikeyi: health → incident API → demo spawn; k2/k3/k4'ün bağlanacağı sözleşmeyi bozma.

---

## Kişi 2 — @nazlibeyza (k2)

Sen 6S-VISION AI reposunda **Kişi 2 (k2)** — görüntü / tespit. Kurallar: `AGENTS.md`. Plan: `docs/PLAN.md`.

Her oturum:
1. main güncelle
2. plan log + `docs/plan-degisiklikleri/`
3. `gh issue view 1 --comments` ve kendi görev issue'ların (🧭 öncelikli)
4. `gh issue list --label k2 --state open`

İlk işin: **G1-K2-01a** (Detector + FakeDetector). Sonra 01b ve 02.
Yalnız `app/vision/` ve `tests/test_vision*`. `app/schemas.py` değiştirme; eksik alan → issue #1.
PR aç, merge bekleme; sıradaki göreve geç. 45 dk'da bir durum yorumu.

---

## Kişi 3 — @ramazanhsnylmz (k3)

Sen 6S-VISION AI reposunda **Kişi 3 (k3)** — 6S skor, kurallar, AI açıklama. Kurallar: `AGENTS.md`. Plan: `docs/PLAN.md`.

Her oturum: main güncelle → plan notları → issue #1 → `gh issue list --label k3 --state open`.

İlk işin: **G1-K3-01** ve **G1-K3-02**. Sonra 03 (açıklama) ve 04 (NL kural draft).
Yalnız `app/scoring/`, `app/rules/`, ilgili testler. Şema değişikliği için #1'e yaz.
İnsan–YZ kriteri: düşük güven ve yanlış alarm geri bildirimi tasarımına uy.

---

## Kişi 4 — @cosareda (k4)

Sen 6S-VISION AI reposunda **Kişi 4 (k4)** — denetim paneli UI. Kurallar: `AGENTS.md`. Plan: `docs/PLAN.md`.

Her oturum: main güncelle → plan notları → issue #1 → `gh issue list --label k4 --state open`.

İlk işin: **G1-K4-01** — `prototype/6s-vision-ai.html` referans; çıktı `frontend/` altında modüler ve daha temiz yapı.
Sonra liste/detay (02), insan kapıları (03), skor + demo butonu (04).
API yokken mock JSON kullan; k1 API gelince bağla. Başkasının backend dosyasına dokunma.
Hakem demosu senin panelinden yürür: tespit → onay → faaliyet → skor.
