from datetime import datetime
#from api.api_client import APIClient
from database.database import DatabaseManager
import mysql.connector

class GoalManager:
    def __init__(self, db_manager=DatabaseManager):
        self.db_manager = db_manager
        #self.api_client = APIClient()

    def ask_user_input(self):
        return input("Kirjuta siia oma eesmärk: ")

    def llm_query(self, goal): #saada_keelemudeli_päring
        #response = self.api_client.ask_llm(goal["user_content"], goal["username"])
        #print("Keelemudeli tagasiside: ", response["text"])
        #return {"text": response["text"]}
        return {"text": "Keelemudeli tagasiside"}

    def ask_if_good(self):
        return input("Kuidas sulle tundub pärast soovituste saamist - \nkas sinu eesmärk meeldib sulle ja sa ei taha seda muuta või \nsee ei meeldi sulle ja sa tahad seda muuta? \nVajuta klahvi <y> kui eesmärk meeldib ja sa ei taha eesmärki muuta. \nVajuta ükskõik millist muud klahvi kui eesmärk ei meeldi ja tahad seda muuta: ").strip().lower() == 'y'
   
    def display_final_goal(self, username): 
        final_goal = self.db_manager.get_final_goal(username)
        if final_goal:
            print(f"Sinu eesmärgi sõnastus on siin: {final_goal['content']}")
            return final_goal
        else:
            print("Ei leidnud eesmärki.")
            return None
        
    def define_goal(self, username): #sõnasta_eesmärk
        goal = {
            "username": username,
            "user_content": None,
            "user_version": None,
            "user_timestamp": None,
            "llm_feedback": None
        }

        for attempt in range(1, 5):
            user_input = self.ask_user_input()

            goal["user_content"] = user_input
            goal["user_version"] = attempt
            goal["user_timestamp"] = datetime.now()

            llm_response = self.llm_query(goal)

            goal["llm_feedback"] = llm_response["text"]

            print(f"debug DG: {goal}")

            # Display the current draft goal and feedback
            #print(f"\nEesmärgi praegune versioon (katse {attempt}): {goal['content']}\n")
            print(f"\nPraegune eesmärk: \n{goal['user_content']}\n")
            print(f"Soovitused selle eesmärgi parandamiseks: \n{goal['llm_feedback']}\n")

            self.db_manager.save_goal(goal)
            
            if attempt == 4:
                print("Eesmärgi sõnastamine lõpetatud, viimane versioon salvestatud")
            else:
                if self.ask_if_good():
                    break

            

            self.display_final_goal(username)

            #if attempt < 4 and not self.ask_if_continue():
            #    break

        #print("Eesmärgi sõnastamine lõpetatud, viimane versioon salvestatud")
