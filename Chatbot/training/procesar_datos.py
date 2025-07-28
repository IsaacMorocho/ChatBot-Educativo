import json

def cargar_intents():
    with open("data/intents.json", "r", encoding="utf-8") as f:
        intents = json.load(f)
    frases = []
    etiquetas = []
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            frases.append(pattern)
            etiquetas.append(intent["tag"])
    return frases, etiquetas
    
# Si quieres hacer pruebas rápidas
if __name__ == "__main__":
    X, y = cargar_intents()
    print(f"Total frases: {len(X)}")
    print(f"Etiquetas únicas: {set(y)}")

