# database.py

import duckdb
from datetime import datetime

class DatabaseManager:
    # Handles database connections and operations for the application.
    # Manages interactions with the database file specified in the database_path.
    def __init__(self, database_path=r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db'): 
    #Initializes the DatabaseManager with a path to the database file.
    #Args: database_path (str): The path to the database file.
        self.database_path = database_path
        self.conn = None

    def create_connection(self):
        #Establishes a connection to the database. If a connection already exists, returns the existing connection.
        #Returns: Connection object to the database.
        if not self.conn:
            self.conn = duckdb.connect(database=self.database_path, read_only=False)
        return self.conn

    def initialize_schema(self):
        # Initializes the database schema by creating necessary tables if they do not already exist.
        # This includes user_profile, user_type, messages, and messages_to_users tables.
        if self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (  # create table "user_profile" where information about concrete user is stored
                user_id INT PRIMARY KEY, # unique identifier of each user
                user_name TEXT NOT NULL, # username of the user
                full_name TEXT, # full name
                email TEXT, # email of the user 
                creation_date TIMESTAMP, # creation of the line i.e. the username in the database
                gender TEXT, #users's gender
                age INT, #user's age
                same_school TEXT, # if the user has brothers, sisters, friends, parents going to or working at the same school; yes if any is true and no if none is true
                grades INT, # average grade - needs further specification
                user_type_id INT,  # column to link to user_type
                FOREIGN KEY (user_type_id) REFERENCES user_type(id)
                );
            """)

            # Create table "user_type" where information about user types is stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user_type (
                    id INT PRIMARY KEY, # a unique identifier for each user type 
                    user_type TEXT UNIQUE NOT NULL, # user type name 
                    text TEXT NOT NULL # user type description
                );
            """)

            # Create table "messages" where all messages are stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT PRIMARY KEY, # unique identifier for each line in the table
                    user_id INT, # to reference the unique user
                    user_name TEXT NOT NULL, # username 
                    user_type INT, # user type 
                    text TEXT, # text, either typed by the user and sent to the LLM or a response from the LLM 
                    timestamp TIMESTAMP NOT NULL, # time when the line was inserted
                    llm_model_spec TEXT, # the type of the LLM that was used 
                    system_message TEXT NOT NULL, # the system message that was part of the message sent to the LLM
                    FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
                );
            """)

            # Create table "messages_to_user" where all messages that are displayed to users are stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages_to_users (
                    id INT PRIMARY KEY, # unique identifier for each line in the table
                    message_key TEXT UNIQUE NOT NULL, # message type 
                    message_text TEXT NOT NULL, # message text
                );
            """) 
   
    def populate_user_types(self): 
        # Populates the user_types with several pre-defined user types that are known to be necessary; uses the insert_user_type function to do that
        # First check if user_types already exist to prevent duplicates
        existing_types = self.conn.execute("SELECT * FROM user_type").fetchall()
        if existing_types:
            return  # Exit if user types are already populated
        user_types = [
            ("pupil_1", "A pupil who only has retrieval access to the database."), 
            ("pupil_2", "A pupil who has read/write access to the database."), 
            ("student", "A student who has read/write access to the database."), 
            ("teacher", "A user who can create educational content."),
            ("admin",  "The G-word goes here")
        ]
        for user_type, text in user_types:
            self.insert_user_type(user_type, text)
                
    #def insert_user_type(self, user_type, text): # inserts a new user type in the user_type table
    #    # Insert a new user type
    #    if self.conn:
    #        self.conn.execute("INSERT INTO user_type (user_type, text) VALUES (?, ?)", (user_type, text))

    def insert_user_type(self, user_type, text):
    #Inserts a new user type into the database.
    #Parameters:
    #user_type (str): The unique identifier for the user type.
    #text (str): A description of the user type.
    #Returns: bool: True if the insertion was successful, False if the user type already exists.
        try:
            existing_type = self.conn.execute("SELECT id FROM user_type WHERE user_type = ?", (user_type,)).fetchone()
            if existing_type is not None:
                return False  # User type already exists
            self.conn.execute("INSERT INTO user_type (user_type, text) VALUES (?, ?)", (user_type, text))
            return True
        except Exception as e:
            print(f"An error occurred while inserting a new user type: {e}")
            return False
   
    def insert_user(self, user_name, full_name, email, creation_date, gender, age, same_school, grades):
        """
        Inserts a new user into the user_profile table.
        Parameters:
        user_name (str): Username of the user.
        full_name (str): Full name of the user.
        email (str): Email of the user.
        other_details (dict): Other relevant user details such as gender, age, etc.
        Returns:
        bool: True if the insertion was successful, else False.
        """
        try:
            self.conn.execute("""
                INSERT INTO user_profile (user_name, full_name, email, creation_date, gender, age, same_school, grades)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?)
            """, ( user_name, full_name, email, creation_date, gender, age, same_school, grades))
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

    
    def log_user_interaction(self, user_name, user_type_id, text, llm_model_spec, origin):
        # Log interactions to the database
        if not self.conn:
            self.create_connection()
            
        timestamp = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO messages (user_name, user_type, text, timestamp, llm_model_spec, system_message) VALUES (?, ?, ?, ?, ?, ?)",
            (user_name, user_type_id, text, timestamp, llm_model_spec, origin)
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
