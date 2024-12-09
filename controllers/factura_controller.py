from flask import request, redirect, url_for, flash, Blueprint
from datetime import datetime
from models.factura_model import Factura
from models.cliente_model import Cliente
from models.producto_model import Producto
from views import factura_view

factura_bp = Blueprint('factura', __name__, url_prefix="/facturas")

@factura_bp.route("/")
def index():
    """Recupera todos los registros de facturas."""
    facturas = Factura.get_all()
    return factura_view.list(facturas)

@factura_bp.route("/create", methods=['GET', 'POST'])
def create():
    """Crea una nueva factura."""
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Recuperar el producto para validar stock
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.create'))

        if cantidad > producto.stock:
            flash(f"Stock insuficiente. Disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.create'))

        # Calcular el total de la factura
        total = producto.precio * cantidad

        # Crear la factura
        factura = Factura(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=cantidad,
            total=total,
            fecha=fecha
        )
        factura.save()

        # Actualizar el stock del producto
        producto.update(stock=producto.stock - cantidad)

        flash("Factura registrada exitosamente.", "success")
        return redirect(url_for('factura.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return factura_view.create(clientes, productos)

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
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.edit', id=id))

        diferencia = nueva_cantidad - factura.cantidad
        if diferencia > 0 and diferencia > producto.stock:
            flash(f"No hay suficiente stock para este cambio. Stock disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.edit', id=id))

        total = producto.precio * nueva_cantidad

        factura.update(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=nueva_cantidad,
            total=total,
            fecha=fecha
        )
        producto.update(stock=producto.stock - diferencia)

        flash("Factura actualizada exitosamente.", "success")
        return redirect(url_for('factura.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
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
