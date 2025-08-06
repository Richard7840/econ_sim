from tests.test_harness import TestHarness
from src.commands import Command
import copy

class TestEconomy(TestHarness):
    def test_initial_treasury(self):
        self.assert_game_state("treasury", 1000)

    def test_treasury_gain_after_turn(self):
        initial_nation_state = copy.deepcopy(self.game.game_state.player_nation)
        initial_game_state = copy.deepcopy(self.game.game_state)
        expected_treasury = self._simulate_treasury_change_for_turn(initial_nation_state, initial_game_state)
        self.run_command("end_turn")
        self.assertAlmostEqual(self.game.game_state.player_nation.treasury, expected_treasury, places=2)

    def test_gdp_growth(self):
        initial_gdp = self.game.game_state.player_nation.civilian_gdp
        self.run_command("end_turn")
        self.assertGreater(self.game.game_state.player_nation.civilian_gdp, initial_gdp)

    def test_tax_rate_effect_on_treasury(self):
        self.game.process_command(Command("set_tax", 0.5))  # 50%
        initial_nation_state = copy.deepcopy(self.game.game_state.player_nation)
        initial_game_state = copy.deepcopy(self.game.game_state)
        expected_treasury = self._simulate_treasury_change_for_turn(initial_nation_state, initial_game_state)
        self.run_command("end_turn")
        self.assertAlmostEqual(self.game.game_state.player_nation.treasury, expected_treasury, places=2)

    def test_social_spending_deduction(self):
        self.game.process_command(Command("budget", {"category": "social_spending", "amount": 100}))
        initial_nation_state = copy.deepcopy(self.game.game_state.player_nation)
        initial_game_state = copy.deepcopy(self.game.game_state)
        expected_treasury = self._simulate_treasury_change_for_turn(initial_nation_state, initial_game_state)
        self.run_command("end_turn")
        self.assertAlmostEqual(self.game.game_state.player_nation.treasury, expected_treasury, places=2)
