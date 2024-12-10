from database import db

# En producto_model.py
from models.compra_model import Compra

class Producto(db.Model):
    __tablename__ = "productos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float(11, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    
    # Relación con la tabla "ventas"
    ventas = db.relationship('Venta', back_populates='producto')
    compras = db.relationship('Compra', back_populates='producto')
    facturas = db.relationship('Factura', back_populates='producto')
    
    def __init__(self, nombre, descripcion, precio, stock):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Producto.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)
    
    def update(self, nombre=None, descripcion=None, precio=None, stock=None):
        if nombre:
            self.nombre = nombre
        if descripcion:
            self.descripcion = descripcion
        if precio:
            self.precio = precio
        if stock:
            self.stock = stock
            
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
