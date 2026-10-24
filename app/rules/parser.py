"""Doğal dil kural taslağı. Sahip: k3. Onay olmadan aktif olmaz."""
from __future__ import annotations

import re
from uuid import uuid4

from app.schemas import Priority, Principle6S, RuleDraft

_ZONE = re.compile(r"(hat\s*\d+|depo|saha|giriş|giris|koridor)", re.IGNORECASE)


def parse_natural_language_rule(text: str) -> RuleDraft:
    lowered = text.lower()
    principle = Principle6S.shitsuke
    if any(word in lowered for word in ("baret", "kke", "eldiven", "gözlük", "gozluk", "güvenlik", "guvenlik")):
        principle = Principle6S.safety
    elif any(word in lowered for word in ("temiz", "çöp", "cop", "leke", "atık", "atik")):
        principle = Principle6S.seiso
    elif any(word in lowered for word in ("yerinde", "düzen", "duzen", "etiket", "raf")):
        principle = Principle6S.seiton
    elif any(word in lowered for word in ("ayıkl", "ayik", "gereksiz", "hurda")):
        principle = Principle6S.seiri
    elif any(word in lowered for word in ("standart", "prosedür", "prosedur", "bakım", "bakim")):
        principle = Principle6S.seiketsu

    priority = Priority.medium
    if any(word in lowered for word in ("baret", "yasak", "acil", "zorunlu", "tehlike")):
        priority = Priority.high
    elif any(word in lowered for word in ("tercih", "uygun olduğunda", "uygun oldugunda")):
        priority = Priority.low

    zone_match = _ZONE.search(text)
    zone = zone_match.group(1) if zone_match else ""
    return RuleDraft(
        id=str(uuid4()),
        raw_text=text,
        zone=zone,
        condition=text.strip(),
        principle_6s=principle,
        priority=priority,
        notify="isg",
        status="pending_approval",
    )
