import asyncio
import json
import subprocess
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from scraper import scrape_all_movies, scrape_movie_showtimes


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = {"data": None, "timestamp": 0}
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/app/")


@app.get("/api/movies")
async def get_movies(refresh: bool = Query(False)):
    now = time.time()
    cache = app.state.cache
    if refresh or not cache["data"] or (now - cache["timestamp"] > 300):
        movies = await scrape_all_movies(max_pages=2)
        cache["data"] = movies
        cache["timestamp"] = now
    return {"movies": cache["data"]}


@app.get("/api/movies/{slug:path}")
async def get_movie_detail(slug: str):
    if slug.startswith("http"):
        url = slug
    elif slug.startswith("/"):
        url = f"https://www.thessalonikiguide.gr{slug}"
    else:
        url = f"https://www.thessalonikiguide.gr/tainia/{slug}/"
    showtimes = await scrape_movie_showtimes(url)
    return showtimes


@app.get("/api/refresh")
async def refresh_movies():
    movies = await scrape_all_movies(max_pages=2)
    app.state.cache["data"] = movies
    app.state.cache["timestamp"] = time.time()
    return {"movies": movies}


def run_sync(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, encoding="utf-8")
        return r.returncode == 0, r.stdout[-200:] if r.stdout else r.stderr[-200:]
    except Exception as e:
        return False, str(e)


@app.get("/api/rebuild")
async def rebuild():
    movies = await scrape_all_movies(max_pages=2)
    for m in movies:
        try:
            st = await scrape_movie_showtimes(m["detail_url"])
            m["showtimes"] = st.get("cinemas", [])
        except Exception:
            m["showtimes"] = []
    # Save snapshot
    with open("snapshot.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    # Run build script
    ok, out = await asyncio.get_event_loop().run_in_executor(None, run_sync, ["python", "build_standalone.py"])
    app.state.cache["data"] = movies
    app.state.cache["timestamp"] = time.time()
    return {"movies": movies, "build_ok": ok, "build_output": out}
