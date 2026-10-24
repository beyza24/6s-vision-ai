"""Ham tespiti olay taslağına çevirir. Store'a yazmaz. Sahip: k2."""
from __future__ import annotations

from app.schemas import BBox, Category, IncidentCreate, IncidentStatus, Priority, Principle6S
from app.vision.detector import Detection

_TABLE: dict[str, tuple[Category, Principle6S, Priority, str]] = {
    "kke": (Category.kke, Principle6S.safety, Priority.high, "Üretim hattı"),
    "zemin": (Category.temizlik, Principle6S.seiso, Priority.medium, "Zemin"),
}


def detection_to_incident(detection: Detection) -> IncidentCreate:
    category, principle, priority, place = _TABLE.get(
        detection.label,
        (Category.diger, Principle6S.shitsuke, Priority.low, "Saha"),
    )
    bbox = None
    if detection.bbox is not None:
        x, y, w, h = detection.bbox
        bbox = BBox(x=x, y=y, w=w, h=h)
    status = IncidentStatus.review if detection.confidence < 0.6 else IncidentStatus.open
    return IncidentCreate(
        camera_id=detection.camera_id,
        category=category,
        principle_6s=principle,
        title=detection.title,
        description=place,
        priority=priority,
        confidence=detection.confidence,
        status=status,
        bbox=bbox,
    )
