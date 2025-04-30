import requests

def fetch_anime_info(mal_id):
    url = f"https://api.jikan.moe/v4/anime/{mal_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()['data']
    synopsis = data.get("synopsis", "")
    genres = ", ".join([g["name"] for g in data.get("genres", [])])
    return {
        "synopsis": synopsis,
        "genres": genres
    }
