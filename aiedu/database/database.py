import duckdb
from datetime import datetime, timedelta
import threading
import uuid
import time
import os

class DatabaseManager:
    def __init__(self, database_path=None, session_timeout=300, max_users=20, backup_interval=300):
        if database_path is None:
            database_path = r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db'
        self.database_path = database_path
        self.conn = None
        self.active_sessions = {}
        self.session_timeout = session_timeout  # 5 minutes in seconds
        self.max_users = max_users
        self.backup_interval = backup_interval
        self.app_active = False
        self.create_connection()
        self.initialize_schema()

    def create_connection(self):
        if not self.conn:
            self.conn = duckdb.connect(database=self.database_path, read_only=False)
        return self.conn

    def initialize_schema(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_type (
            id INT PRIMARY KEY,
            type TEXT UNIQUE NOT NULL,
            text TEXT NOT NULL
        );
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id INT PRIMARY KEY,
            user_name TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            creation_date TIMESTAMP,
            gender TEXT,
            age INT,
            same_school TEXT,
            grades INT,
            user_type_id INT,
            FOREIGN KEY (user_type_id) REFERENCES user_type(id)
        );
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id VARCHAR(36) PRIMARY KEY,
            user_id INT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            session_token TEXT,
            FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
        );
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id VARCHAR(36) PRIMARY KEY,
            session_id VARCHAR(36),
            user_id INT,
            interaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            interaction_text TEXT,
            llm_response TEXT,
            llm_model_spec TEXT,
            FOREIGN KEY (session_id) REFERENCES user_sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
        );
        """)

    def populate_user_types(self):
        user_types = [
            (1, "pupil_1", "A pupil who only has retrieval access to the database."),
            (2, "pupil_2", "A pupil who has read/write access to the database."),
            (3, "student", "A student who has read/write access to the database."),
            (4, "teacher", "A user who can create educational content."),
            (5, "admin", "The G-word goes here")
        ]
        for id, type, text in user_types:
            self.insert_user_type(id, type, text)

    def insert_user_type(self, id, type, text):
        try:
            existing_type = self.conn.execute("SELECT id FROM user_type WHERE type = ?", (type,)).fetchone()
            if existing_type is not None:
                return False  # User type already exists
            self.conn.execute("INSERT INTO user_type (id, type, text) VALUES (?, ?, ?)", (id, type, text))
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user type: {e}")
            return False

    def insert_user(self, user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id):
        try:
            self.conn.execute("""
                INSERT INTO user_profile (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id))
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user: {e}")
            return False

    def start_application(self):
        self.app_active = True
        threading.Thread(target=self.session_cleanup_thread, daemon=True).start()
        threading.Thread(target=self.periodic_backup, daemon=True).start()

    def stop_application(self):
        self.app_active = False
        self.save_final_state()

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
        self.conn.execute("""
        INSERT INTO user_sessions (session_id, user_id, session_token)
        VALUES (?, ?, ?)
        """, (session_id, user_id, session_token))
        return session_id, session_token

    def end_session(self, session_id):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        self.conn.execute("""
        UPDATE user_sessions
        SET end_time = CURRENT_TIMESTAMP
        WHERE session_id = ?
        """, (session_id,))

    def update_session_activity(self, session_id):
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_activity'] = datetime.now()

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
        backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        try:
            self.conn.execute(f"EXPORT DATABASE '{backup_path}'")
            print(f"Backup created: {backup_path}")
        except Exception as e:
            print(f"Backup failed: {e}")

    def save_final_state(self):
        # Ensure all sessions are closed
        for session_id in list(self.active_sessions.keys()):
            self.end_session(session_id)
        
        # Perform final backup
        backup_path = f"{self.database_path}_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        self.conn.execute(f"EXPORT DATABASE '{backup_path}'")
        print(f"Final database state saved to: {backup_path}")

    def log_interaction(self, session_id, user_id, interaction_text, llm_response, llm_model_spec):
        if session_id not in self.active_sessions:
            return False, "Invalid or expired session"
        
        self.update_session_activity(session_id)
        interaction_id = str(uuid.uuid4())
        self.conn.execute("""
        INSERT INTO interactions (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec))
        return True, "Interaction logged successfully"

    def get_user_type(self, user_id):
        return self.conn.execute("""
        SELECT user_type.text 
        FROM user_profile 
        JOIN user_type ON user_profile.user_type_id = user_type.id 
        WHERE user_profile.user_id = ?
        """, (user_id,)).fetchone()

    def get_user_sessions(self, user_id):
        return self.conn.execute("""
        SELECT * FROM user_sessions
        WHERE user_id = ?
        ORDER BY start_time DESC
        """, (user_id,)).fetchall()

    def get_session_interactions(self, session_id):
        return self.conn.execute("""
        SELECT * FROM interactions
        WHERE session_id = ?
        ORDER BY interaction_time ASC
        """, (session_id,)).fetchall()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close_connection()

# Usage example:
if __name__ == "__main__":
    db_manager = ComprehensiveDatabaseManager()
    db_manager.populate_user_types()
    db_manager.start_application()

    # Simulate user interactions
    user_id = 1
    session_id, token = db_manager.create_session(user_id)
    db_manager.log_interaction(session_id, user_id, "Hello, AI!", "Hello! How can I assist you today?", "GPT-3.5")
    time.sleep(2)
    db_manager.log_interaction(session_id, user_id, "What's the weather like?", "I'm sorry, I don't have real-time weather information. You might want to check a weather website or app for the most up-to-date information.", "GPT-3.5")

    # Simulate application running for a while
    time.sleep(10)

    db_manager.stop_application()
