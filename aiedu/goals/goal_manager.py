# goal_manager.py

from datetime import datetime
from api.api_client import APIClient
from database.database import DatabaseManager

class GoalManager:
    def __init__(self, db_manager=DatabaseManager):
        self.db_manager = db_manager
        self.api_client = APIClient()

    def ask_user_input(self): # küsi_kasutaja_sisendit
        return input("Kirjuta siia oma eesmärk: ")

    def validate_input(self, user_input): # valideeri_sisend
        return bool(user_input.strip())

    def llm_query(self, goal): #saada_keelemudeli_päring
        response = self.api_client.ask_llm(goal["content"], goal["user_id"])
        #print("Keelemudeli tagasiside: ", response["text"])
        return {"status": "OK", "text": response["text"], "is_comprehensible": True}

    def handle_error(self, status): # käsitle_viga
        print(f"Tekkis viga: {status}")

    def ask_if_good(self): #küsi_kas_sobib
        return input("Kuidas sulle tundub pärast soovituste saamist - kas sinu eesmärk meeldib sulle või tahad seda muuta? \nVajuta klahvi <y> kui see meeldib ja sa ei taha eesmärki muuta. \nVajuta ükskõik millist muud klahvi kui sa tahad eesmärki muuta: ").strip().lower() == 'y'

    def ask_if_continue(self): #küsi_kas_jätkata
        return input("Kas soovid jätkata eesmärgi täpsustamist? Vajuta klahvi <y> kui soovid jätkata ja ükskõik millist muud klahvi kui ei soovi jätkata: ").strip().lower() == 'y'
    
    def display_final_goal(self, user_id, session_id): #kuvage_lõppeesmärk
        final_goal = self.db_manager.get_final_goal(user_id, session_id)
        if final_goal:
            print(f"Sinu eesmärgi sõnastus on siin: {final_goal['content']}")
            return final_goal
        else:
            print("Ei leidnud eesmärki.")
            return None
        
    def define_goal(self, user_id, session_id): #sõnasta_eesmärk
        goal = {
            "user_id": user_id,
            #"user_id": "student",
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

            # Display the current draft goal and feedback
            #print(f"\nEesmärgi praegune versioon (katse {attempt}): {goal['content']}\n")
            print(f"\nPraegune eesmärk: \n{goal['content']}\n")
            print(f"Soovitused selle eesmärgi parandamiseks: \n{goal['feedback']}\n")

            if attempt == 4:
                goal["is_comprehensible"] = llm_response["is_comprehensible"]
            else:
                if self.ask_if_good():
                    goal["is_valid"] = True
                    break

            self.db_manager.save_goal(goal)

            #if attempt < 4 and not self.ask_if_continue():
            #    break

        if goal["is_valid"]:
            print("Eesmärk edukalt sõnastatud")
        elif not goal["is_comprehensible"]:
            print("Eesmärgi sõnastamine ebaõnnestus")
        else:
            print("Eesmärgi sõnastamine lõpetatud, viimane versioon salvestatud")
