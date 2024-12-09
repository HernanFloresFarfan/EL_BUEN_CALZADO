from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contraseña = request.form['password']
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.verify_password(contraseña):
            session['user_id'] = usuario.id
            session['rol'] = usuario.rol
            if usuario.rol == 'empleado':
                return redirect(url_for('venta.index'))
            else:
                return redirect(url_for('usuario.index'))
        
        flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))
