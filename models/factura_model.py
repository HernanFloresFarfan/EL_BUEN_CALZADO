from database import db

class Factura(db.Model):
    __tablename__ = "facturas"
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)  # Nuevo campo para el subtotal
    descuento = db.Column(db.Float, nullable=False, default=0.0)  # Nuevo campo para descuento
    total = db.Column(db.Float, nullable=False)  # Total después del descuento
    monto_ingreso = db.Column(db.Float, nullable=False, default=0.0)  # Monto ingresado por el cliente
    cambio = db.Column(db.Float, nullable=False, default=0.0)  # Cambio calculado
    fecha = db.Column(db.Date, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    
    # Relaciones con otras tablasventa = db.relationship('Venta', back_populates='factura')  # Relación inversa con Ventaventa = db.relationship('Venta', back_populates='factura')  # Relación inversa con Venta
    cliente = db.relationship('Cliente', back_populates='facturas')
    producto = db.relationship('Producto', back_populates='facturas')
    venta = db.relationship('Venta', back_populates='facturas')  # Relación inversa con Venta

    def __init__(self, cliente_id, producto_id, cantidad, subtotal, descuento, total, monto_ingreso, cambio, fecha, venta_id=None):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.descuento = descuento
        self.total = total
        self.monto_ingreso = monto_ingreso
        self.cambio = cambio
        self.fecha = fecha
        if venta_id:
            self.venta_id = venta_id
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            print("Factura registrada correctamente")
        except Exception as e:
            db.session.rollback()  # Deshacer cualquier cambio en caso de error
            print(f"Error al guardar la factura: {e}")
            raise  # Propagar el error

    @staticmethod    
    def get_all():
        return Factura.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Factura.query.get(id)

    def update(self, cliente_id=None, producto_id=None, cantidad=None, subtotal=None, descuento=None, total=None, monto_ingreso=None, cambio=None, fecha=None, venta_id=None):
        if cliente_id:
            self.cliente_id = cliente_id
        if producto_id:
            self.producto_id = producto_id
        if cantidad:
            self.cantidad = cantidad
        if subtotal is not None:
            self.subtotal = subtotal
        if descuento is not None:
            self.descuento = descuento
        if total is not None:
            self.total = total
        if monto_ingreso is not None:
            self.monto_ingreso = monto_ingreso
        if cambio is not None:
            self.cambio = cambio
        if fecha:
            self.fecha = fecha
        if venta_id is not None:
            self.venta_id = venta_id
        
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    
    
