import math

class Industry:
    def __init__(self, name, tier, profitability=1.0, government_ic=0.0, private_ic=0.0, level_bonuses=None):
        self.name = name
        self.tier = tier
        self.level = 1
        self.government_ic = government_ic
        self.private_ic = private_ic
        self.base_profitability = profitability # Store base profitability
        self.tax_rate = 0.20 # Default tax rate
        self.subsidy_per_ic = 0.0 # Default subsidy
        self.level_bonuses = level_bonuses if level_bonuses is not None else []

    @property
    def ic(self):
        return self.government_ic + self.private_ic

    @property
    def profitability(self):
        # Effective profitability for private IC
        return self.base_profitability * (1 - self.tax_rate) + self.subsidy_per_ic

    def get_ic_reinvestment_cost_reduction(self):
        # Each level decreases cost by 0.05 (5%)
        return (self.level - 1) * 0.05
