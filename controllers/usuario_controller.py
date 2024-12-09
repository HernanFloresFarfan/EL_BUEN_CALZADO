from flask import request,redirect,url_for,Blueprint

from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint('usuario', __name__,url_prefix="/usuarios")

ROLES_VALIDOS = ['admin', 'empleado']

@usuario_bp.route("/")
def index():
    #Recupera todos los registros de  usuarios
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre =  request.form['nombre']
        username =  request.form['username']
        password = request.form['password']
        rol= request.form['rol']
        
        if rol not in ROLES_VALIDOS:
            return "Rol no válido", 400
        
        usuario =  Usuario(nombre,username,password,rol)
        usuario.save()
        return redirect(url_for('usuario.index'))
        
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    usuario = Usuario.get_by_id(id)
    if request.method == 'POST':
        nombre =  request.form['nombre']
        username =  request.form['username']
        password = request.form['password']
        rol= request.form['rol']
        
        if rol not in ROLES_VALIDOS:
            return "Rol no válido", 400
        
        #Actualizar
        usuario.update(nombre=nombre,username=username,password=password,rol=rol)
        return redirect(url_for('usuario.index'))
        
    return usuario_view.edit(usuario)

@usuario_bp.route("/delete/<int:id>")
def delete(id):
    usuario = Usuario.get_by_id(id)
    
    if usuario.ventas:  # Verifica si tiene ventas asociadas
        return "No se puede eliminar el usuario porque tiene ventas asociadas", 400
    
    usuario.delete()
    return redirect(url_for('usuario.index'))

@usuario_bp.route("/<int:id>/ventas")
def ventas(id):
    usuario = Usuario.get_by_id(id)
    ventas = usuario.ventas  # Relación con ventas
    return usuario_view.ventas(usuario, ventas)

@usuario_bp.route("/empleados")
def empleados():
    empleados = Usuario.query.filter_by(rol='empleado').all()
    return usuario_view.list(empleados)