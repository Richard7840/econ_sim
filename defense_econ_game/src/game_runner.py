class GameRunner:
    def __init__(self, game):
        self.game = game

    def run(self):
        while True:
            self.game.view.display_game_state(self.game.game_state)
            action = self.game.controller.get_player_action()
            if action:
                self.handle_action(action)

    def handle_action(self, action):
        if action.type == "end_turn":
            self.game._end_turn()
        elif action.type == "quit":
            exit()
        elif action.type == "research":
            self.game.controller.set_research(self.game.game_state.player_nation, action.payload)
        elif action.type == "policy":
            self.game.controller.set_policy(self.game.game_state.player_nation, action.payload)
        elif action.type == "set_tax":
            self.game.controller.set_tax_rate(self.game.game_state.player_nation, action.payload)
        elif action.type == "budget":
            self.game.controller.set_budget(self.game.game_state.player_nation, action.payload["category"], action.payload["amount"])
        elif action.type == "construction":
            self.handle_construction_action(action.payload)

    def handle_construction_action(self, payload):
        if payload.type == "start_project":
            self.game.controller.start_project(self.game.game_state.player_nation, payload.project_id, payload.target)
        elif payload.type == "cancel_project":
            self.game.controller.cancel_project(self.game.game_state.player_nation, payload.queue_index)
        elif payload.type == "set_ic_focus":
            self.game.controller.set_ic_focus(self.game.game_state.player_nation, payload.policy)
