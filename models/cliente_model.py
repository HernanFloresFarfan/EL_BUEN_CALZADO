from database import db

# En models/cliente_model.py
from models.factura_model import Factura


class Cliente(db.Model):
    __tablename__ = "clientes"
    
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    ci_nit = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    telefono = db.Column(db.String(20),nullable=False)
    
    #Relacion con ventas
    facturas = db.relationship('Factura', back_populates='cliente')
    ventas = db.relationship('Venta',back_populates='cliente')

    
    
    def __init__(self, nombre, ci_nit, email,telefono):
        self.nombre = nombre
        self.ci_nit = ci_nit
        self.email = email
        self.telefono = telefono 
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod    
    def get_all():
        return Cliente.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Cliente.query.get(id)
    
    def update(self, nombre=None, ci_nit=None, email=None, telefono=None):
        if nombre:
            self.nombre = nombre
        if ci_nit:
            self.ci_nit = ci_nit
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()