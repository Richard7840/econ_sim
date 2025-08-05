class GameController:
    def get_player_action(self):
        prompt = "Actions: (E)nd turn, I(n)vest industry, (R)esearch, (P)olicy, (S)et Tax, (B)udget, (Q)uit\n> "
        action_map = {
            'e': 'end turn',
            'n': 'invest industry',
            'r': 'research',
            'p': 'policy',
            's': 'set tax',
            'b': 'budget',
            'q': 'quit'
        }
        user_input = input(prompt).lower()
        return action_map.get(user_input, user_input)

    def set_tax_rate(self, nation, rate):
        nation.tax_rate = rate
        nation._calculate_target_public_opinion()

    def set_budget(self, nation, category, amount):
        if category in nation.budget:
            nation.budget[category] = amount
            nation._calculate_target_public_opinion()
        else:
            print(f"Invalid budget category: {category}")