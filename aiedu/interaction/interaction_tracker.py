# interaction_tracker.py

class InteractionTracker:
    def __init__(self, user_id, max_interactions=3):
        self.user_id = user_id
        self.max_interactions = max_interactions
        self.interactions = 0

    def increment_interaction(self):
        self.interactions += 1

    def is_limit_reached(self):
        return self.interactions >= self.max_interactions
