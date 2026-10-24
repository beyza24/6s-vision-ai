from app.rules.parser import parse_natural_language_rule


def test_parse_baret_rule_is_pending_draft():
    draft = parse_natural_language_rule("Hat 2'de baret zorunlu")
    assert draft.status == "pending_approval"
    assert draft.priority.value == "high"
    assert draft.principle_6s.value == "safety"
    assert "hat 2" in draft.zone.lower()
    assert "baret" in draft.condition.lower()
    assert draft.id
    assert draft.raw_text.startswith("Hat 2")


def test_parse_cleaning_rule():
    draft = parse_natural_language_rule("Depoda zemin temiz kalsın")
    assert draft.principle_6s.value == "seiso"
    assert draft.zone.lower() == "depo"
    assert draft.status == "pending_approval"
