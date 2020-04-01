import os
from flask import Flask, render_template, jsonify, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Usuario, Tienda, Productos, CategoriaProductos, CategoriaTienda, Factura, Detallefactura 
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token)
from flask_bcrypt import Bcrypt



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
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


@app.route('/api/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    usuario = request.json.get('nombre', None)
    clave = request.json.get('clave', None)
    if not usuario:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not clave:
        return jsonify({"msg": "Missing password parameter"}), 400

    usua = Usuario.query.filter_by(nombre = usuario).first()

    if not usua:
        return jsonify({"msg": "Usuario no existe"}), 404

    if bcrypt.check_password_hash(usua.clave, clave):
        access_token = create_access_token(identity = usuario)
        data = {
            "access_token": access_token,
            "Usuario": usua.serialize()
        }
        return jsonify(data), 200

    else:
        return jsonify({"msg": "Usuario errado"}), 401



@app.route('/api/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    usuario = request.json.get('nombre', None)
    clave = request.json.get('clave', None)
    apellido = request.json.get('apellido', None)
    email = request.json.get('email', None)
    direccion = request.json.get('direccion', None)
    telefono = request.json.get('telefono', None)


    if not usuario:
        return jsonify({"msg": "Falta el nombre"}), 400
    if not clave:
        return jsonify({"msg": "Falta la clave"}), 400

    usua = Usuario.query.filter_by(nombre = usuario).first()

    if usua:
        return jsonify({"msg": "Usuario existe"}), 400
        
    usua = Usuario()
    usua.nombre = usuario
    usua.clave = bcrypt.generate_password_hash(clave) 
    usua.apellido = apellido
    usua.email = email
    usua.direccion = direccion
    usua.telefono = telefono
    db.session.add(usua)
    db.session.commit()
    access_token = create_access_token(identity=usua.nombre)
     
    data = {
        "access_token": access_token,
        "Usuario": usua.serialize()
    }
    return jsonify(data), 200
   

if __name__ == '__main__':
    manager.run()


