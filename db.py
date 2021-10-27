from logging import NullHandler
import mysql.connector
from mysql.connector.connection import MySQLConnection
from models import Cliente, PaymentMethod,Prestador, Proposta, TipoPrestador
from datetime import datetime

def get_connection() -> MySQLConnection:
    mydb = None 
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="handcannoterase",
            database='animaai'
        )
    except(Exception) as error:
        raise Exception("Error during connection to db!")
    return mydb

def login(email,password, user_type):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    r = None
    if(user_type == 'cliente'):
        cursor.execute("SELECT * FROM cliente WHERE email='{email}' AND senha='{password}'".format(email=email, password=password))
        result = cursor.fetchone()
        if result is not None:
            r =  Cliente(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],str(result[9]), result[10],result[11],result[12])
    else:
        cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,documento,tipo_documento,telefone,razao_social,cidade,estado,endereco,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, 1,valor FROM prestador p WHERE p.email ='{email}' and p.senha = '{senha}' ".format(email=email,senha=password) )
        x = cursor.fetchone()
        if x is not None:
            r =  Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18])
            cursor.execute('SELECT id_tipo_prestador, t.descricao, t.icone FROM assoc_prestador_tipo_prestador a join tipo_prestador t on a.id_tipo_prestador = t.idtipo_prestador where a.id_prestador = {id_prestador} limit 1'.format(id_prestador=r.id_prestador))
            result2 = cursor.fetchall()
            for y in result2:
                t = TipoPrestador(y[0],y[1],y[2])
                r.tipos_prestador = (t.__dict__)
            cursor.execute("SELECT AVG(rating),COUNT(*) FROM rating where idprestador = {idprestador}".format(idprestador=r.id_prestador))
            result3 = cursor.fetchone()
            r.rating = result3[0]
            r.rating_count = result3[1]
    return r

def get_clientes():
    """ Retorna todos os clientes cadastrados no banco """
    clientes_list = []
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM cliente")
        result = cursor.fetchall()
        print("Users retrieved!")
        for x in result:
            c =  Cliente(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8], x[9],x[10],x[11])
            clientes_list.append(c)
    except(Exception) as error:
        raise Exception("Error getting clientes list")
    return result

