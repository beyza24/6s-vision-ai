"""Tespit açıklaması ve eylem planı. Sahip: k3. Anahtar gerekmez; şablon yeter."""
from __future__ import annotations

from app.schemas import Category, Principle6S

_PRINCIPLE_TR = {
    Principle6S.seiri: "Ayıklama",
    Principle6S.seiton: "Düzen",
    Principle6S.seiso: "Temizlik",
    Principle6S.seiketsu: "Standartlaştırma",
    Principle6S.shitsuke: "Disiplin",
    Principle6S.safety: "Güvenlik",
}

_PLANS: dict[Category, list[str]] = {
    Category.kke: [
        "Eksik kişisel koruyucuyu hemen tamamla",
        "Hat girişine KKE kontrol noktası koy",
        "Vardiya başı kısa eğitim kaydı aç",
    ],
    Category.temizlik: [
        "Alanı vardiya içinde temizle",
        "Atık noktasını işaretle",
        "Temizlik kontrolünü tur listesine ekle",
    ],
    Category.duzen: [
        "Malzemeyi tanımlı yerine geri koy",
        "Yer etiketini yenile",
        "Hat sonu düzen kontrolü ekle",
    ],
    Category.trafik: [
        "Yaya yolunu boşalt",
        "Araç hız sınırını hatırlat",
        "Geçiş işaretini görünür yap",
    ],
    Category.ekipman: [
        "Ekipmanı güvenli duruma al",
        "Arıza etiketini as",
        "Bakım kaydını aç",
    ],
    Category.diger: [
        "Bulguyu İSG sorumlusuna ilet",
        "Geçici önlemi uygula",
        "Kapanış için faaliyet aç",
    ],
}


def build_explanation(
    *,
    title: str,
    category: Category,
    principle: Principle6S,
) -> tuple[str, list[str]]:
    principle_tr = _PRINCIPLE_TR[principle]
    text = (
        f"{title}. Bu bulgu {principle_tr} ilkesine aykırı bir {category.value} tespitidir. "
        "Öneri yapay zekâdandır; son kararı insan verir."
    )
    return text, list(_PLANS[category])
