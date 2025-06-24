# omdb_utils.py
import requests
import logging

def get_movie_details(title, api_key):
    url = f"http://www.omdbapi.com/?t={title}&plot=full&apikey={api_key}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        if data.get("Response") == "True":
            plot = data.get("Plot", "N/A")
            poster = data.get("Poster", "N/A")
            return plot, poster
    except Exception as e:
        logging.error(f"OMDb API error for '{title}': {e}")
    return "N/A", "N/A"