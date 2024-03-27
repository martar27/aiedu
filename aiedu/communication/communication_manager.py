# communication_manager.py

class CommunicationManager:
    def __init__(self, api_client, database):
        self.api_client = api_client
        self.database = database

    def ask_llm(self, question):
        # Logic to send question to LLM and return response
        pass

    def save_message(self, message):
        # Logic to save message to database
        pass

    def get_last_response(self):
        # Logic to retrieve last response from database
        pass
