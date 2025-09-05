import requests

API_URL = "http://127.0.0.1:8000/ask/"

def ask_question(question: str):
    response = requests.post(API_URL, params={"question": question})
    if response.status_code == 200:
        data = response.json()
        print(f"❓ Domanda: {data['question']}")
        print(f"💡 Risposta: {data['answer']}")
    else:
        print("Errore:", response.status_code, response.text)

if __name__ == "__main__":
    # Esempio di test
    ask_question("Riassumi il documento in 3 punti chiave")
