from database.database import DatabaseManager

def insert_user(user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id):
    db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
    db_manager.check_connection()
    cursor = db_manager.conn.cursor()
    cursor.execute("""
        INSERT INTO user_profile (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, user_name, full_name, email, creation_date, gender, age, same_school, grades, user_type_id))
    db_manager.conn.commit()
    cursor.close()

if __name__ == "__main__":
    users = [
        ("kasutaja1", "user1", "Eesnimi1 Perenimi1", "Eesnimi1.Perenimi1@abc.com", "2023-07-26 00:01:00", "M", 12, "jah", 5, 1),
       # ("kasutaja2", "user2", "Eesnimi2 Perenimi2", "Eesnimi2.Perenimi2@def.com", "2023-07-27 12:00:00", "F", 13, "ei", 6, 2),
       # ("kasutaja3", "user3", "Eesnimi3 Perenimi3", "Eesnimi3.Perenimi3@ghj.com", "2023-07-28 23:59:00", "M", 11, "jah", 7, 1)
    ]

    for user in users:
        insert_user(*user)