def insert_cliente(cliente:Cliente):
    """ Insere um novo cliente na tabela cliente """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [cliente.nome, cliente.email, cliente.cep, cliente.senha, cliente.cpf, cliente.cidade, cliente.estado, cliente.endereco, cliente.data_nascimento,cliente.telefone, cliente.numero, cliente.complemento]
        cursor.execute("INSERT INTO cliente(nome,email,cep,senha,cpf,cidade,estado,endereco, data_nascimento,telefone,numero,complemento) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        mydb.commit()
        print("Cliente inserido!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))

def update_cliente(cliente:Cliente):
    """ Insere um novo cliente na tabela cliente """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [cliente.nome, cliente.cep, cliente.cidade, cliente.estado, cliente.endereco,cliente.telefone, cliente.numero,cliente.complemento,cliente.id]
        cursor.execute("UPDATE cliente SET nome = %s, cep= %s, cidade  = %s, estado= %s, endereco= %s, telefone= %s, numero = %s, complemento = %s WHERE id_cliente = %s", values)
        mydb.commit()
        print("Cliente atualizado!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao atualizar o cliente: {error}".format(error=error))

def update_prestador(prestador:Prestador):
    """ Insere um novo prestador na tabela prestador """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [prestador.nome, prestador.cep, prestador.cidade, prestador.estado, prestador.endereco,prestador.telefone, prestador.id_prestador]
        cursor.execute("UPDATE prestador SET nome = %s, cep= %s, cidade  = %s, estado= %s, endereco= %s, telefone= %s WHERE id_prestador = %s", values)
        mydb.commit()
        print("Prestador atualizado!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao atualizar o prestador: {error}".format(error=error))

def update_prestador_servico(id_prestador,descricao,apresentacao,valor,tipo):
    """ Atualiza os dados do serviço do prestador """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [descricao,apresentacao,valor,id_prestador]
        values2  =[id_prestador,tipo]
        cursor.execute("UPDATE prestador SET descricao = %s, apresentacao= %s, valor  = %s WHERE id_prestador = %s", values)
        cursor.execute("INSERT INTO assoc_prestador_tipo_prestador VALUES (%s,%s)",values2)
        mydb.commit()
        print("Prestador atualizado!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao atualizar o prestador: {error}".format(error=error))

def insert_prestador(prestador:Prestador):
    """ Insere um novo prestador na tabela prestador """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [prestador.nome, prestador.email, prestador.cep, prestador.senha, prestador.documento, prestador.tipo_documento, prestador.cidade, prestador.estado, prestador.endereco, prestador.data_nascimento, prestador.telefone]
        cursor.execute("INSERT INTO prestador(nome,email,cep,senha,documento, tipo_documento,cidade,estado,endereco, data_nascimento, telefone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        mydb.commit()
        print("Prestador inserido!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir o prestador: {error}".format(error=error))


def insert_proposta(proposta:Proposta):
    """ Insere uma nova proposta na tabela proposta """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [proposta.data_proposta, proposta.cep, proposta.cidade, proposta.estado, proposta.endereco, proposta.horario_inicio, proposta.horario_fim, proposta.observacoes, proposta.data_criacao, proposta.valor, proposta.id_cliente,proposta.id_prestador,proposta.numero,proposta.complemento,proposta.status]
        cursor.execute("INSERT INTO proposta(data_proposta,cep,cidade,estado,endereco,horario_inicio,horario_fim,observacoes,data_criacao,valor,id_cliente,id_prestador,numero,complemento,status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)", values)
        mydb.commit()
        print("Proposta inserida!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir a proposta: {error}".format(error=error))

def get_prestadores(id_cliente):
    prestadores_list = []
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,documento,tipo_documento,telefone,razao_social,cidade,estado,endereco,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, a.favourite,valor FROM prestador p left join assoc_cliente_prestador_favorito a on p.id_prestador = a.id_prestador and a.id_cliente = {cliente}".format(cliente=id_cliente))
    result = cursor.fetchall()
    print("Users retrieved!")
    for x in result:
        p =  Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16], x[17],x[18])
        cursor.execute('SELECT id_tipo_prestador, t.descricao, t.icone FROM assoc_prestador_tipo_prestador a join tipo_prestador t on a.id_tipo_prestador = t.idtipo_prestador where a.id_prestador = {id_prestador} limit 1'.format(id_prestador=p.id_prestador))
        result2 = cursor.fetchall()
        for y in result2:
            t = TipoPrestador(y[0],y[1],y[2])
            p.tipos_prestador = t.__dict__
        cursor.execute("SELECT AVG(rating) FROM rating where idprestador = {idprestador}".format(idprestador=p.id_prestador))
        result3 = cursor.fetchone()
        p.rating = result3[0]
        print(len(y))
        if len(result2) > 0:
            prestadores_list.append(p)
    return prestadores_list

def get_prestadores_favoritos(id_cliente):
    prestadores_list = []
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,documento,tipo_documento,telefone,razao_social,cidade,estado,endereco,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, a.favourite,valor FROM prestador p join assoc_cliente_prestador_favorito a on p.id_prestador = a.id_prestador and a.id_cliente = {cliente}".format(cliente=id_cliente))
    result = cursor.fetchall()
    print("Users retrieved!")
    for x in result:
        p =  Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16], x[17],x[18])
        cursor.execute('SELECT id_tipo_prestador, t.descricao, t.icone FROM assoc_prestador_tipo_prestador a join tipo_prestador t on a.id_tipo_prestador = t.idtipo_prestador where a.id_prestador = {id_prestador} limit 1'.format(id_prestador=p.id_prestador))
        result2 = cursor.fetchall()
        for y in result2:
            t = TipoPrestador(y[0],y[1],y[2])
            p.tipos_prestador = t.__dict__
        prestadores_list.append(p)
    return prestadores_list

