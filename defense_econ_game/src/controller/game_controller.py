class GameController:
    def get_player_action(self):
        prompt = "Actions: (E)nd turn, I(n)vest industry, (R)esearch, (P)olicy, (Q)uit\n> "
        action_map = {
            'e': 'end turn',
            'n': 'invest industry',
            'r': 'research',
            'p': 'policy',
            'q': 'quit'
        }
        user_input = input(prompt).lower()
        return action_map.get(user_input, user_input)
