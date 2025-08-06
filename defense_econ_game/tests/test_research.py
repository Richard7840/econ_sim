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
        # Assuming 50 RP/turn, 100 cost, so 2 turns. Add one more for safety.
        for _ in range(3):
            self.run_command("end_turn")
        self.assertTrue(self.game.game_state.player_nation.current_research is None or self.game.game_state.player_nation.current_research.is_researched)

    def test_unlocked_industry_appears(self):
        initial_industry_count = len(self.game.game_state.player_nation.industries)
        # Using "Advanced Manufacturing" which unlocks new industries
        self.game.process_command(Command("research", "Advanced Manufacturing"))
        for _ in range(5): # Simulate turns for research completion (rp_cost 200, 50 rp/turn = 4 turns)
            self.run_command("end_turn")
        self.assertGreater(len(self.game.game_state.player_nation.industries), initial_industry_count)
        # Assert that one of the specific new industries is present
        self.assertTrue(any(ind.name == "Advanced Machinery" for ind in self.game.game_state.player_nation.industries))