# this is an api call to LLM for testing purposes

from api.api_client import APIClient
from interaction.interaction_tracker import InteractionManager
from database.database_manager import DatabaseManager

def setup_fictional_user():
    # Create an instance of DatabaseManager
    db_manager = DatabaseManager(database_path="path_to_your_database.db")
    
    # Insert a fictional user
    user_id = 1
    user_name = "testuser"
    full_name = "Test User"
    email = "testuser@example.com"
    gender = "Other"
    age = 30
    same_school = "No"
    grades = 85
    user_type_id = 2  # Assuming '2' is a valid user_type_id in your schema

    # Attempt to insert a new user
    user_added = db_manager.insert_user(user_id, user_name, full_name, email, gender, age, same_school, grades, user_type_id)
    if user_added:
        print("Fictional user created successfully.")
    else:
        print("Failed to create fictional user.")

interaction_manager = InteractionManager()
api_client = APIClient()

# Hardcoded user_id
user_id = 1

def initiate_dialogue():
    for _ in range(interaction_manager.interaction_threshold):  # küsida saab kuni 'interaction_threshold' küsimust
        if interaction_manager.check_interaction_allowed(user_id):
              
            question = input("\nKüsi küsimus tehisarult: ")  
            if not question.strip():  
                print("Sa ei küsinud ju midagi... side lõpp.")
                break

            response = api_client.ask_llm(question, user_id)
            if response is None:
                print("!! API VIGA !!")
                break

            print("\n\nSiin on tehisaru arvamus:\n\n",response.choices[0].message['content'])

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

        else: # igaks juhuks
            break


if __name__ == "__main__":
    initiate_dialogue()
