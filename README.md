# aiedu
AIEdu
## Database Schema Update
The database schema within `database.py` has been updated to support a more structured and analytical approach to handling user interactions with the LLM. Here's a brief overview of the changes:

### Tables:
1. **User_Type Table:**
   - `id`: A unique identifier for each user type.
   - `user_type`: The type of user (e.g., student, professional).
   - `text`: Specific information or messages related to the user type.

2. **User Table:**
   - `id`: A unique identifier for each user entry.
   - `user_name`: The name or identifier of the user.
   - `user_type`: References the `id` in the User_Type table, indicating the user's type.
   - `text`: The message or information associated with the user.
   - `timestamp`: When the data was inserted or updated.
   - `llm_model_spec`: Specifies the LLM model used for generating the response.
   - `origin`: Indicates the origin of the entry (LLM, user, or system administrator).

### Functionality:
- The database now includes functionality to insert and retrieve data from these tables, allowing for detailed examination and analysis of the interactions based on user type and user name.
- This update aims to enhance the system's ability to send user_type and user_name specific calls to the LLM and to analyze the message-specific responses received.

<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>

To integrate `api_client.py` with `database.py`, follow these steps:

1. **Import DatabaseManager in APIClient:**
   Start by importing the `DatabaseManager` class in `api_client.py` so that you can create and use an instance of it within the `APIClient` class.

2. **Initialize Database Connection:**
   Modify the constructor of the `APIClient` class to accept a `DatabaseManager` instance and use it to establish a connection to the database.

3. **Implement Data Retrieval and Storage:**
   Identify the points within `APIClient` where it needs to retrieve data from the database (e.g., system messages) and where it should store data (e.g., API responses).

4. **Modify the Methods to Use DatabaseManager:**
   Within the methods of `APIClient` that require database interaction, call the appropriate methods of the `DatabaseManager` instance.

Here is an example of how you might refactor the `APIClient` class to integrate with `database.py`:

```python
# api_client.py
import os
import openai
from database.database import DatabaseManager  # Import the DatabaseManager class

class APIClient:
    def __init__(self, db_manager: DatabaseManager):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.db_manager = db_manager  # DatabaseManager instance

    def ask_llm(self, question, user_id='kasutaja1'):
        user_type = self.db_manager.get_user_type(user_id)  # Retrieve user type from database
        messages = self.form_message(question, user_type=user_type)
        # ... existing code to call API ...

    def form_message(self, question, user_type="student"):
        # Instead of hard-coding, retrieve system messages from the database
        system_message = self.db_manager.get_system_message(user_type)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        return messages

    # ... other methods ...

# Example usage
db_manager = DatabaseManager()  # Create a DatabaseManager instance
api_client = APIClient(db_manager)  # Pass the DatabaseManager instance to APIClient
```

In `database.py`, you would define the `get_user_type` and `get_system_message` methods if they do not already exist. These methods would contain the SQL queries to fetch the necessary data from the database tables:

```python
# database.py
# ... other methods ...

class DatabaseManager:
    # ... existing methods ...

    def get_user_type(self, user_id):
        # Method to get the user type for a given user_id from the database
        # Implement the SQL query to fetch the user type
        pass

    def get_system_message(self, user_type):
        # Method to get the system message based on user type
        # Implement the SQL query to fetch the appropriate system message
        pass
```

This integration approach keeps the `APIClient` class responsible for handling API interactions, while `DatabaseManager` is solely responsible for direct database interactions, maintaining separation of concerns and making your codebase more maintainable and testable.
