from database import db

class Factura(db.Model):
    __tablename__ = "facturas"
    
    id = db.Column(db.Integer, primary_key=True)
    # Clave foránea única
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    
    # Relaciones con otras tablasventa = db.relationship('Venta', back_populates='factura')  # Relación inversa con Ventaventa = db.relationship('Venta', back_populates='factura')  # Relación inversa con Venta
    cliente = db.relationship('Cliente', back_populates='facturas')
    producto = db.relationship('Producto', back_populates='facturas')
    venta = db.relationship('Venta', back_populates='facturas')  # Relación inversa con Venta

    def __init__(self, cliente_id, producto_id, cantidad, total, fecha,venta_id=None):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total = total
        self.fecha = fecha
        if venta_id:  # Solo asignar venta_id si no es None
            self.venta_id = venta_id
    
    def save(self):
        from models.cliente_model import Cliente
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():
        return Factura.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Factura.query.get(id)

    def update(self, cliente_id=None, producto_id=None, cantidad=None, total=None, fecha=None):
        if cliente_id:
            self.cliente_id = cliente_id
        if producto_id:
            self.producto_id = producto_id
        if cantidad:
            self.cantidad = cantidad
        if total:
            self.total = total
        if fecha:
            self.fecha = fecha
        if venta_id is not None:  # Asegurarse de que venta_id esté definido
            self.venta_id = venta_id  # Actualizar el venta_id si se pasa como argumento  # Asegurarse de actualizar el venta_id si es necesario
        
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
