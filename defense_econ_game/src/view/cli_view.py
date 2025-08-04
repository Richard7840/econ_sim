import math

class CLIView:
    def display_game_state(self, game_state):
        player = game_state.player_nation
        treasury_gain = sum(industry.ic * industry.profitability for industry in player.industries)
        crisis_gain = player.industrial_capacity / 10

        print("--- Game State ---")
        print(f"Turn: {game_state.turn}")
        print(f"Player Nation: {player.name}")
        print(f"  Treasury: {player.treasury} (+{treasury_gain})")
        print(f"  Industrial Capacity: {player.industrial_capacity}")
        print(f"  Research Points: {player.research_points}")
        print(f"  Public Opinion: {player.public_opinion}")
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
        print(f"Crisis Awareness: {game_state.crisis_awareness} (+{crisis_gain})")
        print(f"Social Dissonance: {game_state.social_dissonance} (+0)")
        print("------------------")
