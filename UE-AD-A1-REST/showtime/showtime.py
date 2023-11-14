from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


# Service Home page, default route
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


# Get all showtimes in json format
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    res = make_response(jsonify(schedule), 200)
    return res


@app.route("/showmovies/<date>", methods=['GET'])
def get_movies_bydate(date):
    """
    Get the movies shown at <date> as a string in a json format

    :param date: string
    :return:
    """
    for time in schedule:
        if str(time["date"]) == str(date):
            res = make_response(jsonify(time), 200)
            return res
    return make_response(jsonify({"error": "No movies with this date has been found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
