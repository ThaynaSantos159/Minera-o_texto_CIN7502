# scrapy_project/pipelines.py

"""
Módulo pipelines.py
Este módulo define o pipeline para processar e armazenar os itens coletados pelos Spiders no projeto Scrapy.
O pipeline é responsável por tomar os dados extraídos e processá-los para armazenamento em um banco de dados,
 garantindo que as informações coletadas sejam armazenadas de forma estruturada e consistente.
## Objetivo
O objetivo principal deste módulo é fornecer uma estrutura para processar os itens coletados pelos Spiders e inseri-los
em um banco de dados SQLite. Isso é feito através do uso do SQLAlchemy, uma biblioteca ORM (Object-Relational Mapping)
que facilita a interação entre os objetos Python e os bancos de dados relacionais.
## Componentes Importantes
- **sessionmaker**: Função do SQLAlchemy que é utilizada para configurar e criar sessões de banco de dados, permitindo múltiplas operações com uma única transação.
- **Item**: Classe definida no módulo `models.py` do projeto que representa a estrutura de dados do banco de dados para os itens coletados.
- **db_connect**: Função que configura e retorna uma conexão ao banco de dados.
- **create_table**: Função que inicializa o esquema do banco de dados, criando ou recriando tabelas conforme as definições das classes ORM.

## Funcionalidade do Pipeline

### ScrapyProjectPipeline

Esta classe define o pipeline que processa cada item coletado e o armazena no banco de dados.

#### `__init__(self)`

- Inicializa a conexão com o banco de dados usando a função `db_connect`.
- Cria a tabela no banco de dados caso ainda não exista, usando a função `create_table`.
- Configura uma fábrica de sessões (`sessionmaker`) ligada ao engine do banco de dados.

#### `process_item(self, item, spider)`

Este método processa cada item coletado pelo Spider e o armazena no banco de dados.

- **Parâmetros**:
  - `item` (dict): O item coletado pelo Spider, contendo dados como título, nome do revisor, posição, empresa,
  data de publicação, notas, perguntas e respostas.
  - `spider` (scrapy.Spider): A instância do Spider que coletou o item.

- **Retorno**:
  - `dict`: O item processado, retornado após ser armazenado no banco de dados.

- **Processo**:
  - Cria uma nova sessão de banco de dados.
  - Cria uma instância do modelo `Item` e preenche os campos com os valores extraídos.
  - Adiciona o item à sessão e comita a transação.
  - Em caso de erro, desfaz a transação e gera uma exceção.
  - Fecha a sessão ao final do processo.

### Exemplo de Uso

Este módulo é utilizado para gerenciar transações durante a execução dos Spiders. Cada item raspado é processado e
armazenado no banco de dados através das sessões criadas, garantindo que todas as operações sejam agrupadas em
transações, proporcionando eficiência e segurança no acesso ao banco de dados.

### Notas

- A estrutura da tabela `items` é definida pela classe `Item`, que facilita a manipulação dos dados coletados como
objetos Python, mapeados diretamente para o banco de dados.
- Este arquivo é crucial para a automação da coleta e armazenamento de dados, garantindo que as informações sejam
processadas de maneira eficiente e sem erros.

"""


# Nota: A função sessionmaker do SQLAlchemy é utilizada para configurar e criar sessões de banco de dados.
# Uma sessão permite executar múltiplas operações com uma única transação, garantindo consistência e
# gerenciamento de estado do banco de dados durante o trabalho com objetos ORM.

# No contexto do nosso projeto, a sessão é essencial para interações com o banco de dados que incluem
# adicionar, modificar ou deletar registros. A função db_connect, definida no módulo models, configura
# e retorna uma conexão ao banco de dados, que é usada pelo sessionmaker para criar sessões.

# A função create_table é usada para inicializar o schema do banco de dados com base nas definições de
# classe do modelo ORM, neste caso, criando ou recriando tabelas como definido.

# Exemplo de uso no projeto:
# Usamos o sessionmaker para gerenciar transações durante a execução do spider, onde cada item raspado
# é processado e armazenado no banco de dados através de sessões. Isso garante que todas as operações
# sejam agrupadas em transações, proporcionando eficiência e segurança no acesso ao banco de dados.

# A estrutura da tabela 'items' é definida pela classe Item, que é um modelo ORM derivado do Base,
# facilitando a manipulação dos dados coletados como objetos Python, que são diretamente mapeados para
# o banco de dados.


