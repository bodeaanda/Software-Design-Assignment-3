import httpx
from fastapi import FastAPI
from movie_service.circuit_breaker import CircuitBreaker

app = FastAPI()
breaker = CircuitBreaker(threshold=3, recovery_timeout=10.0)

MOVIES = {
    1: {"title": "Inception", "description": "A mind-bending thriller."},
    2: {"title": "Interstellar", "description": "A space odyssey."},
    3: {"title": "The Matrix", "description": "Reality is a simulation."},
}

FALLBACK_RECOMMENDATIONS = [
    {"id": 99, "title": "Trending: The Dark Knight"},
    {"id": 98, "title": "Trending: Pulp Fiction"},
    {"id": 97, "title": "Trending: Forrest Gump"},
]

RECOMMENDATION_URL = "http://localhost:3002/recommendations"
TIMEOUT = 1.5  

@app.get("/movie/{movie_id}")
async def get_movie(movie_id: int):
    movie = MOVIES.get(movie_id, {"title": "Unknown", "description": "N/A"})
    recommendations = await fetch_recommendations(movie_id)

    return {
        "movie": movie,
        "recommendations": recommendations,
        "circuit_state": breaker.status,
    }

async def fetch_recommendations(movie_id: int):
    async def call_service():
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{RECOMMENDATION_URL}/{movie_id}")
            response.raise_for_status()  
            return response.json()["movie_ids"]

    try:
        ids = await breaker.call(call_service)
        return [{"id": i, "title": f"Movie #{i}"} for i in ids]
    except Exception as e:
        print(f"[MovieService] Fallback activ: {e}")
        return FALLBACK_RECOMMENDATIONS

@app.get("/circuit-status")
async def circuit_status():
    return {"state": breaker.status, "failures": breaker.failures}