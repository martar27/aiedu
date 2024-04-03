# interaction_tracker.py

class InteractionManager:
    def __init__(self):
        self.interaction_counts = {}  # Dictionary to hold user_id: interaction_count
        self.interaction_threshold = 3  # now 3 is hardcoded, can be made configurable

    def log_interaction(self, user_id):
        self.interaction_counts[user_id] = self.interaction_counts.get(user_id, 0) + 1

    def check_interaction_allowed(self, user_id):
        return self.interaction_counts.get(user_id, 0) < self.interaction_threshold
    
    def prompt_continue(self):
#        response = input("Do you want to ask the next question or do you want to terminate the dialogue for now? Press 'y' for yes or 'n' for no: ")
        response = input("Vajuta < y > kui soovid jätkata või < n > kui soovid lõpetada:")
        return response.strip().lower() == 'y'

