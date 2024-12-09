import os
from flask import request, redirect, url_for, Blueprint, flash
from werkzeug.utils import secure_filename
from models.producto_model import Producto
from views import producto_view

# Configuración del Blueprint
producto_bp = Blueprint('producto', __name__, url_prefix="/productos")

# Directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'static/uploads/productos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Crear el directorio de subida si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Valida si un archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        # Procesar la imagen subida
        imagen = request.files.get('imagen')
        #imagen_filename = 'no_disponible.png'  # Imagen predeterminada
        
        if imagen and allowed_file(imagen.filename):
            # Guardar la imagen con un nombre seguro
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
        else:
            imagen_filename = 'no_disponible.png'  # Imagen predeterminada si no se sube una imagen
        
        # Crear un nuevo producto
        producto = Producto(nombre, descripcion, precio, stock, imagen_filename)
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

        # Procesar la imagen subida
        imagen = request.files.get('imagen')
        imagen_filename = producto.imagen  # Mantener la imagen actual si no se sube una nueva
        
        if imagen and allowed_file(imagen.filename):
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            
        
        # Actualizar el producto
        producto.update(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, imagen=imagen_filename)
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
