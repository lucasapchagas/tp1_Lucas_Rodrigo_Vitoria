
# Classe com as querys SLQ utilizadas no programa.
class SQLC:

    CRIAR_DATABASE = """CREATE DATABASE {};"""

    TABELA_PRODUTO = """CREATE TABLE IF NOT EXISTS public.produto (
        asin character varying(15) COLLATE pg_catalog."default" NOT NULL,
        titulo character varying(500) COLLATE pg_catalog."default" NOT NULL,
        grupo character varying(20) COLLATE pg_catalog."default" NOT NULL,
        rank_vendas integer NOT NULL,
        PRIMARY KEY (asin)
    );
    """

    TABELA_SIMILAR = """CREATE TABLE IF NOT EXISTS produto_similar (
        asin VARCHAR(15) NOT NULL,
        asin_similar VARCHAR(15) NOT NULL,
        PRIMARY KEY (asin, asin_similar),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE
    );
    """

    TABELA_CATEGORIAS = """CREATE TABLE IF NOT EXISTS categorias (
        categoria_id integer NOT NULL,
        categoria_nome character varying(100) NOT NULL,
        PRIMARY KEY (categoria_id)
    );
    """

    TABELA_P_CATEGORIA = """CREATE TABLE IF NOT EXISTS produto_categoria (
        asin character varying(15) NOT NULL,
        categoria_id integer NOT NULL,
        PRIMARY KEY (asin, categoria_id),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE,
        FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE CASCADE
    );
    """

    TABELA_AVALIACOES = """CREATE TABLE IF NOT EXISTS avaliacoes (
        avaliacao_id SERIAL NOT NULL,
        asin character varying(15) NOT NULL,
        id_usuario character varying(15) NOT NULL,
        data date NOT NULL,
        nota integer NOT NULL,
        votos integer NOT NULL,
        votos_util integer NOT NULL,
        PRIMARY KEY (avaliacao_id),
        FOREIGN KEY (asin) REFERENCES produto(asin) ON DELETE CASCADE
    );
    """

    INSERE_PRODUTO_CATEGORIA = """INSERT INTO produto_categoria(asin, categoria_id) VALUES %s;"""

    INSERE_PRODUTO_SIMILAR = """INSERT INTO produto_similar(asin, asin_similar) VALUES %s;"""

    INSERE_CATEGORIAS = """INSERT INTO categorias(categoria_id, categoria_nome) VALUES (%s,%s);"""

    INSERE_AVALIACOES = """INSERT INTO avaliacoes(asin, id_usuario, data,nota, votos, votos_util) VALUES %s;"""

    INSERE_PRODUTO = """INSERT INTO produto(asin, titulo, grupo, rank_vendas) VALUES %s;"""

# Classe com as query SQL para a dashboard do programa
class SQLD:

    # Dado um produto, listar os 5 comentários mais úteis e com maior avaliação 
    LETRA_A1P = """SELECT id_usuario, data,nota,votos_util FROM avaliacoes
                WHERE asin = %s AND nota >= 4
                ORDER BY votos_util DESC, nota DESC
                LIMIT 5;
                """
    
    # Dado um produto, listar os 5 comentários mais úteis e com menor avaliação
    LETRA_A2P = """SELECT id_usuario,data,nota,votos_util FROM avaliacoes
                WHERE asin = %s AND nota <= 3
                ORDER BY votos_util ASC,nota DESC
                LIMIT 5;
                """
    
    # Dado um produto, listar os produtos similares com maiores vendas do que ele
    LETRA_B = """ SELECT p2.asin, p2.titulo, p2.rank_vendas FROM produto_similar ps
                INNER JOIN produto p1 ON p1.asin = ps.asin
                INNER JOIN produto p2 ON p2.asin = ps.asin_similar
                WHERE p1.asin = %s AND p2.rank_vendas < p1.rank_vendas
                ORDER BY rank_vendas DESC;
                """
    
    # Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada
    LETRA_C = """SELECT data as data_avaliacao, AVG(nota) as media_avaliacao
                FROM avaliacoes
                WHERE asin = %s
                GROUP BY data
                ORDER BY data;
                """
    
    # Listar os 10 produtos líderes de venda em cada grupo de produtos
    LETRA_D = """
                SELECT grupo, asin, titulo, rank_vendas
                FROM produto
                WHERE grupo = %s AND rank_vendas <> -1 AND rank_vendas <> 0
                ORDER BY grupo, rank_vendas ASC
                FETCH FIRST 10 ROWS ONLY;
                """
    
    # Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
    LETRA_E = """SELECT a.asin, AVG(a.votos_util) as media_votos_util
                FROM avaliacoes a
                INNER JOIN produto p ON p.asin = a.asin
                GROUP BY a.asin
                ORDER BY media_votos_util DESC
                LIMIT 10;
                """
    
    # Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
    LETRA_F = """SELECT c.categoria_nome, AVG(a.votos_util) as media_votos_util
                FROM avaliacoes a
                INNER JOIN produto_categoria pc ON pc.asin = a.asin
                INNER JOIN categorias c ON c.categoria_id = pc.categoria_id
                GROUP BY c.categoria_nome
                ORDER BY media_votos_util DESC
                LIMIT 5;
                """
    
    # Listar os 10 clientes que mais fizeram comentários por grupo de produto
    LETRA_G = """SELECT p.grupo, a.id_usuario, COUNT(*) as total_comentarios
                FROM avaliacoes a
                INNER JOIN produto p ON p.asin = a.asin
                WHERE p.grupo = %s
                GROUP BY p.grupo, a.id_usuario
                ORDER BY p.grupo, total_comentarios DESC
                LIMIT 10;
                """