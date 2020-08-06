import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:Jarb.mysql.pythonanywhere-services.com'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

########## Creado la tabla payments##########
class Payments(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    lastName = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False, unique=True)
    serviceHour = db.Column(db.Integer, nullable = False)
    amountOfService = db.Column(db.Integer, nullable = False)
    dateAmmountUF = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"usuario('{self.name}', '{self.lastName}', '{self.description}', '{self.serviceHour}', '{self.amountOfService}', '{self.amountOfService}', '{self.dateAmmountUF}')"

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "lastName": self.lastName,
            "description": self.description,
            "serviceHour": self.serviceHour,
            "amountOfService":self.amountOfService,
            "dateAmmountUF":self.dateAmmountUF,
            "date":self.date,
        }
