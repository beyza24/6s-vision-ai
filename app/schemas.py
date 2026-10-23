"""Shared schemas — only k1 (@beyza24) edits this file."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Category(str, Enum):
    kke = "kke"
    duzen = "duzen"
    temizlik = "temizlik"
    trafik = "trafik"
    ekipman = "ekipman"
    diger = "diger"


class Principle6S(str, Enum):
    seiri = "seiri"
    seiton = "seiton"
    seiso = "seiso"
    seiketsu = "seiketsu"
    shitsuke = "shitsuke"
    safety = "safety"


class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class IncidentStatus(str, Enum):
    open = "open"
    review = "review"
    resolved = "resolved"
    false_alarm = "false_alarm"


class BBox(BaseModel):
    x: float
    y: float
    w: float
    h: float


class Incident(BaseModel):
    id: str
    camera_id: str = "cam-1"
    timestamp: datetime
    category: Category
    principle_6s: Principle6S
    title: str
    description: str = ""
    priority: Priority = Priority.medium
    confidence: float = Field(ge=0, le=1, default=0.9)
    status: IncidentStatus = IncidentStatus.open
    bbox: Optional[BBox] = None
    ai_explanation: str = ""
    action_plan: list[str] = Field(default_factory=list)
    assignee: Optional[str] = None


class IncidentCreate(BaseModel):
    camera_id: str = "cam-1"
    category: Category
    principle_6s: Principle6S
    title: str
    description: str = ""
    priority: Priority = Priority.medium
    confidence: float = Field(ge=0, le=1, default=0.9)
    status: IncidentStatus = IncidentStatus.open
    bbox: Optional[BBox] = None
    ai_explanation: str = ""
    action_plan: list[str] = Field(default_factory=list)


class AssignBody(BaseModel):
    assignee: str
    note: str = ""


class Scores6S(BaseModel):
    seiri: float
    seiton: float
    seiso: float
    seiketsu: float
    shitsuke: float
    safety: float
    overall: float


class RuleDraft(BaseModel):
    id: str
    raw_text: str
    zone: str = ""
    condition: str = ""
    principle_6s: Principle6S = Principle6S.safety
    priority: Priority = Priority.high
    notify: str = "isg"
    status: str = "pending_approval"
