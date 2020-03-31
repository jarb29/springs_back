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

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usuario = Usuario.query.filter_by(nombre=nombre).first()

    if not usuario:
        return jsonify({"msg": "User not found"}), 404

    if bcrypt.check_password_hash(usuario.contraseña, contraseña):
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=nombre)
        data = {
            "access_token": access_token,
            "user": usuario.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "Usuario errado"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    #if not request.files:
    #    return jsonify({"msg": "Missing FILES in request"}), 400

    #if not request.is_json:
    #    return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.form.get('username', None)
    password = request.form.get('password', None)

    file = request.files['avatar']
    if file:
        if file.filename == '':
            return jsonify({"msg": "Missing avatar parameter"}), 400

    if not username or username=="":
        return jsonify({"msg": "Missing username parameter"}), 400
    
    if not password or password=="":
        return jsonify({"msg": "Missing password parameter"}), 400

    if file and allowed_file_images(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'img/avatars'), filename))

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"msg": "User exists"}), 400

    user = User()
    user.username = username
    user.password = bcrypt.generate_password_hash(password)

    if file:
        user.avatar = filename

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.username)
    data = {
        "access_token": access_token,
        "user": user.serialize()
    }
    return jsonify(data), 200

    




if __name__ == '__main__':
    manager.run()


