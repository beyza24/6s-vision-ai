# 6S-VISION AI — Proje Raporu

ICAAD 2026 · AI-Deathon · Selçuk Üniversitesi  
24 Ekim 2026

**Yapay zekâ görür, insan karar verir.**

Bu rapor, yapılan işi, arayüz ve sunucuda kullanılan yazılım dillerini ve sistemin nasıl kurulduğunu anlatır. Aynı metnin yazdırılabilir kopyası `docs/PROJE-RAPORU.pdf` dosyasındadır.

## 1. Ne yaptık

6S ve iş güvenliği turları belirli aralıklarla yapılır. Fabrikada kamera vardır; kamerayı sürekli izleyen biri her zaman yoktur. İhlal, tur gelene kadar kayıtta kalabilir.

6S-VISION AI bu boşluğu tek bir denetim paneliyle kapatır. Akış şöyledir:

1. Kamera kaydı oynatılır.
2. Görüntü modeli karedeki kişiyi ve kişisel koruyucu ekipmanı etiketler.
3. Kayıtta gerçekten görülen eksiklik, uygunsuzluk listesine bir kez yazılır.
4. Eksiklik sürerse panel “Güvenlik açığı var” uyarısı verir.
5. İş güvenliği uzmanı **Konseyi çalıştır** der. Birden fazla dil modeli aynı olayı ayrı ayrı oylar.
6. Uzman **Doğrulama Yapıldı** veya **Yanlış Alarm** der. İsterse faaliyeti bir kişiye atar.
7. Karar, 6S skoruna ve haftalık vardiya raporuna yansır.

Sistem kişiyi tanımaz. Kayda düşen şey ihlaldir. Son karar her zaman iş güvenliği uzmanındadır. Konsey önerir; paneli kapatmaz.

Bu çalışmada repoda biriken omurga ile panel demosu aynı ekranda buluştu:

- Olay kaydı, durum geçişleri ve skor için çalışan bir API.
- Test videosunun üstünde YOLO etiketleri. Bu kayıtta kötü sınıf olarak “KKE yok” vardır. Listeye bu tespit bir kez düşer.
- On saniyelik süre dolunca listenin üstünde “Güvenlik açığı var” bandı.
- Canlı LLM Council: iki model de ihlal ve yüksek öncelik diyebilir. Oylar, gerekçe ve “Muhalif görüş yok” satırı panelde durur. Bu satır, iki modelin aynı yönde oy verdiği anlamına gelir.
- Doğrulama ve yanlış alarm düğmeleri konsey bittikten sonra da basılabilir. Uzman kararını değiştirebilir.
- Haftalık rapor, iki vardiya, açık kayıt sayısı ve 6S puanlarıyla ekrandan yazdırılır.
- Doğal dille yazılan fabrika kuralı taslak olur. Onaylanmadan devreye girmez.

## 2. Hangi yazılım dilleri kullanıldı

### Arayüz

Arayüz üç dosyadan oluşur. Ayrı bir derleme, paketleyici veya bileşen çerçevesi yoktur.

| Dosya | Dil | Görevi |
|-------|-----|--------|
| `frontend/index.html` | HTML | Sayfa iskeleti, menü, kamera, liste, detay ve düğmeler |
| `frontend/styles.css` | CSS | Koyu denetim masası, kartlar, uyarı bandı, yazdırma düzeni |
| `frontend/app.js` | JavaScript | API çağrıları, sekme, video zamanı, kutu çizimi, konsey ve karar düğmeleri |
| `frontend/mock.js` | JavaScript | API kapalıyken liste ve skor için yedek veri |

Yazı tipi tarayıcıdan IBM Plex Sans ve IBM Plex Mono olarak alınır. Tespit kutuları bir `<canvas>` katmanına, videonun o anki zamanına göre çizilir. Video dosyası HTML5 `<video>` ile oynar.

### Sunucu

Sunucu Python ile yazıldı. Sürüm hedefi sürekli denetimde Python 3.11, yerelde geliştirme Python 3.14 ile yapıldı.

