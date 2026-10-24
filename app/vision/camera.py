"""Kamera kaynağı. Sahip: k2. Statik dosya veya yer tutucu adres."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CameraSource:
    camera_id: str
    url: str

    def read_frame(self) -> bytes:
        path = Path(self.url)
        if path.is_file():
            return path.read_bytes()
        return f"placeholder:{self.camera_id}:{self.url}".encode("utf-8")


def demo_sources() -> list[CameraSource]:
    """Hakem demosu için en az bir kaynak."""
    return [CameraSource(camera_id="cam-1", url="placeholder://hat-2")]
