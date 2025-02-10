from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os
load_dotenv()

# Inicjalizacja aplikacji FastAPI
app = FastAPI()


# Allow frontend requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Klucz API OpenAI 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model danych dla żądania
class Message(BaseModel):
    message: str

# Endpoint do rozmowy z ChatGPT


@app.post("/chat")
async def chat_with_gpt(message: Message):
    try:
        content = "Jesteś asystentem w sklepie internetowym z książkami. Twoim zadaniem jest pomoc użytkownikowi w znalezieniu książek, które pasują do jego zainteresowań, preferencji czy potrzeb. Możesz sugerować książki na podstawie gatunku, autora, rekomendacji, a także odpowiadać na pytania dotyczące dostępności, cen i opisów książek. Jeśli użytkownik prosi o pomoc w wyborze książki, staraj się zaproponować kilka opcji, uwzględniając jego gust, preferencje tematyczne lub aktualne promocje.Jeśli użytkownik zada pytanie o konkretnego autora lub książkę, podaj szczegółowe informacje, takie jak tytuł, opis, recenzje oraz dostępność. Bądź uprzejmy, pomocny i dokładny w swoich odpowiedziach. "


        # wysłanie zapytania do chatGPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # model
            messages=[
                {"role": "system", "content": content},
                # wiadomość od użytkownikla
                {"role": "user", "content": message.message}
            ]
        )

        # Pobieranie odpowiedzi z API
        reply = response.choices[0].message
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Endpoint do recenzji

@app.post("/recenzja")
async def recenzja(message: Message):
    try:
        # Send request to OpenAI API using correct client
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Make sure to use the right model
            messages=[
                {"role": "system", "content": "Jesteś asystentem w sklepie internetowym z książkami. Twoim zadaniem jest napisanie krótkiej recenzji ksiażki."},
                # Use the incoming message from the user
                {"role": "user", "content": message.message}
            ]
        )

        # Pobieranie odpowiedzi z API
        reply = response.choices[0].message
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Endpoint testowy

@app.get("/")
async def root():
    return {"message": "API działa"}
