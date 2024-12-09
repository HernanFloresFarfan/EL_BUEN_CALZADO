from flask import render_template

def list(compras):
    """Renderiza la lista de compras."""
    return render_template('compras/index.html', compras=compras)

def create(productos):
    """Renderiza el formulario para crear una nueva compra."""
    return render_template('compras/create.html', productos=productos)

def edit(compra, productos):
    """Renderiza el formulario para editar una compra existente."""
    return render_template('compras/edit.html', compra=compra, productos=productos)
