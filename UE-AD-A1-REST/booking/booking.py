from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_bookings_for_user(userid):
    json = ""
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            json = booking["dates"]
    if not json:
        res = make_response(jsonify({"error": " user"
                                              " not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    # Checking the validity of the booking (checking if
    # the movie is available at the requested date).
    time_req = requests.get("http://localhost:3202/showmovies/" + req["date"])
    if not time_req.ok:
        return make_response(jsonify({"error": "the booking's movie is not available at the requested date"}), 410)
    else:
        user_found = False
        date_found = False
        movie_found = False

        # Checking if the user exists.
        for booking in bookings:
            if str(booking["userid"]) == str(userid):
                user_found = True
                # Checking if the booking's date exists.
                for bk_date in booking["dates"]:
                    if str(bk_date["date"]) == str(req["date"]):
                        date_found = True
                        # Checking if the booking's movie exists.
                        for available_movie_id in bk_date["movies"]:
                            if str(available_movie_id) == str(req["movieid"]):
                                movie_found = True
                                return make_response(
                                    jsonify({"error": "the requested movie is already booked by that user"}),
                                    409)

                        if not movie_found:
                            bk_date["movies"].append(req["movieid"])
                            return make_response(booking, 200)

                if not date_found:
                    # Adding new element to the "dates" list.
                    new_dict = {
                        'date': req["date"],
                        'movies': [req["movieid"]]
                    }
                    booking["dates"].append(new_dict)
                    return make_response(booking, 200)
        if not user_found:
            # Adding the user to the list of users that ordered, and
            # adding the booking to the user's list of bookings.
            new_dict = {
                'date': req["date"],
                'movies': [req["movieid"]]
            }
            new_booking = {
                'userid': userid,
                'dates': [new_dict]
            }
            bookings.append(new_booking)
            return make_response(new_booking, 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