| Araç | Görevi |
|------|--------|
| FastAPI | HTTP API ve OpenAPI sayfası (`/docs`) |
| Uvicorn | Uygulamayı çalıştıran sunucu |
| Pydantic | Olay, skor, kural ve konsey şemaları |
| python-dotenv | Yerel `.env` dosyasını sürece okur |
| httpx | Canlı konseyin model uçlarına isteği |
| pytest | API, skor, kural, konsey ve panel duman testleri |

Kayıtlar hackathon süresince bellek içi bir depoda durur (`app/store.py`). Ayrı bir veritabanı kurulmaz. Sunucu kapanınca bellek temizlenir.

### Görüntü ve konsey

| Katman | Dil ve kütüphane | Görevi |
|--------|------------------|--------|
| Tespit arayüzü | Python | `Detector` sözleşmesi ve anahtarsız örnek tespit |
| Kutu çıkarma | Python, Ultralytics YOLO, OpenCV | `models/best.pt` ile videodaki her kare |
| Konsey | Python | Sahte oy, canlı oy, başkan sentezi |
| Skor ve kural | Python | 6S puanı ve doğal dil kural taslağı |
| CI | YAML | Sahiplik, gizlilik, test ve plan kontrolü |

YOLO sınıf adları: kask, eldiven, yelek, bot, gözlük, KKE yok, kişi, kask yok, gözlük yok, eldiven yok, bot yok. Test kaydı 3840×2160, saniyede 25 kare, 202 karedir. Tarayıcı modeli çalıştırmaz. Kutular önceden `frontend/baret-kask-boxes.json` içine yazılır.

Canlı konsey, OpenAI ile aynı sohbet biçimini kullanan bir uç noktaya gider. Üyeler `.env` içindeki `COUNCIL_MEMBERS` satırından okunur. Demo düzeneğinde iki üye vardır. İki başarılı oy gelirse panel “Canlı konsey” der. Anahtar yoksa veya canlı çağrı tamamlanmazsa aynı sözleşme “Sahte konsey” ile döner. API anahtarı repoya yazılmaz.

## 3. Proje nasıl yapıldı

### Ekip ve repo

Dört kişi tek repoda çalıştı. Herkes kendi klasörünün sahibidir. `main` dalına doğrudan yazılmaz. Değişiklik çekme isteği ile gelir. Koordinatör birleştirir. GitHub Actions; sahiplik, gizli anahtar, beş megabayt üstü dosya, pytest ve plan kurallarını her istekte çalıştırır.

| Kişi | Rol | Sorumlu olduğu yer |
|------|-----|--------------------|
| K1 @beyza24 | Omurga ve birleştirme | `app/` kökü, API, şema, depo, CI |
| K2 @nazlibeyza | Görüntü | `app/vision/` |
| K3 @ramazanhsnylmz | Skor, kural, konsey | `app/scoring/`, `app/rules/`, `app/council/` |
| K4 @cosareda | Denetim paneli | `frontend/` |

### Kuruluş sırası

