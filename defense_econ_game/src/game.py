import json
from src.models.game_state import GameState
from src.models.nation import Nation
from src.models.technology import Technology
from src.models.event import Event
from src.models.industry import Industry
from src.view.cli_view import CLIView
from src.controller.game_controller import GameController

class Game:
    def __init__(self):
        print("Game initialized.")
        self.game_state = GameState()
        self.game_state.player_nation = Nation("Player")
        self.view = CLIView()
        self.controller = GameController()
        self.load_technologies()
        self.load_events()
        self.load_industries()

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
        print("Loading industries...")
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

    def check_for_events(self):
        for event in self.game_state.available_events:
            if self.game_state.crisis_awareness >= event.trigger_threshold:
                print(f"EVENT: {event.name}")
                print(event.description)
                for effect, value in event.effects.items():
                    current_value = getattr(self.game_state.player_nation, effect)
                    setattr(self.game_state.player_nation, effect, current_value + value)
                self.game_state.available_events.remove(event)

    def run(self):
        while True:
            self.view.display_game_state(self.game_state)
            action = self.controller.get_player_action()

            if action == "research":
                print("Available technologies:")
                for i, tech in enumerate(self.game_state.available_technologies):
                    if not tech.is_researched:
                        print(f"  {i}: {tech.name} ({tech.rp_cost} RP)")
                try:
                    choice = int(input("Enter the number of the technology to research: "))
                    if 0 <= choice < len(self.game_state.available_technologies):
                        self.game_state.player_nation.current_research = self.game_state.available_technologies[choice]
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
            elif action == "invest industry":
                print("Select an industry to invest in:")
                for i, industry in enumerate(self.game_state.player_nation.industries):
                    print(f"  {i}: {industry.name} (Level {industry.level}, IC: {industry.ic})")
                try:
                    choice = int(input("Enter the number of the industry: "))
                    if 0 <= choice < len(self.game_state.player_nation.industries):
                        industry = self.game_state.player_nation.industries[choice]
                        print(f"Investing in {industry.name}. 1 IC costs 10 treasury.")
                        print("Enter amount to invest, or quick select: (1) 10, (2) 100, (3) 500")
                        investment_input = input("> ")
                        amount = 0
                        if investment_input == '1':
                            amount = 10
                        elif investment_input == '2':
                            amount = 100
                        elif investment_input == '3':
                            amount = 500
                        else:
                            try:
                                amount = int(investment_input)
                            except ValueError:
                                print("Invalid input.")

                        if amount > 0:
                            ic_cost_per_unit = 10.0
                            for tech in self.game_state.player_nation.technologies:
                                if tech.name == "Efficient Private Investment" and tech.is_researched:
                                    ic_cost_per_unit *= (1 - tech.private_ic_cost_reduction)
                            cost = amount * ic_cost_per_unit
                            if self.game_state.player_nation.treasury >= cost:
                                self.game_state.player_nation.treasury -= cost
                                industry.government_ic += float(amount)
                                print(f"Invested {cost:.1f} treasury to add {amount} IC to {industry.name}.")
                            else:
                                print("Not enough treasury.")

                        # Leveling
                        while industry.ic >= (100 * (2 ** (industry.level - 1))):
                            industry.level += 1
                            industry.profitability += 0.1 # Increase profitability on level up
                            print(f"{industry.name} leveled up to level {industry.level} (IC: {industry.ic}).")
                            # Check for research efficiency bonus (placeholder for now)
                            if industry.name == "Advanced Manufacturing":
                                print("Advanced Manufacturing industry leveled up! Consider adding research efficiency bonus here.")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
            elif action == "policy":
                print("Select an industry to apply policy to:")
                for i, industry in enumerate(self.game_state.player_nation.industries):
                    print(f"  {i}: {industry.name}")
                try:
                    choice = int(input("Enter the number of the industry: "))
                    if 0 <= choice < len(self.game_state.player_nation.industries):
                        industry = self.game_state.player_nation.industries[choice]
                        policy_type_input = input("Choose policy type ((T)ax break/(S)ubsidy): ").lower()
                        policy_type = {'t': 'tax break', 's': 'subsidy'}.get(policy_type_input, '')

                        if policy_type == "tax break":
                            try:
                                new_tax_rate = float(input("Enter new tax rate (e.g., 0.10 for 10%): "))
                                if 0 <= new_tax_rate <= 0.20: # Max 20% tax
                                    industry.tax_rate = new_tax_rate
                                    print(f"Tax rate for {industry.name} set to {new_tax_rate*100:.0f}%.")
                                else:
                                    print("Invalid tax rate. Must be between 0 and 0.20.")
                            except ValueError:
                                print("Invalid input.")
                        elif policy_type == "subsidy":
                            try:
                                subsidy_amount = float(input("Enter subsidy amount (treasury): "))
                                if subsidy_amount >= 0 and self.game_state.player_nation.treasury >= subsidy_amount:
                                    self.game_state.player_nation.treasury -= subsidy_amount
                                    if industry.private_ic > 0:
                                        industry.subsidy_per_ic = subsidy_amount / industry.private_ic
                                        print(f"Subsidy of {subsidy_amount} applied to {industry.name}. Subsidy per IC: {industry.subsidy_per_ic:.2f}.")
                                    else:
                                        print("Industry has no private IC to apply subsidy to.")
                                else:
                                    print("Invalid subsidy amount or not enough treasury.")
                            except ValueError:
                                print("Invalid input.")
                        else:
                            print("Invalid policy type.")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
            elif action == "set tax":
                try:
                    new_tax_rate = float(input("Enter new national tax rate (e.g., 0.15 for 15%): "))
                    if 0 <= new_tax_rate <= 1.0:
                        self.controller.set_tax_rate(self.game_state.player_nation, new_tax_rate)
                        print(f"National tax rate set to {new_tax_rate*100:.0f}%.")
                    else:
                        print("Invalid tax rate. Must be between 0 and 1.0.")
                except ValueError:
                    print("Invalid input.")
            elif action == "budget":
                budget_category_input = input("Enter budget category ((I)nfrastructure_investment, (S)ocial_spending): ").lower()
                category_map = {
                    'i': 'infrastructure_investment',
                    's': 'social_spending'
                }
                category = category_map.get(budget_category_input, '')

                if category:
                    try:
                        amount = int(input(f"Enter amount for {category}: "))
                        if amount >= 0:
                            self.controller.set_budget(self.game_state.player_nation, category, amount)
                            print(f"Budget for {category} set to {amount}.")
                        else:
                            print("Amount cannot be negative.")
                    except ValueError:
                        print("Invalid input.")
                else:
                    print("Invalid budget category.")
            elif action == "end turn":
                # Research
                if self.game_state.player_nation.current_research:
                    tech = self.game_state.player_nation.current_research
                    effective_rp = self.game_state.player_nation.get_effective_research_points()
                    tech.rp_progress += effective_rp
                    if tech.rp_progress >= tech.rp_cost:
                        tech.is_researched = True
                        self.game_state.player_nation.technologies.append(tech)
                        self.game_state.player_nation.current_research = None
                        print(f"Technology researched: {tech.name}")
                        for industry_name in tech.unlocks_industries:
                            for industry in self.game_state.all_industries:
                                if industry.name == industry_name:
                                    new_industry = Industry(industry.name, industry.tier, industry.profitability, government_ic=0.0, private_ic=0.0, level_bonuses=industry.level_bonuses)
                                    self.game_state.player_nation.industries.append(new_industry)
                                    print(f"New industry unlocked: {new_industry.name}")

                # Economy
                total_treasury_gain = 0
                private_reinvestment_pool = 0
                for industry in self.game_state.player_nation.industries:
                    government_profit = industry.government_ic * industry.base_profitability
                    private_profit = industry.private_ic * industry.profitability # Use effective profitability for private IC

                    total_treasury_gain += government_profit * 0.8 # 80% of government profit to treasury
                    total_treasury_gain += private_profit * industry.tax_rate # Tax rate of private profit to treasury
                    private_reinvestment_pool += private_profit * (1 - industry.tax_rate) # Remaining private profit to reinvestment pool

                # Private Reinvestment (Softmax-like distribution)
                if private_reinvestment_pool > 0:
                    profitable_industries = [ind for ind in self.game_state.player_nation.industries if ind.profitability > 0]
                    if profitable_industries:
                        total_profitability = sum(ind.profitability for ind in profitable_industries)
                        
                        total_private_ic_cost_reduction = 0.0
                        for tech in self.game_state.player_nation.technologies:
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

                self.game_state.player_nation.treasury += total_treasury_gain

                # Update Civilian Economies
                self._update_civilian_economies()

                # Crisis
                self.game_state.crisis_awareness += self.game_state.player_nation.industrial_capacity / 10
                self.check_for_events()

                self.game_state.turn += 1
            elif action == "quit":
                break

    def _update_civilian_economies(self):
        for nation in [self.game_state.player_nation]: # Only player nation for now
            # Deduct budget spending
            nation.treasury -= nation.budget["infrastructure_investment"]
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
