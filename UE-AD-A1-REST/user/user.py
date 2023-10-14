from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/booking/<userid>", methods=['GET'])
def get_booking_by_userid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            data = {"userid": userid}  # create
            r = requests.get("http://localhost:3201/booking", data=data)  # send the request and get a response
            rj = r.json()  # get the json from the response
            # rj["t"] acceder au champs du json t has to be just like kif huwe 7atu 3ndu l reponse 3a format ligne 23
            res = make_response(jsonify(rj), 200)
            return res
    return make_response(jsonify({"error": "Date not available"}), 400)


# do another entry point

if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
