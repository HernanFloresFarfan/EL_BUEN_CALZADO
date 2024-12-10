import os
from flask import request, redirect, url_for, Blueprint, flash
from models.producto_model import Producto
from views import producto_view

# Configuración del Blueprint
producto_bp = Blueprint('producto', __name__, url_prefix="/productos")

@producto_bp.route("/")
def index():
    """Lista todos los productos."""
    productos = Producto.get_all()
    return producto_view.list(productos)

@producto_bp.route("/create", methods=['GET', 'POST'])
def create():
    """Crea un nuevo producto."""
    if request.method == 'POST':
        # Captura los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        # Crear un nuevo producto
        producto = Producto(nombre, descripcion, precio, stock)
        producto.save()
        flash("Producto creado exitosamente.", "success")
        return redirect(url_for('producto.index'))

    return producto_view.create()

@producto_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """Edita un producto existente."""
    producto = Producto.get_by_id(id)
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for('producto.index'))
    
    if request.method == 'POST':
        # Captura los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        # Actualizar el producto
        producto.update(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock)
        flash("Producto actualizado exitosamente.", "success")
        return redirect(url_for('producto.index'))

    return producto_view.edit(producto)

@producto_bp.route("/delete/<int:id>")
def delete(id):
    """Elimina un producto existente."""
    producto = Producto.get_by_id(id)
    if not producto:
        flash("Producto no encontrado.", "error")
    else:
        producto.delete()
        flash("Producto eliminado exitosamente.", "success")
    return redirect(url_for('producto.index'))
