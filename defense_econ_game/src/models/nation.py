from src.models.project_instance import ProjectInstance

class Nation:
    def __init__(self, name):
        self.name = name
        self.treasury = 1000
        self.research_points = 50
        self.public_opinion = 50.0
        self.target_public_opinion = 50.0
        self.industries = []
        self.technologies = []
        self.current_research = None
        self.policies = {}
        self.civilian_gdp = 10000.0
        self.tax_rate = 0.15
        self.budget = {"social_spending": 0}
        self.construction_slots = 3
        self.active_projects: list[ProjectInstance] = []
        self.project_queue: list[ProjectInstance] = []
        self.infrastructure_level = 1
        self.ic_focus_policy = "Balanced"
        self._calculate_target_public_opinion()

    def _calculate_target_public_opinion(self):
        ideal_opinion = 50.0
        ideal_opinion += (self.budget["social_spending"] / 1000) * 100
        ideal_opinion -= (self.tax_rate - 0.15) * 100
        self.target_public_opinion = max(0, min(100, ideal_opinion))

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
        final_growth_rate = 0.01
        final_growth_rate += (self.infrastructure_level - 1) * 0.005
        if self.public_opinion > 75:
            final_growth_rate += 0.01
        elif self.public_opinion < 25:
            final_growth_rate -= 0.02
        else:
            final_growth_rate += 0.005
        tech_bonus = sum(tech.effects.get("gdp_growth_modifier", 0) for tech in self.technologies if tech.is_researched)
        final_growth_rate += tech_bonus
        return final_growth_rate

    def calculate_construction_points(self):
        total_ic = self.industrial_capacity
        ic_focus_modifier = 0.8 if self.ic_focus_policy == "Infrastructure_Focus" else 0.5
        cp_from_ic = total_ic * ic_focus_modifier * 0.1
        tech_bonus = 0  # TODO: Implement technology bonus for CP
        return 5 + cp_from_ic + tech_bonus

    def calculate_projected_treasury_change(self, available_projects):
        """Calculates the projected treasury change for the next turn."""
        # Income
        industrial_profit = sum(
            (ind.government_ic * ind.base_profitability * 0.8) + (ind.private_ic * ind.profitability * ind.tax_rate)
            for ind in self.industries
        )
        projected_gdp = self.civilian_gdp * (1 + self.get_gdp_growth_rate())
        tax_revenue = projected_gdp * self.tax_rate
        total_income = industrial_profit + tax_revenue

        # Expenses
        social_spending = self.budget["social_spending"]
        upkeep_costs = sum(
            p_def['upkeep_cost']
            for proj in self.active_projects
            if (p_def := next((p for p in available_projects if p['id'] == proj.project_id), None))
        )
        total_expenses = social_spending + upkeep_costs

        return total_income - total_expenses