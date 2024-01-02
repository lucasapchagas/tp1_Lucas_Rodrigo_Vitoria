# Trabalho Prático 1 de Bancos de Dados I 📅

Objetivo deste trabalho prático é projetar e implementar um banco de dados sobre produtos vendidos em uma loja de comércio eletrônico, incluindo avaliações e comentários de usuários sobre estes produtos. O trabalho consiste na criação de um Banco de Dados Relacional contendo dados sobre compras de produtos e elaboração de um Dashboard, um painel para monitoramento dos dados de compra, gerando uma série de relatórios.



## Autores 👷🏽👷🏻‍♂️👷🏻‍♀️

- [Lucas Afonso Pereira Chagas](https://www.github.com/lucasapchagas) - 22050316
- [Maria Vitória Costa do Nascimento](https://www.github.com/mariavcnascimento) -  22053592
- [Rodrigo Santos Corrêa](https://www.github.com/rodrigoscorrea) - 22251139


## Requisitos

Para executar este projeto, é essencial a utilização do PostgreSQL como sistema de gerenciamento de banco de dados. Certifique-se de ter o PostgreSQL instalado e configurado adequadamente em seu ambiente de desenvolvimento.


**Importante para a utilização ⚠️**

- [Arquivo de requisitos de dependencias python 🐍](https://github.com/lucasapchagas/tp1_Lucas_Rodrigo_Vitoria/blob/main/documentacao/requirements.txt)

    Ao fazer o clone deste repositorio, entrar na pasta *'/documentacao'* e rodar o arquivo **requirements.txt** utilizando o seguinte comando.

    ```bash
    pip install -r requirements.txt
    ```

- [Arquivo de configuração de variáveis de ambiente 📁](https://github.com/lucasapchagas/tp1_Lucas_Rodrigo_Vitoria/blob/main/scripts/db_config.ini)

    Na pasta *'/scripts'* se encontra o arquivo **db_config.ini** e nele se tem as principais configurações para a utilização dos scripts fornecidos.

    | Parâmetro   | Descrição                           |
    | :---------- | :---------------------------------- |
    | `host`      | IP ou endereço de conexão do SGDB   |
    | `user`      | Username / Nome de usuário do SGDB  |
    | `password`  | Password / Senha de usuário do SGDB |
    | `dbname`    | Nome do banco onde as tabelas serão criadas |
    | `fname ⚠️`  | **Nome do arquivo de entrada** |
## Arquivos 📂

| Arquivo   | Descrição                           |
| :---------- | :---------------------------------- |
| `commands_sql.py` | Usado para armazenar as várias querys SQL usadas no programa   |
| `database_config.py` | Responsável pela configuração e gerenciamento de conexões com o banco de dados PostgreSQL  |
| `queries.py`  | Destinado à execução de consultas SQL no banco de dados |
| `read_file.py`    | Utilizado para leitura e processamento de dados |
| `tp1_3.2.py`  | Extração dos dados do arquivo de entrada, criação do esquema do banco de dados, e povoamento das relações com estes dados |
| `tp1_3.3.py`  | Execução das consultas do Dashboard |
