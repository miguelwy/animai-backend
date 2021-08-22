from logging import NullHandler
import mysql.connector
from mysql.connector.connection import MySQLConnection
from models import Cliente,Prestador

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
            c =  Cliente(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
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
        values = [cliente.nome, cliente.email, cliente.cep, cliente.senha, cliente.cpf, cliente.cidade, cliente.estado, cliente.endereco]
        cursor.execute("INSERT INTO cliente(nome,email,cep,senha,cpf,cidade,estado,endereco) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", values)
        mydb.commit()
        print("Cliente inserido!")
    except(Exception) as error:
        raise Exception("Um erro ocorreu ao inserir o cliente: {error}".format(error=error))

def get_prestadores():
    prestadores_list = []
    mydb = get_connection()
    print("Connected to db!")
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cliente")
    result = cursor.fetchall()
    print("Users retrieved!")
    for x in result:
        p =  Prestador(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
        prestadores_list.append(p)
    return result