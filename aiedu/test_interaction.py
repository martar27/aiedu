from goal_interaction_manager.goal_interaction_manager import InteractionManager
from database.database import DatabaseManager
import uuid

def get_latest_goal(username, interaction_manager):
    cursor = interaction_manager.db_manager.conn.cursor(buffered = True)
    cursor.execute("""
    SELECT content
    FROM goals
    WHERE user_id = %s
    ORDER BY timestamp DESC
    LIMIT 1
    """, (username,))
    result = cursor.fetchone()
    return result[0] if result else None

if __name__ == "__main__":
    db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
    db_manager.create_connection()
    interaction_manager = InteractionManager(db_manager)
    #interaction_manager = InteractionManager()
    #cursor = interaction_manager.db_manager.conn.cursor(buffered = True)
    #cursor.execute("SELECT user_id FROM user_profile WHERE user_id LIKE 'kasutaja%' ORDER BY CAST(SUBSTRING(user_id, 9) AS UNSIGNED) DESC LIMIT 1")
    #result = cursor.fetchone()
    #user_id = result[0] if result else None

    username = input("Sisesta kasutajanimi (kasutaja###): ")

    try:
        latest_goal = get_latest_goal(username, interaction_manager)
        if latest_goal:
            while True:
                print(f"Sinu eesmärk on: {latest_goal}")
                hinne = input(f"Hinda kuidas oled viimase nädalaga liikunud eesmärgi poole skaalal 1 Jehuu!! :)  2 jehuu :| 3 mitte eriti :( : ")
                try: 
                    hinne = int(hinne) 
                    if 1 <= hinne <= 3:
                        break
                    else:
                        print("Palun sisesta hinne vahemikus 1-3")
                except ValueError:
                    print("Palun sisesta number 1, 2 või 3")
            
            session_id = str(uuid.uuid4())
            print(f"Debug TI, funktsioon: __main__, sessioon hinde salvestamiseks, sessiooni ID {session_id} genereeritud")
            interaction_manager.db_manager.create_session(username, session_id)
            print(f"Debug TI, funktsioon: __main__, sessioon hinde salvestamiseks ON AVATUD, sessiooni ID {session_id}")

            cursor = interaction_manager.db_manager.conn.cursor(buffered = True)
            cursor.execute("""
                INSERT INTO marks (session_id, user_id, mark)
                VALUES (%s, %s, %s)
                """, (session_id, username, hinne))
            interaction_manager.db_manager.conn.commit()
            print(f"Debug TI, funktsioon: __main__, sessioon hinde salvestamiseks ja hinne on salvestatud, sessiooni ID {session_id}")
            #print(f"DEBUG salvestatud tabelisse >marks< session_id: {session_id}, user_id: {username}, mark: {hinne}")
            interaction_manager.db_manager.end_session(session_id)
            print(f"Debug TI, funktsioon: __main__, sessioon hinde salvestamiseks on SULETUD, sessiooni ID {session_id}")

            #session_id = str(uuid.uuid4())
            #print(f"Debug TI, funktsioon: __main__, sessioon initiate_dialogue, sessiooni ID {session_id} genereeritud")
            #interaction_manager.db_manager.create_session(username, session_id)
            #print(f"Debug TI, funktsioon: __main__, sessioon initiate_dialogue on AVATUD, sessiooni ID {session_id}")
            interaction_manager.initiate_dialogue(username)   ### SIIN genereeritakse teine uid ja see ei ole sama, mis eelmine uid ehk on kaks erinevat sessiooni ja kaks erinevat uid
            #interaction_manager.db_manager.end_session(session_id)
            #print(f"Debug TI, funktsioon: __main__, sessioon initiate_dialogue on SULETUD, sessiooni ID {session_id}")
        else:
            print(f"Kasutajale {username} ei leitud ühtegi eesmärki.")
    except Exception as e:  
        print(f"Tekkis viga: {e}") 