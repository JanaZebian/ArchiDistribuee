# UE-AD-A1-REST

This project is an example of usage of REST APIs as part of the management of bookings in a movie theater. It corresponds to the Red REST practicum, and contains 4 APIs : <br>1) a  "User" REST API that is meant to manage users
<br>2) a "Booking" REST API that is meant to manage bookings
<br>3) a "Times" REST API that is meant to manage the different schedules at which the movies are broadcasted at the movie theater
<br>4) a "Movie" REST API that is meant to manage the different movies that the movie theater broadcasts.

The User API consumes the Movie and Booking APIs. The Booking API consumes the Times API. Furthermore, the Movie API consumes the OMDb API (https://www.omdbapi.com/).

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

Ce projet représente un exemple d'utilisation d'APIs REST dans le cadre de la gestion de réservations de séances de cinéma. Il correspond au TP REST Rouge, et contient 4 APIs :
<br>1) une API REST "User" ayant pour rôle la gestion des utilisateurs
<br>2) une API REST "Booking" ayant pour rôle la gestion des réservations
<br>3) une API REST "Times" ayant pour rôle la gestion des horaires de projection des différents films proposés par le cinéma
<br>4) une API REST "Movie", ayant pour rôle la gestion des films proposés.

L'API User consomme les APIs Movie et Booking. L'API Booking consomme l'API Times. De plus, l'API Movie consomme l'API OMDb (https://www.omdbapi.com/).

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
