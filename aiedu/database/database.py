# database.py

import duckdb
from datetime import datetime

class DatabaseManager:
    def __init__(self, database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db'): # path needs to be specified
        # Initialization for database connection
        self.database_path = database_path
        self.conn = None

    def create_connection(self):
        # Establish a connection to the database
        if not self.conn:
            self.conn = duckdb.connect(database=self.database_path, read_only=False)
        return self.conn

    def initialize_schema(self):
        # Initialize the database schema
        if self.conn:
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
                FOREIGN KEY (user_name) REFERENCES user(user_name)
                );
            """)

            # Create user_type table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user_type (
                    id INT PRIMARY KEY,
                    user_type TEXT UNIQUE NOT NULL,
                    text TEXT
                );
            """)

            # Create user table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INT PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    user_type INT,
                    text TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    llm_model_spec TEXT,
                    origin TEXT NOT NULL,
                    FOREIGN KEY (user_type) REFERENCES user_type(id)
                );
            """)

    def insert_user_type(self, user_type, text):
        # Insert a new user type
        if self.conn:
            self.conn.execute("INSERT INTO user_type (user_type, text) VALUES (?, ?)", (user_type, text))

    def insert_user(self, user_name, user_type_id, text, timestamp, llm_model_spec, origin):
        # Insert a new user entry
        if self.conn:
            self.conn.execute("INSERT INTO user (user_name, user_type, text, timestamp, llm_model_spec, origin) VALUES (?, ?, ?, ?, ?, ?)",
                              (user_name, user_type_id, text, timestamp, llm_model_spec, origin))

    def insert(self):
        if self.conn:
            messages = [
                ('termination_message', 'Enough of talking now, get to work'),
                ('teacher_greeting', 'You are a good teacher'),
                ('mentor_greeting', 'You are a mentor'),
                ('investor_greeting', 'You are an investor')
            ]
            for key, text in messages:
                self.conn.execute("INSERT INTO system_messages (message_key, message_text) VALUES (?, ?)", (key, text))

    
    def log_user_interaction(self, user_name, user_type_id, text, llm_model_spec, origin):
        # Log interactions to the database
        if not self.conn:
            self.create_connection()
            
        timestamp = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO user (user_name, user_type, text, timestamp, llm_model_spec, origin) VALUES (?, ?, ?, ?, ?, ?)",
            (user_name, user_type_id, text, timestamp, llm_model_spec, origin)
        )


    def get_user_inputs(self):
        if self.conn:
            return self.conn.execute("SELECT * FROM user_inputs").fetchall()
    return None

    def close_connection(self):
        # Lclose the database connection
        if self.conn:
            self.conn.close()
            self.conn = None
