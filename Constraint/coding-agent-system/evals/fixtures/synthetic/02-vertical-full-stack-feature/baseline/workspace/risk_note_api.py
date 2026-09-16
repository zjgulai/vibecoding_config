"""Local API-shaped projection for the synthetic risk-note model."""

from risk_note import RiskNoteService


IMPLEMENTATION_MODE = "baseline"


def member_risk_note(service: RiskNoteService, note_id: str) -> dict:
    return {
        "note_id": note_id,
        "content": service.read(note_id),
        "editable": False,
        "actions": [],
    }
