import mysql.connector
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, host='localhost', database='eduai4', user='mysql_admin', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.create_connection()

    def create_connection(self):
        if not self.conn or not self.conn.is_connected():
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conn.is_connected():
                print('On ühendus MySQL-ga')

    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def insert_user(self, username: str, grade: int) -> Tuple[bool, str]:
        self.create_connection()
        cursor = self.conn.cursor(buffered=True)
        try:
            cursor.execute("""
                INSERT INTO user_profile (username, grade)
                VALUES (%s, %s)
            """, (username, grade))
            self.conn.commit()
            return True, "Kasutaja lisamine õnnestus"
        except mysql.connector.Error as e:
            self.conn.rollback()
            return False, f"Kasutaja lisamisel tekkis viga: {e}"
        finally:
            cursor.close()

    def get_final_goal(self, username: int) -> dict:
        self.create_connection()
        cursor = self.conn.cursor(buffered=True)
        cursor.execute("""
            SELECT user_content
            FROM goals
            WHERE username = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """, (username,))
        goal = cursor.fetchone()
        cursor.close()
        return goal

    def save_goal(self, goal: dict) -> Tuple[bool, str]:
        self.create_connection()
        print(f"Debug DB: goal = {goal}")
        cursor = self.conn.cursor(buffered=True)
        try:
            cursor.execute("""
                INSERT INTO goals (username, user_content, llm_content, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (goal["username"], goal["user_content"], goal["llm_feedback"], goal["user_timestamp"]))
            self.conn.commit()
            return True, "Eesmärk on salvestatud"
        except mysql.connector.Error as e:
            self.conn.rollback()
            return False, f"Eesmärgi salvestamisel tekkis viga: {e}"
        finally:
            cursor.close()

#if __name__ == "__main__":
#    db_manager = DatabaseManager()
