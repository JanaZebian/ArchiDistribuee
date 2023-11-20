from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


# Home page/ default route
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/booking/<userid>", methods=['GET'])
def get_booking_by_userid(userid):
    """
    Method to get in a json format the schedule of a movie from the Booking Service by passing <userid> as a string

    :param userid: string
    :return: json
    """
    for user in users:
        if str(user["id"]) == str(userid):
            r = requests.get("http://localhost:3201/booking")  # send the request and get a response
            rj = r.json()  # get the json from the response
            res = make_response(jsonify(rj), 200)
            return res
    return make_response(jsonify({"error": "Date or userid not available"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def add_in_booking(userid):
    """
    From the user service we question the Booking server to add an item in its database
    :param userid: string
    :return: json
    """
    for user in users:
        if user["id"] == userid:
            r = requests.post("http://localhost:3201/bookings/" + userid, json=request.get_json())
            rj = r.json()
            return make_response(jsonify(rj), 200)
    return make_response(jsonify({"error": "Couldn't find userid"}), 400)



@app.route("/getInfo/<userid>/<movieid>", methods=['GET'])
def get_info_on_movie(userid,movieid):
    """
    Get the info on a film by asking the Movie service and passing "userid" & "movietitle" as strings

    :param userid: string

    :param movieid: string
    :return: json
    """
    for user in users:
        if str(user["id"]) == str(userid):
            r = requests.get("http://localhost:3200/movies/" + movieid)
            rj = r.json()
            return make_response(jsonify(rj), 200)
    return make_response(jsonify({"Error": "At least one arg isn't available"}), 400)


@app.route("/moviebytitle/userid", methods=['GET'])
def get_movie_by_title(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            r = requests.get("http://localhost:3200/moviebytitle")
    return make_response(jsonify({"Error": "Userid doesn't exists"}), 400)

@app.route("/users/all", methods=['GET'])
def get_all_users():
    """
    Method that gets all the users from the users database
    :return: json
    """
    return make_response(jsonify(users), 200)


@app.route("/users/userid/<userid>", methods=['GET'])
def get_user_by_id(userid):
    """
    Method that returns a user by passing his id as an argument
    :param userid: string
    :return: json
    """
    for user in users:
        if user["id"] == userid:
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"Error": "Userid doesn't exist in the database"}), 400)


@app.route("/users/addUser/<userid>", methods=['POST'])
def add_user(userid):
    """
    Method that adds a user
    :param userid: string
    :return: json
    """
    req = request.get_json()
    for user in users:
        if user["id"] == userid:
            return make_response(jsonify({"Error": "Userid exists already in the database"}), 400)
    users.append(req)
    return make_response(jsonify({{"message": "User added to the in database"}}))


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
