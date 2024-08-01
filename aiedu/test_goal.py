from goal_interaction_manager.goal_interaction_manager import GoalManager
import uuid

if __name__ == "__main__":
    goal_manager = GoalManager()
    username = input("Sisesta kasutajanimi: ")
    cursor = goal_manager.db_manager.conn.cursor(buffered = True)
    cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s", (username,))
    result = cursor.fetchone()
    user_id = result[0] if result else None
    cursor.close()  # Ensure cursor is closed after fetching results

    if user_id:
        session_id = str(uuid.uuid4())
        print(f"Debug: Creating session with ID {session_id} for user {username}")
        goal_manager.db_manager.create_session(user_id, session_id)  # Start session
        try:
            goal_manager.define_goal(user_id, session_id)
            #goal_manager.display_final_goal(user_id, session_id)
        except Exception as e:
            print(f"Tekkis viga: {e}")
        finally:
            print(f"Debug: sulen sessiooni ID-ga {session_id}")
            goal_manager.db_manager.end_session(session_id)
            print(f"Debug: sessioon ID-ga {session_id} on suletud.")
    else:
        print("Andmebaasis pole kasutajat.")