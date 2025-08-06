from tests.test_harness import TestHarness
from src.commands import Command
import copy

class TestConstruction(TestHarness):
    def test_project_starts_in_active_slot(self):
        """Test that a project starts in an active slot if one is available."""
        self.run_command("start_project", "build_ic_1", "Ore Mining")
        self.assertEqual(len(self.game.game_state.player_nation.active_projects), 1)
        self.assertEqual(len(self.game.game_state.player_nation.project_queue), 0)

    def test_project_goes_to_queue_when_slots_are_full(self):
        """Test that a project goes to the queue when all construction slots are full."""
        for _ in range(self.game.game_state.player_nation.construction_slots):
            self.run_command("start_project", "build_ic_1", "Ore Mining")
        
        self.run_command("start_project", "build_infrastructure_1")
        self.assertEqual(len(self.game.game_state.player_nation.active_projects), self.game.game_state.player_nation.construction_slots)
        self.assertEqual(len(self.game.game_state.player_nation.project_queue), 1)

    def test_project_completion_adds_ic(self):
        """Test that an IC project completion increases the target industry's government_ic."""
        initial_ic = next(ind.government_ic for ind in self.game.game_state.player_nation.industries if ind.name == "Ore Mining")
        self.run_command("start_project", "build_ic_1", "Ore Mining")
        
        project_def = next(p for p in self.game.game_state.available_projects if p['id'] == "build_ic_1")
        turns_to_complete = int(project_def['cp_cost'] / (5 + sum(ind.ic for ind in self.game.game_state.player_nation.industries) * 0.5 * 0.1)) + 1 # Estimate turns
        
        for _ in range(turns_to_complete):
            self.run_command("end_turn")
        
        final_ic = next(ind.government_ic for ind in self.game.game_state.player_nation.industries if ind.name == "Ore Mining")
        self.assertGreater(final_ic, initial_ic)

    def test_project_completion_adds_infrastructure(self):
        """Test that an infrastructure project completion increases the nation's infrastructure_level."""
        initial_infrastructure = self.game.game_state.player_nation.infrastructure_level
        self.run_command("start_project", "build_infrastructure_1")

        project_def = next(p for p in self.game.game_state.available_projects if p['id'] == "build_infrastructure_1")
        turns_to_complete = int(project_def['cp_cost'] / (5 + sum(ind.ic for ind in self.game.game_state.player_nation.industries) * 0.5 * 0.1)) + 1 # Estimate turns

        for _ in range(turns_to_complete):
            self.run_command("end_turn")
        
        self.assertGreater(self.game.game_state.player_nation.infrastructure_level, initial_infrastructure)

    def test_cancel_active_project(self):
        """Test that an active project can be cancelled."""
        self.run_command("start_project", "build_ic_1", "Ore Mining")
        self.assertEqual(len(self.game.game_state.player_nation.active_projects), 1)
        
        self.game.process_command(Command("construction", {"type": "cancel_project", "queue_index": 0}))
        self.assertEqual(len(self.game.game_state.player_nation.active_projects), 0)

    def test_cancel_queued_project(self):
        """Test that a queued project can be cancelled."""
        for _ in range(self.game.game_state.player_nation.construction_slots):
            self.run_command("start_project", "build_ic_1", "Ore Mining")
        self.run_command("start_project", "build_infrastructure_1") # This goes to queue
        self.assertEqual(len(self.game.game_state.player_nation.project_queue), 1)

        # The queued project is at index `construction_slots` (0-indexed) in the combined list
        cancel_index = self.game.game_state.player_nation.construction_slots 
        self.game.process_command(Command("construction", {"type": "cancel_project", "queue_index": cancel_index}))
        self.assertEqual(len(self.game.game_state.player_nation.project_queue), 0)

    def test_treasury_deduction_for_upkeep(self):
        """Test that treasury is deducted for active project upkeep."""
        self.run_command("start_project", "build_ic_1", "Ore Mining")
        
        # Simulate the treasury change for one turn *after* running the command
        expected_treasury = self._simulate_treasury_change_for_turn(self.game.game_state.player_nation, self.game.game_state)
        self.run_command("end_turn")
        self.assertAlmostEqual(self.game.game_state.player_nation.treasury, expected_treasury, places=2)
