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
            CREATE TABLE IF NOT EXISTS user_profile (  # create table "user_profile" where information about concrete user is stored
                user_id INT PRIMARY KEY, # unique identifier of each user
                user_name TEXT NOT NULL, # username of the user
                full_name TEXT, # full name
                email TEXT, # email of the user 
                creation_date TIMESTAMP, # creation of the line i.e. the username in the database
                gender TEXT, #users's gender
                age INT, #user's age
                same_school TEXT, # if the user has brothers, sisters, friends, parents going to or working in the same school; yes if any is true and no if none is true
                grades INT, # average grade - needs further specification               
                FOREIGN KEY (user_name) REFERENCES user(user_name)
                );
            """)

            # Create table "user_type" where information about user types is stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS user_type (
                    id INT PRIMARY KEY, # a unique identifier for each user type 
                    user_type TEXT UNIQUE NOT NULL, # user type name 
                    text TEXT # user type description
                );
            """)

            # Create table "messages" where all messages are stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT PRIMARY KEY, # unique identifier for each line in the table
                    user_name TEXT NOT NULL, # username 
                    user_type INT, # user type 
                    text TEXT, # text, either typed by the user and sent to the LLM or a response from the LLM 
                    timestamp TIMESTAMP NOT NULL, # time when the line was inserted
                    llm_model_spec TEXT, # the type of the LLM that was used 
                    system_message TEXT NOT NULL, # the system message that was part of the message sent to the LLM
                    FOREIGN KEY (user_type) REFERENCES user_type(id)
                );
            """)

            # Create table "messages_to_user" where all messages that are displayed to users are stored
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages_to_users (
                    id INT PRIMARY KEY, # unique identifier for each line in the table
                    message_type TEXT, # message type 
                    message_text TEXT, # message text
                );
            """) 

# 1. user_profile → user**
# Primary Key (user_profile):** `user_id`
# Foreign Key (user_profile):** `user_name`
# Linkage:** The `user_name` column in the `user_profile` table references the `user_name` column (which is a primary key) in the `user` table. This establishes a relationship where a user_profile record is linked to a specific user.
# 2. user → user_type**
# Primary Key (user_type):** `id`
# Foreign Key (user):** `user_type`
# Linkage:**  The `user_type` column in the `user` table references the `id` column (which is the primary key) in the `user_type` table. This signifies that each user belongs to a specific user type defined in the `user_type` table.
# Key Points**
# Referential Integrity:** These foreign key relationships are essential for maintaining referential integrity within your database. This means ensuring that:
#    * A user profile can't exist without a corresponding user in the `user` table.
#    * A user can't be assigned a `user_type` that doesn't exist in the `user_type` table.
# Data Consistency:** This design helps normalize your database, avoiding data duplication and keeping the data organized and consistent.
    
    def populate_user_types(self): # populates the user_types with several user types that are known to be necessary; uses the insert_user_type function to do that
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
    """
    Inserts a new user type into the database.

    Parameters:
    user_type (str): The unique identifier for the user type.
    text (str): A description of the user type.

    Returns:
    bool: True if the insertion was successful, False if the user type already exists.
    """
    try:
        existing_type = self.conn.execute("SELECT id FROM user_type WHERE user_type = ?", (user_type,)).fetchone()
        if existing_type is not None:
            return False  # User type already exists
        self.conn.execute("INSERT INTO user_type (user_type, text) VALUES (?, ?)", (user_type, text))
        return True
    except Exception as e:
        print(f"An error occurred while inserting a new user type: {e}")
        return False
   
    def insert_user(self, user_name, user_type_id, text, timestamp, llm_model_spec, origin):
        # Insert a new user entry
        if self.conn:
            self.conn.execute("INSERT INTO user (user_name, user_type, text, timestamp, llm_model_spec, origin) VALUES (?, ?, ?, ?, ?, ?)",
                              (user_name, user_type_id, text, timestamp, llm_model_spec, origin))

    def populate_messages_to_users(self):
        if self.conn:
            messages = [
                ('termination_message', 'Enough of talking now, get to work'),
                ('teacher_greeting', 'You are a good teacher'),
                ('mentor_greeting', 'You are a mentor'),
                ('investor_greeting', 'You are an investor')
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
            return self.conn.execute("SELECT user_type.text FROM user JOIN user_type ON user.user_type = user_type.id WHERE user.id = ?", (user_id,)).fetchone()
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
