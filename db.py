from logging import NullHandler
import mysql.connector
from mysql.connector.connection import MySQLConnection
from models import Cliente,Prestador, TipoPrestador
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

def login(email,password):
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cliente WHERE email='{email}' AND senha='{password}'".format(email=email, password=password))
    result = cursor.fetchone()
    cliente = None
    if result is not None:
        cliente =  Cliente(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],str(result[9]), result[10])
    return cliente

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
            c =  Cliente(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8], x[9])
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
        values = [cliente.nome, cliente.email, cliente.cep, cliente.senha, cliente.cpf, cliente.cidade, cliente.estado, cliente.endereco, cliente.data_nascimento,cliente.telefone]
        cursor.execute("INSERT INTO cliente(nome,email,cep,senha,cpf,cidade,estado,endereco, data_nascimento,telefone) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        mydb.commit()
        print("Cliente inserido!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))

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

def get_prestadores(id_cliente):
    prestadores_list = []
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,telefone,razao_social,cidade,estado,endereco,documento,tipo_documento,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, a.favourite FROM prestador p left join assoc_cliente_prestador_favorito a on p.id_prestador = a.id_prestador and a.id_cliente = {cliente}".format(cliente=id_cliente))
    result = cursor.fetchall()
    print("Users retrieved!")
    for x in result:
        p =  Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16], x[17])
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
    cursor.execute("SELECT p.id_prestador,nome,email,cep,senha,telefone,razao_social,cidade,estado,endereco,documento,tipo_documento,DATE_FORMAT(data_nascimento, '%Y-%m-%d'), imagem_perfil,descricao,apresentacao,foto_perfil, a.favourite FROM prestador p left join assoc_cliente_prestador_favorito a on p.id_prestador = a.id_prestador and a.id_cliente = {cliente} WHERE p.id_prestador ={id_prestador} ".format(id_prestador=id,cliente=id_cliente) )
    x = cursor.fetchone()
    p = Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17])
    cursor.execute('SELECT id_tipo_prestador, t.descricao, t.icone FROM assoc_prestador_tipo_prestador a join tipo_prestador t on a.id_tipo_prestador = t.idtipo_prestador where a.id_prestador = {id_prestador} limit 1'.format(id_prestador=p.id_prestador))
    result2 = cursor.fetchall()
    for y in result2:
        t = TipoPrestador(y[0],y[1],y[2])
        p.tipos_prestador = (t.__dict__)
    return p

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
    


