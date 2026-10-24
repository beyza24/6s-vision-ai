"""Başkan: bağımsız oyları tek CouncilVerdict'e indirger."""
from __future__ import annotations

from collections import Counter

from app.schemas import CouncilMemberVote, CouncilVerdict, Priority, Principle6S

_PRINCIPLE_TR = {
    Principle6S.seiri: "Ayıklama",
    Principle6S.seiton: "Düzen",
    Principle6S.seiso: "Temizlik",
    Principle6S.seiketsu: "Standartlaştırma",
    Principle6S.shitsuke: "Disiplin",
    Principle6S.safety: "Güvenlik",
}
_PRIORITY_TR = {
    Priority.high: "yüksek",
    Priority.medium: "orta",
    Priority.low: "düşük",
}


def synthesize(votes: list[CouncilMemberVote], *, mode: str) -> CouncilVerdict:
    if not votes:
        return CouncilVerdict(
            is_violation=False,
            principle_6s=Principle6S.safety,
            priority=Priority.low,
            confidence=0.0,
            synthesis="Konsey oyu yok.",
            dissent="",
            votes=[],
            mode=mode,
        )

    violation_yes = sum(1 for v in votes if v.is_violation)
    is_violation = violation_yes >= (len(votes) + 1) // 2

    principle = Counter(v.principle_6s for v in votes).most_common(1)[0][0]
    priority = Counter(v.priority for v in votes).most_common(1)[0][0]
    confidence = sum(v.confidence for v in votes) / len(votes)

    agreeing = [v for v in votes if v.is_violation == is_violation]
    dissenting = [v for v in votes if v.is_violation != is_violation]

    karar = "ihlal var" if is_violation else "ihlal yok"
    synthesis = (
        f"Öneri: {karar}. "
        f"{len(votes)} modelden {violation_yes} tanesi ihlal dedi. "
        f"İlke {_PRINCIPLE_TR[principle]}, öncelik {_PRIORITY_TR[priority]}. "
    )
    if agreeing and agreeing[0].rationale:
        synthesis += f"Gerekçe: {agreeing[0].rationale} "
    synthesis += "Son karar İSG uzmanındadır."

    dissent = ""
    if dissenting:
        parts = []
        for vote in dissenting:
            side = "ihlal yok" if not vote.is_violation else "ihlal var"
            why = vote.rationale or side
            parts.append(f"{vote.model_name} ({side}): {why}")
        dissent = "Muhalif görüş — " + " | ".join(parts)

    return CouncilVerdict(
        is_violation=is_violation,
        principle_6s=principle,
        priority=priority,
        confidence=round(confidence, 3),
        synthesis=synthesis,
        dissent=dissent,
        votes=votes,
        mode=mode,
        human_final=True,
    )
