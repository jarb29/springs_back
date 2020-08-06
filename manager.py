import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Payments
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import re, string

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

########## Conexion con la base de datos;##########
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Jarb",
    password="Alexander29",
    hostname="Jarb.mysql.pythonanywhere-services.com",
    databasename="Jarb$SpringPrueba",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#########Funcion optional para delimitar el numero de hit para la app##########
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

CORS(app)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
########## Patro de valores de entrada deserviceHour ##########
pattern = re.compile("[\d{}]+$".format(re.escape(string.punctuation)))


########## Conexion con la API de los indicadores economicos##########
r = requests.get("https://mindicador.cl/api").json()
valor_uf = r['uf']['valor']


##########Rutas ##########
@app.route('/')
def root():
    return render_template('index.html')


########## Creando Pagos##########
@app.route('/api/payments', methods=['POST'])
@limiter.limit("10/second")
def created():
    if not request.is_json:
        return jsonify({"msg": "Bad request"}), 400
    if request.method == 'POST':
        name = request.json.get('name', None)
        lastName = request.json.get('lastName', None)
        description = request.json.get('description', None)
        serviceHour = request.json.get('serviceHour', None)

        if not pattern.match(serviceHour):
            return jsonify({"msg": "ServiceHour must be a number"}), 400

        amountOfService = float(serviceHour) * float(valor_uf)
        dayAmmountUf = valor_uf

        if not name:
            return jsonify({"msg": "Name Not Found"}), 400
        if not lastName:
            return jsonify({"msg": "lastName Not Found"}), 400
        if not description:
            return jsonify({"msg": "description Not Found"}), 400
        if not serviceHour:
            return jsonify({"msg": "serviceHour Not Found"}), 400


        usua = Payments()
        usua.name = name
        usua.lastName = lastName
        usua.description = description
        usua.serviceHour = serviceHour
        usua.amountOfService = amountOfService
        usua.dateAmmountUF =dayAmmountUf
        db.session.add(usua)
        db.session.commit()
        return jsonify({"msg": "payment created"}), 201


##########Funcio para buscar o borrar pagos por ID##########
@app.route('/api/payments/<int:id>', methods=['GET', 'DELETE'])
@limiter.limit("10/second")
def get_products(id):
    if not request.is_json:
        return jsonify({"msg": "Bad request"}), 400

    if request.method == 'GET':
        listaProductos = Payments.query.filter_by(id=id).all()
        if not listaProductos :
            return jsonify({"msg": "id Not Found"}), 404
        listaProductos = list(map(lambda listaProductos: listaProductos.serialize(), listaProductos))
        return jsonify(listaProductos), 200

    if request.method == 'DELETE':
        deleteProducto = Payments.query.filter_by(id=id).first()
        if not deleteProducto:
            return jsonify({"msg": "id Not Found"}), 404

        db.session.delete(deleteProducto)
        db.session.commit()
        return jsonify({"msg": "Producto eliminado"}), 200


##########funcion para obtener todos los pagos##########
@app.route('/api/allPayments', methods=['GET'])
@limiter.limit("10/second")
def get_all():
    listaPayments = Payments.query.all()
    if not listaPayments:
        return jsonify({"msg": "Not Found"}), 404
    listaPayments = list(map(lambda listaPayments: listaPayments.serialize(), listaPayments))
    return jsonify(listaPayments), 200


##########Funcion para actualizar los pagos por id##########
@app.route('/api/payments/<int:id>', methods=['PUT'])
@limiter.limit("10/second")
def editarPayment(id):
    if not request.is_json:
        return jsonify({"msg": "Bad request"}), 400

    editPayment = Payments.query.get(id)
    name = request.json.get('name', None)
    lastName = request.json.get('lastName', None)
    description = request.json.get('description', None)
    serviceHour = request.json.get('serviceHour', None)

    if not pattern.match(serviceHour):
            return jsonify({"msg": "ServiceHour must be a number"}), 400

    amountOfService = float(serviceHour) * float(valor_uf)
    dayAmmountUf = valor_uf

    if name != '':
        editPayment.name = name
    if description !='':
        editPayment.description = description
    if lastName  !='':
        editPayment.lastName = lastName
    if serviceHour !='':
        editPayment.serviceHour = serviceHour
        editPayment.amountOfService = amountOfService
        editPayment.dayAmmountUf  = dayAmmountUf
    db.session.commit()
    return jsonify({"msg": "Payment update succesfuly"}), 200


if __name__ == '__main__':
    manager.run()


