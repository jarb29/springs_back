import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    apellido = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    direccion = db.Column(db.String(100), nullable = False, unique=True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    telefono = db.Column(db.String(100), nullable = False)
    clave = db.Column(db.String(100), nullable = True)


class Tienda(db.Model):
    __tablename__ = 'Tienda'
    tienda_id = Column(Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    rut = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    direccion = db.Column(db.String(100), nullable = False, unique=True)
    clave = db.Column(db.String(100), nullable = False, unique=True)
    usuario_id = db.Column(Integer, ForeignKey('usuario.id'))
    usuario = db.relationship(Usuario)

class Productos(db.Model):
    __tablename__ = 'Productos'
    producto_id = db.Column(Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable = False, unique=True)
    foto = db.Column(db.String(100), nullable = False, unique=True)
    stock = db.Column(db.String(100), nullable = False, unique=True)
    precio = db.Column(db.String(100), nullable = False, unique=True)
    clave = db.Column(db.String(100), nullable = False, unique=True)
    tienda_id = db.Column(Integer, ForeignKey('tienda.id'))
    tienda = db.relationship(Tienda)



class CategoriaProductos(db.Model):
    __tablename__ = 'CategoriaProductos'
    categoriaProducto_id = db.Column(Integer, primary_key=True)
    description = db.Column(db.String(100), nullable = False, unique=True)
    producto_id = db.Column(Integer, ForeignKey('producto.id'))
    producto = db.relationship(Productos)


class CategoriaTienda(db.Model):
    __tablename__ = 'CategoriaTienda'
    categoriaTienda_id = db.Column(Integer, primary_key=True)
    description = db.Column(db.String(100), nullable = False, unique=True)
    tienda_id = db.Column(Integer, ForeignKey('tienda.id'))
    tienda = db.relationship(Tienda)




class Factura(db.Model):
    __tablename__ = 'Factura'
    factura_id = db.Column(Integer, primary_key=True)
    usuario_id = db.Column(Integer, ForeignKey('usuario.id'))
    usuario = db.relationship(Usuario)


class Detallefactura(db.Model):
    __tablename__ = 'DetalleFactura'
    Deatallefactura_id = db.Column(Integer, primary_key=True)
    factura_id = db.Column(Integer, ForeignKey('factura.id '))
    factura = db.relationship(Factura)
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email

        }

