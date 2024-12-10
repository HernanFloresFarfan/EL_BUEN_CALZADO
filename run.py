from flask import Flask, request, session, redirect, url_for

from controllers import usuario_controller,cliente_controller,producto_controller,venta_controller

from controllers.auth_controller import auth_bp

from controllers.usuario_controller import usuario_bp

from controllers.compra_controller import compra_bp 

from controllers.factura_controller import factura_bp


from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///calzados.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de la clave secreta
app.secret_key = 'clave_secreta_super_segura'  # Cambia esto por una clave única y segura


db.init_app(app)

app.register_blueprint(auth_bp)
#app.register_blueprint(usuario_bp, url_prefix='/usuarios')
#app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(usuario_bp) 
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)
app.register_blueprint(factura_bp)
app.register_blueprint(compra_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return(dict(is_active =  is_active))
    

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    # Redirige según el rol
    if session.get('rol') == 'admin':
        return redirect(url_for('usuario.index'))
    return redirect(url_for('venta.index'))
    #return "<h1>Aplicacion Calzados</h1>"

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)