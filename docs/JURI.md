# Jüri yedek cevapları

## Yanlış alarm çok olursa?

Güveni düşük tespitler bildirimden önce `review` durumuna düşer. Personelin “Yanlış Alarm” işaretleri eşiği ayarlamak için kullanılır. Pilot hedefi alarm oranını ölçmektir.

## Mahremiyet?

Sistem kişiyi tanımaz, ihlali izler. Kimlik tanıma yok; yüz bulanıklaştırma tasarımda. Amaç cezalandırmak değil riski erken görmek (KVKK).

## YZ bir ihlali kaçırırsa?

Sistem denetimin yerine değil yanına geçer. Periyodik turlar sürer; kamera boşluğunu kapatır.

## Prototip gerçekten çalışıyor mu?

Arayüz ve iş akışı çalışır: doğrulama, faaliyet, skor, kural taslağı. Tespit kutuları bu aşamada örnek/sahte adaptor ile gösterilebilir; gerçek model pilotta bağlanır.

## Hangi model?

Görüntü: nesne tespiti (YOLO ailesi gibi) + fabrikaya özel ince ayar (pilot).  
**Kural ihlali kararı:** tek modele güvenmiyoruz. **LLM Council** (Karpathy tarzı) — birden fazla LLM bağımsız oy verir, bir başkan sentezler; panelde oylar ve muhalefet görünür. Son karar İSG uzmanındadır. Anahtar yoksa demo için fake council çalışır; canlıda OpenAI / OpenRouter / Anthropic / Gemini bağlanabilir.

## Neden konsey, tek model değil?

Yanlış alarm ve ışık/açı hatalarında tek model aşırı emin olabilir. Çoklu model + dissent, insan–YZ güvenilirliğini güçlendirir.

## Neden fabrika?

Kamera altyapısı çoğu zaman var; yeni donanım şart değil. Tekrarlayan ihlaller kayda girer; kazaya giden süre kısalır.
