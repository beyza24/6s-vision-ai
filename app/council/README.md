# LLM Council (k3)

Andrej Karpathy’nin popülerleştirdiği **LLM Council** yaklaşımı:
tek modele güvenmek yerine birden fazla LLM bağımsız değerlendirir;
bir “başkan” oyları sentezler. **Son karar insandadır.**

## Akış

1. Olay özeti (başlık, kategori, görüntü notu, fabrika kuralı) konseyе gider
2. Her üye: ihlal mi? hangi 6S? öncelik? gerekçe?
3. Başkan: çoğunluk + muhalefet notu → `CouncilVerdict`
4. Panelde oylar görünür; İSG uzmanı onaylar / yanlış alarm der

## Dosyalar

- `members.py` — üye tanımları (OpenAI / Anthropic / Gemini / OpenRouter …)
- `fake.py` — anahtarsız demo (3 sahte üye + başkan)
- `live.py` — gerçek API çağrıları (OpenAI-uyumlu endpoint’ler)
- `deliberate.py` — `run_council(incident) -> CouncilVerdict`
- `chairman.py` — oy birleştirme kuralları

## Env

Bkz. kök `.env.example` → `COUNCIL_*` anahtarları.
Anahtar yoksa otomatik `fake` mod.
