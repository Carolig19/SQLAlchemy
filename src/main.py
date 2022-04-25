"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planetas, Favpeople, Favplanetas
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def getPeople():
    all_people = People.query.all()
    print = (all_people, 'holi')
    arreglo_people = list(map(lambda x:x.serialize(), all_people))
    
    return jsonify({"resultado": arreglo_people})

@app.route('/Favpeople', methods=['GET'])
def getPeopleFav():
    all_Favpeople = Favpeople.query.all()
    arreglo_fav = list(map(lambda x:x.serialize(), all_Favpeople))
    
    return jsonify({"resultado": arreglo_fav})

@app.route('/people/<int:people_id>', methods=['GET'])
def getPeopleID(people_id):
    one_people = People.query.get(people_id) #solo para un dato
    if one_people:
        return jsonify({"personaje": one_people.serialize()})
    else:
        return "te equivocaste, error"

@app.route('/favorite/people/<int:people_id>', methods =['POST']) #int: ID del personaje que quiero añadir a favoritos, método es un POST, mando datos adicionales (cuando doy like a un elemento, añado dato a una url)
def addFavPeople(people_id):
    user = request.get_json() #quiero el ID del usuario (a cuál agregarle el favorito)
    newFav = Favpeople() #newFav puede acceder a la clase Favpeople (las carpetitas)
    newFav.id_user = user.user_['id'] #instanciar el id del usuario que añadio el favorito. Usa paréntesis cuadrado pq es un diccionario (:S)
    newFav.uid_people = people_id #valor de la URL (ahí estará)

    db.session.add(newFav) #SQL Alchemy agregar un nuevo favorito 
    db.session.commit() #cuando sé que está correcto, se hace el commit
    return("todo salió bien :D")

@app.route('/favorite/people/<int:people_id>', methods =['DELETE'])
def deleteFavPeople(people_id):
    user = request.get_json()
    allFavs = Favpeople.query.filter_by(id_user=['id'], uid_people=people_id).all()
    

@app.route('/Planetas', methods=['GET'])
def getPlaneta():
    all_planetas = Planetas.query.all()
    print = (all_planetas, 'holi')
    arreglo_planetas = list(map(lambda x:x.serialize(), all_planetas))

@app.route('/Favplanetas', methods=['GET'])
def getPlanetasFav():
    all_Favplanetas = Favplanetas.query.all()
    arreglo_favp = list(map(lambda x:x.serialize(), all_Favpeople))
    
    return jsonify({"resultado": arreglo_favp})

@app.route('/people/<int:Planetas_id>', methods=['GET'])
def getPlanetasID(planetas_id):
    one_planeta = Planetas.query.get(planetas_id) #solo para un dato
    if one_planeta:
        return jsonify({"planetita": one_planeta.serialize()})
    else:
        return "te equivocaste, error"

@app.route('/favorite/Planetas/<int:Planetas_id>', methods =['POST']) #int: ID del planeta que quiero añadir a favoritos, método es un POST, mando datos adicionales (cuando doy like a un elemento, añado dato a una url)
def addFavPlanetas(Planetas_id):
    user = request.get_json() #quiero el ID del usuario (a cuál agregarle el favorito)
    newFavPlanetas = Favplanetas() #newFav puede acceder a la clase Favpeople (las carpetitas)
    newFavPlanetas.id_user = user.user_['id'] #instanciar el id del usuario que añadio el favorito. Usa paréntesis cuadrado pq es un diccionario (:S)
    newFavPlanetas.pid_planetas = Planetas_id #valor de la URL (ahí estará)

    db.session.add(newFavPlanetas) #SQL Alchemy agregar un nuevo favorito 
    db.session.commit() #cuando sé que está correcto, se hace el commit
    return("todo salió bien :D")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
