# cli.py

"""Command Line Interface for interacting with the aiedu application."""
import sys
sys.path.append('../')
from api.api_client import APIClient

def query_llm(): # What exactly is this function doing???
    client = APIClient()
    question = input("Kuidas õpiksin sagedamini kätt tõstma tunnis? Seleta mulle, mida ma peaksin järgmise kahe kuu jooksul tegema selleks, et iga tund kätt tõsta vähemalt ühe korra.")
    response = client.ask_llm(question)
    parsed_response = client.parse_response(response)
    print("LLM vastus:", parsed_response['text'])

def main_cli():
    print("Tere-tere! See on aiedu CLI - küsi LLM-ilt nõu.")
    query_llm()

if __name__ == '__main__':
    main_cli()
