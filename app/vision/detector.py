"""Detector arayüzü ve anahtarsız sahte tespit. Sahip: k2."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Union


@dataclass(frozen=True)
class Detection:
    label: str
    title: str
    confidence: float
    camera_id: str = "cam-1"
    bbox: tuple[float, float, float, float] | None = None


class Detector(Protocol):
    def detect(self, frame: bytes | None = None, path: str | None = None) -> list[Detection]:
        """Kare veya dosya yolundan tespit listesi döndürür."""


Source = Union[bytes, str, None]


class FakeDetector:
    """Sabit KKE ve zemin örnekleri. Gerçek modele bağlanmadan demo için yeter."""

    def detect(self, frame: bytes | None = None, path: str | None = None) -> list[Detection]:
        camera_id = "cam-1"
        return [
            Detection(
                label="kke",
                title="Baretsiz çalışan",
                confidence=0.94,
                camera_id=camera_id,
                bbox=(0.42, 0.18, 0.16, 0.22),
            ),
            Detection(
                label="zemin",
                title="Zeminde döküntü",
                confidence=0.81,
                camera_id=camera_id,
                bbox=(0.10, 0.72, 0.30, 0.12),
            ),
        ]
