import unittest

from risk_note import RiskNoteService
from risk_note_api import member_risk_note
from risk_note_migration import RiskNoteMigration
from risk_note_render import render_risk_note


class RiskNoteFixtureTests(unittest.TestCase):
    def test_member_cannot_update_a_risk_note(self) -> None:
        service = RiskNoteService()
        with self.assertRaises(PermissionError):
            service.update("member", "risk-1", "unsafe change")

    def test_member_api_is_explicitly_read_only(self) -> None:
        service = RiskNoteService()
        self.assertEqual(
            member_risk_note(service, "risk-1"),
            {
                "note_id": "risk-1",
                "content": "Review dependency changes before release.",
                "editable": False,
                "actions": [],
            },
        )

    def test_migration_can_apply_and_restore_without_external_state(self) -> None:
        migration = RiskNoteMigration()
        self.assertEqual(migration.apply(), {"status": "applied"})
        self.assertTrue(migration.applied)
        self.assertEqual(migration.restore(), {"status": "restored"})
        self.assertFalse(migration.applied)

    def test_render_exposes_editing_only_to_admins(self) -> None:
        self.assertTrue(render_risk_note("admin", "note")["editable"])
        self.assertFalse(render_risk_note("member", "note")["editable"])


if __name__ == "__main__":
    unittest.main()
