import json
from src.models.game_state import GameState
from src.models.nation import Nation
from src.models.technology import Technology
from src.models.event import Event
from src.models.industry import Industry
from src.view.cli_view import CLIView
from src.controller.game_controller import GameController

# Constants
BASE_CP = 5
CP_PER_IC_POINT = 0.1

class Game:
    def __init__(self, test_mode=False):
        print("Game initialized.")
        self.game_state = GameState()
        self.game_state.player_nation = Nation("Player")
        self.view = CLIView()
        self.controller = GameController()
        self.load_technologies()
        self.load_events()
        self.load_industries()
        self.load_projects()

    def load_technologies(self):
        with open("c:/Users/rilew/Desktop/Side Projects/game/econ_sim/defense_econ_game/data/technologies.json") as f:
            technologies_data = json.load(f)
            for tech_data in technologies_data:
                self.game_state.available_technologies.append(Technology(tech_data['name'], tech_data['rp_cost'], tech_data.get('unlocks_industries'), tech_data.get('private_ic_cost_reduction', 0.0), tech_data.get('effects')))

    def load_events(self):
        with open("c:/Users/rilew/Desktop/Side Projects/game/econ_sim/defense_econ_game/data/events.json") as f:
            events_data = json.load(f)
            for event_data in events_data:
                self.game_state.available_events.append(Event(event_data['name'], event_data['description'], event_data['trigger_threshold'], event_data['effects']))

    def load_industries(self):
        
        with open("c:/Users/rilew/Desktop/Side Projects/game/econ_sim/defense_econ_game/data/industries.json") as f:
            industries_data = json.load(f)
            for industry_data in industries_data:
                initial_ic = industry_data.get('ic', 10)
                government_ic = float(initial_ic // 2)
                private_ic = float(initial_ic - government_ic)
                industry = Industry(industry_data['name'], industry_data['tier'], industry_data.get('profitability', 1.0), government_ic=government_ic, private_ic=private_ic, level_bonuses=industry_data.get('level_bonuses'))
                self.game_state.all_industries.append(industry)
                if industry.tier == 1:
                    self.game_state.player_nation.industries.append(industry)

    def load_projects(self):
        with open("c:/Users/rilew/Desktop/Side Projects/game/econ_sim/defense_econ_game/data/projects.json") as f:
            self.game_state.available_projects = json.load(f)

    def process_command(self, command):
        self.controller.execute_command(self.game_state, command)