# goal_manager.py

from datetime import datetime
from api.api_client import APIClient
from database.database import DatabaseManager

class GoalManager:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.api_client = APIClient()

    def ask_user_input(self): # küsi_kasutaja_sisendit
        return input("Sisesta oma eesmärk: ")

    def validate_input(self, user_input): # valideeri_sisend
        return bool(user_input.strip())

    def llm_query(self, goal): #saada_keelemudeli_päring
        response = self.api_client.ask_llm(goal["content"], goal["user_id"])
        return {"status": "OK", "text": response["text"], "is_comprehensible": True}

    def handle_error(self, status): # käsitle_viga
        print(f"Tekkis viga: {status}")

    def ask_if_good(self): #küsi_kas_sobib
        return input("Kas see sobib? (y/n): ").strip().lower() == 'y'

    def ask_if_continue(self): #küsi_kas_jätkata
        return input("Kas soovid jätkata? (y/n): ").strip().lower() == 'y'

    def define_goal(self, user_id, session_id): #sõnasta_eesmärk
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

        for attempt in range(1, 4):
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

            if attempt == 3:
                goal["is_comprehensible"] = llm_response["is_comprehensible"]
            else:
                if self.ask_if_good():
                    goal["is_valid"] = True
                    break

            self.db_manager.save_goal(goal)

            if attempt < 3 and not self.ask_if_continue():
                break

        if goal["is_valid"]:
            return "Eesmärk edukalt sõnastatud"
        elif not goal["is_comprehensible"]:
            return "Eesmärgi sõnastamine ebaõnnestus"
        else:
            return "Eesmärgi sõnastamine lõpetatud, viimane versioon salvestatud"
