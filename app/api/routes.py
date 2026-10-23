"""API routes — k1 wires modules owned by k2/k3."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas import (
    AssignBody,
    Category,
    Incident,
    IncidentCreate,
    IncidentStatus,
    Principle6S,
    Priority,
    RuleDraft,
    Scores6S,
)
from app.store import store

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "6s-vision-ai"}


@router.get("/api/incidents", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return store.list_incidents()


@router.get("/api/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str) -> Incident:
    item = store.get_incident(incident_id)
    if not item:
        raise HTTPException(404, "incident not found")
    return item


@router.post("/api/incidents/{incident_id}/confirm", response_model=Incident)
def confirm_incident(incident_id: str) -> Incident:
    item = store.set_status(incident_id, IncidentStatus.open)
    if not item:
        raise HTTPException(404, "incident not found")
    # human confirmed: keep/open for action
    return item


@router.post("/api/incidents/{incident_id}/false-alarm", response_model=Incident)
def false_alarm(incident_id: str) -> Incident:
    item = store.set_status(incident_id, IncidentStatus.false_alarm)
    if not item:
        raise HTTPException(404, "incident not found")
    return item


@router.post("/api/incidents/{incident_id}/assign", response_model=Incident)
def assign_incident(incident_id: str, body: AssignBody) -> Incident:
    item = store.assign(incident_id, body)
    if not item:
        raise HTTPException(404, "incident not found")
    resolved = store.set_status(incident_id, IncidentStatus.resolved)
    assert resolved is not None
    return resolved


@router.get("/api/scores/6s", response_model=Scores6S)
def scores_6s() -> Scores6S:
    try:
        from app.scoring.engine import compute_scores
    except ImportError:
        return Scores6S(
            seiri=80, seiton=80, seiso=80, seiketsu=80, shitsuke=80, safety=80, overall=80
        )
    return compute_scores(store.list_incidents())


class ParseRuleBody(BaseModel):
    text: str


@router.post("/api/rules/parse", response_model=RuleDraft)
def parse_rule(body: ParseRuleBody) -> RuleDraft:
    try:
        from app.rules.parser import parse_natural_language_rule
    except ImportError as exc:
        raise HTTPException(501, "rules module not ready") from exc
    draft = parse_natural_language_rule(body.text)
    return store.add_rule(draft)


@router.post("/api/rules/{rule_id}/approve", response_model=RuleDraft)
def approve_rule(rule_id: str) -> RuleDraft:
    rule = store.approve_rule(rule_id)
    if not rule:
        raise HTTPException(404, "rule not found")
    return rule


@router.post("/api/incidents/{incident_id}/council", response_model=Incident)
def run_incident_council(incident_id: str) -> Incident:
    """Kural ihlali için LLM Council (çoklu model) önerisi üretir. Son karar insanda."""
    item = store.get_incident(incident_id)
    if not item:
        raise HTTPException(404, "incident not found")
    try:
        from app.council.deliberate import run_council
    except ImportError as exc:
        raise HTTPException(501, "council module not ready") from exc
    verdict = run_council(item)
    updated = store.set_council(incident_id, verdict)
    assert updated is not None
    return updated


@router.post("/api/demo/spawn", response_model=Incident)
def demo_spawn() -> Incident:
    """Hakem demosu: örnek baretsiz çalışan olayı + konsey turu."""
    try:
        from app.scoring.explain import build_explanation
    except ImportError:
        build_explanation = None  # type: ignore

    explanation = "YZ baret eksikliğini buldu. 6S Güvenlik ilkesine aykırı."
    plan = ["Baret temini", "Saha eğitimi planı", "Hat girişinde KKE kontrolü"]
    if build_explanation:
        explanation, plan = build_explanation(
            title="Baretsiz çalışan",
            category=Category.kke,
            principle=Principle6S.safety,
        )

    body = IncidentCreate(
        camera_id="cam-1",
        category=Category.kke,
        principle_6s=Principle6S.safety,
        title="Baretsiz çalışan",
        description="Üretim Alanı · Hat 2",
        priority=Priority.high,
        confidence=0.94,
        status=IncidentStatus.open,
        ai_explanation=explanation,
        action_plan=plan,
    )
    created = store.create_incident(body)
    try:
        from app.council.deliberate import run_council

        verdict = run_council(created, prefer_live=False)
        created = store.set_council(created.id, verdict) or created
    except Exception:
        pass
    return created
