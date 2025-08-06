import unittest
from src.game import Game
from src.commands import Command
import copy

class TestHarness(unittest.TestCase):
    def setUp(self):
        """Set up a new game instance for each test."""
        self.game = Game(test_mode=True)

    def run_command(self, command_type, *args):
        """Run a command in the game."""
        if command_type == "start_project":
            project_id = args[0]
            target = args[1] if len(args) > 1 else None
            command = Command("construction", {"type": "start_project", "project_id": project_id, "target": target})
        elif command_type == "end_turn":
            command = Command("end_turn")
        elif command_type == "set_tax":
            command = Command("set_tax", args[0])
        elif command_type == "budget":
            command = Command("budget", {"category": args[0], "amount": args[1]})
        # Add other command types as needed
        else:
            raise ValueError(f"Unknown command type: {command_type}")
        
        self.game.process_command(command)

    def assert_game_state(self, attribute, expected_value):
        """Assert a specific attribute of the game state."""
        self.assertEqual(getattr(self.game.game_state.player_nation, attribute), expected_value)

    def _simulate_gdp_growth(self, nation_state):
        simulated_nation = copy.deepcopy(nation_state)
        final_growth_rate = simulated_nation.get_gdp_growth_rate()
        simulated_nation.civilian_gdp *= (1 + final_growth_rate)
        return simulated_nation.civilian_gdp

    def _simulate_treasury_change_for_turn(self, current_nation_state, current_game_state):
        simulated_nation = copy.deepcopy(current_nation_state)
        simulated_game_state = copy.deepcopy(current_game_state)

        # --- Economy (from execute_command -> end_turn block) ---
        total_treasury_gain_from_industries = 0
        for industry in simulated_nation.industries:
            government_profit = industry.government_ic * industry.base_profitability
            private_profit = industry.private_ic * industry.profitability
            total_treasury_gain_from_industries += government_profit * 0.8
            total_treasury_gain_from_industries += private_profit * industry.tax_rate
        simulated_nation.treasury += total_treasury_gain_from_industries

        # --- Civilian Economies (from _update_civilian_economies) ---
        # Deduct budget spending
        simulated_nation.treasury -= simulated_nation.budget["social_spending"]
        
        

        # Calculate GDP growth rate and update GDP
        final_growth_rate = simulated_nation.get_gdp_growth_rate()
        simulated_nation.civilian_gdp *= (1 + final_growth_rate)

        # Calculate and Add Income (Tax Revenue) based on *updated* GDP
        tax_revenue_from_gdp = simulated_nation.civilian_gdp * simulated_nation.tax_rate
        simulated_nation.treasury += tax_revenue_from_gdp

        # --- Construction (from _update_construction) ---
        for project in simulated_nation.active_projects:
            project_def = next((p for p in simulated_game_state.available_projects if p['id'] == project.project_id), None)
            if project_def:
                simulated_nation.treasury -= project_def['upkeep_cost']

        return simulated_nation.treasury
