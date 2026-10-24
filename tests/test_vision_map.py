from app.schemas import IncidentStatus
from app.vision.detector import Detection, FakeDetector
from app.vision.map_to_incident import detection_to_incident


def test_kke_detection_maps_to_incident_draft():
    detection = FakeDetector().detect()[0]
    draft = detection_to_incident(detection)
    assert draft.category.value == "kke"
    assert draft.principle_6s.value == "safety"
    assert draft.priority.value == "high"
    assert draft.title == "Baretsiz çalışan"
    assert draft.camera_id == "cam-1"
    assert draft.bbox is not None
    assert draft.status == IncidentStatus.open
    assert not hasattr(draft, "id") or getattr(draft, "id", None) in (None,)


def test_low_confidence_maps_to_review_without_store():
    draft = detection_to_incident(
        Detection(label="zemin", title="Islak zemin", confidence=0.42, camera_id="cam-1")
    )
    assert draft.status == IncidentStatus.review
    assert draft.category.value == "temizlik"
