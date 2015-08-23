import re
import sys
import requests
from contextlib import closing


def request_data(imdb_id):
    # make request to imdb api
    url = 'http://www.omdbapi.com/?i={}&plot=short&r=json'.format(imdb_id)
    r = requests.get(url)
    return r.json()


def top_250_ids():
    with closing(open('top250.txt')) as f:
        return [(i+1, line.rstrip('\r\n')) for i, line in enumerate(f)]


def fetch_movies():
    ids = top_250_ids()
    movies = [(i, request_data(id)) for i, id in ids]
    return movies
