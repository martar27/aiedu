# database.py

import duckdb
from datetime import datetime

class DatabaseManager:
    def __init__(self, database_path='path/to/your/database.db'):
        # Initialization for database connection
        self.database_path = database_path
        self.conn = None

    def create_connection(self):
        # Establish a connection to the database
        if not self.conn:
            self.conn = duckdb.connect(database=self.database_path, read_only=False)
        return self.conn

    def initialize_schema(self):
    # user inputs
    if self.conn:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_inputs (
                user_id INTEGER,
                input_text TEXT,
                is_llm_response BOOLEAN,
                timestamp TIMESTAMP
            )
        """)
        # user profiles
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT,
                user_email TEXT,
                join_date TIMESTAMP
            )
        """)
        # system messages
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS system_messages (
                message_key TEXT PRIMARY KEY,
                message_text TEXT
            )
        """)

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
    
    def log_input_to_database(self, user_id, input_text, is_llm_response=False):
        # Log user inputs or LLM responses to the database
        if not self.conn:
            self.create_connection()
            
        timestamp = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO user_inputs (user_id, input_text, is_llm_response, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, input_text, is_llm_response, timestamp)
        )

    def close_connection(self):
        # Logic to close the database connection
        if self.conn:
            self.conn.close()
            self.conn = None
