import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import OperationalError
import configparser
from commands_sql import SQLC
import time
import gc

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

        connection.autocommit = autocommit

        cursor = connection.cursor()        
        cursor.execute("SELECT version();")
        cursor.close()
        return SUCESSO_CONEXAO, connection
    except OperationalError as e:
        print(e)
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
        print(e)
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
        print(e)
        return FALHA_OPERACAO, str(e)
    finally:
        connection[1].close()

def insert_data(connection, data):
    if connection[0] == FALHA_OPERACAO:
        return FALHA_OPERACAO
    try:
        cursor = connection[1].cursor()

        products = data[0]
        reviews = data[1]
        similar = data[2]
        categories = data[3]
        p_categories = data[4]

        # Inserção dos produtos
        tempo = time.time()
        execute_batch(cursor, SQLC.INSERE_PRODUTO, products, page_size= 1000)
        print(f"SQLC.INSERE_PRODUTO: {time.time() - tempo:.2f}s")

        # Inserção das categorias
        tempo = time.time()
        execute_batch(cursor, SQLC.INSERE_CATEGORIAS, categories, page_size= 1000)
        print(f"SQLC.INSERE_CATEGORIAS: {time.time() - tempo:.2f}s")

        # Inserção dos produtos similares
        tempo = time.time()
        execute_batch(cursor, SQLC.INSERE_PRODUTO_SIMILAR, similar, page_size= 1000)
        print(f"SQLC.INSERE_PRODUTO_SIMILAR: {time.time() - tempo:.2f}s")

        del similar
        gc.collect()

        # Inserção dos produtos e suas categorias
        tempo = time.time()
        execute_batch(cursor, SQLC.INSERE_PRODUTO_CATEGORIA, p_categories, page_size= 1000)
        print(f"SQLC.INSERE_PRODUTO_CATEGORIA: {time.time() - tempo:.2f}s")
        
        del p_categories
        gc.collect()

        # Inserção das avaliações
        tempo = time.time()
        execute_batch(cursor, SQLC.INSERE_AVALIACOES, reviews, page_size= 1000)
        print(f"SQLC.INSERE_AVALIACOES: {time.time() - tempo:.2f}s")
        
        connection[1].commit()

        del data, reviews, products, categories
        gc.collect()

        return SUCESSO_CRIAR_BANCO
    except Exception as e:
        print(e)
        return FALHA_OPERACAO, str(e)
    finally:
        cursor.close()
        connection[1].close()