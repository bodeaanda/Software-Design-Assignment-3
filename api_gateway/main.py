import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

MOVIE_SERVICE_URL = "http://localhost:3001"

@app.get("/movie/{movie_id}")
async def get_movie(movie_id: int):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{MOVIE_SERVICE_URL}/movie/{movie_id}")
            return response.json()
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": f"Gateway error: {str(e)}"})

@app.get("/health")
async def health():
    return {"status": "ok"}