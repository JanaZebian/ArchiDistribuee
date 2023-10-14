from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# todo create elements for Ariadne
type_defs = load_schema_from_path('movie.graphql')
query = QueryType()  # créer les objets associés au schéma
mutation = MutationType()
movie = ObjectType('Movie')  # créer les objets associés au schéma
actor = ObjectType('Actor')
query.set_field('movie_with_id',
                r.movie_with_id)  # associer le "resolver" que nous avons codé à la requête associée dans le schéma
query.set_field('get_all_movies', r.get_all_movies) # lien
movie.set_field('actors', r.resolve_actors_in_movie)
mutation.set_field('update_movie_rate', r.update_movie_rate)
schema = make_executable_schema(type_defs, movie, query, mutation,
                                actor)  # nous créons un schéma dit exécutable avec les éléments précédents


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


#####
# graphql entry points

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    # todo to complete
    print("You are connected to the movie server from the user server!")
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)