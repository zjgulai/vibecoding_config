"""Local render model; no browser or UI runtime is involved."""

IMPLEMENTATION_MODE = "baseline"


def render_risk_note(actor_role: str, content: str) -> dict:
    editable = actor_role == "admin"
    return {
        "content": content,
        "editable": editable,
        "controls": ["edit"] if editable else [],
    }
