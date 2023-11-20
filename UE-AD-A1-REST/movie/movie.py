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


# root message/ default that returns the list of movies in the database
@app.route("/", methods=["GET"])
def listofmovies():
    res = ""
    for movie in movies:
        res += movie["title"] + "<br>"
    return res


# first entry point: requesting through a get method a template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


# second entry point: requesting through a get method the movies' json database
@app.route("/json", methods=['GET'])
def get_json():
    return make_response(jsonify(movies), 200)


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """
    third entry point: requesting through a get method the information on a movie by his ID

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
     fourth entry point: requesting through a get accessor the information on a movie by passing its title in the path in a
json format

    :return: json
    """
    json = ""
    # making sure that the passed parameter is valid
    if request.args:
        req = request.args
        for movie in movies:
            # seeing if the title passed exists in the movies database
            if str(movie["title"]) == str(req["title"]):
                # selecting the movie
                json = movie
# checking if the movie title exists and if not return an error message with the corresponding status code 400 or 200
    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    """
    fifth entry point: through a post accessor requesting to add/create a movie by passing its ID

    :param movieid: string
    :return: json
    """
    # accessing the json database with the request method from Flask
    req = request.get_json()

    # checking whether the movie id exists already because if it does there's no need to have the same movie twice
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)
    # adding the movie to the database
    movies.append(req)
    return make_response(jsonify({"message": "movie added"}), 200)


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    """
    sixth entry point: through a PUT accessor modify the rating of a movie by passing its ID and new rating as argument in
the path

    :param movieid: string
    :param rate: float
    :return: json
    """
    for movie in movies:
        # like before checking if the movieID exists is necessary
        if str(movie["id"]) == str(movieid):
            # after the id is found, modify that movie's rating by giving it the rating passed as an argument
            movie["rating"] = int(rate)
            # status code 201 is to indicate that the request has succeeded and has led to the creation of a resource
            return make_response(jsonify(movie), 201)

    return make_response(jsonify({"error": "movie ID not found"}), 400)


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """
    seventh entry point: through the delete method, remove a movie also by passing its ID as an argument

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


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
