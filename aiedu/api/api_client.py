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
        # set OPENAI_API_KEY=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
        # echo %OPENAI_API_KEY%

    def ask_llm(self, question, user_id='kasutaja1'):

        if not self.interaction_manager.check_interaction_allowed(user_id):
            print("Ja see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)")
#            print("This was your last question for this session.")
            return None
        
        user_type = "student" if user_id == "kasutaja1" else "general"
        
        #messages = self.form_message(question) # when user_type is not specified
        messages = self.form_message(question, user_type=user_type)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
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
    def form_message(self, question, user_type = "student"):
        
        if user_type == "student":
            #system_message = "You are a supportive teacher assisting 11-13 year-old children."
            system_message = "Sa oled õpetaja, kes aitab 11-13 aastastel koolilastel arendada enda võimeid."
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
        # Initialize an empty  dictionary
        result = {
            'text': None,
            #'token_count': 0,
            #'received_time': None,
            # more fields
        }
    
        if response:
            try:
                # Extracting the text content in the response
                result['text'] = response.choices[0].message['content']
    
                # Calculating the token count
                #result['token_count'] = len(response.choices[0].message['content'].split())
    
                # Storing the time when the response was received
                #result['received_time'] = datetime.now()
    
                # Extract and store additional information from response 
    
            except Exception as e:
                print(f"An error occurred while processing the response: {e}")
    
        return result
    