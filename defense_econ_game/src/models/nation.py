from src.models.project_instance import ProjectInstance

class Nation:
    def __init__(self, name):
        self.name = name
        self.treasury = 1000
        self.research_points = 50
        self.public_opinion = 50.0 # Initialize at 50.0
        self.target_public_opinion = 50.0 # Initialize at 50.0
        self.industries = []
        self.technologies = []
        self.current_research = None
        self.policies = {}
        self.civilian_gdp = 10000.0 # Initialize with a starting value
        self.tax_rate = 0.15 # Initialize at 0.15 (15%)
        self.budget = {
            "social_spending": 0
        }
        self.construction_slots = 3
        self.active_projects: list[ProjectInstance] = []
        self.project_queue: list[ProjectInstance] = []
        self.infrastructure_level = 1
        self.ic_focus_policy = "Balanced"
        self._calculate_target_public_opinion() # Call after all attributes are initialized

    def _calculate_target_public_opinion(self):
        ideal_opinion = 50.0 # Base ideal opinion
        # Assuming population of 1000 for now for social spending impact
        ideal_opinion += (self.budget["social_spending"] / 1000) * 100 
        ideal_opinion -= (self.tax_rate - 0.15) * 100 # Tax rate impact
        self.target_public_opinion = max(0, min(100, ideal_opinion)) # Clamp ideal opinion

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

    def get_gdp_growth_rate(self):
        final_growth_rate = 0.01 # Base rate

        # Infrastructure Bonus
        final_growth_rate += (self.infrastructure_level - 1) * 0.005

        # Stability Bonus
        if self.public_opinion > 75:
            final_growth_rate += 0.01
        elif self.public_opinion < 25:
            final_growth_rate -= 0.02
        else:
            final_growth_rate += 0.005

        # Technology Bonus
        tech_bonus = 0.0
        for tech in self.technologies:
            if tech.is_researched and "gdp_growth_modifier" in tech.effects:
                tech_bonus += tech.effects["gdp_growth_modifier"]
        final_growth_rate += tech_bonus

        return final_growth_rate
