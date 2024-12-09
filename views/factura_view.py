from flask import render_template

def list(facturas, clientes, productos):
    return render_template('facturas/index.html', facturas=facturas, clientes=clientes, productos=productos)

def create(clientes, productos):
    return render_template('facturas/create.html', clientes=clientes, productos=productos)

def edit(factura, clientes, productos):
    return render_template('facturas/edit.html', factura=factura, clientes=clientes, productos=productos)
