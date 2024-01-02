import psycopg2
from psycopg2 import OperationalError
from commands_sql import SQLD
from database_config import create_connection

FALHA_CONEXAO = "ERRO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CONEXAO = "SUCESSO AO CONECTAR AO BANCO DE DADOS"
SUCESSO_CRIAR_BANCO = "SUCESSO AO CRIAR BANCO DE DADOS"

class QuerySet:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = create_connection(False, self.database_name)
        
        if (self.connection[0] == FALHA_CONEXAO):
            print(FALHA_CONEXAO)
        else:
            self.cursor = self.connection[1].cursor()
    
    def init(self):
        self.close()

        self.connection = create_connection(False, self.database_name)
        
        if (self.connection[0] == FALHA_CONEXAO):
            print(FALHA_CONEXAO)
        else:
            self.cursor = self.connection[1].cursor()

    def close(self):
        if (self.connection[0] == FALHA_CONEXAO):
            print(FALHA_CONEXAO)
        else:
            self.connection[1].cursor().close()
            self.connection[1].close()

    # Letra a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação
    def query_A(self, asin): 
        try:
            print("A) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação:\n")
            print("Os 5 comentarios mais uteis e com maior avaliacao:")
            print("ASIN: {}\n".format(asin))
            self.cursor.execute(SQLD.LETRA_A1P,(asin,))
            print("USUARIO | DATA (YMD) | AVALIACOES | VOTOS UTEIS \n")
            
            linhas = self.cursor.fetchall()
            dict_aux = {} 
            for linha in linhas:
                dict_aux = {"usuario":linha[0],"data":linha[1],"nota":linha[2],"votos_uteis":linha[3]}
                print("{} | {} | {} | {}".format(dict_aux['usuario'],dict_aux['data'],dict_aux['nota'],dict_aux['votos_uteis']))

            print("\nOs 5 comentarios mais uteis e com menor avaliacao:")
            print("ASIN: {}\n".format(asin))    
            self.cursor.execute(SQLD.LETRA_A2P,(asin,))
            print("USUARIO | DATA(YMD) | AVALIACOES | VOTOS UTEIS \n")
            
            linhas = self.cursor.fetchall()
            dict_aux = {}
            for linha in linhas:
                dict_aux = {"usuario":linha[0], "data":linha[1],"nota":linha[2],"votos_uteis":linha[3]}
                print("{} | {} | {} | {}".format(dict_aux['usuario'],dict_aux['data'],dict_aux['nota'],dict_aux['votos_uteis']))
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra b) Dado um produto, listar os produtos similares com maiores vendas do que ele
    def query_B(self, asin):
        try:
            self.cursor.execute(SQLD.LETRA_B,(asin,))
            print("B) Dado um produto, listar os produtos similares com maiores vendas do que ele: \n")
            print("\nASIN | PRODUTO SIMILAR | Rank de vendas\n")
            linhas = self.cursor.fetchall()
            for linha in linhas:
                print(linha)   
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada
    def query_C(self, asin): 
        try:
            self.cursor.execute(SQLD.LETRA_C,(asin,))
            print("C) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada: \nProduto: {}".format(asin))
            print("Data YMD   | Media das Avaliacoes")
            dict_aux = {}
            linhas = self.cursor.fetchall()
            for linha in linhas:
                dict_aux = {"data":linha[0], "media":linha[1]}
                print("{} | {:.2f}".format(dict_aux['data'],dict_aux['media']))
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra d) Listar os 10 produtos líderes de venda em cada grupo de produtos
    def query_D(self):
        try:
            self.cursor.execute("""SELECT DISTINCT grupo FROM produto""")
            grupos = self.cursor.fetchall()
            
            print("D) Listar os 10 produtos líderes de venda em cada grupo de produtos:\n")
            print("Os itens estao descrito na ordem decrescente, ou seja, do mais vendido pro menos vendido")
            for grupo in grupos:
                print("Grupo: ",grupo[0])
                print("ASIN | TITULO | RANK DE VENDAS")
                self.cursor.execute(SQLD.LETRA_D,(grupo,))
                linhas = self.cursor.fetchall()
                
                for linha in linhas:
                    print(linha[1:])   
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
    def query_E(self):
        try:
            self.cursor.execute(SQLD.LETRA_E)
            print("E) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto:\n")
            print("ASIN       | MEDIA AVALIACOES POSITIVAS")

            dict_aux = {}
            linhas = self.cursor.fetchall()
            for linha in linhas:
                dict_aux = {"asin":linha[0],"media":linha[1]}
                print("{} | {:.2f}".format(dict_aux['asin'],float(dict_aux['media'])))
            
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
    def query_F(self):
        try:
            self.cursor.execute(SQLD.LETRA_F)
            print("F) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto:\n")
            print("CATEGORIAS | MEDIA AVALIACAO UTIL")
            linhas = self.cursor.fetchall()

            dict_aux = {}
            for linha in linhas:
                dict_aux = {"categories":linha[0],"media":linha[1]}
                print("{}  {:.2f}".format(dict_aux['categories'],float(dict_aux['media'])))
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()

    # Letra g) Listar os 10 clientes que mais fizeram comentários por grupo de produto
    def query_G(self):
        try:    
            print("G) Listar os 10 clientes que mais fizeram comentários por grupo de produto:\n")
            print("GRUPO | ID_USUARIO | TOTAL COMENTARIOS")
            self.cursor.execute("""SELECT DISTINCT grupo FROM produto""")
            grupos = self.cursor.fetchall()
            for grupo in grupos:
                print("\nGRUPO: {}".format(grupo[0]))
                self.cursor.execute(SQLD.LETRA_G,(grupo,))
                linhas = self.cursor.fetchall()
                for linha in linhas:
                    print(linha[1:])
        except Exception as error:
            print("Aconteceu um erro: ", error)
            self.close()