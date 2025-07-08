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

    let iniciou = false;

    eventSource.onmessage = function(event) {
      const series = JSON.parse(event.data);

      const latMin = -56;
      const latMax = 33;
      const lonMin = -120;
      const lonMax = -30;

      for (let i = 0; i < series.length; i++) {
        const nome = series[i][0];
        const dados = series[i][1];

        const filtrados = [];
        for (let j = 0; j < dados.length; j += 3) {
          const lat = dados[j];
          const lon = dados[j + 1];
          const mag = dados[j + 2];

          if (lat >= latMin && lat <= latMax && lon >= lonMin && lon <= lonMax) {
            filtrados.push(lat, lon, mag);
          }
        }

        if (filtrados.length > 0) {
          globe.addData(filtrados, {
            format: 'magnitude',
            name: nome,
            animated: true
          });
        }
      }

      if (!iniciou) {
        globe.createPoints();    
        settime(globe, 0)();     
        globe.animate();       
        iniciou = true;
      }

      document.body.style.backgroundImage = 'none';
    };
```
A cada 3 segundos, recebe novos dados em JSON no formato:
```
[["2025", [lat1, lon1, mag1, lat2, lon2, mag2, ...]]
```




##  Backend (FastAPI)
- Endpoint /eventos fornece dados via Server-Sent Events (text/event-stream).
- Os dados são simulados com coordenadas aleatórias e magnitudes inteiras.
- Cada resposta acumula dados no mesmo formato, permitindo visualização histórica.

```
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
```

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
