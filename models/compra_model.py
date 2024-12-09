from database import db

class Compra(db.Model):
    __tablename__ = "compras"
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_compra = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    proveedor = db.Column(db.String(100), nullable=False)
    
    # Relación con productos usando cadena
    producto = db.relationship('Producto', back_populates='compras')
    
    def __init__(self, producto_id, cantidad, precio_compra, fecha, proveedor):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.fecha = fecha
        self.proveedor = proveedor
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod    
    def get_all():
        return Compra.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Compra.query.get(id)
    
    def update(self, producto_id=None, cantidad=None, precio_compra=None, fecha=None, proveedor=None):
        if producto_id is not None:
            self.producto_id = producto_id
        if cantidad is not None:
            self.cantidad = cantidad
        if precio_compra is not None:
            self.precio_compra = precio_compra
        if fecha is not None:
            self.fecha = fecha
        if proveedor is not None:
            self.proveedor = proveedor
            
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
