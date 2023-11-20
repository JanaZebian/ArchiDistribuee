# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
import booking_pb2
import booking_pb2_grpc


def get_booking_by_user_id(stub, userid):
    """
    USER acting as a client calling distant procedure to get a booking by a user id
    :param stub: Booking
    :param userid: string
    :return: none
    """
    booking = stub.GetBookingByUserID(userid)
    print(booking)


def get_bookings(stub):
    """
    User acting as a client calling distant method to get all the bookings in the database
    :param stub: Booking
    :return: none
    """
    bookings = stub.GetBookings(booking_pb2.EmptyData())
    for booking in bookings:
        print("UserId: %s " % booking.userid)
        print("Dates: %s" % booking.dates)
        print()


app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


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
    return make_response(jsonify({"message": "User added to the in database"}))


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# CALLING GraphQL requests
@app.route("/movielist/<userid>", methods=['GET'])
def getMovieList(userid):
    """
    User now makes GraphQL requests to the Movie server instead of REST requests to get the list of movies in the
    DataBase

    :param userid: string
    :return: json
    """
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


@app.route("/movieById/<userid>/<id>", methods=['GET'])
def get_movie_by_its_id(userid, id: str):
    for user in users:
        if str(user["id"]) == str(userid):
            print("You are gonna get connected to the movie server!")
            message = """query{
        movie_with_id(_id: "%s") {
            id
            title
            director
            rating
        }
    }""" % id
            response = requests.post("http://localhost:3001/graphql", json={'query': message})
            response_json = response.json()
            return make_response(jsonify(response_json), 200)
    return make_response(jsonify({"error": "UserId not available"}), 400)


if __name__ == "__main__":
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)

        print("-------------- GetMovies --------------")
        userid = booking_pb2.Id(id="dwight_schrute")
        get_booking_by_user_id(stub, userid)

        print("-------------- GetTimes --------------")
        get_bookings(stub)

    channel.close()
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
