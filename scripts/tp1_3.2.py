from database_config import *
import configparser
import time
from read_file import parse_products


def main():
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    database_name = config['database']['dbname'] # Nome do Banco de dados -> Configurado em db_config.ini
    products_file = config['database']['fname'] # Nome do Arquivo de entrada -> Configurado em db_config.ini

    # Criar a database     
    create_database(create_connection(autocommit=True), database_name)

    # Criar as tabelas
    create_tables(create_connection(database_name=database_name))

    # Povoamente das tabelas e parsing dos produtos
    insert_data(create_connection(database_name=database_name), parse_products(products_file))


if __name__ == '__main__':
    main()