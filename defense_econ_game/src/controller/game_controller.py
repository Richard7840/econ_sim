from src.models.project_instance import ProjectInstance
from src.commands import Command
from src.models.industry import Industry

class GameController:
    """
    Handles the game logic and player commands.

    Attributes:
        test_mode (bool): Whether the game is in test mode.
    """
    def __init__(self, test_mode=False):
        """
        Initializes the GameController.

        Args:
            test_mode (bool, optional): Whether the game is in test mode. Defaults to False.
        """
        self.test_mode = test_mode

    def _print(self, *args, **kwargs):
        """
        Prints messages if not in test mode.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.test_mode:
            print(*args, **kwargs)

    def execute_command(self, game_state, command):
        """
        Executes a command.

        Args:
            game_state (GameState): The current state of the game.
            command (Command): The command to execute.
        """
        nation = game_state.player_nation
        if command.type == "end_turn":
            self._process_end_turn(game_state)
        elif command.type == "research":
            self.set_research(nation, command.payload, game_state)
        elif command.type == "policy":
            self.set_policy(nation, command.payload)
        elif command.type == "set_tax":
            self.set_tax_rate(nation, command.payload)
        elif command.type == "budget":
            self.set_budget(nation, command.payload["category"], command.payload["amount"])
        elif command.type == "construction":
            payload = command.payload
            if payload['type'] == "start_project":
                self.start_project(nation, payload['project_id'], payload.get('target'))
            elif payload['type'] == "cancel_project":
                self.cancel_project(nation, payload['queue_index'])
            elif payload['type'] == "set_ic_focus":
                self.set_ic_focus(nation, payload['policy'])

    def _process_end_turn(self, game_state):
        """Processes all end-of-turn game logic in a specific order."""
        self._update_research(game_state)
        self._update_construction(game_state)
        self._update_civilian_economies(game_state)
        self._update_economy(game_state)
        self._check_for_events(game_state)
        game_state.turn += 1

    def _update_research(self, game_state):
        """Handles the research progress and completion."""
        nation = game_state.player_nation
        if nation.current_research:
            tech = nation.current_research
            effective_rp = nation.get_effective_research_points()
            tech.rp_progress += effective_rp
            if tech.rp_progress >= tech.rp_cost:
                tech.is_researched = True
                nation.technologies.append(tech)
                nation.current_research = None
                self._print(f"Technology researched: {tech.name}")
                for industry_name in tech.unlocks_industries:
                    for industry in game_state.all_industries:
                        if industry.name == industry_name:
                            new_industry = Industry(industry.name, industry.tier, industry.profitability, government_ic=0.0, private_ic=0.0, level_bonuses=industry.level_bonuses)
                            nation.industries.append(new_industry)
                            self._print(f"New industry unlocked: {new_industry.name}")

    def _update_construction(self, game_state):
        """Handles construction queue, project progress, and completion."""
        nation = game_state.player_nation
        while len(nation.active_projects) < nation.construction_slots and nation.project_queue:
            nation.active_projects.append(nation.project_queue.pop(0))

        if nation.treasury < 0:
            self._print(f"{nation.name}'s treasury is in deficit. Construction is paused.")
            return

        total_cp_generated = nation.calculate_construction_points()
        cp_per_project = total_cp_generated

        for project in reversed(nation.active_projects):
            project_def = next((p for p in game_state.available_projects if p['id'] == project.project_id), None)
            if not project_def:
                continue

            project.current_cp += cp_per_project
            if project.current_cp >= project_def['cp_cost']:
                self._print(f"Construction of {project_def['name']} completed for {nation.name}.")
                for effect, value in project_def['effects'].items():
                    if effect == "add_ic" and project.target:
                        target_industry = next((i for i in nation.industries if i.name == project.target), None)
                        if target_industry:
                            target_industry.government_ic += value
                    elif effect == "add_infrastructure":
                        nation.infrastructure_level += value
                nation.active_projects.remove(project)

    def _update_civilian_economies(self, game_state):
        """Handles GDP growth and public opinion changes."""
        nation = game_state.player_nation
        
        # Update GDP
        final_growth_rate = nation.get_gdp_growth_rate()
        nation.civilian_gdp *= (1 + final_growth_rate)

        # Update Public Opinion
        opinion_difference = nation.target_public_opinion - nation.public_opinion
        nation.public_opinion += opinion_difference * 0.20
        nation.public_opinion = max(0, min(100, nation.public_opinion))

    def _update_economy(self, game_state):
        """Handles all treasury changes and private sector reinvestment."""
        nation = game_state.player_nation
        
        # Calculate income
        industrial_profit = 0
        private_reinvestment_pool = 0
        for industry in nation.industries:
            government_profit = industry.government_ic * industry.base_profitability
            private_profit = industry.private_ic * industry.profitability
            industrial_profit += government_profit * 0.8
            industrial_profit += private_profit * industry.tax_rate
            private_reinvestment_pool += private_profit * (1 - industry.tax_rate)

        tax_revenue = nation.civilian_gdp * nation.tax_rate
        total_income = industrial_profit + tax_revenue

        # Calculate expenses
        social_spending = nation.budget["social_spending"]
        upkeep_costs = sum(
            p_def['upkeep_cost']
            for proj in nation.active_projects
            if (p_def := next((p for p in game_state.available_projects if p['id'] == proj.project_id), None))
        )
        total_expenses = social_spending + upkeep_costs

        # Update treasury
        nation.treasury += total_income - total_expenses

        # Private Reinvestment
        if private_reinvestment_pool > 0:
            profitable_industries = [ind for ind in nation.industries if ind.profitability > 0]
            if profitable_industries:
                total_profitability = sum(ind.profitability for ind in profitable_industries)
                
                total_private_ic_cost_reduction = sum(
                    tech.private_ic_cost_reduction for tech in nation.technologies if tech.is_researched
                )
                effective_ic_cost_per_unit = 10.0 * (1 - total_private_ic_cost_reduction)

                for industry in profitable_industries:
                    share = industry.profitability / total_profitability
                    investment_amount = private_reinvestment_pool * share
                    industry_ic_cost_multiplier = (1 - industry.get_ic_reinvestment_cost_reduction())
                    final_ic_cost_per_unit = effective_ic_cost_per_unit * industry_ic_cost_multiplier
                    if final_ic_cost_per_unit > 0:
                        ic_to_add = investment_amount / final_ic_cost_per_unit
                        industry.private_ic += ic_to_add

    def _check_for_events(self, game_state):
        """Checks for and triggers events."""
        for event in game_state.available_events[:]:
            if game_state.crisis_awareness >= event.trigger_threshold:
                self._print(f"EVENT: {event.name}")
                self._print(event.description)
                for effect, value in event.effects.items():
                    current_value = getattr(game_state.player_nation, effect)
                    setattr(game_state.player_nation, effect, current_value + value)
                game_state.available_events.remove(event)

    def set_research(self, nation, tech_name, game_state):
        """Sets the current research for a nation."""
        if not self.test_mode:
            self._print(f"Available technologies: {[tech.name for tech in game_state.available_technologies]}")
        for tech in game_state.available_technologies:
            if tech.name == tech_name and not tech.is_researched:
                nation.current_research = tech
                self._print(f"Researching {tech.name}...")
                return
        self._print("Invalid technology or already researched.")

    def set_policy(self, nation, policy_data):
        """Sets a policy for a nation."""
        industry_name = policy_data["industry"]
        policy_type = policy_data["type"]
        amount = policy_data["amount"]

        industry = next((i for i in nation.industries if i.name == industry_name), None)
        if not industry:
            self._print("Industry not found.")
            return

        if policy_type == "tax break":
            if 0 <= amount <= 0.20:
                industry.tax_rate = amount
                self._print(f"Tax rate for {industry.name} set to {amount*100:.0f}%.")
            else:
                self._print("Invalid tax rate. Must be between 0 and 0.20.")
        elif policy_type == "subsidy":
            if amount >= 0 and nation.treasury >= amount:
                nation.treasury -= amount
                if industry.private_ic > 0:
                    industry.subsidy_per_ic = amount / industry.private_ic
                    self._print(f"Subsidy of {amount} applied to {industry.name}. Subsidy per IC: {industry.subsidy_per_ic:.2f}.")
                else:
                    self._print("Industry has no private IC to apply subsidy to.")
            else:
                self._print("Invalid subsidy amount or not enough treasury.")
        else:
            self._print("Invalid policy type.")

    def set_tax_rate(self, nation, rate):
        """Sets the tax rate for a nation."""
        nation.tax_rate = rate
        nation._calculate_target_public_opinion()

    def set_budget(self, nation, category, amount):
        """Sets the budget for a nation."""
        if category in nation.budget:
            nation.budget[category] = amount
            nation._calculate_target_public_opinion()
        else:
            self._print(f"Invalid budget category: {category}")

    def start_project(self, nation, project_id, target=None):
        """Starts a construction project for a nation."""
        if len(nation.active_projects) < nation.construction_slots:
            nation.active_projects.append(ProjectInstance(project_id, target))
        else:
            nation.project_queue.append(ProjectInstance(project_id, target))

    def cancel_project(self, nation, queue_index):
        """Cancels a construction project for a nation."""
        if 0 <= queue_index < len(nation.active_projects):
            nation.active_projects.pop(queue_index)
        elif 0 <= queue_index - len(nation.active_projects) < len(nation.project_queue):
            nation.project_queue.pop(queue_index - len(nation.active_projects))

    def set_ic_focus(self, nation, policy):
        """Sets the industrial capacity focus for a nation."""
        nation.ic_focus_policy = policy