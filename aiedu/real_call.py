# this is an api call to LLM for testing purposes

from api.api_client import APIClient
from interaction.interaction_tracker import InteractionManager

interaction_manager = InteractionManager()
api_client = APIClient()

# Hardcoded user ID for testing
user_id = "kasutaja1"

def initiate_dialogue():
    for _ in range(3):  # Loop for up to 3 exchanges
        if interaction_manager.check_interaction_allowed(user_id):
            #question = input("Ask your question: ")  # Get question from user
            question = input("\nKüsi küsimus tehisarult: ")  # Get question from user
            if not question.strip():  # Check if the input is empty
                print("Sa ei küsinud ju midagi... side lõpp.")
                break

            response = api_client.ask_llm(question, user_id)
            if response is None:
                #print("An error occurred while interacting with the OpenAI API.")
                print("!! API VIGA !!")
                break
#            print("Response:", response['text']) #response.choices[0].message['content'])
            print("\n\nSiin on tehisaru arvamus:\n\n",response.choices[0].message['content'])

            interaction_manager.log_interaction(user_id)

            count = interaction_manager.get_interaction_count(user_id)
            print(f"\nSee on sinu {count}. küsimus selles sessioonis.")
            if count == interaction_manager.interaction_threshold: # uus omistamine ja võrdlemine
                print("\nJa see oligi sinu selle sessiooni viimane küsimus! Hakka nüüd tegutsema :)\n")
                break

            # After each exchange, check if the user wants to continue
            if not interaction_manager.prompt_continue():
                print("\nKasutaja lõpetas dialoogi.\n")
                break

        else: # igaks juhuks
            break

# Start the dialogue
if __name__ == "__main__":
    initiate_dialogue()
