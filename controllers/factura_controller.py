from flask import request, redirect, url_for, flash, Blueprint, render_template
from datetime import datetime
from models.factura_model import Factura
from models.cliente_model import Cliente
from models.producto_model import Producto
from models.venta_model import Venta
from views import factura_view

factura_bp = Blueprint('factura', __name__, url_prefix="/facturas")

@factura_bp.route("/")
def index():
    """Recupera todos los registros de facturas."""
    facturas = Factura.get_all()
    clientes = Cliente.query.all()  # Obtener todos los clientes
    productos = Producto.query.all()  # Obtener todos los productos
    ventas = Venta.query.all()
    return factura_view.render_facturas(facturas=facturas, clientes=clientes, productos=productos, ventas=ventas)

@factura_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']
        venta_id = request.form['venta_id']
        
        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return redirect(url_for('factura.create'))

        # Validar cliente
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            flash("Cliente no encontrado.", "error")
            return redirect(url_for('factura.create'))

        # Validar producto
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.create'))
        
        # Validar venta_id
        venta = Venta.query.get(venta_id)
        if not venta:
            flash("Venta no encontrada.", "error")
            return redirect(url_for('factura.create'))

        if cantidad <= 0:
            flash("La cantidad debe ser mayor que cero.", "error")
            return redirect(url_for('factura.create'))

        if cantidad > producto.stock:
            flash(f"Stock insuficiente. Disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.create'))

        # Crear factura
        total = producto.precio * cantidad
        factura = Factura(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, total=total, fecha=fecha, venta_id=venta_id)
        factura.save()

        # Actualizar stock del producto
        producto.update(stock=producto.stock - cantidad)

        flash("Factura registrada exitosamente.", "success")
        return redirect(url_for('factura.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    ventas = Venta.query.all()
    return factura_view.create(clientes, productos, ventas)


@factura_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """Edita una factura existente."""
    factura = Factura.get_by_id(id)
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for('factura.index'))

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        nueva_cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']
        venta_id = request.form['venta_id']
        #fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return redirect(url_for('factura.edit', id=id))

        # Validar producto
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.edit', id=id))

        # Validar diferencia de cantidad
        diferencia = nueva_cantidad - factura.cantidad
        if diferencia > 0 and diferencia > producto.stock:
            flash(f"No hay suficiente stock para este cambio. Stock disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.edit', id=id))
        
        # Validar venta_id
        venta = Venta.query.get(venta_id)
        if not venta:
            flash("Venta no encontrada.", "error")
            return redirect(url_for('factura.edit', id=id))

        total = producto.precio * nueva_cantidad

        # Actualizar la factura, incluyendo el venta_id
        factura.update(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=nueva_cantidad,
            total=total,
            fecha=fecha,
            venta_id=venta_id  # Actualizar el venta_id también
        )

        # Actualizar el stock del producto
        producto.update(stock=producto.stock - diferencia)

        flash("Factura actualizada exitosamente.", "success")
        return redirect(url_for('factura.index'))
    
    
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    ventas = Venta.query.all()
    return factura_view.edit(factura, clientes, productos)

@factura_bp.route("/delete/<int:id>")
def delete(id):
    """Elimina una factura."""
    factura = Factura.get_by_id(id)
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for('factura.index'))

    producto = Producto.get_by_id(factura.producto_id)
    if producto:
        producto.update(stock=producto.stock + factura.cantidad)

    factura.delete()

    flash("Factura eliminada exitosamente.", "success")
    return redirect(url_for('factura.index'))
