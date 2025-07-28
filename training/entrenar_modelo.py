import json
import os
import joblib
import random
import re
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from procesar_datos import cargar_intents
from sklearn.metrics.pairwise import cosine_similarity

def predecir(pregunta, modelo, vectorizador):
    pregunta = limpiar_texto(pregunta)

    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        intents_data = json.load(f)

    #Vectorizar pregunta
    X_pregunta = vectorizador.transform([pregunta])

    mejor_similitud = 0
    mejor_respuesta = None

    for intent in intents_data["intents"]:
        patterns = intent.get("patterns", [])
        if patterns:
            patterns_vect = vectorizador.transform([limpiar_texto(p) for p in patterns])
            similitudes = cosine_similarity(X_pregunta, patterns_vect).flatten()
            max_sim_idx = similitudes.argmax()
            max_sim_val = similitudes[max_sim_idx]

            # Umbral para considerar "suficiente" similitud
            if max_sim_val > mejor_similitud and max_sim_val > 0.5:
                respuestas = intent.get("responses", [])
                if max_sim_idx < len(respuestas):
                    mejor_respuesta = respuestas[max_sim_idx]
                else:
                    mejor_respuesta = random.choice(respuestas) if respuestas else None
                mejor_similitud = max_sim_val

    if mejor_respuesta:
        return mejor_respuesta

    # Si no se encontró respuesta por similitud, usar la predicción del modelo
    X = vectorizador.transform([pregunta])
    prediccion = modelo.predict(X)[0]

    for intent in intents_data["intents"]:
        if intent["tag"] == prediccion:
            return random.choice(intent["responses"])

    return "Lo siento, no entiendo tu pregunta. ¿Puedes reformularla?"

# -------------------------
# CONFIGURACIÓN
# -------------------------
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

MODEL_PATH = "model/modelo_entrenado.pkl"
VECTORIZER_PATH = "model/vectorizador.pkl"
INTENTS_PATH = "data/intents.json"

# -------------------------
# PREPROCESAMIENTO EXTRA
# -------------------------
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\d+", "", texto)   
    return texto.strip()

# -------------------------
# ENTRENAMIENTO DEL MODELO
# -------------------------
def entrenar_modelo(frases, etiquetas):
    # Preprocesamiento adicional
    frases = [limpiar_texto(frase) for frase in frases]

    # División de datos estratificada
    splitter = StratifiedShuffleSplit(n_splits=1000, test_size=config["training"]["test_size"], random_state=config["model"]["random_state"])
    for train_idx, test_idx in splitter.split(frases, etiquetas):
        X_train = [frases[i] for i in train_idx]
        X_test = [frases[i] for i in test_idx]
        y_train = [etiquetas[i] for i in train_idx]
        y_test = [etiquetas[i] for i in test_idx]

    # Vectorización TF-IDF
    vectorizador = TfidfVectorizer(
        ngram_range=tuple(config["vectorizer"]["ngram_range"]),
        max_features=config["vectorizer"]["max_features"],
        sublinear_tf=True
    )


    X_train_vect = vectorizador.fit_transform(X_train)
    X_test_vect = vectorizador.transform(X_test)

    # Modelo
    tipo_modelo = config["model"]["type"]
    if tipo_modelo == "logistic_regression":
        modelo = LogisticRegression(
            max_iter=config["model"]["max_iter"],
            C=1.5,  # control de regularización
            solver='lbfgs',
            random_state=config["model"]["random_state"]
        )
    elif tipo_modelo == "naive_bayes":
        modelo = MultinomialNB()
    else:
        raise ValueError(f"Modelo '{tipo_modelo}' no soportado.")

    modelo.fit(X_train_vect, y_train)

    # Evaluación
    y_pred = modelo.predict(X_test_vect)
    print("Reporte de clasificación:")
    print(classification_report(y_test, y_pred))
    print(f"Precision: {accuracy_score(y_test, y_pred):.2f}")

    return modelo, vectorizador

# -------------------------
# GUARDAR MODELOS
# -------------------------
def guardar_modelo(modelo, vectorizador):
    os.makedirs("model", exist_ok=True)
    joblib.dump(modelo, MODEL_PATH)
    joblib.dump(vectorizador, VECTORIZER_PATH)
    print("Modelo y vectorizador guardados.")

# -------------------------
# RESPUESTA CON MATCH EXACTO
# -------------------------
def predecir(pregunta, modelo, vectorizador):
    pregunta = limpiar_texto(pregunta)

    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        intents_data = json.load(f)

    # Vectorizar pregunta
    X_pregunta = vectorizador.transform([pregunta])

    mejor_similitud = 0
    mejor_respuesta = None

    for intent in intents_data["intents"]:
        patterns = intent.get("patterns", [])
        if patterns:
            patterns_vect = vectorizador.transform([limpiar_texto(p) for p in patterns])
            similitudes = cosine_similarity(X_pregunta, patterns_vect).flatten()
            max_sim_idx = similitudes.argmax()
            max_sim_val = similitudes[max_sim_idx]

            # Umbral para considerar "suficiente" similitud (por ejemplo 0.5)
            if max_sim_val > mejor_similitud and max_sim_val > 0.5:
                respuestas = intent.get("responses", [])
                if max_sim_idx < len(respuestas):
                    mejor_respuesta = respuestas[max_sim_idx]
                else:
                    mejor_respuesta = random.choice(respuestas) if respuestas else None
                mejor_similitud = max_sim_val

    if mejor_respuesta:
        return mejor_respuesta

    # Si no se encontró respuesta por similitud, usar la predicción del modelo
    X = vectorizador.transform([pregunta])
    prediccion = modelo.predict(X)[0]

    for intent in intents_data["intents"]:
        if intent["tag"] == prediccion:
            return random.choice(intent["responses"])

    return "Lo siento, no entiendo tu pregunta. ¿Puedes reformularla?"

# -------------------------
# EJECUCIÓN
# -------------------------
if __name__ == "__main__":
    frases, etiquetas = cargar_intents()
    modelo, vectorizador = entrenar_modelo(frases, etiquetas)
    guardar_modelo(modelo, vectorizador)
