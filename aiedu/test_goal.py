from goal_interaction_manager.goal_interaction_manager import GoalManager
import uuid

if __name__ == "__main__":
    goal_manager = GoalManager()
    username = input("Sisesta kasutajanimi: ")
    cursor = goal_manager.db_manager.conn.cursor()
    cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s", (username,))
    result = cursor.fetchone()
    user_id = result[0] if result else None

    if user_id:
        session_id = str(uuid.uuid4())
        goal_manager.define_goal(user_id, session_id)
        goal_manager.display_final_goal(user_id, session_id)
    else:
        print("Andmebaasis pole kasutajat.")