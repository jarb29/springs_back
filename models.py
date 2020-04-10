import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    apellido = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    direccion = db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(100), nullable = False)
    clave = db.Column(db.String(100), nullable = True)
    usuario_factura = db.relationship('Factura',  backref= 'detale_factura', lazy = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"usuario('{self.nombre}', '{self.apellido}', '{self.email}', '{self.direccion}', '{self.telefono}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "direccion": self.direccion,
            "telefono":self.telefono,
        }  



class Tienda(db.Model):
    __tablename__ = 'tienda'
    id = Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    rut = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(120), nullable = False, unique=True)
    latitude = db.Column(db.String(100), nullable = False, unique=True)
    longitude = db.Column(db.String(100), nullable = False, unique=True)
    clave = db.Column(db.String(100), nullable = False)
    productos_tienda = db.relationship('Productos', backref= 'productos_t', lazy = True)
  
    
    def __repr__(self):
        return f"Tienda('{self.nombre}', '{self.rut}', '{self.email}', '{self.latitude}', '{self.longitude}', '{self.categoria}', '{self.clave}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "rut": self.rut,
            "email": self.email,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "categoria": self.categoria,
        }  



class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False)
    avatar = db.Column(db.String(100), nullable = False, default = 'favicon.ico')
    stock = db.Column(db.String(100), nullable = False)
    precio = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    tienda_id = db.Column(db.Integer, db.ForeignKey('tienda.id'), nullable=False)
    factura_Productos = db.relationship('Detallefactura', backref= 'factura_p', lazy = True)

    def __repr__(self):
        return f"Productos('{self.nombre}', '{self.avatar}', '{self.stock}', '{self.precio}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "avatar": self.avatar,
            "stock": self.stock,
            "precio": self.precio,
            "categoria":self.categoria,
            "description":self.description,
        }  


class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    usuario_factura_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    factura_detalle = db.relationship('Detallefactura',  backref= 'detalle', lazy = True)
    total = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.id}"

    def serialize(self):
        return {
            "id": self.id,
             "usuario": self.usuario,
             "factura_detalle": self.factura_detalle,
             "total": self.total,
        }  


class Detallefactura(db.Model):
    __tablename__ = 'detallefactura'
    id = db.Column(db.Integer, primary_key=True)
    productos_comprados = db.Column(db.String(100), nullable = False)
    factura_id = db.Column(db.String(100), db.ForeignKey('factura.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    precio = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"Detallefactura('{self.id}')"

    def serialize(self):
        return {
            "id": self.id,
            "productos_comprados": self.productos_comprados,
            "factura_id": self.factura_id,
            "producto_id": self.producto_id ,
            "precio:": self.precio,
        }  



