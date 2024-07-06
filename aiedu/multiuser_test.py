import threading
import time
from datetime import datetime
from api.api_client import APIClient
from interaction.interaction_tracker import InteractionManager
from database.database import DatabaseManager

# Create a threading lock
db_lock = threading.Lock()

def setup_fictional_user(user_id, user_name):
    with db_lock:
        with DatabaseManager(database_path=r'C:\\Users\\Marti Taru\\Documents\\GitHub\\aiedu\\aiedu\\database.db') as db_manager:
            db_manager.populate_user_types()
            full_name = f"{user_name} Fullname"
            email = f"{user_name}@example.com"
            creation_date = datetime.now()
            gender = "Other"
            age = 30
            same_school = "No"
            grades = 85
            user_type_id = 2  # Assuming '2' is a valid user_type_id in your schema

            user_added = db_manager.insert_user(user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
            if user_added:
                print(f"Fictional user {user_name} created successfully.")
            else:
                print(f"Failed to create fictional user {user_name}.")

def user_interaction(user_id, user_name):
    interaction_manager = InteractionManager()
    api_client = APIClient()
    with db_lock:
        with DatabaseManager(database_path=r'C:\\Users\\Marti Taru\\Documents\\GitHub\\aiedu\\aiedu\\database.db') as db_manager:
            session_id, session_token = db_manager.create_session(user_id)
            for _ in range(interaction_manager.interaction_threshold):
                if interaction_manager.check_interaction_allowed(user_id):
                    question = f"Question from {user_name}"
                    print(f"{user_name} QUESTION: {question}")

                    response = api_client.ask_llm(question, user_id)
                    print(f"{user_name} LLM RESPONSE: {response}")
                    if response is None:
                        print("!! API ERROR !!")
                        break

                    db_manager.log_interaction(session_id, user_id, question, response['text'], "GPT3.5")

                    interaction_manager.log_interaction(user_id)
                    count = interaction_manager.get_interaction_count(user_id)
                    print(f"{user_name} interaction count: {count}")
                    if count == interaction_manager.interaction_threshold:
                        print(f"{user_name} reached interaction limit.")
                        break

                else:
                    break

if __name__ == "__main__":
    # Setup fictional users
    users = [(1, "testuser1"), (2, "testuser2"), (3, "testuser3")]

    # Create fictional users
    for user_id, user_name in users:
        setup_fictional_user(user_id, user_name)

    # Simulate interactions
    threads = []
    for user_id, user_name in users:
        thread = threading.Thread(target=user_interaction, args=(user_id, user_name))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Multi-user simulation completed.")
