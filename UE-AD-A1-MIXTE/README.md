# UE-AD-A1-MIXTE

This project is an example of usage of mixed APIs as part of the management of bookings in a movie theater. It corresponds to the Green Mixed practicum, and contains 4 APIs : <br>1) a  "User" REST API that is meant to manage users
<br>2) a "Booking" gRPC API that is meant to manage bookings
<br>3) a "Times" gRPC API that is meant to manage the different schedules at which the movies are broadcasted at the movie theater
<br>4) a "Movie" GraphQL API that is meant to manage the many movies that the movie theater displays.

The User API consumes the Movie and Booking APIs. The Booking API consumes the Times API.

To run the project's code, open 4 terminals in the project's folder.
<br>Then, run the following commands in the first terminal :

cd movie<br>
python movie.py

then run the following commands in the second one :

cd showtime<br>
python showtime.py

then run the following commands in the third one :

cd booking<br>
python booking.py

then run the following commands in the fourth one :

cd user<br>
python user.py

-------------------------------------Version française-------------------------------------

Ce projet est un exemple d'utilisation d'APIs mixtes dans le cadre de la gestion de réservations de séances de cinéma. Il correspond au TP Mixte Vert, et contient 4 APIs : <br>1) une API REST "User" ayant pour rôle la gestion des utilisateurs
<br>2) une API gRPC "Booking" ayant pour rôle la gestion des réservations
<br>3) une API gRPC "Times" ayant pour rôle la gestion des horaires de passage des différents films proposés
<br>4) une API GraphQL "Movie", ayant pour rôle la gestion des films proposés.

L'API User consomme les APIs Movie et Booking. L'API Booking consomme l'API Times.

Pour lancer le code de ce projet, ouvrir 4 terminaux, tous dans le répertoire du projet.<br>Ensuite, effectuer les commandes suivantes dans le premier terminal :

cd movie<br>
python movie.py

puis les suivantes dans le second :

cd showtime<br>
python showtime.py

puis les suivantes dans le troisième :

cd booking<br>
python booking.py

puis les suivantes dans le quatrième :

cd user<br>
python user.py

