from flask import Flask, request

from controllers import usuario_controller,cliente_controller,producto_controller,venta_controller

from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Calzados.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de la clave secreta
app.secret_key = 'clave_secreta_super_segura'  # Cambia esto por una clave única y segura


db.init_app(app)

app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return(dict(is_active =  is_active))
    

@app.route("/")
def home():
    return "<h1>Aplicacion Calzados</h1>"

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)