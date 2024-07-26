# api_client.py
import os
import openai
from datetime import datetime
from database.database import DatabaseManager  # Import the DatabaseManager class


# APIClient klass kapseldab interaktsioonid OpenAI või muu LLM-i API-ga.

class APIClient:
    def __init__(self):
        # Initsialiseeri API key keskkonna muutujast OPENAI_API_KEY
        self.api_key = os.getenv('OPENAI_API_KEY') 
        openai.api_key = self.api_key
        self.student_user_ids = ["kasutaja1", "kasutaja2", "kasutaja3"] # initial list of student user ids. this object is dyamic and will be updated with the actual list of student user ids from the database. currently it is a hard-coded list.
        #self.db_manager = db_manager  # DatabaseManager instance
        #db_path = os.getenv('DATABASE_PATH')
        #self.db_manager = DatabaseManager(db_path)
        
        #self.db_manager = DatabaseManager(r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db') # DatabaseManager instance for DuckDB
        self.db_manager = DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') # DatabaseManager instance for MySQL
        self.db_manager.create_connection()

##    def ask_llm(self, question, user_id):
##        try:
##            response = openai.ChatCompletion.create(
##                model="gpt-3.5-turbo",  # Use the appropriate model name
##                messages=[
##                    {"role": "system", "content": "You are a helpful assistant."},
##                    {"role": "user", "content": question}
##                ]
##            )
##            return response
##        except Exception as e:
##            print(f"An error occurred while interacting with the OpenAI API: {e}")
##            return None

# generation of a simulated response, without interaction with OpenAI's API
#    def ask_llm(self, question, user_id):
#        try:
#            # Simulate API call to OpenAI's GPT
#            response = {
#                'choices': [{
#                    'message': {
#                        'content': f'Simulated response to the question: {question}'
#                    }
#                }]
#            }
#            return response
#        except Exception as e:
#            print(f"An error occurred while interacting with the OpenAI API: {e}")
#            return None
    
    def ask_llm(self, question, user_id="kasutaja1"):
##        user_type = self.db_manager.get_user_type(user_id)  # Retrieve user type from database        
        print(ele for ele in student_user_ids)
        user_type = "student" if user_id in self.student_user_ids else "general"
        print(f"Debug user_type: {user_type}")
        #user_type = "student" if user_id == "kasutaja1" else "general"
##        
##        #messages = self.form_message(question) # user_type not specified
        messages = self.form_message(question, user_type=user_type)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
##            #return response.choices[0].message['content']
            #self.db_manager.log_interaction(user_id, question, response.choices[0].message['content'], datetime.now(), 'gpt-3.5-turbo', "System message based on context")
            self.db_manager.log_interaction(user_id, question, response.choices[0].message['content'], datetime.now(), 'gpt-3.5-turbo')
##            return response
            result = {'text': response.choices[0].message['content']}
            return result
        except Exception as e:
            print(f"An error occurred while interacting with the OpenAI API: {e}")
            return None

    # The method form_messages will form a message depending on user group
    # It will use different, predefined system_messages that can be retrieved from the database 
    # Or the system_message can be hard-coded here like now. 
    def form_message(self, question, user_type = "student"):
        if user_type == "student":
            #system_message = "You are a supportive teacher assisting 11-13 year-old children."
            #system_message = "Sa oled abivalmis õpetaja, kes aitab 11-13 aastaseid kooliõpilasi. Neile nõu andes lähtud sa aktiivse õppimise, aktiivse õppija ning probleemõppe metoodikast."
#            system_message = "Hinda selle eesmärgi sobivust 11-13 aasta vanuse kooliõpilase jaoks. Anna tagasisidet ja soovitusi eesmärgi parandamiseks 11-13 aastasele kooliõpilasele. Ära anna käitumissoovitusi eesmärgi saavutamiseks."
            #system_message = ""
            system_message = "Sa oled 11-13 aastaste õpilaste haridusnõustaja. Sa loed 11-13 aastase õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta soovituste andmiseks eesmärgi sõnastamise süsteemi 3R: Kas eesmärk on saavutatav? Kas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära anna otseseid käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu õpilase poole otse ja kasuta selleks otsest kõnet."
        #elif user_type == "professional":
            #system_message = "Hinda selle eesmärgi sobivust 11-13 aasta vanuse kooliõpilase jaoks. Anna tagasisidet ja soovitusi eesmärgi parandamiseks 11-13 aastasele kooliõpilasele. Ära anna käitumissoovitusi eesmärgi saavutamiseks."
            #system_message = ""
        #else:
            #system_message = "Sa oled 11-13 aastaste õpilaste haridusnõustaja. Sa loed 11-13 aastase õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta soovituste andmiseks eesmärgi sõnastamise süsteemi 3R: Kas eesmärk on saavutatav? Kas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära anna otseseid käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu õpilase poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Sa loed 11-13 aasta õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta tagasiside andmiseks eesmärgi sõnastamise süsteemi ABCDE: Kas eesmärk on saavutatav seitsme nädala jooksul koolis? Kas sa usud, et sa suudad eesmärgi saavutada? Kas sa oled valmis pingutama eesmärgi saavutamiseks? Kas sa oled oma eesmärgi kirja pannud? Kas see eesmärk teeb sind energiliseks ja teotahteliseks? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi GROW: Mida sa tahad saavutada? Mida sa praegu oskad, tead ja teed selle eesmärgi suhtes? Mida sa saaksid teha, et oma eesmärki saavutada? Mida konkreetselt sa teed? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi OKR: Mida sa tahad saavutada? Kuidas sa mõõdad enda edenemist ja saad aru, et oled oma eesmärgile lähemale liikunud või selle saavutanud? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi WOOP: Mida sa tahad saavutada? Mis on parim võimalik tulemus? Mis võiks takistada eesmärgi saavutamist? Kuidas sa saad takistustest üle? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid ja selgeid ja lühidaid, konkreetseid soovitusi just eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele. Lähtu SMART Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "You are a general assistant."
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        
        return messages

    def parse_response(self, response):
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