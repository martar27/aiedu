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

