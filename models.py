import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    apellido = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    direccion = db.Column(db.String(100), nullable = False, unique=True)
    telefono = db.Column(db.String(100), nullable = False)
    clave = db.Column(db.String(100), nullable = True)
    usuario = db.relationship('Tienda', backref= 'tienda', lazy = True)
    usuarioFactura = db.relationship('Factura',  backref= 'factura', lazy = True)

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
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    rut = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    direccion = db.Column(db.String(100), nullable = False, unique=True)
    telefono = db.Column(db.String(100), nullable = False, unique=True)
    clave = db.Column(db.String(100), nullable = False, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'))
    productos = db.relationship('Productos', backref= 'productos', lazy = True)
    tienda_id = db.Column(db.Integer, db.ForeignKey('CategoriaTienda.id'))

     def __repr__(self):
        return f"Tienda('{self.nombre}', '{self.rut}', '{self.email}', '{self.direccion}', '{self.telefono}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "rut": self.apellido,
            "email": self.email,
            "direccion": self.direccion,
            "telefono":self.telefono,
        }  






class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    foto = db.Column(db.String(100), nullable = False, unique=True)
    stock = db.Column(db.String(100), nullable = False, unique=True)
    precio = db.Column(db.String(100), nullable = False, unique=True)
    tienda_id = db.Column(db.Integer, db.ForeignKey('Tienda.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('CategoriaProductos.id'))

     def __repr__(self):
        return f"Productos('{self.nombre}', '{self.foto}', '{self.stock}', '{self.precio}', '{self.telefono}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "fot": self.foto,
            "stock": self.stock,
            "precio": self.precio,
         
        }  
     



class CategoriaProductos(db.Model):
    __tablename__ = 'categoriaProductos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable = False, unique=True)
    producto = db.relationship('Productos', backref= 'CategoryProduc', lazy = True)

     def __repr__(self):
        return f"CategoriaProductos('{self.id}', '{self.description}')"

    def serialize(self):
        return {
            "id":self.id,
            "description": self.description,
        }  

    


class CategoriaTienda(db.Model):
    __tablename__ = 'categoriaTienda'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable = False, unique=True)
    tiendaCategory = db.relationship('Tienda',  backref= 'categoria', lazy = True)
    
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
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'))
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
    factura_id = db.Column(db.Integer, db.ForeignKey('Factura.id'))

     def __repr__(self):
        return f"Detallefactura('{self.id}')"

    def serialize(self):
        return {
            "id": self.id,
        }  



