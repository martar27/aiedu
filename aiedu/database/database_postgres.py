import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import threading
import uuid
import time
import os

class DatabaseManager:
    def __init__(self, host='localhost', database='aiedu', user='postgres', password='', session_timeout=300, max_users=20, backup_interval=300):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.active_sessions = {}
        self.session_timeout = session_timeout  # 5 minutes in seconds
        self.max_users = max_users
        self.backup_interval = backup_interval
        self.app_active = False
        self.create_connection()
        self.initialize_schema()

    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def create_connection(self):
        if not self.conn:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                print('Connected to PostgreSQL database')
            except Exception as e:
                print(f"Error: {e}")
                self.conn = None
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_type (
            id SERIAL PRIMARY KEY,
            user_type VARCHAR(50) UNIQUE NOT NULL,
            text TEXT NOT NULL
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(50) NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            creation_date TIMESTAMP,
            gender VARCHAR(10),
            age INT,
            same_school VARCHAR(50),
            grades INT,
            user_type_id INT,
            FOREIGN KEY (user_type_id) REFERENCES user_type(id)
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id UUID PRIMARY KEY,
            user_id INT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            session_token TEXT,
            FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
        );""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id UUID PRIMARY KEY,
            session_id UUID,
            user_id INT,
            interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interaction_text TEXT,
            llm_response TEXT,
            llm_model_spec TEXT,
            FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
        );""")
        self.conn.commit()
        cursor.close()

    def populate_user_types(self):
        cursor = self.conn.cursor()
        user_types = [
            (1, "pupil_1", "A pupil who only has retrieval access to the database."),
            (2, "pupil_2", "A pupil who has read/write access to the database."),
            (3, "student", "A student who has read/write access to the database."),
            (4, "teacher", "A user who can create educational content."),
            (5, "admin", "The G-word goes here")
        ]
        for id, type, text in user_types:
            self.insert_user_type(id, type, text)
        cursor.close()

    def insert_user_type(self, id, user_type, text):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id FROM user_type WHERE user_type = %s", (user_type,))
            existing_type = cursor.fetchone()
            if existing_type is not None:
                return False  # User type already exists
            cursor.execute("INSERT INTO user_type (id, user_type, text) VALUES (%s, %s, %s)", (id, user_type, text))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user type: {e}")
            return False
        finally:
            cursor.close()

    def insert_user(self, user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user_profile (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user: {e}")
            return False
        finally:
            cursor.close()

    def create_session(self, user_id):
        if len(self.active_sessions) >= self.max_users:
            return None, "Maximum number of concurrent users reached"

        session_id = str(uuid.uuid4())
        session_token = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            'user_id': user_id,
            'last_activity': datetime.now(),
            'token': session_token
        }
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO user_sessions (session_id, user_id, session_token)
        VALUES (%s, %s, %s)
        """, (session_id, user_id, session_token))
        self.conn.commit()
        cursor.close()
        return session_id, session_token

    def end_session(self, session_id):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE user_sessions
        SET end_time = CURRENT_TIMESTAMP
        WHERE session_id = %s
        """, (session_id,))
        self.conn.commit()
        cursor.close()

    def update_session_activity(self, session_id):
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = datetime.now()
            cursor = self.conn.cursor()
            cursor.execute("""
            UPDATE user_sessions
            SET start_time = %s
            WHERE session_id = %s
            """, (datetime.now(), session_id))
            self.conn.commit()
            cursor.close()

    def log_interaction(self, session_id, user_id, interaction_text, llm_response, llm_model_spec):
        if session_id not in self.active_sessions:
            return False, "Invalid or expired session"

        self.update_session_activity(session_id)
        interaction_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO interactions (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec))
        self.conn.commit()
        cursor.close()
        return True, "Interaction logged successfully"

    def session_cleanup_thread(self):
        while self.app_active:
            current_time = datetime.now()
            for session_id, session_data in list(self.active_sessions.items()):
                if (current_time - session_data['last_activity']).total_seconds() > self.session_timeout:
                    self.end_session(session_id)
            time.sleep(60)  # Check every minute

    def periodic_backup(self):
        while self.app_active:
            self.backup_database()
            time.sleep(self.backup_interval)

    def backup_database(self):
        backup_dir = os.path.join(os.path.dirname(self.database_path), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
        try:
            backup_command = f"pg_dump -U {self.user} -h {self.host} {self.database} > {backup_path}"
            os.system(backup_command)
            print(f"Backup created: {backup_path}")
        except Exception as e:
            print(f"Backup failed: {e}")

    def save_final_state(self):
        # Ensure all sessions are closed
        for session_id in list(self.active_sessions.keys()):
            self.end_session(session_id)
        
        # Perform final backup
        backup_path = f"{self.database}_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        try:
            backup_command = f"pg_dump -U {self.user} -h {self.host} {self.database} > {backup_path}"
            os.system(backup_command)
            print(f"Final database state saved to: {backup_path}")
        except Exception as e:
            print(f"Final backup failed: {e}")

    def get_user_type(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT user_type.text 
        FROM user_profile 
        JOIN user_type ON user_profile.user_type_id = user_type.id 
        WHERE user_profile.user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_user_sessions(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM user_sessions
        WHERE user_id = %s
        ORDER BY start_time DESC
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_session_interactions(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM interactions
        WHERE session_id = %s
        ORDER BY interaction_time ASC
        """, (session_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def __del__(self):
        self.close_connection()
