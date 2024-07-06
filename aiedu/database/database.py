# MySQL
# Claude

import mysql.connector # MySQL connector to connect functions in different modules to MySQL database
from mysql.connector import Error # Error handling for MySQL
from datetime import datetime, timedelta # datetime for timestamping and timedelta for session timeout
import threading # threading for session cleanup and periodic backup. Thread is a separate flow of execution of a program
import uuid # universally unique identifier for session_id to ensure uniqueness for each session and interaction
import time # time for sleep function
import os # os for creating directories and paths
import subprocess # subprocess for running mysqldump command to create backups
from typing import List, Tuple, Optional # typing for type hints in functions, that is, to specify the type of arguments and return values in functions and classes making the code more readable and maintainable

class DatabaseManager: # DatabaseManager class to manage the MySQL database engine and the tables in the database. it contains all the necessary functions to interact with the database as well as database schema and initialization
    
    ## Initialization and Connection Management ##

    def __init__(self, host: str = 'localhost', database: str = 'mysql_db', user: str = 'root', password: str = '', 
                 session_timeout: int = 300, max_users: int = 20, backup_interval: int = 300): # __init__ method to initialize the DatabaseManager class with default values for host, database, user, password, session_timeout, max_users, and backup_interval
        self.host = host # host to connect to the MySQL database
        self.database = database # database name to connect to the MySQL database
        self.user = user
        self.password = password
        self.conn = None
        self.active_sessions = {} # active_sessions dictionary to store the active sessions with session_id as key and session data as value
        self.session_timeout = session_timeout
        self.max_users = max_users
        self.backup_interval = backup_interval
        self.app_active = False # app_active flag to indicate whether the application is active or not
        self.lock = threading.Lock() # created a new lock object to ensure the safety of each thread for active_sessions dictionary
        self.create_connection() # created a connection to the MySQL database
        self.initialize_schema() # initialized the schema of the MySQL database

    def __enter__(self): # __enter__ method to enter the context manager and return the instance of the DatabaseManager class. It is used to initialize the DatabaseManager class with the context manager
        return self

    def __exit__(self, exc_type, exc_value, traceback): # __exit__ method to exit the context manager and close the connection to the MySQL database. It is used to close the connection to the MySQL database when exiting the context manager
        self.shutdown()

    def create_connection(self) -> None: # create_connection method to create a connection to the MySQL database using the host, database, user, and password provided
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(f"Error: {e}")
            self.conn = None

    def check_connection(self) -> None: # check_connection method to check if the connection to the MySQL database is active and reconnect if necessary. It is used to ensure that the connection to the MySQL database is active before executing any queries
        if not self.conn or not self.conn.is_connected():
            self.create_connection()

    def close_connection(self) -> None: # close_connection method to close the connection to the MySQL database. It is used to close the connection to the MySQL database when the application is shut down
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_schema(self) -> None: # initialize_schema method to initialize the schema of the MySQL database with the required tables, columns, and relationships between the tables. It is used to create the necessary tables in the MySQL database if they do not exist
        self.check_connection() # first thing to do is to check the connection to the MySQL database; if not, then create a new connection
        cursor = self.conn.cursor() # create a cursor object to execute queries on the MySQL database
        try: # try block to execute the queries to create the tables in the MySQL database
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_type (
                id INT PRIMARY KEY,
                user_type VARCHAR(50) UNIQUE NOT NULL,
                text TEXT NOT NULL
            );""")
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id INT PRIMARY KEY,
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
                session_id VARCHAR(36) PRIMARY KEY,
                user_id INT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                session_token TEXT,
                FOREIGN KEY (user_id) REFERENCES user_profile(user_id)
            );""")
            
            cursor.execute("""
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
            );""")
            self.conn.commit() # commit the changes to the MySQL database i.e. save the changes
        except Error as e: # except block to handle any errors that occur during the execution of the queries
            print(f"An error occurred while initializing schema: {e}") 
            self.conn.rollback() # rollback the changes if an error occurs i.e. undo the changes which in the case of this function is creating the tables i.e. the tables are not created
        finally: # finally block to close the cursor after executing the queries
            cursor.close() # close the cursor object i.e. release the resources and memory used by the cursor, deleting the cursor object

