import json


def movie_with_id(_, info, _id):  # comme c'est de type query (type de base) the first arg is _ for now, no nned for info here given by GRAPHQL, argument should be exactly like in the "schema" : "_id"
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def get_all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as mfile:
        movies = json.load(mfile)
        return movies['movies'] # pour envoyer la liste des movies


def update_movie_rate(_, info, _id, _rate):  # mutation is a basic type
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):  # this time the first param is movie, cause Movie is calling actor
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors
