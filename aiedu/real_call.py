# this is a real api call to LLM for testing purposes


"""
from api.api_client import APIClient

def make_real_llm_call():
    client = APIClient()
    question = "Ma tahaksin järgmise kahe kuu jooksul rohkem kätt tõsta tunnis, aga ei tea, kuidas seda küll saada. Palun anna mulle nõu, mida peaksin tegema, et ma igas tunnis vähemalt ühe korra kätt tõstaksin."
    raw_response = client.ask_llm(question)

    parsed_response = client.parse_response(raw_response)
    print("OPENAI vastus:", parsed_response['text'])

if __name__ == "__main__":
    make_real_llm_call()
    print("Kõik selleks korraks :)")
"""
##########################################
##########################################

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
            question = input("Küsi oma küsimus: ")  # Get question from user
            if not question.strip():  # Check if the input is empty
                print("Empty question detected, ending dialogue.")
                break

            response = api_client.ask_llm(user_id, question)
            if response is None:
                #print("An error occurred while interacting with the OpenAI API.")
                print("!! API VIGA !!")
                break
#            print("Response:", response['text']) #response.choices[0].message['content'])
            print("Response:", response.choices[0].message['content'])

            # After each exchange, check if the user wants to continue
            if not interaction_manager.prompt_continue():
                print("Dialogue ended by user.")
                break
        else:
            print("Maximum number of interactions reached.")
            break

# Start the dialogue
if __name__ == "__main__":
    initiate_dialogue()
