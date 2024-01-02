from database_config import *
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    database_name = config['database']['dbname']
    products_file = config['database']['fname']

    # Criar a database     
    conexao = create_connection()
    create_database(conexao, database_name)

    # Criar as tabelas
    create_tables(create_connection(False, database_name))

    # Ler o arquivo de entrada e povoar as tabelas
    products = parse_products(products_file)
    insert_data(create_connection(False, database_name), products)

if __name__ == '__main__':
    main()