# UE-AD-A1-MIXTE

Ce projet représente un exemple d'utilisation d'APIs mixtes dans le cadre de la gestion de réservations de séances de cinéma. Il correspond au TP Mixte Vert, et contient 4 APIs : <br>1) une API REST "User" ayant pour rôle la gestion des utilisateurs
<br>2) une API gRPC "Booking" ayant pour rôle la gestion des réservations
<br>3) une API gRPC "Times" ayant pour rôle la gestion des horaires de passage des différents films proposés
<br>4) une API GraphQL "Movie", ayant pour rôle la gestion des films proposés.

L'API User consomme les APIs Movie et Booking. L'API Booking consomme l'API Times.

Pour lancer le code de ce projet, ouvrir 4 terminaux, tous dans le répertoire du projet.<br>Ensuite, effectuer les commandes suivantes dans le premier terminal :

cd movie<br>
python movie.py

puis les suivantes dans le second :

cd ..\showtime<br>
python showtime.py

puis les suivantes dans le troisième :

cd ..\booking<br>
python booking.py

puis les suivantes dans le quatrième :

cd ..\user<br>
python user.py
