from src.models.project_instance import ProjectInstance

class GameController:
    def get_player_action(self):
        prompt = "Actions: (E)nd turn, (R)esearch, (P)olicy, (S)et Tax, (B)udget, (C)onstruction, (Q)uit\n> "
        action_map = {
            'e': 'end turn',
            'r': 'research',
            'p': 'policy',
            's': 'set tax',
            'b': 'budget',
            'c': 'construction',
            'q': 'quit'
        }
        user_input = input(prompt).lower()
        return action_map.get(user_input, user_input)

    def set_tax_rate(self, nation, rate):
        nation.tax_rate = rate
        nation._calculate_target_public_opinion()

    def set_budget(self, nation, category, amount):
        if category in nation.budget:
            nation.budget[category] = amount
            nation._calculate_target_public_opinion()
        else:
            print(f"Invalid budget category: {category}")

    def start_project(self, nation, project_id, target=None):
        if len(nation.active_projects) < nation.construction_slots:
            nation.active_projects.append(ProjectInstance(project_id, target))
        else:
            nation.project_queue.append(ProjectInstance(project_id, target))

    def cancel_project(self, nation, queue_index):
        if 0 <= queue_index < len(nation.active_projects):
            project = nation.active_projects.pop(queue_index)
            # Partial refund logic can be added here
        elif 0 <= queue_index - len(nation.active_projects) < len(nation.project_queue):
            nation.project_queue.pop(queue_index - len(nation.active_projects))

    def set_ic_focus(self, nation, policy):
        nation.ic_focus_policy = policy
