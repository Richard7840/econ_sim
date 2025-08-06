from src.models.nation import Nation

class GameState:
    def __init__(self):
        self.turn = 0
        self.player_nation = None
        self.ai_nations = []
        self.available_technologies = []
        self.crisis_awareness = 0
        self.social_dissonance = 0
        self.available_events = []
        self.all_industries = []
        self.available_projects = []
