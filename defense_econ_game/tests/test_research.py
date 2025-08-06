from tests.test_harness import TestHarness
from src.commands import Command

class TestResearch(TestHarness):
    def test_research_progress(self):
        # Using "Industrialization" as an available technology
        self.game.process_command(Command("research", "Industrialization"))
        initial_progress = self.game.game_state.player_nation.current_research.rp_progress
        self.run_command("end_turn")
        self.assertGreater(self.game.game_state.player_nation.current_research.rp_progress, initial_progress)

    def test_technology_completion(self):
        # Using "Industrialization" as an available technology with rp_cost 100
        self.game.process_command(Command("research", "Industrialization"))
        # Simulate enough turns to complete research (adjust based on actual RP gain)
        # Calculate turns needed dynamically
        tech = self.game.game_state.player_nation.current_research
        effective_rp = self.game.game_state.player_nation.get_effective_research_points()
        turns_needed = int((tech.rp_cost + effective_rp - 1) // effective_rp) # Ceiling division
        turns_to_run = turns_needed + 1 # Add one more for safety
        for _ in range(turns_to_run):
            self.run_command("end_turn")
        self.assertTrue(self.game.game_state.player_nation.current_research is None or self.game.game_state.player_nation.current_research.is_researched)

    def test_unlocked_industry_appears(self):
        initial_industry_count = len(self.game.game_state.player_nation.industries)
        # Using "Advanced Manufacturing" which unlocks new industries
        self.game.process_command(Command("research", "Advanced Manufacturing"))
        tech = self.game.game_state.player_nation.current_research
        effective_rp = self.game.game_state.player_nation.get_effective_research_points()
        turns_needed = int((tech.rp_cost + effective_rp - 1) // effective_rp) # Ceiling division
        turns_to_run = turns_needed + 1 # Add one more for safety
        for _ in range(turns_to_run):
            self.run_command("end_turn")
        self.assertGreater(len(self.game.game_state.player_nation.industries), initial_industry_count)
        # Assert that one of the specific new industries is present
        self.assertTrue(any(ind.name == "Advanced Machinery" for ind in self.game.game_state.player_nation.industries))