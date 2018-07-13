import requests


# More info about the below REST requests here - https://api.thetvdb.com/swagger

# Authentication : Obtaining and refreshing your JWT token
def post_login():
    # Returns a session token to be included in the rest of the requests.
    task = {"apikey": "GMF7D81TXRBLW3EX", "userkey": "6MD4CVDHE6HKZC6H", "username": "cian12493r1f"}
    resp = requests.post('https://api.thetvdb.com/login', json=task)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


def get_refresh_token(bearer_token):
    # Refreshes your current, valid JWT token and returns a new token.
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    resp = requests.get('https://api.thetvdb.com/refresh_token', headers=headers)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


# Episodes : Information about a specific episode
def get_episode_id(bearer_token, episode_id):
    # Returns the full information for a given episode id.
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    resp = requests.get('https://api.thetvdb.com/episode/{}'.format(episode_id), headers=headers)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


# Search : Search for a particular series
def get_search_series(bearer_token, series_name):
    # Allows the user to search for a series
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    payload = {"name": series_name}
    resp = requests.get('https://api.thetvdb.com/search/series', headers=headers, params=payload)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


# Series : Information about a specific series
def get_series_id(bearer_token, series_id):
    # Returns a series records that contains all information known about a particular series id.
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    resp = requests.get('https://api.thetvdb.com/series/{}'.format(series_id), headers=headers)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


def get_series_id_episodes_query(bearer_token, series_id, season_num, episode_num):
    # This route allows the user to query against episodes for the given series.
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    payload = {"id": series_id, "airedSeason": season_num, "airedEpisode": episode_num}
    resp = requests.get('https://api.thetvdb.com/series/{}/episodes/query'.format(series_id),
                        headers=headers, params=payload)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


# Users : Routes for handling user data.
def get_user_favorites(bearer_token):
    # Returns an array of favorite series for a given user, will be a blank array if no favorites exist.
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    resp = requests.get('https://api.thetvdb.com/user/favorites', headers=headers)

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()


# OMDB API - More info at http://www.omdbapi.com/

def get_film_by_title(api_key, film_title, film_year):
    # Returns information for a film based on the title and year
    payload = {"apikey": api_key, "t": film_title, "y": film_year}
    resp = requests.get('http://www.omdbapi.com/', params=payload)

    if resp.status_code == 200 or resp.status_code == 201:
        print(resp.json())
        return resp.json()


def search_film_by_title(api_key, film_title, film_year):
    # Searches for a film based on the title and year
    payload = {"apikey": api_key, "s": film_title, "y": film_year}
    resp = requests.get('http://www.omdbapi.com/', params=payload)

    if resp.status_code == 200 or resp.status_code == 201:
        print(resp.json())
        return resp.json()
