"""Konsey oturumu: üyeler oy verir → başkan sentezler."""
from __future__ import annotations

from app.council.chairman import synthesize
from app.council.fake import collect_fake_votes
from app.schemas import CouncilVerdict, Incident


def run_council(incident: Incident, *, prefer_live: bool = True) -> CouncilVerdict:
    mode = "fake"
    votes = []
    if prefer_live:
        try:
            from app.council.live import collect_live_votes, live_available

            if live_available():
                votes = collect_live_votes(incident)
                if len(votes) >= 2:
                    mode = "live"
                else:
                    votes = []
        except Exception:
            votes = []
            mode = "fake"

    if not votes:
        votes = collect_fake_votes(incident)
        mode = "fake"

    return synthesize(votes, mode=mode)
