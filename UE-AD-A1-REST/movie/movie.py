import requests
from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

# reading the json file corresponding to the movie service
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


@app.route("/", methods=["GET"])
def listofmovies():
    """
    Root message/default that returns the list of movies in the movie database

    :return:
    """
    res = ""
    for movie in movies:
        res += movie["title"] + "<br>"
    return res


@app.route("/template", methods=['GET'])
def template():
    """
    First entry point: requests the rendering of  a template through
    a GET method HTTP request

    :return:
    """
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    """
    Second entry point: requesting the movies' json database through a GET
    method HTTP request

    :return:
    """
    return make_response(jsonify(movies), 200)


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """
    Third entry point: requesting a movie's data using its ID through a
    GET method HTTP request

    :param movieid: string
    :return: json
    """
    for movie in movies:
        # making sure that the movie ID exists in the database before answering the request
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify(movie), 200)
    return make_response(jsonify({"error": "Movie ID not found"}), 400)


@app.route("/moviebytitle", methods=['GET'])
def get_movie_by_title():
    """
     Fourth entry point: requesting a movie's data in a json format through a GET method HTTP request, by passing the movie's title in the URL

    :return: json
    """
    json = ""
    # making sure that the passed parameter is valid
    if request.args:
        req = request.args
        for movie in movies:
            # checking if the title passed exists in the movies database
            if str(movie["title"]) == str(req["title"]):
                # selecting the movie
                json = movie
    # checking if the movie title exists and if not return an error
    # message with the corresponding status code 400 or 200
    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    """
    Fifth entry point: requesting the addition/creation of a movie through
    a POST method HTTP request, by passing the movie's ID in the URL

    :param movieid: string
    :return: json
    """
    # accessing the json database with the request method from Flask
    req = request.get_json()

    # checking whether the movie id already exists because if it does
    # there's no need to have the same movie twice
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)
    # adding the movie to the database
    movies.append(req)
    return make_response(jsonify({"message": "movie added"}), 200)


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    """
    Sixth entry point : modifying the rating of a movie through a PUT method
    HTTP request by passing its ID and new rating as arguments in the URL

    :param movieid: string
    :param rate: float
    :return: json
    """
    for movie in movies:
        # like before checking if the movieID exists is necessary
        if str(movie["id"]) == str(movieid):
            # after the id is found, modify that movie's rating by giving
            # it the rating passed as an argument
            movie["rating"] = int(rate)
            # status code 201 is to indicate that the request has succeeded
            # and has led to the creation of a resource
            return make_response(jsonify(movie), 201)

    return make_response(jsonify({"error": "movie ID not found"}), 400)


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """
    Seventh entry point : removing a movie through a DELETE
    method HTTP request, by passing its ID as an argument
    in the URL

    :param movieid: string
    :return: json
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            # removing the movie
            movies.remove(movie)
            # deletion is complete
            return make_response(jsonify(movie), 200)

    return make_response(jsonify({"error": "movie ID not found"}), 400)


@app.route("/omdb/<title>/<year>/", methods=['GET'])
def omdb_movie_by_title(title, year):
    """
    Eighth entry point : requesting the OMDb API (https://www.omdbapi.com/)
    through a GET method HTTP request, to retrieve the data of the movie with
    the specified title, from and after the specified release year.
    If -1 is passed as the year argument, the entry point will only look for the movie
    by title. If no movie with the exact same title is found, this entry point
    looks for a another movie, the title of which contains the specified title,
    and returns its data. If no such movie is found, an error is returned.

    :param title: string
    :param year: integer
    :return: data about the specified movie, by title, release year (optionally)
    """
    req_url = "http://www.omdbapi.com/?apikey=39f879ba&t=" + title
    if int(year) != -1:
        req_url += "&y=" + str(year)
    response = requests.get(req_url)
    response_json = response.json()
    # When certain errors occur, the OMDb API still returns
    # a response with a 200 status code, so it is necessary
    # to check for an "Error" field in the response.
    if response.status_code == 200 and "Error" not in response_json:
        response_data = {
            'title': response_json["Title"],
            'rating': float(response_json["imdbRating"]) if response_json["imdbRating"] != "N/A" else -1,
            'director': response_json["Director"],
            # There is no risk of ID conflict here, as we use hyphens ("-")
            # in our movies' IDs, and OMDb does not in the IMDb IDs of theirs.
            'id': response_json["imdbID"]
        }
        return make_response(jsonify(response_data),200)
    return make_response(jsonify({"error":"the OMDb API encountered an error when processing the request"}),400)


@app.route("/omdb/<movieid>", methods=['GET'])
def omdb_movie_by_id(movieid):
    """
    Ninth entry point : requesting the OMDb API (https://www.omdbapi.com/) through
    a GET method HTTP request, to retrieve the data of the movie with the
    specified IMDb ID. If no such movie is found, an error is returned.

    :param movieid: string
    :return: data about the specified movie, by IMDb ID
    """
    req_url = "http://www.omdbapi.com/?apikey=39f879ba&i=" + movieid
    response = requests.get(req_url)
    response_json = response.json()
    # When certain errors occur, the OMDb API still returns
    # a response with a 200 status code, so it is necessary
    # to check for an "Error" field in the response.
    if response.status_code == 200 and "Error" not in response_json:
        response_data = {
            'title': response_json["Title"],
            'rating': float(response_json["imdbRating"]) if response_json["imdbRating"] != "N/A" else -1,
            'director': response_json["Director"],
            # There is no risk of ID conflict here, as we use hyphens ("-")
            # in our movies' IDs, and OMDb does not in the IMDb IDs of theirs.
            'id': response_json["imdbID"]
        }
        return make_response(jsonify(response_data),200)
    return make_response(jsonify({"error":"the OMDb API encountered an error when processing the request"}),400)

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
