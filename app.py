import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Usuario, Tienda, Productos, Factura, Detallefactura 
from flask_mail import Mail, Message
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
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'jarb29@gmail.com'
app.config['MAIL_PASSWORD'] = 'Amesti2020'


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
 
def send_mail(subject, sender, recipients, message):
    msg = Message(subject,
                  sender=sender,
                  recipients=[recipients])
    msg.html = message
    mail.send(msg)

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
    html = render_template('email-registerCliente.html', user=usua)
    send_mail("Registro", "jarb29@gmail.com", usua.email, html)




    access_token = create_access_token(identity=usua.nombre)
   
     
    data = {
        "access_token": access_token,
        "Usuario": usua.serialize()
    }
    return jsonify(data),  200
   



@app.route('/api/register/producto', methods=['POST'])
def producto():

    nombre = request.form.get('nombreProducto', None)
    description = request.form.get('descripcion', None)
    stock = request.form.get('stock', None)
    precio = request.form.get('precio', None)
    tienda_id = request.form.get('tienda_id', None)
    categoria = request.form.get('categoria', None)
    file = request.files['avatar']

  
    if file:
        if file.filename == '': 
            return jsonify({"msg": "Agregar nombre a la foto"}), 400
    if not nombre or nombre =='':
        return jsonify({"msg": "Falta el nombre del producto"}), 400
    if not description or description == '':
        return jsonify({"msg": "Falta la description "}), 400
    if not stock or stock == '':
        return jsonify({"msg": "Falta la cantidad disponible "}), 400
    if not precio or precio == '':
        return jsonify({"msg": "Falta el precio"}), 400
    if not tienda_id:
        return jsonify({"msg": "Falta el id de la tienda relacionada"}), 400
    if not categoria or categoria == '':
        return jsonify({"msg": "Falta la categoria"}), 400

    if file and allowed_file_images(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename))

    usua = Productos.query.filter_by(tienda_id=tienda_id, nombre = nombre).first()
   
    if usua:
        return jsonify({"msg": "EL producto ya existe"}), 400
    usua = Productos()
    usua.nombre = nombre 
    usua.stock = stock
    usua.description = description
    usua.precio = precio
    usua.categoria = categoria
    usua.tienda_id = tienda_id 

    if file:
        usua.avatar = filename

    db.session.add(usua)
    db.session.commit()
    data = {
        "Producto": usua.serialize()
    }
    return jsonify(data), 200



@app.route('/api/admin/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def productos(id):
    if request.method == 'GET':
        listaProductos = Productos.query.filter_by(tienda_id=id).all()
        listaProductos = list(map(lambda listaProductos: listaProductos.serialize(), listaProductos))
        return jsonify(listaProductos), 200
    
    if request.method == 'DELETE':
        deleteProducto = Productos.query.filter_by(id=id).first()
        db.session.delete(deleteProducto)
        db.session.commit()

        return jsonify({"msg": "Producto eliminado"}), 200


@app.route('/api/editar/producto/<int:id>', methods=['PUT'])
@jwt_required
def editarProducto(id):
    editProducto = Productos.query.get(id)

    nombre = request.form.get('nombre', None)
    description = request.form.get('descripcion', None)
    stock = request.form.get('stock', None)
    precio = request.form.get('precio', None)
    tienda_id = request.form.get('tienda_id', None)
    categoria = request.form.get('categoria', None)
    

    if nombre != '':
        editProducto.nombre = nombre
    if description !='':
        editProducto.description = description
    if stock !='':
        editProducto.stock = stock
    if precio != '':
        editProducto.precio = precio 

    db.session.commit()

    return ({'msg': 'Producto actualizado'})  



@app.route('/api/tienda/<int:id>', methods=['GET'])
@jwt_required
def tiendaSeleccionada(id):
    listaProductos = Productos.query.filter_by(tienda_id=id).all()
    listaProductos = list(map(lambda listaProductos: listaProductos.serialize(), listaProductos))
    return jsonify(listaProductos), 200


@app.route('/api/producto/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename)






@app.route('/api/tienda/<filename>')
def uploaded_fil(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename)







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
    html = render_template('email-registerTienda.html', user=usua)
    send_mail("Registro", "jarb29@gmail.com", usua.email, html)
    
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






@app.route('/api/checkout/<int:id>', methods=['PUT'])
def checkout(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    ItemCompradoId= request.json.get('ItemProductoCompradoId', None)
    CantidaProductoComprado = request.json.get('CantidaProductoComprado', None)
    precioProductoSeleccionado = request.json.get('precioProductoSeleccionado', None)
    usuario_id = request.json.get('usuario_id', None)
    totalFactura = request.json.get('totalFactura', None)

    productos = Productos.query.filter(Productos.id.in_(ItemCompradoId)).all()

    
 
    usua = Factura()
    usua.usuario_factura_id = usuario_id
    usua.total = totalFactura
    db.session.add(usua)
    db.session.commit()
       



    factura_id = str(Factura.query.order_by(Factura.id.desc()).first())
    print(factura_id)
    i=0
    for prod in productos:
        usua = Detallefactura()
        usua.productos_comprados = int(CantidaProductoComprado[i])
        usua.factura_id= factura_id
        usua.producto_id = int(ItemCompradoId[i])
        usua.precio = int(precioProductoSeleccionado[i])
        db.session.add(usua)
        db.session.commit()
        i=i+1


    i=0
    for prod in productos:
     
        prod.stock = int(prod.stock) - int(CantidaProductoComprado[i])
        i=i+1
        db.session.commit()

    datosProductos = Productos.query.filter_by(tienda_id = id).all()
    datosProductos = list(map(lambda datosProductos: datosProductos.serialize(), datosProductos))
    
    
    return jsonify(datosProductos), 200





















if __name__ == '__main__':
    manager.run()


