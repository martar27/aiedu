# api_client.py
import os
import openai
from datetime import datetime

# APIClient klass kapseldab interaktsioonid OpenAI või muu LLM-i API-ga.

class APIClient:
    def __init__(self):
        # Initsialiseeri API key keskkonna muutujast OPENAI_API_KEY
        self.api_key = os.getenv('OPENAI_API_KEY') 
        openai.api_key = self.api_key

    def ask_llm(self, question, user_id='kasutaja1'):
      
        user_type = "student" if user_id == "kasutaja1" else "general"
        
        #messages = this.form_message(question) # user_type not specified
        messages = this.form_message(question, user_type=user_type)
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
    # It will use different, predefined system_messages that can be retrieved from the database 
    # Or the system_message can be hard-coded here like now. 
    def form_message(this, question, user_type = "student"):
        if user_type == "student":
            #system_message = "You are a supportive teacher assisting 11-13 year-old children."
            system_message = "Sa oled abivalmis õpetaja, kes aitab 11-13 aastaseid kooliõpilasi. Neile nõu andes lähtud sa aktiivse õppimise, aktiivse õppija ning probleemõppe metoodikast."
        elif user_type == "professional":
            system_message = "You are an assistant providing professional advice."
        else:
            system_message = "You are a general assistant."
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        
        return messages

    def parse_response(this, response):
        # sõnastik vastuse töötlemiseks
        result = {
            'text': None,
            #'token_count': 0,
            #'received_time': None,
            # more fields
        }
    
        if response:
            try:
                # eralda vastusest tekst
                result['text'] = response.choices[0].message['content']
    
                # Calculating the token count
                #result['token_count'] = len(response.choices[0].message['content'].split())
    
                # Storing the time when the response was received
                #result['received_time'] = datetime.now()
    
                # Extract and store additional information from response 
    
            except Exception as e:
                print(f"An error occurred while processing the response: {e}")
    
        return result
    