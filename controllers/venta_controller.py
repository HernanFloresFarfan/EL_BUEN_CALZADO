from flask import request, redirect, url_for, Blueprint, flash, session
from datetime import datetime
from models.venta_model import Venta
from models.producto_model import Producto
from models.cliente_model import Cliente
from models.usuario_model import Usuario 
from views import venta_view

venta_bp = Blueprint('venta', __name__, url_prefix="/ventas")

@venta_bp.route("/")
def index():
    """Recupera todos los registros de ventas."""
    ventas = Venta.get_all()
    return venta_view.list(ventas)

@venta_bp.route("/create", methods=['GET', 'POST'])
def create():
    """Crea un nuevo registro de venta."""
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
            return redirect(url_for('venta.create'))

        if cantidad > producto.stock:
            flash(f"Stock insuficiente. Disponible: {producto.stock}.", "error")
            return redirect(url_for('venta.create'))

        # Calcular el total de la venta
        total = producto.precio * cantidad

        # Recuperar el empleado desde la sesión
        empleado_id = session.get('user_id')
        if not empleado_id:
            flash("Usuario no autenticado.", "error")
            return redirect(url_for('login'))

        # Crear la venta
        venta = Venta(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=cantidad,
            total=total,
            fecha=fecha,
            empleado_id=empleado_id
        )
        venta.save()

        # Actualizar el stock del producto
        producto.update(stock=producto.stock - cantidad)

        flash("Venta registrada exitosamente.", "success")
        return redirect(url_for('venta.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    empleados = Usuario.query.all()  # Agregar esto para obtener empleados
    return venta_view.create(clientes, productos, empleados)

@venta_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """Edita un registro de venta existente."""
    venta = Venta.get_by_id(id)
    if not venta:
        flash("Venta no encontrada.", "error")
        return redirect(url_for('venta.index'))

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        nueva_cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('venta.edit', id=id))

        diferencia = nueva_cantidad - venta.cantidad
        if diferencia > 0 and diferencia > producto.stock:
            flash(f"No hay suficiente stock para este cambio. Stock disponible: {producto.stock}.", "error")
            return redirect(url_for('venta.edit', id=id))

        total = producto.precio * nueva_cantidad

        venta.update(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=nueva_cantidad,
            total=total,
            fecha=fecha
        )
        producto.update(stock=producto.stock - diferencia)

        flash("Venta actualizada exitosamente.", "success")
        return redirect(url_for('venta.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return venta_view.edit(venta, clientes, productos)

@venta_bp.route("/delete/<int:id>")
def delete(id):
    """Elimina un registro de venta."""
    venta = Venta.get_by_id(id)
    if not venta:
        flash("Venta no encontrada.", "error")
        return redirect(url_for('venta.index'))

    producto = Producto.get_by_id(venta.producto_id)
    if producto:
        producto.update(stock=producto.stock + venta.cantidad)

    venta.delete()

    flash("Venta eliminada exitosamente.", "success")
    return redirect(url_for('venta.index'))
