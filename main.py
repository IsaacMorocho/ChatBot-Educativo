import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
from streamlit_chat import message

# ---- CARGA Y PREPARACIÓN DE DATOS ----

df = pd.read_excel("lesiones_comunes_dataset.xlsx")

# Crear columna de porcentaje de daño estimado
def calcular_dano(gravedad):
    niveles = {"leve": 20, "moderada": 50, "grave": 80}
    return niveles.get(gravedad.lower(), 50)

df["porcentaje_dano"] = df["Gravedad"].apply(calcular_dano)

# Separar variables predictoras y objetivo
X = df[["Edad", "Sexo", "Tipo_Lesion", "Zona_Afectada", "Contexto"]]
y = df["porcentaje_dano"]

# Preprocesamiento
numeric_features = ["Edad"]
categorical_features = ["Sexo", "Tipo_Lesion", "Zona_Afectada", "Contexto"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(), categorical_features)
    ]
)

# Modelo con red neuronal
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", MLPRegressor(hidden_layer_sizes=(20, 10), max_iter=500, random_state=42))
])

# Entrenamiento
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# ---- INTERFAZ STREAMLIT ----

st.set_page_config(page_title="Asistente de Lesiones", layout="wide")
st.title("🧠 Asistente de Predicción Médica y Chat en Vivo")

col1, col2 = st.columns(2)

# ---- SECCIÓN 1: PREDICTOR ----
with col1:
    st.header("🔍 Predicción de Porcentaje de Daño")

    Edad = st.slider("Edad", min_value=1, max_value=100, value=30)
    Sexo = st.selectbox("Sexo", df["Sexo"].unique())
    Tipo_Lesion = st.selectbox("Tipo de lesión", df["Tipo_Lesion"].unique())
    Zona_Afectada = st.selectbox("Zona afectada", df["Zona_Afectada"].unique())
    Contexto = st.selectbox("Contexto", df["Contexto"].unique())

    if st.button("Calcular porcentaje de daño"):
        entrada = pd.DataFrame({
            "Edad": [Edad],
            "Sexo": [Sexo],
            "Tipo_Lesion": [Tipo_Lesion],
            "Zona_Afectada": [Zona_Afectada],
            "Contexto": [Contexto]
        })
        pred = model.predict(entrada)[0]
        st.success(f"✅ Porcentaje estimado de daño: {pred:.2f}%")

# ---- SECCIÓN 2: CHATBOT BOTPRESS EMBEBIDO ----
with col2:
    st.header("🤖 Chatbot Médico")

    components.html(
        """
        <iframe 
            src="https://cdn.botpress.cloud/webchat/v3.2/shareable.html?configUrl=https://files.bpcontent.cloud/2025/08/04/01/20250804015604-WYOMHCIQ.json"
            width="100%" 
            height="600px" 
            style="border:none;">
        </iframe>
        """,
        height=620
    )
