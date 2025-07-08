from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import time
from pydantic import BaseModel
from typing import List, Any
import json
import os
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dados-populacionais")
def get_dados():
    path = os.path.join(os.path.dirname(__file__), "population909500.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

dados_acumulados = [["2025", []]]

@app.get("/eventos")
async def eventos(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            novos_pontos = []
            for _ in range(random.randint(5, 10)):
                lat = random.uniform(-33, 5)    
                lon = random.uniform(-74, -34) 
                mag = random.randint(1, 10)    
                novos_pontos.extend([lat, lon, mag])

            dados_acumulados[0][1].extend(novos_pontos)

            json_str = json.dumps(dados_acumulados)

            yield f"data: {json_str}\n\n"

            await asyncio.sleep(3)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
