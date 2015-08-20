import re
import sys
import requests
from contextlib import closing


def request_data(imdb_id):
    url = 'http://www.omdbapi.com/?i={}&plot=short&r=json'.format(imdb_id)
    r = requests.get(url)
    return r.json()


def top_250_ids():
    with closing(open('top250.txt')) as f:
        return [line.rstrip('\r\n') for line in f]


def fetch_movies():
    ids = top_250_ids()[:10]
    movies = [request_data(id) for id in ids]    
    return movies
