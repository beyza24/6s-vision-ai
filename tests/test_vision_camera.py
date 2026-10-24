from pathlib import Path

from app.vision.camera import CameraSource, demo_sources


def test_demo_has_at_least_one_source():
    sources = demo_sources()
    assert len(sources) >= 1
    frame = sources[0].read_frame()
    assert sources[0].camera_id == "cam-1"
    assert frame.startswith(b"placeholder:")


def test_static_file_source(tmp_path: Path):
    image = tmp_path / "frame.bin"
    image.write_bytes(b"frame-bytes")
    source = CameraSource(camera_id="cam-2", url=str(image))
    assert source.read_frame() == b"frame-bytes"
