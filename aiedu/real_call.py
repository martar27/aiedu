# this is a real api call to LLM for testing purposes

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
