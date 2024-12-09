from flask import render_template

def list(clientes):
    return render_template('clientes/index.html' , clientes = clientes)
 
def create():
    return render_template('clientes/create.html')

def edit(cliente):
    return render_template('clientes/edit.html', cliente =  cliente)
