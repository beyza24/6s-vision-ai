# 6S-VISION AI

Yapay zekâ destekli fabrika düzeni ve iş güvenliği denetim paneli.  
**Yapay zekâ görür, insan karar verir.**

ICAAD 2026 · AI-Deathon · Selçuk Üniversitesi

## Ekip

| Kişi | GitHub | Rol |
|------|--------|-----|
| K1 | [@beyza24](https://github.com/beyza24) | Omurga + koordinatör (merge) |
| K2 | [@nazlibeyza](https://github.com/nazlibeyza) | Görüntü / tespit |
| K3 | [@ramazanhsnylmz](https://github.com/ramazanhsnylmz) | 6S skor + kurallar + AI açıklama |
| K4 | [@cosareda](https://github.com/cosareda) | Denetim paneli UI |

Süreç: `AGENTS.md` · Plan: `docs/PLAN.md` · Promptlar: `docs/BASLANGIC-PROMPTLARI.md`

## Hızlı başlangıç

```bash
gh repo clone beyza24/6s-vision-ai
cd 6s-vision-ai
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Aç: http://127.0.0.1:8000/ · API docs: http://127.0.0.1:8000/docs

```bash
python -m pytest -q
```

## Hakem demosu (2 dk)

1. **Demo: yeni tespit** → baretsiz çalışan (%94)  
2. AI açıklama + eylem planı  
3. **Doğrula** → **Faaliyet ata & çöz** → skor güncellenir  
4. İstersen **Yanlış Alarm** ile insan kapısını göster  

## Problem (kısa)

6S/İSG turları periyodik; kameralar var ama sürekli izleyen yok. İhlaller geç fark edilir.

## Çözüm akışı

Gözlemle → Tespit et → 6S ile ilişkilendir → İnsan doğrular → Düzelt ve izle
