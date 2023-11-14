import json


def movie_with_id(_, info, _id):
    """
    seeing as it's of query type (basic type) the first arg is _ for now, no need for info here it's given by GRAPHQL,
    argument should be exactly like in the schema : "_id"

    This method gets the movie by passing its id as a parameter

    :param _:
    :param info:
    :param _id: string
    :return: movie
    """
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def get_all_movies(_, info):
    """
    Method to get all the movies in the database

    :param _:
    :param info:
    :return: movie list
    """
    with open('{}/data/movies.json'.format("."), "r") as mfile:
        movies = json.load(mfile)
        # to send the list of movies
        return movies['movies']


def update_movie_rate(_, info, _id, _rate):  # mutation is a basic type
    """
    This method is to change/update a movie's rate by passing its id and the new rating

    :param _:
    :param info:
    :param _id: string
    :param _rate: float
    :return: Movie json
    """

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


def resolve_actors_in_movie(movie, info):
    """
    this time the first param is movie, cause Movie is calling actor

    :param movie: Movie
    :param info:
    :return: Actors
    """
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors