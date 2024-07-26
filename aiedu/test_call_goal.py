from goals.goal_manager import GoalManager
from database.database import DatabaseManager
from datetime import datetime
import uuid

def main():
    # initialise DatabaseManager with the same parameters as in test_call.py
    db_manager = DatabaseManager(host='localhost', database='eduai1', user='mysql_admin', password='Mysql#2869')
    #user_id = 11  # Example user_id
    #user_id = ""  # Example user_id
    #max_user_id = db_manager.get_max_user_id() # First, retrieve the maximum user_id from the database
    #user_id = max_user_id + 1 if max_user_id else 1 # Increment the maximum user_id by 1 if it exists, otherwise set user_id to 1
        # Retrieve the last created user_id from the database
    cursor = db_manager.conn.cursor()
    cursor.execute("SELECT user_id FROM user_profile WHERE user_id LIKE 'kasutaja%' ORDER BY CAST(SUBSTRING(user_id, 9) AS UNSIGNED) DESC LIMIT 1")
    result = cursor.fetchone()

    # Set user_id for the main function
    user_id = result[0] if result else None  # Handle the case where no users exist

    if user_id:
        session_id = str(uuid.uuid4())

        goal_manager = GoalManager(db_manager=db_manager)


    #session_id = str(uuid.uuid4())  # Example session_id

    #goal_manager = GoalManager(db_manager=db_manager)
    
    # Step 1: Define and refine goal
        result = goal_manager.define_goal(user_id, session_id)
    #print("Vahetulemus: ", result)
    
    # Step 2: Retrieve and display final goal
        final_goal = goal_manager.display_final_goal(user_id, session_id)
        print("\nLõplik eesmärk: ", final_goal)
    else:
        print("No user found in the database.")
    
    # Step 3: Ask LLM for help to achieve the goal
    #if final_goal:
    #    goal_manager.ask_llm_for_help(user_id, session_id, final_goal)

def setup_fictional_user():
    #used_user_ids = ["kasutaja1"]
    # Create an instance of DatabaseManager
    with DatabaseManager(host='localhost', database='eduai1', user='mysql_admin', password='Mysql#2869') as db_manager:
    #with DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869') as db_manager:
        db_manager.populate_user_types()
        #with DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\mysql_database.db') as db_manager: #implementation with context manager for DuckDB
        #db_manager = DatabaseManager(database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db') #implementation without context manager
        
       # Insert a fictional user
        cursor = db_manager.conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTRING(user_id, 9) AS UNSIGNED)) FROM user_profile WHERE user_id LIKE 'kasutaja%'")
        result = cursor.fetchone()
        max_id = result[0] if result[0] is not None else 0  # If no existing users, start from 0
        new_user_id = f"kasutaja{max_id + 1}"
        user_name = f"testkasutaja{max_id + 1}"
        full_name = f"Test Kasutaja {max_id + 1}"
        email = f"testkasutaja{max_id+1}@example.com"
        creation_date = datetime.now()
        gender = "Other"
        age = 30
        same_school = "No"
        grades = 85
        user_type_id = 2  # Assuming '2' is a valid user_type_id in your schema

        # Attempt to insert a new user
        #user_added = db_manager.insert_user(user_id, user_name, full_name, email, gender, age, same_school, grades, user_type_id)
        user_added = db_manager.insert_user(new_user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
        if user_added:
            print("Fictional user created successfully.")
        else:
            print("Failed to create fictional user.")

if __name__ == "__main__":
    setup_fictional_user()
    main()
