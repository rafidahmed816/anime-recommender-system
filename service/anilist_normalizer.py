def normalize_anilist_data(anilist_data):
    """
    Transforms AniList API response to match cleaned Jikan dataset format.
    """
    synopsis = anilist_data.get("description", "").replace("<br>", " ").replace("\n", " ")
    
    # Combine genres and tags (optional)
    genres = anilist_data.get("genres", [])
    tags = [tag["name"] for tag in anilist_data.get("tags", []) if tag.get("isMediaSpoiler") == False]
    combined_genres = ", ".join(genres + tags)
    
    # Get studio names
    studios = [studio["node"]["name"] for studio in anilist_data.get("studios", {}).get("edges", [])]

    return {
        "synopsis": synopsis,
        "genres": ", ".join(genres),
        "themes": ", ".join(tags),        
        "studios": ", ".join([studio["name"] for studio in studios]) 

    }
