from goals.goal_manager import GoalManager
from database.database import DatabaseManager
import mysql.connector

def main():
    db_manager = DatabaseManager(host='localhost', database='eduai', user='mysql_admin', password='Mysql#2869')
    db_manager.create_connection()
    goal_manager = GoalManager(db_manager)

    username = input("Sisesta kasutajanimi: ")
    
    cursor = db_manager.conn.cursor(buffered = True)
    #cursor.execute("SELECT user_id FROM user_profile WHERE user_id = %s", (username,))
    cursor.execute("SELECT user_id FROM user_profile WHERE username = %s", (username,))
    result = cursor.fetchone()
    user_id = result[0] if result else None
    cursor.close()  # Ensure cursor is closed after fetching results

    if user_id:
        try:
            goal_manager.define_goal(user_id)
            #goal_manager.display_final_goal(user_id, session_id)
        except Exception as e:
            print(f"Tekkis viga: {e}")
    else:
        print("Andmebaasis pole kasutajat.")


if __name__ == "__main__":
    main()