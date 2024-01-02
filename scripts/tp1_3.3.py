from queries import *
from database_config import *
from datetime import datetime
import configparser

CONFIG_PREFIXO = "postgres=# "
CONFIG_VERSAO = "1.0"
AUTORES = "Lucas Chagas, Maria Vitoria e Rodrigo Santos"

STRING_INVALIDO = "Comando inválido. Para ver os comandos disponiveis use: ajuda"

STRING_AJUDA = f"""
Dashboard TP1 BD - {CONFIG_VERSAO} por {AUTORES}

Comandos Disponiveis (Observação: o programa não faz distinção de letras maisculas e minusculas):

[A] - Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e listar os 5 comentários mais úteis e com menor avaliação
    Input: ASIN
[B] - Dado um produto, listar os produtos similares com maiores vendas do que ele
    Input: ASIN
[C] - Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada
    Input: ASIN
[D] - Listar os 10 produtos líderes de venda em cada grupo de produtos
[E] - Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
[F] - Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
[G] - Listar os 10 clientes que mais fizeram comentários por grupo de produto

[H/HELP/AJUDA] - Imprime essa mensagem
[Q/S/QUIT/SAIR] - Sair do Programa
"""

def main():
    config = configparser.ConfigParser()
    config.read('db_config.ini')

    database_name = config['database']['dbname']
    QUERY_SET = QuerySet(database_name)

    printMotd()
    printHelp()

    programa_rodando = True
    while programa_rodando:
        programa_rodando = getInput(QUERY_SET)
        QUERY_SET.init()

    QUERY_SET.close()

def printMotd():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%d/%m/%Y as %H:%M ')
    print(CONFIG_PREFIXO + "Seja Bem vindo ao Dashboard Postgres, hoje é " + data_formatada)

def printQmssg():
    print(CONFIG_PREFIXO + f"Muito obrigado por usar o Dashboard Postgres {CONFIG_VERSAO} =)")

def printHelp():
    print(CONFIG_PREFIXO + STRING_AJUDA)

def getInput(query_set):
    return parseOption(query_set, input(CONFIG_PREFIXO).upper())

def getAsin():
    return input(CONFIG_PREFIXO + "Digite o ASIN do produto\n").upper()

def parseOption(query_set, comando):
    if comando == 'A':
        query_set.query_A(getAsin())
    elif comando == 'B':
        query_set.query_B(getAsin())
    elif comando == 'C':
        query_set.query_C(getAsin())
    elif comando == 'D':
        query_set.query_D()
    elif comando == 'E':
        query_set.query_E()
    elif comando == 'F':
        query_set.query_F()
    elif comando == 'G':
        query_set.query_G()
    elif comando == 'H' or comando == "HELP" or comando == "AJUDA":
        printHelp()
    elif comando == 'Q' or comando == "S" or comando == "EXIT" or comando == "SAIR":
        printQmssg()
        return False
    else:
        print(STRING_INVALIDO)

    return True

if __name__ == '__main__':
    main()