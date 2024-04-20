# this is an api call to LLM for testing purposes

from api.api_client import APIClient
from interaction.interaction_tracker import InteractionManager
from database.database import DatabaseManager  # Ensure this import is correct

def setup_fictional_user():
    # Create an instance of DatabaseManager
    db_manager = DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db')
    
    # Insert a fictional user
    user_added = db_manager.insert_user(
        1,  # user_id
        "username",  # user_name
        "Full Name",  # full_name
        "email@example.com",  # email
        "gender",  # gender
        25,  # age
        "No",  # same_school
        90,  # grades
        2   # user_type_id
    )

    # Attempt to insert a new user
    #user_added = db_manager.insert_user(user_id, user_name, full_name, email, gender, age, same_school, grades, user_type_id)
    if user_added:
        print("Fictional user created successfully.")
    else:
        print("Failed to create fictional user.")

def initiate_dialogue():
    # First, ensure the fictional user is setup
    setup_fictional_user()

    interaction_manager = InteractionManager()
    api_client = APIClient()

    for _ in range(interaction_manager.interaction_threshold):
        if interaction_manager.check_interaction_allowed(1):
            
            question = input("\nKüsi küsimus tehisarult: ")
            if not question.strip():
                print("Sa ei küsinud ju midagi... side lõpp.")
                break

            response = api_client.ask_llm(question, 1)
            if response is None:
                print("!! API VIGA !!")
                break

            print("\n\nSiin on tehisaru arvamus:\n\n", response.choices[0].message['content'])

            interaction_manager.log_interaction(1)

            count = interaction_manager.get_interaction_count(1)
            print(f"\nSee on sinu {count}. küsimus selles sessioonis.")
            if count == interaction_manager.interaction_threshold:
                print("\nJa see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)\n")
                break

            if not interaction_manager.prompt_continue():
                print("\nKasutaja lõpetas dialoogi.\n")
                break

        else:
            break

if __name__ == "__main__":
    initiate_dialogue()
