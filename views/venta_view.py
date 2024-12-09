from flask import render_template

def list(ventas):
    """
    Renderiza la lista de ventas.
    Se muestra la información básica de cada venta, incluyendo cliente, producto y total.
    """
    return render_template('ventas/index.html' , ventas=ventas)
 
def create(clientes, productos, empleados):
    """
    Renderiza el formulario de creación de ventas.
    Ahora incluye empleados (usuarios que pueden realizar ventas) como un parámetro adicional.
    """
    #se requiere prouctos y clientes
    return render_template('ventas/create.html',clientes=clientes,productos=productos, empleados=empleados)

    #se requiere prouctos y clientes
def edit(venta,clientes,productos, empleados):
    """
    Renderiza el formulario de edición de ventas.
    Incluye todos los datos relacionados con la venta, como cliente, producto, empleado, cantidad, y total.
    """
    return render_template('ventas/edit.html' ,venta=venta,clientes=clientes,productos=productos, empleados=empleados)