## User and Session Management ##

    def populate_user_types(self) -> None: # populate the user_type table with predefined user types. It is used to insert predefined user types into the user_type table in the MySQL database
        user_types = [
            (1, "pupil_1", "A pupil who only has retrieval access to the database."),
            (2, "pupil_2", "A pupil who has read/write access to the database."),
            (3, "student", "A student who has read/write access to the database."),
            (4, "teacher", "A user who can create educational content."),
            (5, "admin", "The G-word goes here")
        ]
        for id, type, text in user_types:
            self.insert_user_type(id, type, text) # insert the predefined user types into the user_type table in the MySQL database

    def insert_user_type(self, id: int, user_type: str, text: str) -> bool: # insert a new user type into the user_type table. It is used to insert a new user type into the user_type table in the MySQL database
        self.check_connection() # first thing to do is to check the connection to the MySQL database; if not, then create a new connection
        cursor = self.conn.cursor() # create a cursor object to execute queries on the MySQL database
        try:
            cursor.execute("SELECT id FROM user_type WHERE user_type = %s", (user_type,)) # execute a query to check if the user type already exists in the user_type table
            existing_type = cursor.fetchone() # fetch the result of the query
            if existing_type is not None: # if the user type already exists, return False
                return False  # User type already exists
            cursor.execute("INSERT INTO user_type (id, user_type, text) VALUES (%s, %s, %s)", (id, user_type, text)) # if the user type does not exist already, insert the new user type into the user_type table
            self.conn.commit() # commit the changes to the MySQL database i.e. save the changes
            return True # return True if the user type is successfully inserted
        except Error as e: # except block to handle any errors that occur during the execution of the queries
            print(f"An error occurred while inserting a new user type: {e}")
            self.conn.rollback() # rollback the changes if an error occurs i.e. undo the changes which in the case of this function is inserting the new user type
            return False
        finally:
            cursor.close() # close the cursor object i.e. release the resources and memory used by the cursor, deleting the cursor object

    def insert_user(self, user_id: int, user_name: str, full_name: str, email: str, creation_date: datetime, # insert a new user into the user_profile table. It is used to insert a new user into the user_profile table in the MySQL database
                    gender: str, age: int, same_school: str, grades: int, user_type_id: int) -> bool:
        self.check_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user_profile (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id))
            self.conn.commit()
            return True
        except Error as e:
            print(f"An error occurred while inserting a new user: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def create_session(self, user_id: int) -> Tuple[Optional[str], str]: # create a new session for a user. It is used to create a new session for a user in the user_sessions table in the MySQL database. Tuple... means that the function returns a tuple with the first element being an optional string and the second element being a string
        with self.lock: # lock the active_sessions dictionary to ensure thread safety by creating a lock object 
            if len(self.active_sessions) >= self.max_users: # check if the maximum number of concurrent users has been reached
                return None, "Maximum number of concurrent users reached"

            session_id = str(uuid.uuid4()) # generate a unique session_id using the uuid module
            session_token = str(uuid.uuid4()) # generate a unique session_token using the uuid module
            self.check_connection() # check the connection to the MySQL database; if not, then create a new connection
            cursor = self.conn.cursor() # create a cursor object to execute queries on the MySQL database
            try:
                cursor.execute("""
                INSERT INTO user_sessions (session_id, user_id, session_token)
                VALUES (%s, %s, %s)
                """, (session_id, user_id, session_token))
                self.conn.commit()
                self.active_sessions[session_id] = {
                    'user_id': user_id,
                    'last_activity': datetime.now(), # timestamp of the start time of the session
                    'token': session_token
                }
                return session_id, session_token
            except Error as e:
                print(f"An error occurred while creating a session: {e}")
                self.conn.rollback()
                return None, "Failed to create session"
            finally:
                cursor.close()

    def end_session(self, session_id: str) -> None:
        with self.lock:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            self.check_connection()
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                UPDATE user_sessions
                SET end_time = CURRENT_TIMESTAMP
                WHERE session_id = %s
                """, (session_id,))
                self.conn.commit()
            except Error as e:
                print(f"An error occurred while ending a session: {e}")
                self.conn.rollback()
            finally:
                cursor.close()

    def logout_user(self, session_id: str) -> bool:
        with self.lock:
            if session_id in self.active_sessions:
                self.end_session(session_id)
                return True
            return False

    def update_session_activity(self, session_id: str) -> None: # update the last activity timestamp of a session. It is used to update the last activity timestamp of a session in the active_sessions dictionary
        with self.lock:
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['last_activity'] = datetime.now()
                self.check_connection()
                cursor = self.conn.cursor()
                try:
                    cursor.execute("""
                    UPDATE user_sessions
                    SET start_time = %s
                    WHERE session_id = %s
                    """, (datetime.now(), session_id))
                    self.conn.commit()
                except Error as e:
                    print(f"An error occurred while updating session activity: {e}")
                    self.conn.rollback()
                finally:
                    cursor.close()

    def log_interaction(self, session_id: str, user_id: int, interaction_text: str, llm_response: str, llm_model_spec: str) -> Tuple[bool, str]:
        if session_id not in self.active_sessions:
            return False, "Invalid or expired session"

        self.update_session_activity(session_id)
        interaction_id = str(uuid.uuid4())
        self.check_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO interactions (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (interaction_id, session_id, user_id, interaction_text, llm_response, llm_model_spec))
            self.conn.commit()
            return True, "Interaction logged successfully"
        except Error as e:
            print(f"An error occurred while logging interaction: {e}")
            self.conn.rollback()
            return False, "Failed to log interaction"
        finally:
            cursor.close()

## Utility Functions ##

    def session_cleanup_thread(self) -> None: # to periodically check and end inactive sessions. It is used to periodically check the active sessions and end the inactive sessions based on the session timeout
        while self.app_active:
            current_time = datetime.now()
            with self.lock:
                for session_id, session_data in list(self.active_sessions.items()):
                    if (current_time - session_data['last_activity']).total_seconds() > self.session_timeout:
                        self.end_session(session_id)
            time.sleep(60)  # Check every minute

    def periodic_backup(self) -> None:
        while self.app_active:
            self.backup_database()
            time.sleep(self.backup_interval)

    def backup_database(self) -> None:
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
        try:
            subprocess.run([
                "mysqldump",
                f"-u{self.user}",
                f"-p{self.password}",
                self.database
            ], stdout=open(backup_path, 'w'), check=True)
            print(f"Backup created: {backup_path}")
        except subprocess.CalledProcessError as e:
            print(f"Backup failed: {e}")

    def save_final_state(self) -> None:
        with self.lock:
            for session_id in list(self.active_sessions.keys()):
                self.end_session(session_id)
        
        backup_path = f"{self.database}_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        try:
            subprocess.run([
                "mysqldump",
                f"-u{self.user}",
                f"-p{self.password}",
                self.database
            ], stdout=open(backup_path, 'w'), check=True)
            print(f"Final database state saved to: {backup_path}")
        except subprocess.CalledProcessError as e:
            print(f"Final backup failed: {e}")

    def get_user_type(self, user_id: int) -> Optional[str]:
        self.check_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT user_type.text 
            FROM user_profile 
            JOIN user_type ON user_profile.user_type_id = user_type.id 
            WHERE user_profile.user_id = %s
            """, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"An error occurred while getting user type: {e}")
            return None
        finally:
            cursor.close()

    def get_user_sessions(self, user_id: int) -> List[Tuple]:
        self.check_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM user_sessions
            WHERE user_id = %s
            ORDER BY start_time DESC
            """, (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"An error occurred while getting user sessions: {e}")
            return []
        finally:
            cursor.close()

    def get_session_interactions(self, session_id: str) -> List[Tuple]:
        self.check_connection()
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT * FROM interactions
            WHERE session_id = %s
            ORDER BY interaction_time ASC
            """, (session_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"An error occurred while getting session interactions: {e}")
            return []
        finally:
            cursor.close()

## Application Lifecycle Management ##

    def start(self) -> None:
        self.app_active = True
        threading.Thread(target=self.session_cleanup_thread, daemon=True).start()
        threading.Thread(target=self.periodic_backup, daemon=True).start()

#    def shutdown(self) -> None:
#        self.app_active = False
#        self.save_final_state()
#        self.close_connection()

    def shutdown(self) -> None:
        self.app_active = False
        
        # Ensure all sessions are ended properly
        with self.lock:
            for session_id in list(self.active_sessions.keys()):
                self.end_session(session_id)
        
        # Create final backup
        self.save_final_state()
        
        # Close the database connection
        self.close_connection()