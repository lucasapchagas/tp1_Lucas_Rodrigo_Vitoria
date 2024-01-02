import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import OperationalError
import configparser
from commands_sql import SQLC,SQLD
from read_file import parse_products

FALHA_OPERACAO = "FALHA AO OPERAR O BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

def create_connection(autocommit = False, database_name='postgres'):
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    try:
        connection = psycopg2.connect(
            host=config['database']['host'],
            database= database_name,
            user=config['database']['user'],
            password=config['database']['password']
        )

        connection.autocommit = True

        cursor = connection.cursor()        
        cursor.execute("SELECT version();")
        cursor.close()
        return SUCESSO_CONEXAO, connection
    except OperationalError as e:
        return FALHA_OPERACAO, str(e)

def create_database(connection, database_name):
    
    print(connection)
    if (connection[0] == FALHA_OPERACAO):
        return
    
    try:
        COMANDO_SQL = SQLC.CRIAR_DATABASE.format(database_name)
        
        cursor = connection[1].cursor()
        cursor.execute(COMANDO_SQL)
        cursor.close()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_OPERACAO, str(e)
    finally:
        connection[1].commit()
        connection[1].close()

def create_tables(connection):
    if (connection[0] == FALHA_OPERACAO):
        return
    
    try:
        cursor = connection[1].cursor()
        
        cursor.execute(SQLC.TABELA_PRODUTO)
        cursor.execute(SQLC.TABELA_SIMILAR)
        cursor.execute(SQLC.TABELA_CATEGORIAS)
        cursor.execute(SQLC.TABELA_P_CATEGORIA)
        cursor.execute(SQLC.TABELA_AVALIACOES)

        cursor.close()
        connection[1].commit()

        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_OPERACAO, str(e)
    finally:
        connection[1].close()

def insert_data(connection, products):
    if (connection[0] == FALHA_OPERACAO):
        return
    try:
        cursor = connection[1].cursor()
        categorias_unicas = set()
        #1º loop varre os produtos e filtra suas categorias, pois sua inserção vem primeiro
        for produto in products:
            for categoria in produto['categories']:
                categorias_unicas.add((categoria['name'], categoria['id']))
        #Inserção das categorias
        for nome_categoria, id_categoria in categorias_unicas:
            cursor.execute(SQLC.INSERE_CATEGORIAS,(id_categoria,nome_categoria))
       
        #2º Loop povoa todas as demais tabela, pois pode ser feita inserção direta    
        for i in range(len(products)): 
            actual_product = products[i]   
            #Insere os produtos
            actual_product_insert = [(actual_product['asin'],actual_product['title'],actual_product['group'],actual_product['salesrank'])] 
            execute_values(cursor, SQLC.INSERE_PRODUTO,actual_product_insert, page_size=10000)
        
            #Insere os produtos e suas devidas categorias 
            for categoria in actual_product['categories']:
                actual_product_insert = [(actual_product['asin'],categoria['id'])]
                execute_values(cursor,SQLC.INSERE_PRODUTO_CATEGORIA,actual_product_insert,page_size=10000)

            #Insere os asins e seus similares
            for i in range(len(actual_product['similar'])):
                actual_product_insert = [(actual_product['asin'],actual_product['similar'][i])]
                execute_values(cursor, SQLC.INSERE_PRODUTO_SIMILAR,actual_product_insert, page_size=10)

            #Insere as avaliações e seus dados atrelados   
            for i in range(len(actual_product['reviews'])):
                actual_product_insert = [(actual_product['asin'],actual_product['reviews'][i]['customer'],actual_product['reviews'][i]['date'],actual_product['reviews'][i]['rating'],actual_product['reviews'][i]['votes'],actual_product['reviews'][i]['helpful'])]
                execute_values(cursor, SQLC.INSERE_AVALIACOES,actual_product_insert, page_size=10000) 
                
        return SUCESSO_CRIAR_BANCO
    except OperationalError as e:
        return FALHA_OPERACAO, str(e)
    finally:
        cursor.close()
        connection[1].close()
