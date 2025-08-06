from src.game import Game
from src.commands import Command

def get_player_action_from_input():
    prompt = "Actions: (E)nd turn, (R)esearch, (P)olicy, (S)et Tax, (B)udget, (C)onstruction, (Q)uit\n> "
    user_input = input(prompt).lower()

    if user_input == 'e':
        return Command("end_turn")
    elif user_input == 'q':
        return Command("quit")
    elif user_input == 'r':
        # For now, hardcode a research command for testing
        return Command("research", "Advanced Construction")
    elif user_input == 'c':
        print("Construction Actions: (S)tart, (C)ancel, (F)ocus")
        construction_action = input("> ").lower()
        if construction_action == 's':
            # For now, hardcode a project start for testing
            return Command("construction", Command("start_project", "build_ic_1", "Ore Mining"))
        elif construction_action == 'c':
            # For now, hardcode a project cancel for testing
            return Command("construction", Command("cancel_project", 0))
        elif construction_action == 'f':
            # For now, hardcode a focus change for testing
            return Command("construction", {"type": "set_ic_focus", "policy": "Infrastructure_Focus"})

    return None

if __name__ == "__main__":
    game = Game()
    while True:
        game.view.display_game_state(game.game_state)
        action = get_player_action_from_input()
        if action:
            game.process_command(action)
        if action and action.type == "quit":
            break