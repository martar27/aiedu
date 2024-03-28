# api_client.py
import os
import openai
from datetime import datetime

# The APIClient class encapsulates the interactions with the OpenAI API.
# It is designed to handle the construction and sending of requests based on different user types,
# allowing for flexible and user-specific interactions with the LLM.

class APIClient:
    def __init__(self):
        # Initialize with an API key from the environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def ask_llm(self, question):
        # High-level method to interact with the LLM.
        messages = self.form_message(question)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            #return response.choices[0].message['content']
            return response
        except Exception as e:
            print(f"An error occurred while interacting with the OpenAI API: {e}")
            return None

    # The method form_messages will form a message depending on user group
    # It will use different, predefined system_messages that can be retrieved from the database that is in use
    # Or the system_message can be inserted manually i.e. be hard-coded 
    def form_message(self, question, user_type):
        # Tailor the system message based on the user type or other context
        if user_type == "student":
            system_message = "You are a supportive teacher assisting 11-13 year-old children."
        elif user_type == "professional":
            system_message = "You are an assistant providing professional advice."
        else:
            system_message = "You are a general assistant."
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        
        return messages


    def parse_response(self, response):
        # Initialize an empty  dictionary (or another object to store the extracted data)
        result = {
            'text': None,
            'token_count': 0,
            'received_time': None,
            # add more fields when necessary
        }
    
        if response:
            try:
                # Extracting the text content in the response
                result['text'] = response.choices[0].message['content']
    
                # Calculating the token count
                result['token_count'] = len(response.choices[0].message['content'].split())
    
                # Storing the time when the response was received
                result['received_time'] = datetime.now()
    
                # Extract and store additional information from response 
    
            except Exception as e:
                print(f"An error occurred while processing the response: {e}")
    
        return result
