"""Script for CI (GitHub Actions): scrape all movies + showtimes, save snapshot, build HTML."""
import asyncio, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

from scraper import scrape_all_movies, scrape_movie_showtimes


async def main():
    print("Scraping movie listing...")
    movies = await scrape_all_movies(max_pages=2)
    print(f"Found {len(movies)} movies, fetching showtimes...")

    for i, m in enumerate(movies, 1):
        try:
            st = await scrape_movie_showtimes(m["detail_url"])
            m["showtimes"] = st.get("cinemas", [])
        except Exception as e:
            m["showtimes"] = []
        print(f"  [{i}/{len(movies)}] {m['title'][:40]} — {len(m['showtimes'])} cinemas")

    # Save snapshot
    with open("snapshot.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    print(f"\nSaved snapshot.json ({len(json.dumps(movies, ensure_ascii=False))} bytes)")

    # Build HTML
    sys.path.insert(0, os.path.dirname(__file__))
    import build_standalone
    print("ThessCinema.html regenerated.")


if __name__ == "__main__":
    asyncio.run(main())
