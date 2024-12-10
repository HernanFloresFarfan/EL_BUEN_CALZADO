from flask import request, redirect, url_for, Blueprint, flash,render_template
from datetime import datetime
from models.producto_model import Producto
from models.compra_model import Compra
from views import compra_view

compra_bp = Blueprint('compra', __name__, url_prefix="/compras")

@compra_bp.route("/")
def index():
    """Recupera todos los registros de compras."""
    compras = Compra.get_all()
    return compra_view.list(compras)

@compra_bp.route("/create", methods=['GET', 'POST'])
def create():
    """Crea un nuevo registro de compra."""
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        precio_compra = float(request.form['precio_compra'])
        fecha_str = request.form['fecha']
        proveedor = request.form['proveedor']

        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Fecha inválida. Usa el formato AAAA-MM-DD.", "error")
            return redirect(url_for('compra.create'))

        # Recuperar el producto para verificar si existe
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('compra.create'))

        # Crear la compra
        compra = Compra(
            producto_id=producto_id,
            cantidad=cantidad,
            precio_compra=precio_compra,
            fecha=fecha,
            proveedor=proveedor
        )
        compra.save()

        # Actualizar el stock del producto
        producto.update(stock=producto.stock + cantidad)

        flash("Compra registrada exitosamente.", "success")
        return redirect(url_for('compra.index'))

    # Pasar todos los productos disponibles al formulario
    productos = Producto.query.all()
    return compra_view.create(productos)

@compra_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """Edita un registro de compra existente."""
    compra = Compra.get_by_id(id)
    if not compra:
        flash("Compra no encontrada.", "error")
        return redirect(url_for('compra.index'))

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        nueva_cantidad = int(request.form['cantidad'])
        precio_compra = float(request.form['precio_compra'])
        fecha_str = request.form['fecha']
        proveedor = request.form['proveedor']

        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Fecha inválida. Usa el formato AAAA-MM-DD.", "error")
            return redirect(url_for('compra.edit', id=id))

        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('compra.edit', id=id))

        # Calcular la diferencia en el stock
        diferencia = nueva_cantidad - compra.cantidad

        # Actualizar la compra
        compra.update(
            producto_id=producto_id,
            cantidad=nueva_cantidad,
            precio_compra=precio_compra,
            fecha=fecha,
            proveedor=proveedor
        )

        # Actualizar el stock del producto
        producto.update(stock=producto.stock + diferencia)

        flash("Compra actualizada exitosamente.", "success")
        return redirect(url_for('compra.index'))

    productos = Producto.query.all()
    return compra_view.edit(compra, productos)

@compra_bp.route("/delete/<int:id>")
def delete(id):
    """Elimina un registro de compra."""
    compra = Compra.get_by_id(id)
    if not compra:
        flash("Compra no encontrada.", "error")
        return redirect(url_for('compra.index'))

    # Recuperar el producto para actualizar el stock
    producto = Producto.get_by_id(compra.producto_id)
    if producto:
        producto.update(stock=producto.stock - compra.cantidad)

    compra.delete()

    flash("Compra eliminada exitosamente.", "success")
    return redirect(url_for('compra.index'))