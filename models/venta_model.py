from database import db
from sqlalchemy.orm import relationship  # Asegúrate de importar relationship

class Venta(db.Model):
    __tablename__ = "ventas"
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)  # Nuevo campo
    fecha = db.Column(db.DateTime, nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # Nuevo campo
    
    # Relaciones
    cliente = db.relationship('Cliente', back_populates='ventas')
    producto = db.relationship('Producto', back_populates='ventas')
    empleado = db.relationship('Usuario', back_populates='ventas')  # Relación con usuarios
    facturas = db.relationship('Factura', back_populates='venta')  # Relación uno a uno con facturas
    
    def __init__(self, cliente_id, producto_id, cantidad, total, fecha, empleado_id):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha
        self.empleado_id = empleado_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod    
    def get_all():
        return Venta.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Venta.query.get(id)
    
    def update(self, cliente_id=None, producto_id=None, cantidad=None, total=None, fecha=None, empleado_id=None):
        if cliente_id:
            self.cliente_id = cliente_id
        if producto_id:
            self.producto_id = producto_id
        if cantidad is not None:
            self.cantidad = cantidad
        if total is not None:
            self.total = total
        if fecha:
            self.fecha = fecha
        if empleado_id:
            self.empleado_id = empleado_id
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
