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

        del data
        gc.collect()

        tempo_inicial = time.time()

        # Inserção dos produtos
        execute_batch(cursor, SQLC.INSERE_PRODUTO, products)
        connection[1].commit()
        
        del products
        gc.collect()

        # Inserção das categorias
        execute_batch(cursor, SQLC.INSERE_CATEGORIAS, categories)
        connection[1].commit()

        del categories
        gc.collect()

        # Inserção dos produtos e suas categorias
        execute_batch(cursor, SQLC.INSERE_PRODUTO_CATEGORIA, p_categories)
        connection[1].commit()
        
        del p_categories
        gc.collect()

        # Inserção dos produtos similares
        execute_batch(cursor, SQLC.INSERE_PRODUTO_SIMILAR, similar)
        connection[1].commit()
        
        del similar
        gc.collect()

        # Inserção das avaliações
        execute_batch(cursor, SQLC.INSERE_AVALIACOES, reviews)
        connection[1].commit()
        
        del reviews
        gc.collect()

        tempo_final = time.time()
        print(f"Dados completamente inseridos no banco: {tempo_final - tempo_inicial:.2f}s")

        return SUCESSO_CRIAR_BANCO
    except Exception as e:
        print(e)
        return FALHA_OPERACAO, str(e)
    finally:
        cursor.close()
        connection[1].close()