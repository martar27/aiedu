from database.database import DatabaseManager

def insert_users():
    db_manager = DatabaseManager(host='localhost', database='eduai', user='mysql_admin', password='Mysql#2869')
    db_manager.create_connection()
    users = [
        ("kasutaja4", 4),
        ("kasutaja5", 5),
        ("kasutaja6", 6)
    ] 
    for user in users:
        success, message = db_manager.insert_user(user[0], user[1])
        print(message)
    
    db_manager.close_connection()


if __name__ == "__main__":
    insert_users()