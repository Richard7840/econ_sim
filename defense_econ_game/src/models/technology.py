class Technology:
    def __init__(self, name, rp_cost, unlocks_industries=None, private_ic_cost_reduction=0.0, effects=None):
        self.name = name
        self.rp_cost = rp_cost
        self.rp_progress = 0
        self.is_researched = False
        self.unlocks_industries = unlocks_industries if unlocks_industries is not None else []
        self.private_ic_cost_reduction = private_ic_cost_reduction
        self.effects = effects if effects is not None else {}
        self.private_ic_cost_reduction = private_ic_cost_reduction
