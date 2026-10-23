"""Anahtarsız demo konseyi — farklı 'model kişilikleri' ile oy üretir."""
from __future__ import annotations

from app.schemas import (
    Category,
    CouncilMemberVote,
    Incident,
    Priority,
    Principle6S,
)


def _base_principle(incident: Incident) -> Principle6S:
    return incident.principle_6s


def collect_fake_votes(incident: Incident) -> list[CouncilMemberVote]:
    principle = _base_principle(incident)
    title = incident.title.lower()
    looks_kke = incident.category == Category.kke or "baret" in title or "kke" in title

    # Üye A — muhafazakâr güvenlik modeli
    vote_a = CouncilMemberVote(
        member_id="council-a",
        model_name="gpt-family-sim",
        provider="openai-sim",
        is_violation=True if looks_kke else incident.confidence >= 0.5,
        principle_6s=Principle6S.safety if looks_kke else principle,
        priority=Priority.high if looks_kke else incident.priority,
        confidence=min(0.98, max(0.7, incident.confidence + 0.02)),
        rationale="KKE/güvenlik sinyali güçlü; ihlal olasılığı yüksek.",
    )

    # Üye B — bağlamcı, biraz şüpheci
    vote_b = CouncilMemberVote(
        member_id="council-b",
        model_name="claude-family-sim",
        provider="anthropic-sim",
        is_violation=True if looks_kke else incident.confidence >= 0.75,
        principle_6s=principle,
        priority=Priority.high if looks_kke else Priority.medium,
        confidence=min(0.95, max(0.55, incident.confidence - 0.05)),
        rationale="Görüntü bağlamı sınırlı; yine de 6S ilkesine aykırı görünüyor."
        if looks_kke
        else "Kanıt orta seviyede; insan incelemesi önerilir.",
    )

    # Üye C — muhalif / yanlış alarm riski vurgular
    vote_c = CouncilMemberVote(
        member_id="council-c",
        model_name="gemini-family-sim",
        provider="google-sim",
        is_violation=looks_kke and incident.confidence >= 0.6,
        principle_6s=principle,
        priority=Priority.medium if not looks_kke else Priority.high,
        confidence=min(0.9, max(0.4, incident.confidence - 0.12)),
        rationale="Açı/ışık hatası olabilir; çoğunluk ihlal dese bile dissent kaydı düşülmeli."
        if looks_kke
        else "İhlal eşiği net değil; review öneririm.",
    )

    return [vote_a, vote_b, vote_c]
