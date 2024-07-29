from database.database import DatabaseManager

def insert_users():
    db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
    users = [
        ("kasutaja1", "user1", "Eesnimi1 Perenimi1", "Eesnimi1.Perenimi1@abc.com", "2023-07-26 00:01:00", "M", 12, "jah", 5, 1),
        # ("kasutaja2", "user2", "Eesnimi2 Perenimi2", "Eesnimi2.Perenimi2@def.com", "2023-07-27 12:00:00", "F", 13, "ei", 6, 2),
        # ("kasutaja3", "user3", "Eesnimi3 Perenimi3", "Eesnimi3.Perenimi3@ghj.com", "2023-07-28 23:59:00", "M", 11, "jah", 7, 1)
    ] 
    for user in users:
        db_manager.insert_user(*user)

def populate_user_types():
    db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
    db_manager.populate_user_types()

def insert_user_type(user_type_id, user_type):
    db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
    db_manager.insert_user_type(user_type_id, user_type)

if __name__ == "__main__":
    populate_user_types()
    insert_users()