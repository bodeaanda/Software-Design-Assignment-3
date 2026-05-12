import os
import asyncio
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

CHAOS_MODE = os.getenv("CHAOS_MODE", "false").lower() == "true"

@app.get("/recommendations/{movie_id}")
async def get_recommendations(movie_id: int):
    if CHAOS_MODE:
        if random.random() < 0.5:
            return JSONResponse(
                status_code=503,
                content={"error": "Service unavailable (chaos mode)"}
            )
        delay = random.uniform(3, 10)
        print(f"[CHAOS] Sleeping {delay:.1f}s...")
        await asyncio.sleep(delay)

    return {"movie_ids": [1, 2, 3, 4, 5]}