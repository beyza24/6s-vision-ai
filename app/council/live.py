"""Canlı LLM Council üyeleri — OpenAI-uyumlu chat completions.

Anahtar yoksa deliberate.py fake'e düşer.
k3 bu dosyayı gerçek sağlayıcılarla genişletebilir (Anthropic, Gemini, OpenRouter).
"""
from __future__ import annotations

import json
import os
from typing import Any

import httpx

from app.schemas import CouncilMemberVote, Incident, Priority, Principle6S


def _member_configs() -> list[dict[str, str]]:
    """Env'den 1–N üye. Örnek: COUNCIL_MEMBERS=openai:gpt-4o-mini,openrouter:anthropic/claude-3.5"""
    raw = os.getenv("COUNCIL_MEMBERS", "").strip()
    members: list[dict[str, str]] = []
    if raw:
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if ":" in part:
                provider, model = part.split(":", 1)
            else:
                provider, model = "openai", part
            members.append({"provider": provider.strip(), "model": model.strip()})
    else:
        # tek varsayılan
        model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        members.append({"provider": "openai", "model": model})
    return members


def _endpoint_for(provider: str) -> tuple[str, str]:
    if provider == "openrouter":
        return (
            os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            os.getenv("OPENROUTER_API_KEY", os.getenv("COUNCIL_API_KEY", "")),
        )
    if provider == "anthropic":
        # Anthropic native API farklı; hackathon'da OpenRouter veya uyumlu proxy beklenir
        return (
            os.getenv("ANTHROPIC_BASE_URL", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")),
            os.getenv("ANTHROPIC_API_KEY", os.getenv("COUNCIL_API_KEY", "")),
        )
    if provider == "google":
        return (
            os.getenv("GOOGLE_BASE_URL", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")),
            os.getenv("GOOGLE_API_KEY", os.getenv("COUNCIL_API_KEY", "")),
        )
    return (
        os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        os.getenv("OPENAI_API_KEY", os.getenv("COUNCIL_API_KEY", "")),
    )


def live_available() -> bool:
    for m in _member_configs():
        _, key = _endpoint_for(m["provider"])
        if key:
            return True
    return False


def _prompt(incident: Incident) -> str:
    return (
        "Sen bir fabrika 6S/İSG denetim kurulunun üyesiniz. "
        "Kimlik tanıma yapma; yalnızca ihlali değerlendir.\n"
        f"Başlık: {incident.title}\n"
        f"Açıklama: {incident.description}\n"
        f"Kategori: {incident.category.value}\n"
        f"Önerilen 6S: {incident.principle_6s.value}\n"
        f"Dedektör güveni: {incident.confidence}\n\n"
        "JSON döndür: "
        '{"is_violation":bool,"principle_6s":"seiri|seiton|seiso|seiketsu|shitsuke|safety",'
        '"priority":"high|medium|low","confidence":0-1,"rationale":"kısa Türkçe"}'
    )


def _parse_vote(member_id: str, provider: str, model: str, content: str) -> CouncilMemberVote:
    data: dict[str, Any]
    try:
        start = content.find("{")
        end = content.rfind("}")
        data = json.loads(content[start : end + 1])
    except Exception:
        data = {
            "is_violation": True,
            "principle_6s": "safety",
            "priority": "medium",
            "confidence": 0.5,
            "rationale": content[:240],
        }
    return CouncilMemberVote(
        member_id=member_id,
        model_name=model,
        provider=provider,
        is_violation=bool(data.get("is_violation", True)),
        principle_6s=Principle6S(str(data.get("principle_6s", "safety"))),
        priority=Priority(str(data.get("priority", "medium"))),
        confidence=float(data.get("confidence", 0.5)),
        rationale=str(data.get("rationale", "")),
    )


def collect_live_votes(incident: Incident) -> list[CouncilMemberVote]:
    votes: list[CouncilMemberVote] = []
    prompt = _prompt(incident)
    for idx, cfg in enumerate(_member_configs()):
        base, key = _endpoint_for(cfg["provider"])
        if not key:
            continue
        url = base.rstrip("/") + "/chat/completions"
        payload = {
            "model": cfg["model"],
            "messages": [
                {"role": "system", "content": "Yalnız geçerli JSON üret."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        with httpx.Client(timeout=45.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
        votes.append(_parse_vote(f"live-{idx}", cfg["provider"], cfg["model"], content))
    return votes
