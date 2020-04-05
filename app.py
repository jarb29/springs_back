import os
from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Usuario, Tienda, Productos, CategoriaProductos, CategoriaTienda, Factura, Detallefactura 
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
mail = Mail(app)
manager.add_command("db", MigrateCommand)


def allowed_file_images(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/api/loging', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':

        usuario = request.json.get('email', None)
        clave = request.json.get('clave', None)
        if not usuario:
            return jsonify({"msg": "Falta introducir el email"}), 400
        if not clave:
            return jsonify({"msg": "Falta introducir la clave"}), 400

        usua = Usuario.query.filter_by(email = usuario).first()

        if not usua:
            return jsonify({"msg": "Usuario no existe"}), 404

        if bcrypt.check_password_hash(usua.clave, clave):
            access_token = create_access_token(identity = usua.nombre)
            data = {
                "access_token": access_token,
                "Usuario": usua.serialize()
            }
            return jsonify(data), 200
        else:
            return jsonify({"msg": "email/ clave errados favor verificar"}), 401



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
    if not apellido:
        return jsonify({"msg": "Falta el apellido"}), 400
    if not email:
        return jsonify({"msg": "Falta el email"}), 400
    usua = Usuario.query.filter_by(email = email).first()
    if usua:
        return jsonify({"msg": "Usuario existe por favor elegir diferente Email"}), 400
    if not direccion:
        return jsonify({"msg": "Falta la direccion"}), 400
    if not telefono:
        return jsonify({"msg": "Falta el telefono"}), 400
    if not clave:
        return jsonify({"msg": "Falta la clave"}), 400
    

    
        
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
    return jsonify(data),  200
   



@app.route('/api/register/producto', methods=['POST'])
def producto():
    if not request.files:
        return jsonify({"msg": "No hay archivos"}), 400
    
    current_user = get_jwt_identity('id')
    usuario = request.form.get('nombre', None)
    stock = request.form.get('stock', None)
    precio = request.form.get('precio', None)
    file = request.files['avatar']

    if file:
        if file.filename == '': 
            return jsonify({"msg": "Agregar nombre a la foto"}), 400

    if not usuario or usuario =='':
        return jsonify({"msg": "Falta el nombre del producto"}), 400
    if not stock or stock == '':
        return jsonify({"msg": "Falta la cantidad dsiponible "}), 400
    if not precio or precio == '':
        return jsonify({"msg": "Falta el precio"}), 400
    
    if file and allowed_file_images(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename))

    usua = Productos.query.filter_by(nombre = usuario).first()

    if usua:
        return jsonify({"msg": "EL producto ya existe"}), 400
        
    usua = Productos()
    usua.nombre = usuario 
    usua.stock = stock
    usua.precio = precio

    if file:
        usua.avatar = filename


    db.session.add(usua)
    db.session.commit()
     
    data = {

        "Producto": usua.serialize()
   
    }
    return jsonify(data), 200

@app.route('/api/productos', methods=['GET'])
def productos():
    listaProductos = Productos.query.get(productos)
    return jsonify(listaPproductos.serialize()), 200




@app.route('/api/registerTienda', methods=['POST'])
def registerTienda():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    usuario = request.json.get('nombre', None)
    categoria = request.json.get('categoria', None)
    rut = request.json.get('rut', None)
    email = request.json.get('email', None)
    latitude = request.json.get('latitude', None)
    longitude = request.json.get('longitude', None)
    clave = request.json.get('clave', None)
  


    if not usuario:
        return jsonify({"msg": "Falta el nombre de la Tienda"}), 400
    if not categoria:
        return jsonify({"msg": "Falta la categoria de la Tienda"}), 400
    if not rut:
        return jsonify({"msg": "Falta el rut de la Tienda"}), 400
    usua_rut = Tienda.query.filter_by(rut = rut).first()
    if usua_rut:
        return jsonify({"msg": "Favor proveer Rut valido"}), 400
    if not email:
        return jsonify({"msg": "Falta el Email de la Tienda"}), 400
    usua = Tienda.query.filter_by(email = email).first()
    if usua:
        return jsonify({"msg": "Usuario existe por favor elegir un Email diferente"}), 400
    if not latitude:
        return jsonify({"msg": "Falta la latitude de la Tienda"}), 400
    if not longitude:
        return jsonify({"msg": "Falta el longitud de la Tienda"}), 400
    if not clave:
        return jsonify({"msg": "Falta la clave"}), 400
    

    
        
    usua = Tienda()
    usua.nombre = usuario
    usua.clave = bcrypt.generate_password_hash(clave) 
    usua.categoria = categoria
    usua.rut = rut
    usua.email = email
    usua.latitude = latitude
    usua.longitude = longitude
    db.session.add(usua)
    db.session.commit()
    access_token = create_access_token(identity=usua.nombre)
   
     
    data = {
        "access_token": access_token,
        "Tienda": usua.serialize()
    }
    return jsonify(data),  200




@app.route('/api/logingTienda', methods=['POST'])
def logingTienda():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':

        usuario = request.json.get('email', None)
        clave = request.json.get('clave', None)
        if not usuario:
            return jsonify({"msg": "Falta introducir el email"}), 400
        if not clave:
            return jsonify({"msg": "Falta introducir la clave"}), 400

        usua = Tienda.query.filter_by(email = usuario).first()

        if not usua:
            return jsonify({"msg": "Usuario no existe"}), 404

        if bcrypt.check_password_hash(usua.clave, clave):
            access_token = create_access_token(identity = usua.nombre)
            data = {
                "access_token": access_token,
                "Tienda": usua.serialize()
            }
            return jsonify(data), 200
        else:
            return jsonify({"msg": "email/ clave errados favor verificar"}), 401



@app.route('/api/mapa', methods=['GET'])
@jwt_required
def protected():

    datosProductos = Tienda.query.all()
    datosProductos = list(map(lambda datosProductos: datosProductos.serialize(), datosProductos))
    
    return jsonify(datosProductos), 200













if __name__ == '__main__':
    manager.run()


