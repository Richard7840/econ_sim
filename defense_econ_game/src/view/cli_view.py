import math

class CLIView:
    """
    The command-line interface view for the game.
    """
    def display_game_state(self, game_state):
        """
        Displays the current game state to the user.

        Args:
            game_state (GameState): The current state of the game.
        """
        player = game_state.player_nation
        projected_treasury_change = player.calculate_projected_treasury_change(game_state.available_projects)
        crisis_gain = player.industrial_capacity / 10

        print("--- Game State ---")
        print(f"Turn: {game_state.turn}")
        print(f"Player Nation: {player.name}")
        print(f"  Treasury: {player.treasury:.1f} ({projected_treasury_change:+.1f})")
        print(f"  Industrial Capacity: {player.industrial_capacity}")
        print(f"  Research Points: {player.research_points}")
        opinion_change_rate = (player.target_public_opinion - player.public_opinion) * 0.20
        print(f"  Public Opinion: {player.public_opinion:.1f} (Target: {player.target_public_opinion:.1f}, Change: {opinion_change_rate:+.1f})")
        projected_gdp_increase = player.civilian_gdp * player.get_gdp_growth_rate()
        print(f"  Civilian GDP: {player.civilian_gdp:.2f} (+{projected_gdp_increase:.2f})")
        print(f"  Tax Rate: {player.tax_rate*100:.0f}%")
        print(f"  Social Spending: {player.budget['social_spending']}")
        print(f"  Infrastructure Level: {player.infrastructure_level}")
        print(f"  IC Focus: {player.ic_focus_policy}")
        print("  Industries:")
        profitable_industries = [ind for ind in player.industries if ind.profitability > 0]
        total_profitability = sum(ind.profitability for ind in profitable_industries)

        for industry in player.industries:
            reinvestment_share = 0
            if total_profitability > 0 and industry.profitability > 0:
                reinvestment_share = (industry.profitability / total_profitability) * 100
            print(f"    - {industry.name} (Tier {industry.tier}, Level {industry.level}, Gov IC: {industry.government_ic:.1f}, Private IC: {industry.private_ic:.1f}, Base Profit: {industry.base_profitability:.1f}, Tax: {industry.tax_rate*100:.0f}%, Subsidy/IC: {industry.subsidy_per_ic:.2f}, Effective Profit: {industry.profitability:.1f}, Reinvestment Share: {reinvestment_share:.1f}%)")
        
        effective_rp = player.get_effective_research_points()
        if player.current_research:
            research = player.current_research
            turns_to_complete = math.ceil((research.rp_cost - research.rp_progress) / effective_rp) if effective_rp > 0 else 'N/A'
            print(f"  Current Research: {research.name} ({research.rp_progress}/{research.rp_cost} RP) (+{effective_rp:.1f} RP/turn) - {turns_to_complete} turns remaining")
        else:
            print(f"  Current Research: None (+{effective_rp:.1f} RP/turn)")
            
        print(f"  Researched Technologies: {[tech.name for tech in player.technologies]}")
        print(f"Crisis Awareness: {game_state.crisis_awareness:.1f} (+{crisis_gain:.1f})")
        print(f"Social Dissonance: {game_state.social_dissonance} (+0)")

        print("--- Construction ---")
        print(f"Construction Slots: {len(player.active_projects)}/{player.construction_slots}")
        if player.active_projects:
            print("Active Projects:")
            total_cp_generated = player.calculate_construction_points()
            cp_per_project = total_cp_generated

            for i, project in enumerate(player.active_projects):
                project_def = next((p for p in game_state.available_projects if p['id'] == project.project_id), None)
                if project_def:
                    target_str = f" [{project.target}]" if project.target else ""
                    print(f"  {i+1}. {project_def['name']}{target_str} ({project.current_cp:.0f}/{project_def['cp_cost']} CP, +{cp_per_project:.1f} CP/turn)")
        if player.project_queue:
            print("Project Queue:")
            for i, project in enumerate(player.project_queue):
                project_def = next((p for p in game_state.available_projects if p['id'] == project.project_id), None)
                if project_def:
                    target_str = f" [{project.target}]" if project.target else ""
                    print(f"  {i+1+len(player.active_projects)}. {project_def['name']}{target_str}")
        print("------------------")