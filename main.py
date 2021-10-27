from flask import Flask, request
import db
import json
from models import Cliente, PaymentMethod, Prestador, Proposta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    try:
        data = request.get_json()
        result = db.login(data['email'],data['password'],data['userType'])
        r = None
        t = None
        if data['userType'] == 'cliente':
            t = 1
        else:
            t = 2
        if result is None:
            r = {
                'client':None,
                'error':True,
                'message':'Usuário ou senha incorretos!',
                'type':t
            }
        else:
            r = {
                'client':json.dumps(result.__dict__),
                'error':False,
                'message':'Login realizado com sucesso!',
                'type':t
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
        cliente = Cliente(None, data['name'],data['email'],None,data['password'],data['cpf'],None,None,None,data['dataNascimento'],data['phone'])
        db.insert_cliente(cliente)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))
        return "Erro ao inserir"
    return "Cliente inserido"

@app.route("/clientes/update", methods=['POST'])
@cross_origin()
def update_cliente():
    try:
        data = request.get_json()
        c = data['cliente']
        cliente = Cliente(c['id'], c['nome'],c['email'],c['cep'],c['senha'],c['cpf'],c['cidade'],c['estado'],c['endereco'],c['data_nascimento'],c['telefone'],c['numero'],c['complemento'])
        db.update_cliente(cliente)
    except(Exception) as error:
        print("Um erro ocorreu ao atualizar o cliente: {error}".format(error=error))
        return "Erro ao atualizar"
    return "Cliente atualizado"

@app.route("/prestadores/update", methods=['POST'])
@cross_origin()
def update_prestador():
    try:
        data = request.get_json()
        c = data['prestador']
        prestador = Prestador(c['id_prestador'], c['nome'],c['email'],c['cep'],c['senha'],c['documento'],None,c['telefone'],None,c['cidade'],c['estado'],c['endereco'],c['data_nascimento'],None,c['descricao'],c['apresentacao'],"",None)
        db.update_prestador(prestador)
    except(Exception) as error:
        print("Um erro ocorreu ao atualizar o prestador: {error}".format(error=error))
        return "Erro ao atualizar"
    return "Prestador atualizado"


@app.route("/prestadores/update-service", methods=['POST'])
@cross_origin()
def update_prestador_servico():
    try:
        data = request.get_json()
        id_prestador= data['id_prestador']
        descricao = data['descricao']
        apresentacao = data['apresentacao']
        valor = data['valor']
        type = data['type']
        db.update_prestador_servico(id_prestador,descricao,apresentacao,valor, type)
    except(Exception) as error:
        print("Um erro ocorreu ao atualizar o prestador: {error}".format(error=error))
        return "Erro ao atualizar"
    return "Prestador atualizado"

@app.route("/prestadores/insert", methods=['POST'])
@cross_origin()
def insert_prestadores():
    try:
        data = request.get_json()
        prestador = Prestador(None,data['name'],data['email'],None,data['password'],data['documento'],data['documentType'],data['phone'],None,None,None,None,data['dataNascimento'])
        db.insert_prestador(prestador)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o prestador: {error}".format(error=error))
        return "Erro ao inserir prestador"
    return "Prestador inserido"

@app.route('/proposta/get', methods=['POST'])
@cross_origin()
def get_propostas():
    try:
        data = request.get_json()
        propostas = None
        propostas = db.get_propostas(data['id_prestador'])
    except(Exception) as error:
        print("Um erro ocorreu ao consultar as propostas: {error}".format(error=error))
        return "Erro ao consultar propostas"
    return str(json.dumps([ob.__dict__ for ob in propostas]))

@app.route('/proposta/getbyid', methods=['POST'])
@cross_origin()
def get_propostas_by_id():
    try:
        data = request.get_json()
        proposta = db.get_propostas_by_id(data['id_proposta'])
    except(Exception) as error:
        print("Um erro ocorreu ao consultar as propostas: {error}".format(error=error))
        return "Erro ao consultar propostas"
    return str(json.dumps(proposta.__dict__))

@app.route('/proposta/getbyclient', methods=['POST'])
@cross_origin()
def get_propostas_by_client():
    try:
        data = request.get_json()
        propostas = db.get_propostas_by_client(data['id_cliente'])
    except(Exception) as error:
        print("Um erro ocorreu ao consultar as propostas: {error}".format(error=error))
        return "Erro ao consultar propostas"
    return str(json.dumps([ob.__dict__ for ob in propostas]))

@app.route("/proposta/insert", methods=['POST'])
def insert_proposta():
    try:
        data = request.get_json()
        p = data['proposta']
        proposta = Proposta(None,p['data_proposta'],p['cep'],p['cidade'],p['estado'],p['endereco'],p['horario_inicio'],p['horario_fim'],p['observacoes'],p['data_criacao'],p['valor'],p['id_cliente'],p['id_prestador'],p['numero'],p['complemento'],1)
        db.insert_proposta(proposta)
    except(Exception) as error:
        print("Um erro ocorreu ao inserir o prestador: {error}".format(error=error))
        return "Erro ao inserir proposta"
    return "Proposta inserida"

@app.route("/proposta/status", methods=['POST'])
def atualizar_proposta():
    try:
        data = request.get_json()
        db.approve_proposta(data['id_proposta'],data['status'])
    except(Exception) as error:
        return "Erro ao atualizar proposta"
    return "Proposta atualizada"

@app.route("/prestadores/favoritar", methods=['POST'])
@cross_origin()
def insert_favorito():
    print("favoritado")
    data = request.get_json()
    try:
        if data['favorito'] is None:
            db.insert_favourite(data['id_prestador'],data['id_cliente'])
        else:
            db.delete_favourite(data['id_prestador'],data['id_cliente'])
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return "Prestador Favorito Inserido"

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

@app.route("/prestadores/get", methods=['GET','POST'])
def get_prestadores():
    prestadores = None
    data = request.get_json()
    try:
        prestadores = db.get_prestadores(data['id_cliente'])
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return str(json.dumps([ob.__dict__ for ob in prestadores]))

@app.route("/prestadores/favoritos/get", methods=['GET','POST'])
def get_prestadores_favoritos():
    prestadores = None
    data = request.get_json()
    try:
        prestadores = db.get_prestadores_favoritos(data['id_cliente'])
        print(prestadores[0].estado)
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return str(json.dumps([ob.__dict__ for ob in prestadores]))

@app.route("/prestadores/getid", methods=['POST'])
def get_prestadores_by_id():
    prestador = None
    data = request.get_json()
    try:
        prestador = db.get_prestador_by_id(data['id_prestador'],data['id_cliente'])
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return str(json.dumps(prestador.__dict__))

@app.route("/payment-methods/insert", methods=['POST'])
@cross_origin()
def add_payment_method():
    data = request.get_json()
    paymentMethod = PaymentMethod(data['idpayment_method'],data['id_client'],data['card_number'],data['card_flag'],data['safety_code'],data['owner_cpf'],data['due_date'],data['owner_name'])
    try:
        db.insert_payment_method(paymentMethod)
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return "Metodo inserido com sucesso!"

@app.route("/payment-methods/get", methods=['POST'])
@cross_origin()
def get_payment_methods():
    data = request.get_json()
    try:
        payments = db.get_payment_methods_by_client(data['id_client'])
    except(Exception) as error:
        print("Error {error}".format(error= error))
    return str(json.dumps([ob.__dict__ for ob in payments]))

@app.route("/prestadores/delete")
def delete_prestadores():
    return "<p>Delete Service Provider!</p>"


    








