# controllers/decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    """
    Decorador que restringe el acceso a una vista si el rol del usuario no es el especificado.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar si el usuario está logueado y tiene el rol adecuado
            if 'user_id' not in session:
                flash("Debes iniciar sesión para acceder a esta página.", "danger")
                return redirect(url_for('auth.login'))  # Redirige al login si no está logueado

            # Verificar el rol y la página que se está intentando acceder
            if role == 'empleado' and session.get('role') != 'empleado':
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for('home'))  # Redirige al home si no tiene el rol adecuado
            elif role == 'admin' and session.get('role') != 'admin':
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for('home'))  # Redirige al home si no tiene el rol adecuado

            return f(*args, **kwargs)
        return decorated_function
    return decorator

