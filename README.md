# Proyecto Final - Fundamentos de Inteligencia Artificial

Este proyecto implementa un **ChatBot educativo** con capacidades de inteligencia artificial para brindar **asistencia en primeros auxilios**, utilizando la plataforma **Botpress**, junto con un modelo predictivo de soporte desarrollado en **Python**.

## 🤖 ChatBot Educativo - Primeros Auxilios

El chatbot está diseñado para ofrecer información inmediata, clara y precisa sobre situaciones comunes de emergencia, como quemaduras, fracturas, desmayos, etc. Combina flujos conversacionales de **Botpress** con un modelo de **aprendizaje automático** personalizado.

## ⚙️ Características

* Integración de flujos personalizados con **Botpress**.
* Incorporación de un **modelo de predicción** en Python para respuestas inteligentes.
* Dataset en formato `.xlsx` con temas de primeros auxilios.
* Estructura modular de carpetas para fácil mantenimiento.
* Interfaz amigable con Streamlit (desde `main.py`).
* Posibilidad de ampliación con más flujos, integraciones y plugins.

## 🧠 Temáticas abordadas

* 🔥 Quemaduras
* 🦴 Fracturas
* 💊 Heridas comunes
* 🤕 Golpes y traumatismos
* 🚑 Reanimación cardiopulmonar (RCP)
* 😵‍💫 Desmayos
* 🐍 Mordeduras
* Y más...

## 📁 Estructura del proyecto

```
my-bot/
│
├── .botpress/
│   ├── dist/
│   │   └── index.cjs                # Código generado por Botpress
│   └── implementation/
│       ├── plugins/                 # Plugins del bot
│       └── typings/                 # Tipos para flujos, estados, acciones, etc.
│           ├── actions/
│           ├── events/
│           ├── integrations/
│           ├── states/
│           ├── tables/
│           └── workflows/
│               └── index.ts
│
├── src/
│   ├── index.ts                    # Código principal del bot
│   ├── bot.definition.ts          # Definición del bot
│
├── main.py                        # Script con modelo de predicción en Python + Streamlit
├── lesiones_comunes_dataset.xlsx  # Dataset personalizado
├── first_aid_instructions_translate.xlsx # Instrucciones de primeros auxilios traducidas
│
├── package.json                   # Configuración del proyecto Node.js
├── tsconfig.json                  # Configuración de TypeScript
├── package-lock.json
├── project.cache.json
└── README.md                      # Este archivo
```

## 🧪 Requisitos

### Backend con Python

* Python 3.10 o superior
* Streamlit
* pandas
* scikit-learn
* openpyxl

### Chatbot

* Node.js
* Botpress
* TypeScript

## 🚀 Despliegue

Este bot puede integrarse y desplegarse en plataformas como:

* **Render**
* **Heroku**
* **Vercel** (para frontend)
* **Railway** (para backend)

Además, el bot puede conectarse a otros sistemas como asistentes virtuales o sistemas de emergencia educativa.

## 📎 Informe del Proyecto

[Proyecto Final Fundamentos de Inteligencia Artificial_Mejia, Morocho.pdf](https://github.com/user-attachments/files/21588324/Proyecto.Final.Fundamentos.de.Inteligencia.Artificial_Mejia.Morocho.pdf)

## 👥 Autores

* Joshua Morocho
* Josué Mejía
