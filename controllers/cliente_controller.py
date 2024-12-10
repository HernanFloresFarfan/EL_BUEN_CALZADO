from flask import request,redirect,url_for,Blueprint
from controllers.decorators import role_required
from models.cliente_model import Cliente
from views import cliente_view


cliente_bp = Blueprint('cliente', __name__,url_prefix="/clientes")

@cliente_bp.route("/")
@role_required(['admin', 'empleado'])
def index():
    #Recupera todos los registros de  clientes
    clientes = Cliente.get_all()
    return cliente_view.list(clientes)

@cliente_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre =  request.form['nombre']
        email =  request.form['email']
        telefono =  request.form['telefono']
        
        cliente =  Cliente(nombre,email,telefono)
        cliente.save()
        return redirect(url_for('cliente.index'))
        
    return cliente_view.create()

@cliente_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    cliente = Cliente.get_by_id(id)
    if request.method == 'POST':
        nombre =  request.form['nombre']
        email =  request.form['email']
        telefono =  request.form['telefono']
        
        #Actualizar
        cliente.update(nombre=nombre,email=email,telefono=telefono)
        return redirect(url_for('cliente.index'))
        
    return cliente_view.edit(cliente)

@cliente_bp.route("/delete/<int:id>")
def delete(id):
    cliente = Cliente.get_by_id(id)
    cliente.delete()
    return redirect(url_for('cliente.index'))