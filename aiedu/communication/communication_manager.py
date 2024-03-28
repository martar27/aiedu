# communication_manager.py

class CommunicationManager:
    def handle_user_input(self, user_id, input_text):
    # Log the user's input
        self.database_manager.log_input_to_database(user_id, input_text, is_llm_response=False)
    
    # Check if further interaction is allowed based on the flag from the Interaction module
        if not self.interaction_manager.check_interaction_allowed(user_id):
        # Retrieve and return a specific message when the threshold is reached
            termination_message = self.database_manager.get_termination_message(user_id)
        return termination_message
    
    # If interaction is allowed, send the input to the LLM and log the response
        response = self.api_client.ask_llm(input_text)
        self.database_manager.log_input_to_database(user_id, response, is_llm_response=True)
        return response