import os
from flask import Flask, render_template, jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.route('/')
def root():
    return render_template('index.html')



    

@app.route('/api/users', methods = ['GET'])
def users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 209


if __name__ == '__main__':
    manager.run()


