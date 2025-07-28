# Proyecto Final - Fundamentos de inteligencia Artificial

Para este proyecto se escogio el tema de un ChatBot educativo enfocado al tema de los primeros auxilios.

## ChatBot Educativo - Primeros Auxilios

Este proyecto consiste en el desarrollo de un **chatbot educativo con inteligencia artificial** especializado en brindar asistencia básica sobre **primeros auxilios**. Está diseñado para ofrecer información clara, rápida y accesible ante situaciones de emergencia comunes, como quemaduras, fracturas, entre otros.

## Características

- Entrenamiento con datos personalizados sobre primeros auxilios.
- Identificación de intenciones usando modelos de Machine Learning.
- Respuestas automáticas y comprensibles para situaciones críticas.
- Interfaz web simple desarrollada con Flask.
- Modelo exportado con `joblib` para facilitar el despliegue.
- Preparado para desplegarse en plataformas como Render o Heroku.

## Temáticas abordadas

El chatbot responde preguntas sobre:

- 🔥 Quemaduras
- 🦴 Fracturas
- 🚑 Reanimación cardiopulmonar (RCP)
- 😵‍💫 Desmayos
- Y otras situaciones de primeros auxilios

## Estructura del proyecto
ChatBot-Educativo/

├── app.py # Servidor principal con Flask

├── model/

│ ├── modelo_entrenado.pkl

│ └── vectorizador.pkl

├── data/

│ └── intents.json # Dataset de intenciones y respuestas

├── templates/

│ └── index.html # Interfaz del usuario

├── static/

│ └── styles.css

├── Procfile

├── requirements.txt

└── README.md

## Requisitos 
 Los requisitos que se necesitan para este proyecto son:

- Python 3.10 o superior
- Flask
- scikit-learn
- joblib


Y para ejecutar localmente:

python app.py



Link del modelo desplegado:

https://chatbot-educativo-bd90.onrender.com/

#  Informe

[Proyecto Final Fundamentos de Inteligencia Artificial_Mejia, Morocho .pdf](https://github.com/user-attachments/files/21477487/Proyecto.Final.Fundamentos.de.Inteligencia.Artificial_Mejia.Morocho.pdf)


## Autores

- Joshua Morocho

- Josué Mejía
