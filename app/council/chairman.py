"""Başkan: bağımsız oyları tek CouncilVerdict'e indirger."""
from __future__ import annotations

from collections import Counter

from app.schemas import CouncilMemberVote, CouncilVerdict, Priority, Principle6S


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

    synthesis_parts = [
        f"Konsey {len(votes)} model ile değerlendirdi; "
        f"{'ihlal' if is_violation else 'ihlal yok'} yönünde {violation_yes}/{len(votes)} oy.",
        f"Çoğunluk ilkesi: {principle.value}, öncelik: {priority.value}.",
    ]
    if agreeing:
        synthesis_parts.append("Gerekçe özeti: " + agreeing[0].rationale)

    dissent = ""
    if dissenting:
        dissent = "; ".join(
            f"{v.model_name}: {v.rationale or ('ihlal yok' if not v.is_violation else 'ihlal var')}"
            for v in dissenting
        )

    return CouncilVerdict(
        is_violation=is_violation,
        principle_6s=principle,
        priority=priority,
        confidence=round(confidence, 3),
        synthesis=" ".join(synthesis_parts),
        dissent=dissent,
        votes=votes,
        mode=mode,
        human_final=True,
    )
