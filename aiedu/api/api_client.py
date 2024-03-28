# api_client.py
import os
import openai

class APIClient:
    def __init__(self):
        # Initialize with an API key from the environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def ask_llm(self, question):
        # Send a question to the OpenAI API and handle the response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a supportive teacher assisting 11-13 year-old children."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"An error occurred while interacting with the OpenAI API: {e}")
            return None

    # Preserving the existing methods
    def send_request(self, data):
        # Logic to send a request to the API
        pass

    def receive_response(self):
        # Logic to handle the response from the API
        pass

