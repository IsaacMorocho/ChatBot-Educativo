from flask import Flask, render_template, request, jsonify
from joblib import load
import os
import json
import random

app = Flask(__name__)

# Rutas a los archivos del modelo
model_path = os.path.join('model', 'modelo_entrenado.pkl')
vectorizer_path = os.path.join('model', 'vectorizador.pkl')

try:
    # Cargar el modelo y vectorizador con joblib
    model = load(model_path)
    vectorizer = load(vectorizer_path)
    
    # Cargar intents para mostrar información
    with open(os.path.join('data', 'intents.json'), 'r', encoding='utf-8') as f:
        intents_data = json.load(f)
        
except Exception as e:
    print(f"Error al cargar los recursos: {str(e)}")
    raise
@app.route('/random_examples')
def random_examples():
    all_patterns = []
    for intent in intents_data['intents']:
        all_patterns.extend(intent.get('patterns', []))
    
    ejemplos = random.sample(all_patterns, min(5, len(all_patterns)))
    return jsonify({'examples': ejemplos})

@app.route('/')
def home():
    example_intents = [intent['patterns'][0] for intent in intents_data['intents'] if intent['patterns']]
    return render_template('index.html', examples=example_intents[:5])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.json['message']
        print("Pregunta recibida:", user_input)

        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)
        predicted_tag = prediction[0]
        print("Intención predicha:", predicted_tag)

        # Buscar el intent que coincide con la predicción
        intent = next((intent for intent in intents_data['intents'] if intent['tag'] == predicted_tag), None)
        if intent:
            # Vectorizar todos los patterns del intent
            patterns = intent.get('patterns', [])
            if patterns:
                patterns_vectors = vectorizer.transform(patterns)

                # Calcular similitud coseno con la pregunta
                from sklearn.metrics.pairwise import cosine_similarity
                similarities = cosine_similarity(input_vector, patterns_vectors).flatten()

                # Índice del patrón más similar
                best_match_idx = similarities.argmax()

                # Obtener la respuesta correspondiente
                responses = intent.get('responses', [])
                if best_match_idx < len(responses):
                    response = responses[best_match_idx]
                else:
                    # Si no hay respuesta en el mismo índice, escoger una random
                    response = random.choice(responses) if responses else "Lo siento, no tengo una respuesta para eso."
            else:
                response = "Lo siento, no tengo una respuesta para eso."
        else:
            response = "Lo siento, no tengo una respuesta para eso."

        print("Respuesta generada:", response)
        return jsonify({'response': response, 'intent': predicted_tag})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Solo se usa en desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=True)
