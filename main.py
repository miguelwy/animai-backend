from flask import Flask, request
import db
import json
from models import Cliente
app = Flask(__name__)

@app.route("/clientes/get")
def get_cliente():
    clientes = None
    try:
        clientes = db.get_clientes()
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return json.dumps(clientes)

@app.route("/clientes/insert", methods=['POST'])
def insert_cliente():
    try:
        data = request.get_json()
        cliente = Cliente(data['nome'],data['email'],data['cep'],data['senha'],data['cpf'],data['cidade'],data['estado'],data['endereco'])
        db.insert_cliente(cliente)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))
        return "Erro ao inserir"
    return "Cliente inserido"

@app.route("/clientes/delete")
def delete_cliente():
    return "<p>Delete User!</p>"

@app.route("/prestadores/get")
def get_prestadores():
    prestadores = None
    try:
        clientes = db.get_clientes()
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return str(clientes)

@app.route("/prestadores/insert")
def insert_prestadores():
    try:
        data = request.get_json()
        cliente = Cliente(data['nome'],data['email'],data['cep'],data['senha'],data['cpf'],data['cidade'],data['estado'],data['endereco'])
        db.insert_cliente(cliente)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o prestador: {error}".format(error=error))
        return "Erro ao inserir prestador"
    return "Prestador inserido"

@app.route("/prestadores/delete")
def delete_prestadores():
    return "<p>Delete Service Provider!</p>"


@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(data)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))
        return "Erro ao inserir"
    return "Cliente inserido"






