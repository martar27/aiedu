from goals.goal_manager import GoalManager
from database.database import DatabaseManager

def main():
    user_id = 1  # Example user_id
    session_id = "example-session-id"  # Example session_id

    # initialise DatabaseManager with the same parameters as in test_call.py
    db_manager = DatabaseManager(host='localhost', database='mysql_db', user='mysql_admin', password='Mysql#2869')

    goal_manager = GoalManager(db_manager=db_manager)
    
    # Step 1: Define and refine goal
    result = goal_manager.define_goal(user_id, session_id)
    print(result)
    
    # Step 2: Retrieve and display final goal
    final_goal = goal_manager.display_final_goal(user_id, session_id)
    print(final_goal)
    
    # Step 3: Ask LLM for help to achieve the goal
    #if final_goal:
    #    goal_manager.ask_llm_for_help(user_id, session_id, final_goal)

if __name__ == "__main__":
    main()