def get_prestador_by_id(id,id_cliente):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,documento,tipo_documento,telefone,razao_social,cidade,estado,endereco,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, a.favourite,valor FROM prestador p left join assoc_cliente_prestador_favorito a on p.id_prestador = a.id_prestador and a.id_cliente = {cliente} WHERE p.id_prestador ={id_prestador} ".format(id_prestador=id,cliente=id_cliente) )
    x = cursor.fetchone()
    p = Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18])
    cursor.execute('SELECT id_tipo_prestador, t.descricao, t.icone FROM assoc_prestador_tipo_prestador a join tipo_prestador t on a.id_tipo_prestador = t.idtipo_prestador where a.id_prestador = {id_prestador} limit 1'.format(id_prestador=p.id_prestador))
    result2 = cursor.fetchall()
    for y in result2:
        t = TipoPrestador(y[0],y[1],y[2])
        p.tipos_prestador = (t.__dict__)
    cursor.execute("SELECT AVG(rating),COUNT(*) FROM rating where idprestador = {idprestador}".format(idprestador=p.id_prestador))
    result3 = cursor.fetchone()
    p.rating = result3[0]
    p.rating_count = result3[1]
    return p

def get_propostas(id_prestador):
    mydb = get_connection()
    propostas = []
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT id_proposta,DATE_FORMAT(data_proposta, '%Y-%m-%d'),cep,cidade,estado,endereco,'18:30','18:30',observacoes,DATE_FORMAT(data_criacao, '%Y-%m-%d'),valor,id_cliente,id_prestador,numero,complemento,status FROM proposta WHERE id_prestador = {id_prestador} and status = 1".format(id_prestador=id_prestador) )
    result = cursor.fetchall()
    for x in result:
        p = Proposta(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15])
        propostas.append(p)
    return propostas

def get_propostas_by_client(id_client):
    mydb = get_connection()
    propostas = []
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT id_proposta,DATE_FORMAT(data_proposta, '%Y-%m-%d'),cep,cidade,estado,endereco,'18:30','18:30',observacoes,DATE_FORMAT(data_criacao, '%Y-%m-%d'),valor,id_cliente,id_prestador,numero,complemento,status FROM proposta WHERE id_cliente = {id_client} order by id_proposta DESC".format(id_client=id_client) )
    result = cursor.fetchall()
    for x in result:
        p = Proposta(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15])
        propostas.append(p)
    return propostas

def get_propostas_by_id(id_proposta):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT id_proposta,DATE_FORMAT(data_proposta, '%Y-%m-%d'),cep,cidade,estado,endereco,'18:30','18:30',observacoes,DATE_FORMAT(data_criacao, '%Y-%m-%d'),valor,id_cliente,id_prestador,numero,complemento,status FROM proposta WHERE id_proposta = {id_proposta} ".format(id_proposta=id_proposta) )
    x = cursor.fetchone()
    proposta = Proposta(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15])
    return proposta

def get_payment_methods_by_client(id_client):
    payment_methods = []
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT idpayment_method,id_client,card_number,card_flag,safety_code,owner_cpf,DATE_FORMAT(due_date, '%Y-%m-%d'), owner_name FROM payment_method WHERE id_client = {id_client} ".format(id_client=id_client) )
    result = cursor.fetchall()
    for x in result:
        pm = PaymentMethod(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
        payment_methods.append(pm)
    return payment_methods

def insert_payment_method(paymentMethod):
    """ Insere um novo metodo de pagamento na tabela payment_method """
    try:
        mydb = get_connection()
        print("Connected to db!")
        cursor = mydb.cursor()
        values = [paymentMethod.id_client,paymentMethod.card_number,paymentMethod.card_flag,paymentMethod.safety_code,paymentMethod.owner_cpf,paymentMethod.due_date,paymentMethod.owner_name]
        cursor.execute("INSERT INTO payment_method(id_client,card_number,card_flag,safety_code,owner_cpf,due_date,owner_name) VALUES(%s, %s, %s,%s,%s,%s,%s)", values)
        mydb.commit()
        print("Metodo de pagamento inserido!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir o metodo de pagamento: {error}".format(error=error))

def approve_proposta(id_proposta,status):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("UPDATE proposta SET status = {status} WHERE id_proposta = {id_proposta} ".format(id_proposta=id_proposta,status=status) )
    mydb.commit()


def insert_favourite(id_prestador,id_cliente):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute('INSERT INTO assoc_cliente_prestador_favorito VALUES ({id_cliente},{id_prestador} ,1)'.format(id_prestador=id_prestador,id_cliente=id_cliente))
    mydb.commit()


def delete_favourite(id_prestador,id_cliente):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM assoc_cliente_prestador_favorito WHERE id_cliente = {id_cliente} AND id_prestador = {id_prestador}'.format(id_prestador=id_prestador,id_cliente=id_cliente))
    mydb.commit()
    


