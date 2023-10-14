# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
# import grpc
from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/movielist/<userid>", methods=['GET'])
def getMovieList(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            print("You are gonna get connected to the movie server!")
            message = """query{
    get_all_movies {
        title
        rating
        actors {
            id
            firstname
            lastname
            birthyear
        }
    }
}"""
            response = requests.post("http://localhost:3001/graphql", json={'query': message})
            response_json = response.json()
            return make_response(jsonify(response_json), 200)
    return make_response(jsonify({"error": "UserId not available"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
