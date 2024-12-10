from flask import render_template

from controllers.decorators import role_required 



def list(productos):
    return render_template('productos/index.html' , productos=productos)
 
def create():
    return render_template('productos/create.html')

def edit(producto):
    return render_template('productos/edit.html' ,producto=producto)
