from flask import Flask, request
import db
import json
from models import Cliente, Prestador
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        result = db.login(data['email'],data['password'])
        r = None
        if result is None:
            r = {
                'client':None,
                'error':True,
                'message':'Usuário ou senha incorretos!'
            }
        else:
            r = {
                'client':json.dumps(result.__dict__),
                'error':False,
                'message':'Login realizado com sucesso!'
            }
        return r
    except(Exception) as error:
        print("Ocorreu um erro ao realizar o login: {error}".format(error=error))
        return "Erro ao realizar login!"

@app.route("/clientes/insert", methods=['POST'])
@cross_origin()
def insert_cliente():
    try:
        data = request.get_json()
        cliente = Cliente(None, data['name'],data['email'],None,data['password'],data['cpf'],None,None,None,data['dataNascimento'])
        db.insert_cliente(cliente)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))
        return "Erro ao inserir"
    return "Cliente inserido"

@app.route("/prestadores/insert", methods=['POST'])
@cross_origin()
def insert_prestadores():
    try:
        data = request.get_json()
        prestador = Prestador(None,data['name'],data['email'],None,data['password'],data['documento'],data['documentType'],None,None,None,None,None,data['dataNascimento'])
        db.insert_prestador(prestador)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o prestador: {error}".format(error=error))
        return "Erro ao inserir prestador"
    return "Prestador inserido"
    

@app.route("/clientes/get")
def get_cliente():
    clientes = None
    try:
        clientes = db.get_clientes()
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return json.dumps(clientes)



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



@app.route("/prestadores/delete")
def delete_prestadores():
    return "<p>Delete Service Provider!</p>"








