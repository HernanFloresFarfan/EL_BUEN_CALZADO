from flask import render_template

def render_facturas(facturas, clientes, productos, ventas):
    return render_template('facturas/index.html', facturas=facturas, clientes=clientes, productos=productos, ventas=ventas)

def create(clientes, productos, ventas, cantidad_vendida=None):
    return render_template('facturas/create.html', clientes=clientes, productos=productos, ventas=ventas, cantidad_vendida=cantidad_vendida)

def edit(factura, clientes, productos):
    return render_template('facturas/edit.html', factura=factura, clientes=clientes, productos=productos)
