from tests.test_harness import TestHarness
from src.commands import Command

class TestPolicy(TestHarness):
    def test_tax_break_policy_effect(self):
        # Assuming "Food Production" is an industry
        industry_name = "Food Production"
        initial_tax_rate = next(ind.tax_rate for ind in self.game.game_state.player_nation.industries if ind.name == industry_name)
        
        self.game.process_command(Command("policy", {"industry": industry_name, "type": "tax break", "amount": 0.10}))
        
        new_tax_rate = next(ind.tax_rate for ind in self.game.game_state.player_nation.industries if ind.name == industry_name)
        self.assertEqual(new_tax_rate, 0.10)

    def test_subsidy_policy_effect(self):
        industry_name = "Ore Mining"
        initial_treasury = self.game.game_state.player_nation.treasury
        
        self.game.process_command(Command("policy", {"industry": industry_name, "type": "subsidy", "amount": 50}))
        
        self.assertLess(self.game.game_state.player_nation.treasury, initial_treasury)
        # More specific assertion would check subsidy_per_ic if private_ic > 0

    def test_ic_focus_policy_change(self):
        self.game.process_command(Command("construction", {"type": "set_ic_focus", "policy": "Infrastructure_Focus"}))
        self.assertEqual(self.game.game_state.player_nation.ic_focus_policy, "Infrastructure_Focus")
