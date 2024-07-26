# this is an api call to LLM for testing purposes
from datetime import datetime
from api.api_client import APIClient
from interaction.interaction_tracker import InteractionManager
from database.database import DatabaseManager

def setup_fictional_user():
    # Create an instance of DatabaseManager
    with DatabaseManager(host='localhost', database='eduai1', user='mysql_admin', password='Mysql#2869') as db_manager:
    #with DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') as db_manager:
        db_manager.populate_user_types()
        #with DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\mysql_database.db') as db_manager: #implementation with context manager for DuckDB
        #db_manager = DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db') #implementation without context manager
        
        # Clear the user_profile table before inserting a new user because otherwise the user_id will conflict with the existing user_id
        #db_manager.clear_user_profile_table()

       # Insert a fictional user
        #max_user_id = db_manager.get_max_user_id() # First, retrieve the maximum user_id from the database
        #user_id = max_user_id + 1 if max_user_id else 1 # Increment the maximum user_id by 1 if it exists, otherwise set user_id to 1
        user_id = kasutaja1
        user_name = "testuser"
        full_name = "Test User"
        email = "testuser@example.com"
        creation_date = datetime.now()
        gender = "Other"
        age = 30
        same_school = "No"
        grades = 85
        user_type_id = 2  # Assuming '2' is a valid user_type_id in your schema

        # Attempt to insert a new user
        #user_added = db_manager.insert_user(user_id, user_name, full_name, email, gender, age, same_school, grades, user_type_id)
        user_added = db_manager.insert_user(user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
        if user_added:
            print("Fictional user created successfully.")
        else:
            print("Failed to create fictional user.")

interaction_manager = InteractionManager()
api_client = APIClient()
#db_manager = DatabaseManager(database_path=r'C:\\Users\\Marti Taru\\Documents\\GitHub\\aiedu\\aiedu\\database.db') #implementation without context manager

# Hardcoded user_id
#user_id = 1

#def initiate_dialogue():
#    with DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') as db_manager:
#        while True:
#            user_input = input("Vajuta < y > kui soovid jätkata või ükskõik millist muud klahvi kui soovid lõpetada: ")
#            if user_input.lower() != 'y':
#                break
#
#            session_id, session_token = db_manager.create_session(user_id)
#            if session_id is None:
#                print("Viga sessiooni loomisel. Programm lõpetab töö.")
#                break
#
#            #for count in range(interaction_manager.interaction_threshold):
#            #    if not interaction_manager.check_interaction_allowed(user_id):
#            #        print("Interaktsioonide limiit on täis. Sessioon lõpeb.")
#            #        break
#
#                question = input("\nKüsi küsimus tehisarult: ")  
#                if not question.strip():  
#                    print("Sa ei küsinud ju midagi... side lõpp.")
#                    break
#
#                response = api_client.ask_llm(question, user_id)
#                if response is None:
#                    print("!! API VIGA !!")
#                    break
#                
#                print("\nSiin on tehisaru arvamus:\n", response['text'])
#
#                try:
#                    db_manager.log_interaction(session_id, user_id, question, response['text'], "GPT3.5")
#                except TypeError as e:
#                    print(f"Viga API suhtluses: {e}")
#                    break
#
#                interaction_manager.log_interaction(user_id)
#                count = interaction_manager.get_interaction_count(user_id)
#                print(f"\nSee on sinu {count}. küsimus selles sessioonis.")
#                
#                if count == interaction_manager.interaction_threshold:
#                    print("\nJa see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)\n")
#                    break
#
#            db_manager.end_session(session_id)
#            print("\nSessioon on lõppenud. Aitäh kasutamast!\n")
#
#    print("Programm lõpetas töö. Head päeva!")


def initiate_dialogue():
    with DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') as db_manager: # implementation with context manager for MySQL
    #with DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db') as db_manager: # implementation with context manager for DuckDB
        session_id, session_token = db_manager.create_session(user_id)
        for _ in range(interaction_manager.interaction_threshold):  # küsida saab kuni 'interaction_threshold' küsimust
            if interaction_manager.check_interaction_allowed(user_id):
                
                question = input("\nKüsi küsimus tehisarult: ")  
                #print(f"KASUTAJAKÜSIMUS: {question}")
                if not question.strip():  
                    print("Sa ei küsinud ju midagi... side lõpp.")
                    break

                response = api_client.ask_llm(question, user_id)
                #print(f"KEELEMUDELI VASTUS: {response}")
                if response is None:
                    print("!! API VIGA !!")
                    break

                print("\n\nSiin on tehisaru arvamus:\n\n", response['text'])

                try:
                    db_manager.log_interaction(session_id, user_id, question, response['text'], "GPT3.5")
                except TypeError as e:
                    print(f"Viga API suhtluses: {e}")
                    break

                interaction_manager.log_interaction(user_id)
                count = interaction_manager.get_interaction_count(user_id)
                print(f"\nSee on sinu {count}. küsimus selles sessioonis.")
                if count == interaction_manager.interaction_threshold: # uus omistamine ja võrdlemine
                    print("\nJa see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)\n")
                    break

                # pärast igat küsimust kontrolli, kas kasutaja soovib jätkata
                if not interaction_manager.prompt_continue():
                    print("\nKasutaja lõpetas dialoogi.\n")
                    break

        db_manager.end_session(session_id)
        print("\nSessioon on lõppenud. Aitäh kasutamast!\n")



if __name__ == "__main__":
    setup_fictional_user()
    initiate_dialogue()
    #with DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') as db_manager:
    #    db_manager.verify_user_profile()
    #    db_manager.verify_user_sessions()
    #    db_manager.verify_interactions()