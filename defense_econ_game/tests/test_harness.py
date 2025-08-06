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
        else:
            raise ValueError(f"Unknown command type: {command_type}")
        
        self.game.process_command(command)

    def assert_game_state(self, attribute, expected_value):
        """Assert a specific attribute of the game state."""
        self.assertEqual(getattr(self.game.game_state.player_nation, attribute), expected_value)

    def _simulate_treasury_change_for_turn(self, current_nation_state, current_game_state):
        """Simulates the treasury change for a turn to use in tests."""
        projected_change = current_nation_state.calculate_projected_treasury_change(
            current_game_state.available_projects
        )
        return current_nation_state.treasury + projected_change