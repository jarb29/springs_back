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
    usuario = db.relationship('Tienda', backref= 'tienda', lazy = True)
    usuariofactura = db.relationship('Factura',  backref= 'detale_factura', lazy = True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    productos_tienda = db.relationship('Productos', backref= 'productos_tienda', lazy = True)
    tienda_id = db.Column(db.Integer, db.ForeignKey('categoriatienda.id'))
    
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
    tienda_id = db.Column(db.Integer, db.ForeignKey('tienda.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('categoriaproductos.id'))

    def __repr__(self):
        return f"Productos('{self.nombre}', '{self.avatar}', '{self.stock}', '{self.precio}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "avatar": self.avatar,
            "stock": self.stock,
            "precio": self.precio,
        }  
     



class CategoriaProductos(db.Model):
    __tablename__ = 'categoriaproductos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable = False)
    producto = db.relationship('Productos', backref= 'CategoryProduc', lazy = True)

    def __repr__(self):
        return f"CategoriaProductos('{self.id}', '{self.description}')"

    def serialize(self):
        return {
            "id":self.id,
            "description": self.description,
        }  

    


class CategoriaTienda(db.Model):
    __tablename__ = 'categoriatienda'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable = False)
    tiendaCategory = db.relationship('Tienda',  backref= 'categoria_portienda', lazy = True)
    
    def __repr__(self):
        return f"CategoriaTienda('{self.id}', '{self.description}')"

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
        }  


class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    factura = db.relationship('Detallefactura',  backref= 'detalle', lazy = True)

    def __repr__(self):
        return f"Factura('{self.id}')"

    def serialize(self):
        return {
            "id": self.id,
        }  


class Detallefactura(db.Model):
    __tablename__ = 'detallefactura'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'))

    def __repr__(self):
        return f"Detallefactura('{self.id}')"

    def serialize(self):
        return {
            "id": self.id,
        }  



