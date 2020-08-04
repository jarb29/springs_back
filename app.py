import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Payments
from flask_mail import Mail, Message
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests




BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)



JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
mail = Mail(app)
manager.add_command("db", MigrateCommand)



@app.route('/')
def root():
    return render_template('index.html')


@app.route('/api/payments', methods=['POST'])
@limiter.limit("10/second")
def created():
    if not request.is_json:
        return jsonify({"msg": "Bad request"}), 400
    if request.method == 'POST':
        r = requests.get("https://mindicador.cl/api").json()
        valor_uf = r['uf']['valor']
        
        name = request.json.get('name', None)
        lastName = request.json.get('lastName', None)
        description = request.json.get('description', None)
        serviceHour = request.json.get('serviceHour', None)
        amountOfService = serviceHour * valor_uf 
        dayAmmountUf = valor_uf 

        if not name:
            return jsonify({"msg": "Name Not Found"}), 404
        if not lastName:
            return jsonify({"msg": "lastName Not Found"}), 400
        if not description:
            return jsonify({"msg": "description Not Found"}), 400
        if not serviceHour:
            return jsonify({"msg": "serviceHour Not Found"}), 400
        if not amountOfService:
            return jsonify({"msg": "amountOfService Not Found"}), 400
        if not dayAmmountUf:
            return jsonify({"msg": "dayAmmountUf  Not Found"}), 400
        
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


@app.route('/api/allPayments', methods=['GET'])
@limiter.limit("10/second")
def get_all():
    listaPayments = Payments.query.all()
    if not listaPayments:
        return jsonify({"msg": "Not Found"}), 404
    listaPayments = list(map(lambda listaPayments: listaPayments.serialize(), listaPayments))
    return jsonify(listaPayments), 200


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
    amountOfService = request.json.get('amountOfService', None)
    dayAmmountUf = request.json.get('dayAmmountUf', None)
    

    if name != '':
        editPayment.name = name
    if description !='':
        editPayment.description = description
    if lastName  !='':
        editPayment.lastName = lastName 
    if serviceHour !='':
        editPayment.serviceHour = serviceHour
    if amountOfService != '':
        editPayment.amountOfService = amountOfService
    db.session.commit()
    return jsonify({"msg": "Payment update succesfuly"}), 200



if __name__ == '__main__':
    manager.run()


