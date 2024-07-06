import duckdb

def view_database_contents(database_path):
    conn = duckdb.connect(database=database_path, read_only=True)
    
    print("USER_TYPE Table:")
    user_type_data = conn.execute("SELECT * FROM user_type").fetchall()
    for row in user_type_data:
        print(row)
    
    print("\nUSER_PROFILE Table:")
    user_profile_data = conn.execute("SELECT * FROM user_profile").fetchall()
    for row in user_profile_data:
        print(row)
    
    print("\nUSER_SESSIONS Table:")
    user_sessions_data = conn.execute("SELECT * FROM user_sessions").fetchall()
    for row in user_sessions_data:
        print(row)
    
    print("\nINTERACTIONS Table:")
    interactions_data = conn.execute("SELECT * FROM interactions").fetchall()
    for row in interactions_data:
        print(row)
    
    conn.close()


# Example usage:
if __name__ == "__main__":
    database_path = r'C:\Users\Marti Taru\Documents\GitHub\aiedu\aiedu\database.db'
    view_database_contents(database_path)
