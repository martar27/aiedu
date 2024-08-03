# api_client.py
import os
import openai
from datetime import datetime
from database.database import DatabaseManager  # Import the DatabaseManager class


# APIClient klass kapseldab interaktsioonid OpenAI või muu LLM-i API-ga.

class APIClient:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.student_user_ids = []
        # Initsialiseeri API key keskkonna muutujast OPENAI_API_KEY
        self.api_key = os.getenv('OPENAI_API_KEY') 
        openai.api_key = self.api_key
                # Initialize the DatabaseManager instance
        #self.db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
        self.db_manager.create_connection()
        
        # Fetch student user IDs from the database
        self.student_user_ids = self.fetch_student_user_ids()

    def fetch_student_user_ids(self):
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT user_id FROM user_profile WHERE user_type_id IN (SELECT id FROM user_type WHERE user_type LIKE 'student%')")
        #cursor.execute("SELECT user_type_id FROM user_profile WHERE user_type_id IN (SELECT id FROM user_type WHERE user_type LIKE 'student%')")
        student_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return student_ids

    def ask_llm(self, question, user_id):
        if user_id in self.student_user_ids[:2]:  
            user_type = "student"
        else:
            user_type = "general"
        
        #messages = self.form_message(question) # user_type not specified
        messages = self.form_message(question, user_type=user_type)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            #print(f"debug AC, funktsioon: ask_llm, question sent to LLM {question}")
            interaction_text = response.choices[0].message['content']
            print(f"debug AC, funktsioon: ask_llm, LLM response '{interaction_text}'")
            
            session_active = any(uid == user_id for sid, uid in self.db_manager.active_sessions.items())
            #session_active = self.db_manager.active_sessions
            print(f"debug AC, funktsioon: ask_llm, kasutaja {user_id} sessioon on aktiivne: {session_active}")
            if session_active:
                session_id = next(sid for sid, uid in self.db_manager.active_sessions.items() if uid == user_id)
                print(f">>>debug AC, funktsioon: ask_llm: kasutaja {user_id} sessioon on aktiivne: {self.db_manager.active_sessions}")
                print(f">>>debug AC, funktsioon: ask_llm, kutsumine log_interaction: session_id {session_id}, user_id {user_id}, question {question}, interaction_text {interaction_text}, 'gpt-3.5-turbo'")
                self.db_manager.log_interaction(session_id, user_id, question, interaction_text, 'gpt-3.5-turbo')
                print(f">>>debug AC, funktsioon: ask_llm, log_interaction on lõpetatud")
            #return interaction_text
            return {'text': interaction_text}
        except Exception as e:
            print(f"An error occurred while interacting with the OpenAI API: {e}")
            return None
     
    def form_message(self, question, user_type = "student"):
        #print(f"DEBUG form_message received user_type = {user_type}")
        if user_type == "student":
            #system_message = "You are a supportive teacher assisting 11-13 year-old children."
            #system_message = "Sa oled abivalmis õpetaja, kes aitab 11-13 aastaseid kooliõpilasi. Neile nõu andes lähtud sa aktiivse õppimise, aktiivse õppija ning probleemõppe metoodikast."
#            system_message = "Hinda selle eesmärgi sobivust 11-13 aasta vanuse kooliõpilase jaoks. Anna tagasisidet ja soovitusi eesmärgi parandamiseks 11-13 aastasele kooliõpilasele. Ära anna käitumissoovitusi eesmärgi saavutamiseks."
            #system_message = ""
            system_message = "Sa oled 11-13 aastaste õpilaste haridusnõustaja. Sa loed 11-13 aastase õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta soovituste andmiseks eesmärgi sõnastamise süsteemi 3R: Kas eesmärk on saavutatav? Kas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära anna otseseid käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu õpilase poole otse ja kasuta selleks otsest kõnet."
        #elif user_type == "professional":
            #system_message = "Hinda selle eesmärgi sobivust 11-13 aasta vanuse kooliõpilase jaoks. Anna tagasisidet ja soovitusi eesmärgi parandamiseks 11-13 aastasele kooliõpilasele. Ära anna käitumissoovitusi eesmärgi saavutamiseks."
            #system_message = ""
        else:
            #print(f"Debug-warning: form_message received user_type = {user_type} that was not supposed to happen.")
            #system_message = "Sa oled 11-13 aastaste õpilaste haridusnõustaja. Sa loed 11-13 aastase õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta soovituste andmiseks eesmärgi sõnastamise süsteemi 3R: Kas eesmärk on saavutatav? Kas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära anna otseseid käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu õpilase poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Sa loed 11-13 aasta õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta tagasiside andmiseks eesmärgi sõnastamise süsteemi ABCDE: Kas eesmärk on saavutatav seitsme nädala jooksul koolis? Kas sa usud, et sa suudad eesmärgi saavutada? Kas sa oled valmis pingutama eesmärgi saavutamiseks? Kas sa oled oma eesmärgi kirja pannud? Kas see eesmärk teeb sind energiliseks ja teotahteliseks? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi GROW: Mida sa tahad saavutada? Mida sa praegu oskad, tead ja teed selle eesmärgi suhtes? Mida sa saaksid teha, et oma eesmärki saavutada? Mida konkreetselt sa teed? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi OKR: Mida sa tahad saavutada? Kuidas sa mõõdad enda edenemist ja saad aru, et oled oma eesmärgile lähemale liikunud või selle saavutanud? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid, selgeid, lühidaid soovitusi eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele järgmiseks seitsmeks nädalaks. Kasuta eesmärgi sõnastamise süsteemi WOOP: Mida sa tahad saavutada? Mis on parim võimalik tulemus? Mis võiks takistada eesmärgi saavutamist? Kuidas sa saad takistustest üle? Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Anna konkreetseid ja selgeid ja lühidaid, konkreetseid soovitusi just eesmärgi sõnastamiseks 11-13 aastasele kooliõpilasele. Lähtu SMART Ära anna käitumissoovitusi eesmärgi saavutamiseks. Pöördu tema poole otse ja kasuta selleks otsest kõnet."
            system_message = "Sa oled 11-13 aastaste õpilaste haridusnõustaja. Sa loed 11-13 aastase õpilase poolt sõnastatud eesmärki koolis tegutsemiseks seitsme nädala jooksul. Anna konkreetseid, selgeid, lühidaid soovitusi selle eesmärgi parandamiseks. Kasuta soovituste andmiseks eesmärgi sõnastamise süsteemi 3R: Kas eesmärk on saavutatav? Kas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära anna otseseid käitumissoovitusi eesmärgi saavutamiseks. Ara anna ise vastuseid nendele küsimustele, anna neid küsimusi kasutades tagasisidet õpilasele. Pöördu õpilase poole otse ja kasuta selleks otsest kõnet."
            #system_message = "Sa oled kommionu."
            #print(f"DEBUG system message used in form_message {system_message}")
        
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