1. **Prototip.** Panelin yerleşimi önce `prototype/6s-vision-ai.html` içinde, sunucusuz tek dosya olarak denendi.
2. **Sözleşme.** Olayın alanları kilitlendi: kamera, zaman, kategori, 6S ilkesi, başlık, öncelik, güven, durum, açıklama, eylem planı ve isteğe bağlı konsey sonucu. Durumlar açıktır: `open`, `review`, `resolved`, `false_alarm`.
3. **Omurga.** FastAPI ayağa kalktı. `/health` ve olay uçları bellek içi depoya bağlandı. Panel dosyaları aynı sürecin kök yolundan yayınlandı.
4. **Görüntü sözleşmesi.** Tespit, başlık, güven ve kutu döndüren bir arayüze ayrıldı. Testler model dosyası olmadan da geçer. Bunun için sabit örnek tespit vardır.
5. **Skor, kural, konsey.** Açık kayıt puanı düşürür. Yanlış alarm puana girmez. Doğal dil kuralı onay bekleyen taslak olur. Konsey üyeleri bağımsız oy verir. Başkan ilke, öncelik, gerekçe ve muhalefeti tek sonuca bağlar.
6. **Panel.** Menüde ana sayfa, uygunsuzluklar, raporlar, 6S skorları ve ayarlar vardır. Liste satırı detayı açar. Detayda AI analizi, eylem planı, geçmiş ve konsey sekmeleri durur.
7. **Test kaydı.** Eğitilmiş `best.pt` ağırlığı, baret ve kask videosunun her karesinden geçirildi. Kutular zamana göre JSON’a yazıldı. Sayfa, videonun `currentTime` değeriyle aynı kareyi tuvale çizer. Kayıtta olmayan sınıflar listeden çıkarılır.
8. **Canlı karar.** “Konseyi çalıştır” ilgili olay için `POST /api/incidents/{id}/council` çağırır. Dönen oylar konsey sekmesinde gösterilir. Uzman doğrular veya yanlış alarm der. Bu iki düğme, konsey turu bittikten sonra da açık kalır.

### Uçtan uca istek

```text
Tarayıcı  →  GET /  ve  frontend/*.js
Video     →  baret-kask.mp4 + baret-kask-boxes.json
Tespit    →  POST /api/incidents
Konsey    →  POST /api/incidents/{id}/council
Karar     →  POST .../confirm  veya  .../false-alarm
Skor      →  GET /api/scores/6s
```

Panel, `GET /api/incidents` ve `GET /api/scores/6s` cevap vermezse yedek veriyle açılır. Olay oluşturma ve konsey çağrısı yedek veriye düşmez. Böylece canlı konsey sessizce sahte cevaba dönmez.

## 4. Ekranda duran parçalar

- **Kamera.** Test videosu, oynat/duraklat ve YOLO kutuları.
- **Uygunsuzluk listesi.** Kayıttaki eksiklik bir karttır. Aynı başlık ikinci kez eklenmez.
- **Güvenlik açığı.** Kötü sınıf yaklaşık on saniye sürerse kırmızı bant açılır. Kısa kopmalar süreyi sıfırlamaz.
- **Detay.** İlke, durum, güven, AI açıklaması ve önerilen aksiyon.
- **LLM Council.** Üye adı, ihlal oyu, öncelik ve gerekçe. Canlı veya sahte olduğu ilk cümlede yazar.
- **Raporlar.** Haftalık özet, vardiya dağılımı ve yazdırma.
- **6S skorları.** Ayıklama, düzen, temizlik, standartlaştırma, disiplin ve güvenlik.
- **Ayarlar.** Doğal dille kural taslağı ve onay.

## 5. Bilinçli sınırlar

- Depo bellek içindedir. Kalıcı veritabanı bu sürümün dışındadır.
- Video ve `best.pt` boyutu, deponun beş megabayt dosya sınırının üstündedir. Bu iki dosya git’e girmez. Kutu JSON’u da yerelde üretilir.
- Konsey anahtarı yalnız geliştirme makinesindeki `.env` dosyasındadır.
- Yüz tanıma ve kişi eşleme yoktur.
- Haftalık PDF, tarayıcının yazdırma penceresinden alınır. Bu dosya ise projenin kendisini anlatan ayrı rapordur.

## 6. Çalıştırma

```bash
gh repo clone beyza24/6s-vision-ai
cd 6s-vision-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Panel: http://127.0.0.1:8000/  
API belgeleri: http://127.0.0.1:8000/docs  
Test: `python -m pytest -q`

Canlı konsey için `.env` içine uç adres, anahtar ve `COUNCIL_MEMBERS` yazılır. Bu dosya git’e eklenmez. YOLO kutularını yeniden üretmek için video, `models/best.pt` ve `scripts/export_yolo_boxes.py` aynı makinede bulunmalıdır.
