import asyncio, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(__file__) or '.')
sys.path.insert(0, '.')
from scraper import scrape_all_movies, scrape_movie_showtimes

async def main():
    movies = await scrape_all_movies(max_pages=1)
    print(f"Found {len(movies)} movies from page 1")
    if movies:
        print(f"First movie: {movies[0]['title']}")
        st = await scrape_movie_showtimes(movies[0]['detail_url'])
        print(f"Showtimes cinemas: {len(st.get('cinemas',[]))}")
    else:
        print("No movies scraped - scraper may be broken")

asyncio.run(main())
