from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from reportlab.lib.utils import ImageReader  # Importar ImageReader
from reportlab.platypus import Paragraph  # Importar Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from flask import request, redirect, url_for, flash, Blueprint, render_template
from datetime import datetime
from views import factura_view
from decimal import Decimal

from models.factura_model import Factura
from models.cliente_model import Cliente
from models.producto_model import Producto
from models.venta_model import Venta
from database import db


factura_bp = Blueprint('factura', __name__, url_prefix="/facturas")  # Define el Blueprint si no está definido

@factura_bp.route("/")
def index():
    """Recupera todos los registros de facturas."""
    facturas = Factura.get_all()
    clientes = Cliente.query.all()  # Obtener todos los clientes
    productos = Producto.query.all()  # Obtener todos los productos
    ventas = Venta.query.all()
    return factura_view.render_facturas(facturas=facturas, clientes=clientes, productos=productos, ventas=ventas)

@factura_bp.route("/create", methods=['GET', 'POST'])
def create():
    cantidad_vendida = {}  # Diccionario para almacenar la cantidad vendida por producto
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad_str = request.form['cantidad']
        fecha_str = request.form['fecha']
        venta_id = request.form['venta_id']
        
        # Convertir los valores a Decimal
        descuento = Decimal(request.form.get('descuento', 0))  # Descuento como Decimal
        monto_ingreso = Decimal(request.form.get('monto_ingreso', 0))  # Monto ingresado como Decimal
        
        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return redirect(url_for('factura.create'))

        # Validar cliente
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            flash("Cliente no encontrado.", "error")
            return redirect(url_for('factura.create'))

        # Validar producto
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.create'))
        
        # Validar venta_id
        venta = Venta.query.get(venta_id)
        if not venta:
            flash("Venta no encontrada.", "error")
            return redirect(url_for('factura.create'))
        
        # Intentar convertir la cantidad a entero
        try:
            cantidad = int(cantidad_str)  # Convertir la cantidad a entero
        except ValueError:
            flash("La cantidad debe ser un número válido.", "error")
            return redirect(url_for('factura.create'))

        # Validar cantidad
        if cantidad <= 0:
            flash("La cantidad debe ser mayor que cero.", "error")
            return redirect(url_for('factura.create'))

        # Verificar que el producto seleccionado está en la venta y obtener su cantidad
        cantidad_vendida[producto.id] = cantidad_vendida.get(producto.id, 0) + venta.cantidad

        # Verificar stock disponible
        if cantidad > producto.stock:
            flash(f"Stock insuficiente. Disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.create'))

        # Calcular subtotal, total y cambio
        subtotal = Decimal(producto.precio) * Decimal(cantidad)
        total = subtotal - descuento
        
        if total < 0:
            flash("El descuento no puede ser mayor que el subtotal.", "error")
            return redirect(url_for('factura.create'))

        # Redondear los valores de total y monto_ingreso a dos decimales
        total = total.quantize(Decimal('0.01'))  # Redondear el total a dos decimales
        monto_ingreso = monto_ingreso.quantize(Decimal('0.01'))  # Redondear el monto ingresado a dos decimales

        # Depuración: Imprimir valores de total y monto ingresado
        print(f"Subtotal: {subtotal}, Descuento: {descuento}, Total calculado: {total}, Monto ingresado: {monto_ingreso}")

        # Verificar que el monto ingresado no sea menor que el total
        if monto_ingreso < total:
            flash(f"El monto ingresado no puede ser menor que el total ({total}).", "error")
            return redirect(url_for('factura.create'))

        # Crear factura
        print(f"Cliente: {cliente_id}, Producto: {producto_id}, Cantidad: {cantidad}, Total: {total}")
        factura = Factura(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, subtotal=subtotal, descuento=descuento, total=total, monto_ingreso=monto_ingreso, cambio=monto_ingreso - total, fecha=fecha, venta_id=venta_id)
        factura.save()

        # Actualizar stock del producto
        producto.update(stock=producto.stock - cantidad)

        flash("Factura registrada exitosamente.", "success")
        return redirect(url_for('factura.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    ventas = Venta.query.all()
    
    return factura_view.create(clientes, productos, ventas, cantidad_vendida)


@factura_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """Edita una factura existente."""
    factura = Factura.get_by_id(id)
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for('factura.index'))

    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        nueva_cantidad = int(request.form['cantidad'])
        fecha_str = request.form['fecha']
        descuento = float(request.form.get('descuento', 0))
        monto_ingreso = float(request.form.get('monto_ingreso', 0))
        venta_id = request.form['venta_id']
        #fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        # Validar fecha
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Formato de fecha inválido.", "error")
            return redirect(url_for('factura.edit', id=id))
        
        # Validar venta_id
        venta = Venta.query.get(venta_id)
        if not venta:
            flash("Venta no encontrada.", "error")
            return redirect(url_for('factura.edit', id=id))

        # Validar producto
        producto = Producto.get_by_id(producto_id)
        if not producto:
            flash("Producto no encontrado.", "error")
            return redirect(url_for('factura.edit', id=id))

        diferencia = nueva_cantidad - factura.cantidad
        if diferencia > 0 and diferencia > producto.stock:
            flash(f"No hay suficiente stock para este cambio. Stock disponible: {producto.stock}.", "error")
            return redirect(url_for('factura.edit', id=id))

        # Calcular subtotal, total y cambio
        subtotal = producto.precio * nueva_cantidad
        total = subtotal - descuento
        
        if total < 0:
            flash("El descuento no puede ser mayor que el subtotal.", "error")
            return redirect(url_for('factura.edit', id=id))

        cambio = monto_ingreso - total
        if monto_ingreso < total:
            flash("El monto ingresado no puede ser menor que el total.", "error")
            return redirect(url_for('factura.edit', id=id))

        # Actualizar factura
        factura.update(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=nueva_cantidad,
            subtotal=subtotal,
            descuento=descuento,
            total=total,
            monto_ingreso=monto_ingreso,
            cambio=cambio,
            fecha=fecha
        )

        # Actualizar stock del producto
        producto.update(stock=producto.stock - diferencia)

        flash("Factura actualizada exitosamente.", "success")
        return redirect(url_for('factura.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()
    ventas = Venta.query.all()
    return factura_view.edit(factura, clientes, productos)

@factura_bp.route("/delete/<int:id>")
def delete(id):
    """Elimina una factura."""
    factura = Factura.get_by_id(id)
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for('factura.index'))

    producto = Producto.get_by_id(factura.producto_id)
    if producto:
        producto.update(stock=producto.stock + factura.cantidad)

    factura.delete()

    flash("Factura eliminada exitosamente.", "success")
    return redirect(url_for('factura.index'))


@factura_bp.route("/print/<int:id>")
def print_factura(id):
    """Generar e imprimir la factura en formato PDF."""
    factura = Factura.get_by_id(id)
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for('factura.index'))

    cliente = Cliente.query.get(factura.cliente_id)
    producto = Producto.query.get(factura.producto_id)
    venta = Venta.query.get(factura.venta_id)

    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 12)

    # Encabezado
    pdf.drawString(200, 750, "FACTURA")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 730, f"NIT: 12345678")
    pdf.drawString(50, 715, f"FACTURA No: {factura.id:07}")
    pdf.drawString(50, 700, f"NOMBRE: {cliente.nombre}")
    pdf.drawString(50, 685, f"COD_CLIENTE: {cliente.id}")
    pdf.drawString(50, 670, f"FECHA DE EMISION: {factura.fecha.strftime('%d/%m/%Y')}")

    # Detalles de compra
    pdf.drawString(50, 650, "DETALLE DE COMPRA:")
    pdf.drawString(50, 630, "Producto")
    pdf.drawString(200, 630, "Cantidad")
    pdf.drawString(300, 630, "Precio (Bs)")
    pdf.drawString(400, 630, "Subtotal (Bs)")
    pdf.drawString(50, 610, f"{producto.nombre}")
    pdf.drawString(200, 610, f"{factura.cantidad}")
    pdf.drawString(300, 610, f"{round(producto.precio, 2)}")
    pdf.drawString(400, 610, f"{round(factura.subtotal, 2)}")
    
    # Totales
    pdf.drawString(50, 570, f"SUBTOTAL BS: {round(factura.subtotal, 2)}")
    pdf.drawString(50, 555, f"DESCUENTO BS: {round(factura.descuento, 2)}")
    pdf.drawString(50, 540, f"TOTAL BS: {round(factura.total, 2)}")
    pdf.drawString(50, 525, f"MONTO DE INGRESO BS: {round(factura.monto_ingreso, 2)}")
    pdf.drawString(50, 510, f"CAMBIO BS: {round(factura.cambio, 2)}")

    # Línea de separación
    pdf.setLineWidth(0.5)  # Grosor de la línea
    line_y = 495  # Coordenada vertical ajustada para la línea
    pdf.line(50, line_y, 550, line_y)  # Línea horizontal debajo de los totales

    # Leyenda ajustada automáticamente
    styles = getSampleStyleSheet()
    leyenda_style = styles["Normal"]
    leyenda_style.fontSize = 9  # Tamaño de fuente reducido
    leyenda_style.leading = 12  # Espaciado entre líneas

    leyenda_text = (
        "Ley Nro 453: Tienes derecho a recibir información sobre las características y contenido "
        "de productos que consumes. Esta factura respeta los derechos del consumidor."
    )
    leyenda_paragraph = Paragraph(leyenda_text, leyenda_style)
    leyenda_paragraph.wrapOn(pdf, 380, 50)  # Ancho de 380 píxeles
    leyenda_paragraph.drawOn(pdf, 50, line_y - 40)  # Posición ajustada debajo de la línea

    # QR Code ajustado
    qr_data = "https://siat.impuestos.gob.bo"  # Contenido del QR
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)
    pdf.drawImage(qr_image, 450, line_y - 100, 80, 80)  # Ajusta la posición y tamaño del QR
    
    # Vendedor
    if venta.empleado:
        pdf.drawString(50, 420, f"USTED FUE ATENDIDO POR: {venta.empleado.nombre}")
    else:
        pdf.drawString(50, 420, "USTED FUE ATENDIDO POR: No registrado")
        
    # Guardar PDF
    pdf.save()
    buffer.seek(0)

    # Enviar archivo PDF
    return send_file(buffer, as_attachment=True, download_name=f"Factura_{factura.id}.pdf", mimetype="application/pdf")

