# 🌐 Visualizador de Dados Populacionais em Globo 3D

Este projeto exibe um globo 3D interativo que recebe e atualiza automaticamente dados populacionais (ou de magnitude) ao longo do tempo, usando **Server-Sent Events (SSE)** com uma API feita em **FastAPI**.

---

## 📁 Estrutura

- `index.html`: Página principal que carrega e renderiza o globo com dados animados.
- `main.py`: Backend com FastAPI que emite dados em tempo real no endpoint `/eventos`.
- `Dockerfile` e `docker-compose.yml`: Infraestrutura para rodar backend e frontend juntos.

---

## 🧭 Como Funciona

### Frontend (`index.html`)

- Usa WebGL (como Globe.js) para renderizar um globo.
- Conecta-se ao backend via `EventSource`:

```javascript
const eventSource = new EventSource('http://localhost:8000/eventos');
```
A cada 3 segundos, recebe novos dados em JSON no formato:
```
[["2025", [lat1, lon1, mag1, lat2, lon2, mag2, ...]]
```

##  Backend (FastAPI)
- Endpoint /eventos fornece dados via Server-Sent Events (text/event-stream).
- Os dados são simulados com coordenadas aleatórias e magnitudes inteiras.
- Cada resposta acumula dados no mesmo formato, permitindo visualização histórica.

## 🚀 Como Rodar o Projeto
- Requisitos
- Docker

Docker Compose

### Passos
1. Clone o repositório
2. Execute:
```
docker compose up --build
```

## 🚀 Como Rodar o Projeto Localmente
```
python -m http.server 8080
```
