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


# Method to get in a json format the schedule of a movie by passing <userid> as a string
@app.route("/booking/<userid>", methods=['GET'])
def get_booking_by_userid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            data = {"userid": userid}  # create
            r = requests.get("http://localhost:3201/booking", data=data)  # send the request and get a response
            rj = r.json()  # get the json from the response
            # rj["t"] access the json filed "t" and it has to be just like how it's written in the response
            res = make_response(jsonify(rj), 200)
            return res
    return make_response(jsonify({"error": "Date or userid not available"}), 400)


# Get the info on a film by asking the Movie service and passing "userid" & "movietitle" as strings
@app.route("/getInfo/<userid>/<movieid>", methods=['GET'])
def get_info_on_movie(userid,movieid):
    for user in users:
        if str(user["id"]) == str(userid):
            r = requests.get("http://localhost:3200/movies/" + movieid)
            rj = r.json()
            return make_response(jsonify(rj), 200)
    return make_response(jsonify({"Error": "At least one arg isn't available"}))


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
