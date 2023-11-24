# UE-AD-A1-MIXTE

Ce projet représente un exemple d'utilisation d'APIs mixtes dans le cadre de la gestion de réservations de séances de cinéma. Il correspond au TP Mixte Vert, et contient 4 APIs : -1) une API REST "User" ayant pour rôle la gestion des utilisateurs
2) une API gRPC "Booking" ayant pour rôle la gestion des réservations
3) une API gRPC "Times" ayant pour rôle la gestion des horaires de passage des différents films proposés
4) une API GraphQL "Movie", ayant pour rôle la gestion des films proposés.

L'API User consomme les APIs Movie et Booking. L'API Booking consomme l'API Times.

Pour lancer le code de ce projet, effectuer les commandes suivantes :

cd ..\showtime
python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. showtime.proto
cd UE-AD-A1-MIXTE\booking
python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. booking.proto

cd UE-AD-A1-MIXTE
