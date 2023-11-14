from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

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
   # On vérifie que la commande soit valide (que le film
   # soit disponible à la date demandée).
   time_req = requests.get("http://localhost:3202/showmovies/" + req["date"])
   if not time_req.ok:
      return make_response(jsonify({"error": "the booking's movie is not available at the requested date"}), 410)
   else:
      utilisateur_trouve = False
      date_trouvee = False
      film_trouve = False
      # On recherche si l'utilisateur existe
      for booking in bookings:
         if str(booking["userid"]) == str(userid):
            utilisateur_trouve = True
            # On recherche si la date de la commande existe
            for bk_date in booking["dates"]:
               if str(bk_date["date"]) == str(req["date"]):
                  date_trouvee = True
                  # On recherche si le film de la commande existe
                  for movie_id_disp in bk_date["movies"]:
                     if str(movie_id_disp) == str(req["movieid"]):
                        film_trouve = True
                        return make_response(jsonify({"error": "the requested movie is already booked by that user"}),
                                             409)
                  if not film_trouve:
                     bk_date["movies"].append(req["movieid"])
                     return make_response(booking, 200)
            if not date_trouvee:
               # Ajout du nouvel élément à la liste dates
               new_dict = {
                  'date': req["date"],
                  'movies': [req["movieid"]]
               }
               booking["dates"].append(new_dict)
               return make_response(booking, 200)
      if not utilisateur_trouve:
         # Ajout de l'utilisateur à la liste des utilisateurs qui ont
         # réservé, et ajout de la réservation à la liste de réservations
         # de l'utilisateur
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
