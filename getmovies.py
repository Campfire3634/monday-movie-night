import requests
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

# API keys
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase setup
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['results'][0] if data['results'] else None

def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&append_to_response=credits,external_ids"
    response = requests.get(url)
    return response.json()

def upsert_movie(movie, watched_date):
    # Insert movie
    response = supabase.table("movies").upsert({
        "title": movie['title'],
        "release_year": int(movie['release_date'][:4]) if movie['release_date'] else None,
        "tmdb_id": movie['id'],
        "imdb_id": movie['external_ids'].get('imdb_id'),
        "runtime": movie.get('runtime'),
        "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
        "overview": movie.get('overview'),
        "date_watched": watched_date
    }).execute()
    return response.data[0]['id']

def upsert_people_and_roles(movie_id, people, role_type):
    for person in people:
        # Add person to people table
        person_resp = supabase.table("people").upsert({
            "name": person['name'],
            "tmdb_id": person['id']
        }, on_conflict=["tmdb_id"]).execute()

        person_id = person_resp.data[0]['id']
        # Add relationship
        supabase.table("movie_people").upsert({
            "movie_id": movie_id,
            "person_id": person_id,
            "role": role_type,
            "character": person.get('character') if role_type == "Actor" else None
        }).execute()

# Example usage
movie_titles = [
    ("They Live","1988-11-04"),
]

for title, watched_date in movie_titles:
    search_result = search_movie(title)
    if not search_result:
        print(f"Not found: {title}")
        continue

    details = get_movie_details(search_result['id'])
    movie_id = upsert_movie(details, watched_date)

    cast = details['credits'].get('cast', [])[:5]  # Top 5 cast
    crew = details['credits'].get('crew', [])
    directors = [c for c in crew if c['job'] == 'Director']
    producers = [c for c in crew if c['job'] == 'Producer']

    upsert_people_and_roles(movie_id, cast, "Actor")
    upsert_people_and_roles(movie_id, directors, "Director")
    upsert_people_and_roles(movie_id, producers, "Producer")

    print(f"Imported: {title}")
