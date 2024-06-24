# scrapy_project/models.py


# Nota: SQLAlchemy é uma biblioteca ORM (Object-Relational Mapping) para Python, que facilita a interação
# entre objetos Python e bancos de dados relacionais de maneira coerente e eficiente. Ela permite definir
# estruturas de tabelas em código Python e automatizar a transferência de dados entre o banco de dados
# e os objetos Python de forma transparente.

# A função create_engine é usada para iniciar a conexão com o banco de dados, neste caso, um banco SQLite.
# As classes Column, Integer, String, e Text são tipos de coluna que podem ser usados para definir
# os campos das tabelas no banco de dados.

# Base é uma classe gerada pela função declarative_base, que serve como classe base para todas as
# entidades do modelo. Os modelos definidos herdam de Base e são mapeados automaticamente para as
# tabelas no banco de dados.

# Importação de componentes da biblioteca SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base



# Define a base para as classes declarativas do SQLAlchemy
Base = declarative_base()


def db_connect():
    """
    Estabelece a conexão com o banco de dados.

    Retorna:
        engine: Objeto de engine do SQLAlchemy conectado ao banco de dados SQLite.
    """
    return create_engine('sqlite:///scrapy_project.db', connect_args={'check_same_thread': False})


def create_table(engine):
    """
    Cria a tabela no banco de dados. Se a tabela já existir, ela será recriada.

    Args:
        engine: O objeto de engine do SQLAlchemy.
    """
    Base.metadata.drop_all(engine)  # Limpar a tabela existente
    Base.metadata.create_all(engine)  # Criar a tabela com a nova estrutura


class Item(Base):
    """
    Define a estrutura da tabela 'items' no banco de dados.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)  # Coluna de ID primária
    title = Column(Text)  # Coluna de título
    reviewer_name = Column(String(100))  # Coluna de nome do avaliador
    reviewer_position = Column(String(100))  # Coluna de posição do avaliador
    reviewer_company = Column(String(100))  # Coluna de empresa do avaliador
    published_date = Column(String(100))  # Coluna de data de publicação
    published_time = Column(String)

    # Grades como colunas separadas
    custo_beneficio = Column(String(50))
    facilidade_uso = Column(String(50))
    funcionalidades = Column(String(50))
    suporte_cliente = Column(String(50))

    # Answers como colunas separadas
    preferencias = Column(Text)
    melhorias = Column(Text)
    problemas_resolvidos_beneficios = Column(Text)

