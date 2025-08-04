class Nation:
    def __init__(self, name):
        self.name = name
        self.treasury = 1000
        self.research_points = 50
        self.public_opinion = 75
        self.industries = []
        self.technologies = []
        self.current_research = None
        self.policies = {}

    @property
    def industrial_capacity(self):
        return sum(industry.ic for industry in self.industries)

    def get_effective_research_points(self):
        bonus = 0
        if self.current_research:
            for industry in self.industries:
                for level_bonus in industry.level_bonuses:
                    if level_bonus['level'] <= industry.level and 'research_bonus' in level_bonus:
                        research_bonus_info = level_bonus['research_bonus']
                        if research_bonus_info['technology_name'] == self.current_research.name:
                            bonus += research_bonus_info['bonus_per_level'] * industry.level
        return self.research_points * (1 + bonus)