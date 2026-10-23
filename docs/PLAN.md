# 6S-VISION AI — Ürün Planı

**Slogan:** Yapay zekâ görür, insan karar verir.  
**Etkinlik:** ICAAD 2026 · AI-Deathon  
**Repo:** beyza24/6s-vision-ai  
**Referans prototip:** `prototype/6s-vision-ai.html`

## 1. Açık kararlar

| Karar | Sahip | Durum |
|-------|-------|--------|
| Tespit ilk turda sahte/adaptor; gerçek model pilot sonrası | k1 | kilitli |
| Ortak şema yalnız k1 değiştirir | k1 | kilitli |
| UI `frontend/` altında; prototip salt referans | k4 | kilitli |
| Merge yalnız k1 (@beyza24) | k1 | kilitli |

## 2. Hakem kriterleri (hedef kanıt)

| Kriter (20) | Kanıt |
|-------------|--------|
| Problem gerçekliği | Sunum + README problem özeti |
| YZ kullanımı | Tespit + 6S eşleme + açıklama + NL kural |
| Uygulanabilirlik | Mevcut kamera / Faz 1 tek hat; çalışan API+UI |
| İnsan–YZ güvenilirlik | Doğrula / yanlış alarm / düşük güven→inceleme |
| Sunum | Demo scripti: tespit→onay→faaliyet→skor |

## 3. Teknik kararlar (yalnız k1)

- Backend: Python 3.11 + FastAPI
- Store: bellek içi (hackathon); şema `app/schemas.py`
- Frontend: statik panel (`frontend/`), API'ye bağlanır
- Vision: `Detector` arayüzü + `FakeDetector` (k2); gerçek model opsiyonel adaptor
- Kurallar: doğal dil → yapılandırılmış kural (k3); onay olmadan aktif olmaz
- Gizlilik: kimlik yok; ihlal kaydı

## 4. Şema / API imzaları (yalnız k1)

### Incident (özet)

- `id`, `camera_id`, `timestamp`
- `category` (kke | duzen | temizlik | trafik | ekipman | diger)
- `principle_6s` (seiri | seiton | seiso | seiketsu | shitsuke | safety)
- `title`, `description`, `priority` (high | medium | low)
- `confidence` (0–1), `status` (open | review | resolved | false_alarm)
- `bbox` opsiyonel, `ai_explanation`, `action_plan`, `assignee` opsiyonel

### Endpoint taslağı

- `GET /health`
- `GET /api/incidents`, `GET /api/incidents/{id}`
- `POST /api/incidents/{id}/confirm`
- `POST /api/incidents/{id}/false-alarm`
- `POST /api/incidents/{id}/assign`
- `GET /api/scores/6s`
- `POST /api/rules/parse` (NL → draft), `POST /api/rules/{id}/approve`
- `POST /api/demo/spawn` (demo tespit)

Alan ekleme → issue #1; uygular k1.

## 5. Klasör sahipliği

Bkz. `AGENTS.md` Bölüm 0 ve `.github/ownership.json`.

## 6–9. (rezerve)

## 10. Gün 1 görevleri

### Kişi 1 — @beyza24

**G1-K1-01 Repo iskeleti ve CI** (S1)  
- Kabul: FastAPI ayağa kalkar, ownership+test CI yeşil, `/health` 200.

**G1-K1-02 Şema ve bellek store** (S1)  
- Kabul: `Incident` modeli + CRUD store; birim test geçer.

**G1-K1-03 Incident API** (S1)  
- Kabul: liste/detay/confirm/false-alarm/assign endpoint'leri; OpenAPI görünür.

**G1-K1-04 Skor ve kural route iskeleti** (S1)  
- Kabul: k3 modüllerini çağıran ince route'lar; fake ile 200.

**G1-K1-05 Demo spawn + CORS** (S1)  
- Kabul: `POST /api/demo/spawn` olay üretir; frontend localhost'tan çağırabilir.

### Kişi 2 — @nazlibeyza

**G1-K2-01a Detector arayüzü + FakeDetector** (S1)  
- Kabul: `detect(frame|path) -> list[Detection]`; fake sabit KKE/zemin örnekleri; test yeşil.

**G1-K2-01b Kamera / feed soyutlaması** (S1)  
- Kabul: `CameraSource` (static image veya placeholder URL); demo için en az 1 kaynak.

**G1-K2-02 Detection → Incident taslağı** (S1)  
- Kabul: ham tespiti şema alanlarına map eden saf fonksiyon; k1 store'una yazmaz, dönüş değeri verir.

### Kişi 3 — @ramazanhsnylmz

**G1-K3-01 6S eşleme ve öncelik** (S1)  
- Kabul: kategori/principle → priority kuralları; test tablosu.

**G1-K3-02 Skor motoru** (S1)  
- Kabul: açık/çözülmüş/tekrarlayan olaylardan 6 boyutlu skor; `GET` için saf fonksiyon.

**G1-K3-03 AI açıklama + eylem planı (şablon)** (S1)  
- Kabul: tespit için açıklama ve 2–3 maddelik eylem planı üretir (şablon veya LLM; anahtar `.env`).

**G1-K3-04 NL kural parser (draft)** (S1)  
- Kabul: örnek cümleden alan/koşul/öncelik/principle çıkarır; durum `pending_approval`.

### Kişi 4 — @cosareda

**G1-K4-01 Prototipten frontend iskeleti** (S1)  
- Kabul: `frontend/` altında çalışan panel; Ana Sayfa iskeleti; prototip kopyalanmış değil modüler dosyalar.

**G1-K4-02 Olay listesi + detay paneli** (S1)  
- Kabul: API yoksa mock JSON; API varsa bağlanır. Durum chip'leri görünür.

**G1-K4-03 İnsan kapıları** (S1)  
- Kabul: Doğrula / Yanlış Alarm / Faaliyet ata butonları API'yi (veya mock) çağırır.

**G1-K4-04 6S skor kartı + demo butonu** (S1)  
- Kabul: skor alanı + "Demo: yeni tespit" hakem demosu için hazır.

## 11. Gün 2 / cilâ (öncelik sırası)

**G2-K2-01** Düşük güven → `review` durumu üretimi  
**G2-K3-05** Yanlış alarm geri bildiriminin eşiğe etkisi (basit)  
**G2-K3-06** Kural onay akışı UI sözleşmesi  
**G2-K4-05** Raporlar ekranı (hafif) + mahremiyet notu UI  
**G2-K1-06** README hakem özeti + demo scripti  
**G2-K1-07** Sunum linkleri / jüri yedek cevapları `docs/JURI.md`

## 12–13. (rezerve)

## 14. Kabul (görev bitişi)

Bir görev bitmiş sayılır ancak:

1. Plandaki **Kabul** satırı sağlanır  
2. `python -m pytest -q` yerel ve CI yeşil  
3. PR açılmış ve issue bağlı  

Merge koordinatördedir; agent merge beklemeden sıradakine geçer.
