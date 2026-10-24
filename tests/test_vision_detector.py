from app.vision.detector import FakeDetector


def test_fake_detector_returns_kke_and_floor():
    found = FakeDetector().detect()
    labels = [item.label for item in found]
    assert labels == ["kke", "zemin"]
    assert found[0].title == "Baretsiz çalışan"
    assert found[0].confidence >= 0.9
    assert found[1].bbox is not None


def test_detect_accepts_frame_or_path():
    detector = FakeDetector()
    from_frame = detector.detect(frame=b"jpeg-bytes")
    from_path = detector.detect(path="frames/hat-2.jpg")
    assert [item.label for item in from_frame] == ["kke", "zemin"]
    assert [item.label for item in from_path] == ["kke", "zemin"]
