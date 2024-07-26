from goals.goal_manager import GoalManager
from database.database import DatabaseManager
import uuid

def main():
    # initialise DatabaseManager with the same parameters as in test_call.py
    db_manager = DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869')
    user_id = 11  # Example user_id
    #max_user_id = db_manager.get_max_user_id() # First, retrieve the maximum user_id from the database
    #user_id = max_user_id + 1 if max_user_id else 1 # Increment the maximum user_id by 1 if it exists, otherwise set user_id to 1
    session_id = str(uuid.uuid4())  # Example session_id



    goal_manager = GoalManager(db_manager=db_manager)
    
    # Step 1: Define and refine goal
    result = goal_manager.define_goal(user_id, session_id)
    #print("Vahetulemus: ", result)
    
    # Step 2: Retrieve and display final goal
    final_goal = goal_manager.display_final_goal(user_id, session_id)
    print("\nLõplik eesmärk: ", final_goal)
    
    # Step 3: Ask LLM for help to achieve the goal
    #if final_goal:
    #    goal_manager.ask_llm_for_help(user_id, session_id, final_goal)

if __name__ == "__main__":
    main()
