import asyncio
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.thessalonikiguide.gr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

GREEK_DAYS = {
    "\u0394\u03b5": "Mon",
    "\u03a4\u03c1": "Tue",
    "\u03a4\u03b5": "Wed",
    "\u03a0\u03b5": "Thu",
    "\u03a0\u03b1": "Fri",
    "\u03a3\u03b1": "Sat",
    "\u039a\u03c5": "Sun",
}


async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text


def extract_movies_from_listing(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    movies = []
    for article in soup.select("article.mb-25"):
        card = article.select_one("div[itemscope][itemtype='http://schema.org/Movie']")
        if not card:
            continue
        title_el = card.select_one("h3[itemprop='name'] a")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        detail_url = title_el.get("href", "")
        poster_el = card.select_one("img.alignleft.wp-post-image")
        poster = ""
        if poster_el:
            poster = poster_el.get("data-lazy-src") or poster_el.get("src") or ""
            if "data:image" in poster:
                noscript = poster_el.find_parent().find("noscript")
                if noscript:
                    ns_img = noscript.select_one("img")
                    if ns_img:
                        poster = ns_img.get("src") or ""

        imdb_el = card.select_one("span.bg-orange")
        imdb = ""
        if imdb_el:
            score_el = imdb_el.find_next("span")
            if score_el:
                score_b = score_el.select_one("b")
                if score_b:
                    imdb = score_b.get_text(strip=True)

        genres = [g.get_text(strip=True) for g in card.select("span[itemprop='genre']")]
        year_el = card.select_one("span[itemprop='datePublished']")
        year = year_el.get("content", "") if year_el else ""

        collapse_id = card.select_one("a[data-bs-toggle='collapse']")
        collapse_target = ""
        if collapse_id:
            href = collapse_id.get("href", "")
            if href.startswith("#"):
                collapse_target = href[1:]

        cinemas = []
        description = ""
        cast = ""
        director = ""
        writer = ""
        if collapse_target:
            collapse_div = article.select_one(f"div.collapse#{collapse_target}")
            if collapse_div:
                desc_el = collapse_div.select_one("div[itemprop='description']")
                if desc_el:
                    description = desc_el.get_text(strip=True)

                # Cast / director / writer live inside the same div.mb-20 block,
                # so we must NOT use find_parent("div").get_text() (it returns
                # all three fields concatenated). Use schema.org microdata
                # (itemprop=actor/director/author) or fall back to the parent <li>.
                def _names(selector: str) -> str:
                    names = []
                    for el in collapse_div.select(selector):
                        # inner <span itemprop="name"> holds the clean value
                        name_el = el.select_one('[itemprop="name"]')
                        txt = (name_el.get_text(strip=True) if name_el
                               else el.get_text(strip=True))
                        if txt:
                            names.append(txt.strip().strip(","))
                    # de-dupe while preserving order
                    seen = set()
                    uniq = []
                    for n in names:
                        if n and n not in seen:
                            seen.add(n)
                            uniq.append(n)
                    return ", ".join(uniq)

                cast = _names('[itemprop="actor"]')
                director = _names('[itemprop="director"]')
                writer = _names('[itemprop="author"]')

                # Fallback for pages without microdata: parse the <li> text and
                # cut at the next known label.
                def _li_fallback(label_pattern: str) -> str:
                    texts = collapse_div.find_all(string=re.compile(label_pattern))
                    if not texts:
                        return ""
                    li = texts[0].find_parent("li")
                    if li is None:
                        return ""
                    txt = li.get_text(separator=" ", strip=True)
                    # remove the label itself
                    txt = re.sub(r"^.*?" + label_pattern + r"\s*:?\s*", "", txt).strip()
                    # cut off any trailing label (e.g. cast string contains
                    # "Σκηνοθεσία :" + "Σενάριο :" after it)
                    cut = re.split(r"Σκηνοθεσία|Σενάριο|Ηθοποιοί", txt)[0].strip()
                    return cut.strip(" ,:")

                if not cast:
                    cast = _li_fallback(r"Ηθοποιοί")
                if not director:
                    director = _li_fallback(r"Σκηνοθεσία")
                if not writer:
                    writer = _li_fallback(r"Σενάριο")

                for cinema_link in collapse_div.select("div.row a.d-block"):
                    name = cinema_link.get_text(strip=True)
                    href = cinema_link.get("href", "")
                    if name:
                        cinemas.append({"name": name, "url": href})

        movies.append({
            "title": title,
            "detail_url": detail_url,
            "poster": poster,
            "imdb": imdb,
            "genres": genres,
            "year": year,
            "description": description,
            "cast": cast,
            "director": director,
            "writer": writer,
            "trailer": "",
            "cinemas": cinemas,
        })
    return movies


def extract_movie_details(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    details = {}
    overview = soup.select_one("h2#perigrafi")
    if overview:
        div = overview.find_next_sibling("div")
        if div:
            text = div.get_text(strip=True, separator=" ")
            if text:
                details["description"] = text
    trailer_heading = soup.select_one("h2#mov-trailer")
    if trailer_heading:
        container = trailer_heading.find_next_sibling("div")
        if container:
            src = ""
            player = container.select_one(".rll-youtube-player")
            if player:
                src = player.get("data-src", "")
            if not src:
                iframe = container.select_one("iframe")
                if iframe:
                    src = iframe.get("src", "")
            if src:
                match = re.search(r"(?:v=|/embed/)([A-Za-z0-9_-]{6,20})", src)
                details["trailer"] = "https://www.youtube.com/watch?v=" + match.group(1) if match else src
    return details


def parse_showtimes(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    section = soup.select_one("h2#paizetai")
    if not section:
        return {"cinemas": []}
    container = section.find_parent("section") or section.find_next_sibling()
    cinema_results = []
    for cinema_block in container.select("div.mb-10.text-13.text-md-14"):
        toggle = cinema_block.select_one("a[data-bs-toggle='collapse']")
        if not toggle:
            continue
        name_el = toggle.select_one("span.fw-600")
        if not name_el:
            continue
        cinema_name = name_el.get_text(strip=True)
        info_div = cinema_block.select_one("div.pb-20.pt-5.text-gray.text-12")
        address = ""
        phone = ""
        cinema_url = ""
        if info_div:
            link = info_div.select_one("a.text-blue.fw-600")
            if link:
                cinema_url = link.get("href", "")
            spans = info_div.select("span.dots")
            if len(spans) > 0:
                address = spans[0].get_text(strip=True)
            if len(spans) > 1:
                phone = spans[1].get_text(strip=True)

        halls = []
        for table in cinema_block.select("table.python-table.text-center"):
            rows = table.select("tr")
            hall_name = ""
            days = []
            showtimes = []
            for i, row in enumerate(rows):
                cells = row.select("td")
                if not cells:
                    continue
                if len(cells) == 1 and cells[0].get("colspan") == "7":
                    hall_name = cells[0].get_text(strip=True) or "\u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1"
                elif len(cells) == 7 and i == 1:
                    days = [c.get_text(strip=True) for c in cells]
                elif len(cells) == 7:
                    day_times = []
                    for c in cells:
                        raw = c.get_text(strip=True, separator="\n")
                        times = re.findall(r"\d{1,2}:\d{2}", raw)
                        day_times.append(times)
                    showtimes.append(day_times)
            halls.append({
                "name": hall_name or "\u0391\u03af\u03b8\u03bf\u03c5\u03c3\u03b1",
                "days": days,
                "showtimes": showtimes,
            })
        cinema_results.append({
            "name": cinema_name,
            "url": cinema_url,
            "address": address,
            "phone": phone,
            "halls": halls,
        })
    return {"cinemas": cinema_results}


async def scrape_all_movies(max_pages: int = 2) -> list[dict]:
    all_movies = []
    urls = [f"{BASE_URL}/cinema/"]
    for i in range(2, max_pages + 1):
        urls.append(f"{BASE_URL}/cinema/page/{i}/")
    for url in urls:
        try:
            html = await fetch_html(url)
            movies = extract_movies_from_listing(html)
            all_movies.extend(movies)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return all_movies


async def scrape_movie_showtimes(detail_url: str) -> dict:
    if not detail_url.startswith("http"):
        detail_url = BASE_URL + detail_url
    html = await fetch_html(detail_url)
    result = parse_showtimes(html)
    result.update(extract_movie_details(html))
    return result


if __name__ == "__main__":
    async def test():
        movies = await scrape_all_movies(max_pages=1)
        print(f"Found {len(movies)} movies")
        for m in movies[:2]:
            print(f"  {m['title']} - {', '.join(m['cinemas'][:3]) if m['cinemas'] else 'no cinemas'}")
            if m['detail_url']:
                showtimes = await scrape_movie_showtimes(m['detail_url'])
                print(f"    Showtimes: {len(showtimes.get('cinemas', []))} cinemas")
    asyncio.run(test())
