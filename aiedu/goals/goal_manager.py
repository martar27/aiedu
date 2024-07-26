# goal_manager.py

from datetime import datetime
from api.api_client import APIClient
from database.database import DatabaseManager
import re

class GoalManager:
    def __init__(self, db_manager=DatabaseManager):
        self.db_manager = db_manager
        self.api_client = APIClient()

    def ask_user_input(self): # küsi_kasutaja_sisendit
        return input("Kirjuta siia oma eesmärk: ")

    def validate_input(self, user_input):
        if len(user_input) < 10 or len(user_input) > 200:
            return False
    
        cleaned_input = user_input.strip().lower()
        
        if len(set(cleaned_input)) < 5:  # Check for unique characters, must be more than 4 unique characters
            return False
    
        word_pattern = re.compile(r'\b\w{2,}\b') # Check for word-like structures
        words = word_pattern.findall(cleaned_input)
        if len(words) < 2:  # Less than 2 word-like structures
            return False
        
        # LLM check for meaningfulness
        if not self.llm_meaningfulness_check(user_input):
            return False
        
        return True

    def llm_meaningfulness_check(self, text):
    # Placeholder for LLM integration
    # This method would use a language model to assess if the text is meaningful
    # It should be tolerant of errors and childlike language
    
    # response = self.llm.analyze(text)
    # return response.is_meaningful
        
        return True

    def llm_query(self, goal): #saada_keelemudeli_päring
        response = self.api_client.ask_llm(goal["content"], goal["user_id"])
        #print("Keelemudeli tagasiside: ", response["text"])
        return {"status": "OK", "text": response["text"], "is_comprehensible": True}

    def handle_error(self, status): 
        print(f"Tekkis viga: {status}")

    def ask_if_good(self): #küsi_kas_sobib
        return input("Kuidas sulle tundub pärast soovituste saamist - \nkas sinu eesmärk meeldib sulle ja sa ei taha seda muuta või \nsee ei meeldi sulle ja sa tahad seda muuta? \nVajuta klahvi <y> kui eesmärk meeldib ja sa ei taha eesmärki muuta. \nVajuta ükskõik millist muud klahvi kui eesmärk ei meeldi ja tahad seda muuta: ").strip().lower() == 'y'

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
