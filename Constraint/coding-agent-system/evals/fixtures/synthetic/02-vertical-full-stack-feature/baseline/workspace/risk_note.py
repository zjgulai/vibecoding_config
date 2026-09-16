"""Deterministic local domain model used only by the synthetic EVAL-02 fixture."""

IMPLEMENTATION_MODE = "baseline"


class RiskNoteService:
    def __init__(self) -> None:
        self._notes = {"risk-1": "Review dependency changes before release."}

    def read(self, note_id: str) -> str:
        return self._notes[note_id]

    def update(self, actor_role: str, note_id: str, content: str) -> None:
        if actor_role != "admin":
            raise PermissionError("only an admin can update a risk note")
        self._notes[note_id] = content
