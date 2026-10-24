"""Kategori ve 6S ilkesinden öncelik. Sahip: k3."""
from __future__ import annotations

from app.schemas import Category, Priority, Principle6S

_CATEGORY_PRIORITY: dict[Category, Priority] = {
    Category.kke: Priority.high,
    Category.trafik: Priority.high,
    Category.ekipman: Priority.medium,
    Category.duzen: Priority.medium,
    Category.temizlik: Priority.low,
    Category.diger: Priority.low,
}

_PRINCIPLE_FLOOR: dict[Principle6S, Priority] = {
    Principle6S.safety: Priority.high,
    Principle6S.seiri: Priority.medium,
    Principle6S.seiton: Priority.medium,
    Principle6S.seiso: Priority.low,
    Principle6S.seiketsu: Priority.medium,
    Principle6S.shitsuke: Priority.low,
}

_RANK = {Priority.low: 0, Priority.medium: 1, Priority.high: 2}

_CATEGORY_PRINCIPLE: dict[Category, Principle6S] = {
    Category.kke: Principle6S.safety,
    Category.trafik: Principle6S.safety,
    Category.ekipman: Principle6S.seiketsu,
    Category.duzen: Principle6S.seiton,
    Category.temizlik: Principle6S.seiso,
    Category.diger: Principle6S.shitsuke,
}


def map_principle(category: Category) -> Principle6S:
    return _CATEGORY_PRINCIPLE[category]


def map_priority(category: Category, principle: Principle6S) -> Priority:
    """Kategori taban önceliği; ilke tabanı daha yüksekse onu kullan."""
    base = _CATEGORY_PRIORITY[category]
    floor = _PRINCIPLE_FLOOR[principle]
    return base if _RANK[base] >= _RANK[floor] else floor
