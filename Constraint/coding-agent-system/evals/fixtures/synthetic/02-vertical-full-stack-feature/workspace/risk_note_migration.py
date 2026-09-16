"""In-memory migration stub; it neither connects to nor modifies a database."""

IMPLEMENTATION_MODE = "baseline"


class RiskNoteMigration:
    def __init__(self) -> None:
        self.applied = False

    def apply(self) -> dict:
        self.applied = True
        return {"status": "applied"}

    def restore(self) -> dict:
        self.applied = False
        return {"status": "restored"}
