from datetime import datetime
from api.api_client import APIClient
from database.database import DatabaseManager
import re
import uuid

class GoalManager:
    def __init__(self):
        self.db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
        self.api_client = APIClient()

    def ask_user_input(self):
        return input("Kirjuta siia oma eesmärk: ")

    def validate_input(self, user_input):
        if len(user_input) < 10 or len(user_input) > 200:
            return False

        cleaned_input = user_input.strip().lower()

        if len(set(cleaned_input)) < 5:
            return False

        word_pattern = re.compile(r'\b\w{2,}\b')
        words = word_pattern.findall(cleaned_input)
        if len(words) < 2:
            return False

        if not self.llm_meaningfulness_check(user_input):
            return False

        return True

    def llm_meaningfulness_check(self, text):
        return True

    def llm_query(self, goal):
        response = self.api_client.ask_llm(goal["content"], goal["user_id"])
        return {"status": "OK", "text": response["text"], "is_comprehensible": True}

    def handle_error(self, status):
        print(f"Tekkis viga: {status}")

    def ask_if_good(self):
        return input("Kuidas sulle tundub pärast soovituste saamist - \nkas sinu eesmärk meeldib sulle ja sa ei taha seda muuta või \nsee ei meeldi sulle ja sa tahad seda muuta? \nVajuta klahvi <y> kui eesmärk meeldib ja sa ei taha eesmärki muuta. \nVajuta ükskõik millist muud klahvi kui eesmärk ei meeldi ja tahad seda muuta: ").strip().lower() == 'y'

    def ask_if_continue(self):
        return input("Kas soovid jätkata eesmärgi täpsustamist? Vajuta klahvi <y> kui soovid jätkata ja ükskõik millist muud klahvi kui ei soovi jätkata: ").strip().lower() == 'y'

    def display_final_goal(self, user_id, session_id):
        final_goal = self.db_manager.get_final_goal(user_id, session_id)
        if final_goal:
            print(f"Sinu eesmärgi sõnastus on siin: {final_goal['content']}")
            return final_goal
        else:
            print("Ei leidnud eesmärki.")
            return None

    def define_goal(self, user_id, session_id):
        goal = {
            "user_id": user_id,
            "session_id": session_id,
            "content": None,
            "version": None,
            "timestamp": None,
            "feedback": None,
            "is_comprehensible": False,
            "is_valid": False
        }

        for attempt in range(1, 5):
            user_input = self.ask_user_input()
            if not self.validate_input(user_input):
                continue

            goal["content"] = user_input
            goal["version"] = attempt
            goal["timestamp"] = datetime.now()

            llm_response = self.llm_query(goal)
            if llm_response["status"] != "OK":
                self.handle_error(llm_response["status"])
                continue

            goal["feedback"] = llm_response["text"]

            print(f"\nPraegune eesmärk: \n{goal['content']}\n")
            print(f"Soovitused selle eesmärgi parandamiseks: \n{goal['feedback']}\n")

            if attempt == 4:
                goal["is_comprehensible"] = llm_response["is_comprehensible"]
            else:
                if self.ask_if_good():
                    goal["is_valid"] = True
                    break

            self.db_manager.save_goal(goal)

        if goal["is_valid"]:
            print("Eesmärk edukalt sõnastatud")
        elif not goal["is_comprehensible"]:
            print("Eesmärgi sõnastamine ebaõnnestus")
        else:
            print("Eesmärgi sõnastamine lõpetatud, viimane versioon salvestatud")

class InteractionManager:
    def __init__(self):
        self.db_manager = DatabaseManager(host='localhost', database='eduai4', user='mysql_admin', password='Mysql#2869')
        self.api_client = APIClient()
        self.interaction_counts = {}
        self.interaction_threshold = 3

    def log_interaction(self, user_id):
        self.interaction_counts[user_id] = self.interaction_counts.get(user_id, 0) + 1

    def get_interaction_count(self, user_id):
        return self.interaction_counts.get(user_id, 0)

    def check_interaction_allowed(self, user_id):
        return self.interaction_counts.get(user_id, 0) < self.interaction_threshold

    def prompt_continue(self):
        response = input("\nVajuta < y > kui soovid jätkata või ükskõik millist muud klahvi kui soovid lõpetada:\n")
        return response.strip().lower() == 'y'

    def initiate_dialogue(self, user_id):
        session_id, session_token = self.db_manager.create_session(user_id)
        for _ in range(self.interaction_threshold):
            if self.check_interaction_allowed(user_id):
                question = input("\nKirjuta siia kuidas su eesmärgi täitmine läks eelmisel nädalal: ")
                if not question.strip():
                    print("Sa ei öelnud midagi... siis ongi side lõpp.")
                    break

                response = self.api_client.ask_llm(question, user_id)
                if response is None:
                    print("!! API VIGA !!")
                    break

                print("\nSiin on arvamus ja soovitused mida sa võiksid teha järgmisel nädalal, et oma eesmärki saavutada:\n", response['text'])

                try:
                    self.db_manager.log_interaction(session_id, user_id, question, response['text'], "GPT3.5")
                except TypeError as e:
                    print(f"Viga API suhtluses: {e}")
                    break

                self.log_interaction(user_id)
                count = self.get_interaction_count(user_id)
                print(f"\nSee on sinu {count}. küsimus selles sessioonis.")
                if count == self.interaction_threshold:
                    print("\nJa see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)\n")
                    break

                if not self.prompt_continue():
                    print("\nKasutaja lõpetas dialoogi.\n")
                    break

        self.db_manager.end_session(session_id)
        print("\nSessioon on lõppenud. Aitäh kasutamast!\n")

    def assess_goal_progress(self, user_id):
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
        SELECT content
        FROM goals
        WHERE user_id = %s
        ORDER BY timestamp DESC
        LIMIT 1
        """, (user_id,))
        result = cursor.fetchone()
        goal = result[0] if result else None

        if goal:
            while True:
                print(f"Sinu eesmärk on: {goal}")
                score = input("Hinda kuidas oled viimase nädalaga liikunud eesmärgi poole skaalal 1 Jehuu!! :)  2 jehuu :| 3 mitte eriti :(")
                try:
                    score = int(score)
                    if 1 <= score <= 3:
                        break
                    else:
                        print("Palun sisesta hinne vahemikus 1-3")
                except ValueError:
                    print("Palun sisesta number 1, 2 või 3")
            cursor.execute("""
                INSERT INTO marks (session_id, user_id, mark)
                VALUES (%s, %s, %s)
            """, (uuid.uuid4(), user_id, score))
            self.initiate_dialogue(user_id)
        else:
            print(f"Kasutajale {user_id} ei leitud ühtegi eesmärki.")

if __name__ == "__main__":
    interaction_manager = InteractionManager()
    user_id = input("Sisesta kasutajanimi (kasutaja###): ")
    interaction_manager.assess_goal_progress(user_id)
    interaction_manager.initiate_dialogue(user_id)