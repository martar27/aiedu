import mysql.connector
from mysql.connector import Error

class InitializeDatabase:
    def __init__(self, host='localhost', database='eduai', user='mysql_admin', password='Mysql#2869'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def initialize_schema(self):
        conn = mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor(buffered=True)
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    grade INT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    goal_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    user_content TEXT NOT NULL,
                    llm_content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    user_content TEXT NOT NULL,
                    llm_content TEXT NOT NULL,                  
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marks (
                    mark_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    mark INT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                )
            """)
            conn.commit()
            print('Andmebaasi skeem on edukalt initsialiseeritud.')
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Viga andmebaasi initsialiseerimisel: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db = InitializeDatabase()
    init_db.initialize_schema()