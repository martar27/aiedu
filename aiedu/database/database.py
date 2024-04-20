# database.py

import duckdb
from datetime import datetime

class DatabaseManager:
    # Handles database connections and operations for the application.
    # Manages interactions with the database file specified in the database_path.
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db'
        self.database_path = database_path
        self.conn = None
        self.create_connection()
        self.initialize_schema()
    #Initializes the DatabaseManager with a path to the database file.
    #Args: database_path (str): The path to the database file.
        
    def create_connection(self):
        #Establishes a connection to the database. If a connection already exists, returns the existing connection.
        #Returns: Connection object to the database.
        if not self.conn:
            self.conn = duckdb.connect(database=self.database_path, read_only=False)
        return self.conn

    def initialize_schema(self):
        # Initializes the database schema by creating necessary tables if they do not already exist.
        # This includes user_type, user_profile, messages, and messages_to_users tables.
        if self.conn:
            # First, create the user_type table
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_type (
                id INT PRIMARY KEY, 
                type TEXT UNIQUE NOT NULL, 
                text TEXT NOT NULL 
                );
            """)
    
            # Then, create the user_profile table
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
    
            # Create other tables as needed
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT PRIMARY KEY,
                user_id INT,
                user_name TEXT NOT NULL,
                user_type_id INT,
                text TEXT,
                timestamp TIMESTAMP NOT NULL,
                llm_model_spec TEXT,
                system_message TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                );
            """)
    
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages_to_users (
                id INT PRIMARY KEY,
                message_key TEXT UNIQUE NOT NULL,
                message_text TEXT NOT NULL
                );
            """) 

   
    def populate_user_types(self): 
        # Populates the user_types with several pre-defined user types that are known to be necessary; uses the insert_user_type function to do that
        # First check if user_types already exist to prevent duplicates
        existing_types = self.conn.execute("SELECT * FROM user_type").fetchall()
        if existing_types:
            return  # Exit if user types are already populated
        user_types = [
            (1, "pupil_1", "A pupil who only has retrieval access to the database."), 
            (2, "pupil_2", "A pupil who has read/write access to the database."), 
            (3, "student", "A student who has read/write access to the database."), 
            (4, "teacher", "A user who can create educational content."),
            (5, "admin",  "The G-word goes here")
        ]
        for id, user_type, text in user_types:
            self.insert_user_type(id, user_type, text)
                
    #def insert_user_type(self, user_type, text): # inserts a new user type in the user_type table
    #    # Insert a new user type
    #    if self.conn:
    #        self.conn.execute("INSERT INTO user_type (user_type, text) VALUES (?, ?)", (user_type, text))

    def insert_user_type(self, id, user_type, text):
    #Inserts a new user type into the database.
    #Parameters:
    #user_type (str): The unique identifier for the user type.
    #text (str): A description of the user type.
    #Returns: bool: True if the insertion was successful, False if the user type already exists.
        try:
            existing_type = self.conn.execute("SELECT id FROM user_type WHERE user_type = ?", (user_type,)).fetchone()
            if existing_type is not None:
                return False  # User type already exists
            self.conn.execute("INSERT INTO user_type (id, user_type, text) VALUES (?, ?, ?)", (id, user_type, text))
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user type: {e}")
            return False
   
    def insert_user(self, user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id):
        """
        Inserts a new user into the user_profile table.
        Parameters:
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
        Returns:
        bool: True if the insertion was successful, else False.
        """
        try:
            self.conn.execute("""
                INSERT INTO user_profile (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id))
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user: {e}")
            return False
    
    def populate_messages_to_users(self):
        if self.conn:
            messages = [
                ('termination_message', 'Enough of talking now, get to work'),
                ('message_2', 'You are a good teacher'),
                ('message_3', 'You are a mentor')                
            ]
            for key, text in messages:
                self.conn.execute("INSERT INTO messages_to_users (message_key, message_text) VALUES (?, ?)", (key, text))

    
    def log_user_interaction(self, user_name, user_type_id, text, timestamp, llm_model_spec, system_message):
        # Log interactions to the database
        if not self.conn:
            self.create_connection()
            
        timestamp = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO messages (user_name, user_type_id, text, timestamp, llm_model_spec, system_message) VALUES (?, ?, ?, ?, ?, ?)",
            (user_name, user_type_id, text, timestamp, llm_model_spec, system_message)
        )

    def get_user_inputs(self):
        if self.conn:
            return self.conn.execute("SELECT * FROM user_inputs").fetchall()
    return None

    def get_user_type(self, user_id): 
        # Method to get the user type for a given user_id from the database
        # Implement the SQL query to fetch the user type
        if self.conn:
            return self.conn.execute("SELECT user_type.text FROM user_profile JOIN user_type ON user_profile.user_type_id = user_type.id WHERE user_profile.user_id = ?", (user_id,)).fetchone()
        #pass

    def get_system_message(self, user_type):
        # Method to get the system message based on user type
        # Implement the SQL query to fetch the appropriate system message
        pass

    def close_connection(self):
        # Lclose the database connection
        if self.conn:
            self.conn.close()
            self.conn = None
