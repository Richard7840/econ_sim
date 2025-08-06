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
            # Research
            if nation.current_research:
                tech = nation.current_research
                effective_rp = nation.get_effective_research_points()
                tech.rp_progress += effective_rp
                if tech.rp_progress >= tech.rp_cost:
                    tech.is_researched = True
                    nation.technologies.append(tech)
                    nation.current_research = None
                    if not self.test_mode:
                        print(f"Technology researched: {tech.name}")
                    for industry_name in tech.unlocks_industries:
                        for industry in game_state.all_industries:
                            if industry.name == industry_name:
                                new_industry = Industry(industry.name, industry.tier, industry.profitability, government_ic=0.0, private_ic=0.0, level_bonuses=industry.level_bonuses)
                                nation.industries.append(new_industry)
                                if not self.test_mode:
                                    print(f"New industry unlocked: {new_industry.name}")

            # Economy
            total_treasury_gain = 0
            private_reinvestment_pool = 0
            for industry in nation.industries:
                government_profit = industry.government_ic * industry.base_profitability
                private_profit = industry.private_ic * industry.profitability # Use effective profitability for private IC

                total_treasury_gain += government_profit * 0.8 # 80% of government profit to treasury
                total_treasury_gain += private_profit * industry.tax_rate # Tax rate of private profit to treasury
                private_reinvestment_pool += private_profit * (1 - industry.tax_rate) # Remaining private profit to reinvestment pool

            # Private Reinvestment (Softmax-like distribution)
            if private_reinvestment_pool > 0:
                profitable_industries = [ind for ind in nation.industries if ind.profitability > 0]
                if profitable_industries:
                    total_profitability = sum(ind.profitability for ind in profitable_industries)
                    
                    total_private_ic_cost_reduction = 0.0
                    for tech in nation.technologies:
                        if tech.is_researched:
                            total_private_ic_cost_reduction += tech.private_ic_cost_reduction
                    
                    effective_ic_cost_per_unit = 10.0 * (1 - total_private_ic_cost_reduction)

                    for industry in profitable_industries:
                        share = industry.profitability / total_profitability
                        investment_amount = private_reinvestment_pool * share
                        
                        # Apply industry-specific IC cost reduction
                        industry_ic_cost_multiplier = (1 - industry.get_ic_reinvestment_cost_reduction())
                        final_ic_cost_per_unit = effective_ic_cost_per_unit * industry_ic_cost_multiplier

                        # Convert investment amount to IC (1 IC costs effective_ic_cost_per_unit treasury)
                        ic_to_add = investment_amount / final_ic_cost_per_unit
                        industry.private_ic += ic_to_add

            nation.treasury += total_treasury_gain

            self._update_civilian_economies(game_state)
            self._update_construction(game_state)
            self._check_for_events(game_state)

            game_state.turn += 1

        elif command.type == "research":
            self.set_research(nation, command.payload, game_state)
        elif command.type == "policy":
            self.set_policy(nation, command.payload)
        elif command.type == "set_tax":
            self.set_tax_rate(nation, command.payload)
        elif command.type == "budget":
            self.set_budget(nation, command.payload["category"], command.payload["amount"])
        elif command.type == "construction":
            if command.payload['type'] == "start_project":
                self.start_project(nation, command.payload['project_id'], command.payload.get('target'))
            elif command.payload['type'] == "cancel_project":
                self.cancel_project(nation, command.payload['queue_index'])
            elif command.payload['type'] == "set_ic_focus":
                self.set_ic_focus(nation, command.payload['policy'])

    def set_research(self, nation, tech_name, game_state):
        """
        Sets the current research for a nation.

        Args:
            nation (Nation): The nation to set the research for.
            tech_name (str): The name of the technology to research.
            game_state (GameState): The current state of the game.
        """
        if not self.test_mode:
            print(f"Available technologies: {[tech.name for tech in game_state.available_technologies]}")
        for tech in game_state.available_technologies:
            if tech.name == tech_name and not tech.is_researched:
                nation.current_research = tech
                if not self.test_mode:
                    print(f"Researching {tech.name}...")
                return
        if not self.test_mode:
            if not self.test_mode:
                print("Invalid technology or already researched.")

    def set_policy(self, nation, policy_data):
        """
        Sets a policy for a nation.

        Args:
            nation (Nation): The nation to set the policy for.
            policy_data (dict): The policy data.
        """
        # This logic was previously in Game.run()
        industry_name = policy_data["industry"]
        policy_type = policy_data["type"]
        amount = policy_data["amount"]

        industry = next((i for i in nation.industries if i.name == industry_name), None)
        if not industry:
            if not self.test_mode:
                print("Industry not found.")
            return

        if policy_type == "tax break":
            if 0 <= amount <= 0.20:
                industry.tax_rate = amount
                if not self.test_mode:
                    if not self.test_mode:
                        print(f"Tax rate for {industry.name} set to {amount*100:.0f}%.")
            else:
                if not self.test_mode:
                    print("Invalid tax rate. Must be between 0 and 0.20.")
        elif policy_type == "subsidy":
            if amount >= 0 and nation.treasury >= amount:
                nation.treasury -= amount
                if industry.private_ic > 0:
                    industry.subsidy_per_ic = amount / industry.private_ic
                    if not self.test_mode:
                        print(f"Subsidy of {amount} applied to {industry.name}. Subsidy per IC: {industry.subsidy_per_ic:.2f}.")
                else:
                    print("Industry has no private IC to apply subsidy to.")
            else:
                print("Invalid subsidy amount or not enough treasury.")
        else:
            print("Invalid policy type.")

    def _update_civilian_economies(self, game_state):
        """
        Updates the civilian economies of all nations.

        Args:
            game_state (GameState): The current state of the game.
        """
        for nation in [game_state.player_nation]: # Only player nation for now
            # Deduct budget spending
            nation.treasury -= nation.budget["social_spending"]

            # Calculate GDP growth rate
            final_growth_rate = nation.get_gdp_growth_rate()

            # Update GDP
            nation.civilian_gdp *= (1 + final_growth_rate)

            # Calculate and Add Income (Tax Revenue)
            tax_revenue = nation.civilian_gdp * nation.tax_rate
            nation.treasury += tax_revenue

            # Gradually move current public opinion towards target
            opinion_difference = nation.target_public_opinion - nation.public_opinion
            nation.public_opinion += opinion_difference * 0.20 # Move 20% of the difference per turn
            nation.public_opinion = max(0, min(100, nation.public_opinion)) # Clamp between 0 and 100

    def _update_construction(self, game_state):
        """
        Updates the construction projects of all nations.

        Args:
            game_state (GameState): The current state of the game.
        """
        for nation in [game_state.player_nation]: # TODO: Update for AI nations
            # First, manage the queue
            while len(nation.active_projects) < nation.construction_slots and nation.project_queue:
                nation.active_projects.append(nation.project_queue.pop(0))

            if nation.treasury < 0:
                print(f"{nation.name}'s treasury is in deficit. Construction is paused.")
                continue

            total_ic = sum(industry.ic for industry in nation.industries)
            ic_focus_modifier = 0.5 # Balanced
            if nation.ic_focus_policy == "Infrastructure_Focus":
                ic_focus_modifier = 0.8
            
            cp_from_ic = total_ic * ic_focus_modifier * 0.1 # CP_PER_IC_POINT

            tech_bonus = 0
            # TODO: Implement technology bonus for CP

            total_cp_generated = 5 + cp_from_ic + tech_bonus # BASE_CP

            cp_per_project = total_cp_generated

            for project in reversed(nation.active_projects):
                project_def = next((p for p in game_state.available_projects if p['id'] == project.project_id), None)
                if not project_def:
                    continue

                nation.treasury -= project_def['upkeep_cost']
                project.current_cp += cp_per_project

                if project.current_cp >= project_def['cp_cost']:
                    print(f"Construction of {project_def['name']} completed for {nation.name}.")
                    # Apply effects
                    for effect, value in project_def['effects'].items():
                        if effect == "add_ic":
                            if project.target:
                                target_industry = next((i for i in nation.industries if i.name == project.target), None)
                                if target_industry:
                                    target_industry.government_ic += value
                        elif effect == "add_infrastructure":
                            nation.infrastructure_level += value
                    nation.active_projects.remove(project)

    def _check_for_events(self, game_state):
        """
        Checks for and triggers events.

        Args:
            game_state (GameState): The current state of the game.
        """
        for event in game_state.available_events:
            if game_state.crisis_awareness >= event.trigger_threshold:
                print(f"EVENT: {event.name}")
                print(event.description)
                for effect, value in event.effects.items():
                    current_value = getattr(game_state.player_nation, effect)
                    setattr(game_state.player_nation, effect, current_value + value)
                game_state.available_events.remove(event)

    def set_tax_rate(self, nation, rate):
        """
        Sets the tax rate for a nation.

        Args:
            nation (Nation): The nation to set the tax rate for.
            rate (float): The new tax rate.
        """
        nation.tax_rate = rate
        nation._calculate_target_public_opinion()

    def set_budget(self, nation, category, amount):
        """
        Sets the budget for a nation.

        Args:
            nation (Nation): The nation to set the budget for.
            category (str): The budget category to set.
            amount (float): The new budget amount.
        """
        if category in nation.budget:
            nation.budget[category] = amount
            nation._calculate_target_public_opinion()
        else:
            print(f"Invalid budget category: {category}")

    def start_project(self, nation, project_id, target=None):
        """
        Starts a construction project for a nation.

        Args:
            nation (Nation): The nation to start the project for.
            project_id (str): The ID of the project to start.
            target (str, optional): The target of the project. Defaults to None.
        """
        if len(nation.active_projects) < nation.construction_slots:
            nation.active_projects.append(ProjectInstance(project_id, target))
        else:
            nation.project_queue.append(ProjectInstance(project_id, target))

    def cancel_project(self, nation, queue_index):
        """
        Cancels a construction project for a nation.

        Args:
            nation (Nation): The nation to cancel the project for.
            queue_index (int): The index of the project in the queue.
        """
        if 0 <= queue_index < len(nation.active_projects):
            project = nation.active_projects.pop(queue_index)
            # Partial refund logic can be added here
        elif 0 <= queue_index - len(nation.active_projects) < len(nation.project_queue):
            nation.project_queue.pop(queue_index - len(nation.active_projects))

    def set_ic_focus(self, nation, policy):
        """
        Sets the industrial capacity focus for a nation.

        Args:
            nation (Nation): The nation to set the IC focus for.
            policy (str): The new IC focus policy.
        """
        nation.ic_focus_policy = policy