# Importação de componentes do SQLAlchemy e definições do módulo models
from sqlalchemy.orm import sessionmaker
from scrapy_project.models import Item, db_connect, create_table


class ScrapyProjectPipeline(object):
    """Pipeline para processar e armazenar itens coletados pelo Spider."""

    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir."""
        # Conecta ao banco de dados
        engine = db_connect()
        # Cria a tabela no banco de dados, se ainda não existir
        create_table(engine)
        # Cria uma fábrica de sessões ligadas ao engine
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Processa e armazena cada item no banco de dados.

        Args:
            item (dict): O item coletado pelo Spider.
            spider (scrapy.Spider): A instância do Spider que coletou o item.

        Returns:
            dict: O item processado.
        """
        # Cria uma nova sessão
        session = self.Session()
        # Cria uma instância do modelo Item
        scraped_item = Item()

        # Preenche os campos do item com os valores extraídos
        scraped_item.title = item.get('title', 'No title')
        scraped_item.reviewer_name = item.get('reviewer_name', 'No name')
        scraped_item.reviewer_position = item.get('reviewer_position', 'No position')
        reviewer_company = item.get('reviewer_company', 'No company')
        scraped_item.reviewer_company = self.clean_reviewer_company(reviewer_company)
        # Processar data e hora de publicação
        published_date = item.get('published_date', 'No date')
        scraped_item.published_date, scraped_item.published_time = self.extract_date_and_time(published_date)

        grades = item.get('grades', {})
        scraped_item.custo_beneficio = self.convert_grade(grades.get('Custo beneficio', 'width:0%;'))
        scraped_item.facilidade_uso = self.convert_grade(grades.get('Facilidade de uso', 'width:0%;'))
        scraped_item.funcionalidades = self.convert_grade(grades.get('Funcionalidades', 'width:0%;'))
        scraped_item.suporte_cliente = self.convert_grade(grades.get('Suporte ao cliente', 'width:0%;'))

        # Extração dos valores para os campos de answers
        answers = item.get('answers', {})
        scraped_item.preferencias = answers.get('O que você mais gosta?', 'No answer')
        scraped_item.melhorias = answers.get(
            'O que você não gosta, ou acha que poderia melhorar ainda mais neste produto?', 'No answer')
        scraped_item.problemas_resolvidos_beneficios = answers.get(
            'Quais são os problemas que você resolveu com astrea? e quais benefícios você obteve?', 'No answer')

        try:
            # Adiciona o item à sessão e comita a transação
            session.add(scraped_item)
            session.commit()
        except Exception as e:
            # Em caso de erro, desfaz a transação
            session.rollback()
            raise e
        finally:
            # Fecha a sessão
            session.close()
        return item

    def convert_grade(self, grade_str):
        """
        Converte uma string de porcentagem em uma nota de 1 a 5 estrelas.

        Args:
            grade_str (str): A string da porcentagem (e.g., 'width:80%;').

        Returns:
            int: A nota correspondente de 1 a 5 estrelas.
        """
        try:
            # Extrai a porcentagem da string
            percentage = float(grade_str.strip('width:; %')) / 100.0
            # Converte a porcentagem para a escala de 1 a 5 estrelas
            return round(percentage * 5)
        except ValueError:
            return 0  # Retorna 0 se a conversão falhar

    def extract_date_and_time(self, published_date_str):
        """
        Extrai a data e a hora da string de publicação.

        Args:
            published_date_str (str): A string da data de publicação (e.g., 'Publicado em 13 de Maio de 2020, 00:17').

        Returns:
            tuple: A data e a hora separadas (e.g., ('13 de Maio de 2020', '00:17')).
        """
        try:
            # Remove a parte "Publicado em" e divide em data e hora
            clean_str = published_date_str.replace('Publicado em ', '')
            date_part, time_part = clean_str.split(', ')
            return date_part, time_part
        except ValueError:
            return 'No date', 'No time'  # Retorna valores padrão se a extração falhar

    def clean_reviewer_company(self, company_str):
        """
        REMOVE O PREFIXO 'NA ' DA STRING DA EMPRESA DO REVISOR.

        Args:
            company_str (str): A STRING DA EMPRESA DO REVISOR (E.G., 'NA AMARAL ADVOGADOS').

        Returns:
            str: A STRING LIMPA SEM O PREFIXO 'NA ' (E.G., 'AMARAL ADVOGADOS').
        """
        return company_str.replace('na ', '').strip() if company_str.startswith('na ') else company_str.strip()