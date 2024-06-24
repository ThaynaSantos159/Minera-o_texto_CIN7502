# scrapy_project/items.py

"""
Módulo items.py
Este módulo define a estrutura dos itens que serão extraídos pelo projeto Scrapy. Ele é uma parte crucial do projeto,
pois especifica os campos de dados que o Scrapy irá coletar durante o processo de web scraping.
## Objetivo
O principal objetivo deste módulo é criar uma classe que representa os itens a serem extraídos das páginas web.
Um item em Scrapy é um contêiner para armazenar os dados coletados, similar a um dicionário Python, mas com a capacidade
de organizar e validar dados de maneira mais eficiente.

## Importações
- **scrapy**: Biblioteca de código aberto que facilita a extração de dados de websites. Permite a coleta de dados
estruturados, manipulação de requisições, e exportação dos dados em vários formatos.
## Estrutura dos Itens
A classe `ScrapyProjectItem` herda de `scrapy.Item` e define campos para armazenar as informações coletadas.
Cada campo é uma instância de `scrapy.Field`, que especifica os diferentes tipos de dados que serão extraídos.
## Campos Definidos

- **title**: Campo para armazenar o título da avaliação do produto.
- **reviewer_name**: Campo para armazenar o nome do revisor que escreveu a avaliação.
- **reviewer_position**: Campo para armazenar a posição do revisor, como "Gerente" ou "Diretor".
- **reviewer_company**: Campo para armazenar o nome da empresa do revisor.
- **published_date**: Campo para armazenar a data de publicação da avaliação.
- **grades**: Campo para armazenar as notas de avaliação dadas pelo revisor, como "Custo-benefício" e "Facilidade de uso".
- **answers**: Campo para armazenar perguntas e respostas da avaliação, contendo feedback detalhado ou opiniões específicas.

## Notas
Este módulo é fundamental para definir a estrutura dos dados que serão coletados e armazenados, facilitando a
organização e análise dos dados raspados. A estrutura definida aqui permite que o Scrapy trate e organize as
informações de forma eficiente e estruturada, garantindo que os dados coletados sejam úteis para análises posteriores.
"""

# Nota: Scrapy é uma biblioteca de código aberto e 'framework' para extração de dados de 'websites'.
# Ela fornece ferramentas para scraping eficiente de páginas da 'Web', permitindo a coleta de dados estruturados.
# Scrapy é especialmente útil para projetos de 'web' scraping e crawling de dados em larga escala,
# permitindo manipular requisições, seguir 'links' e exportar os dados coletados em diversos formatos.
# Utilizamos Scrapy neste projeto para automatizar a extração de avaliações de produtos de 'sites' especializados,
# facilitando a análise e armazenamento dos dados coletados num banco de dados.


# Importação da biblioteca scrapy
import scrapy


# Define uma classe chamada ScrapyProjectItem que herda de scrapy.Item
class ScrapyProjectItem(scrapy.Item):
    """Classe para definir os campos de itens que serão extraídos pelo Scrapy."""

    # Campo para armazenar o título da avaliação
    title = scrapy.Field()

    # Campo para armazenar o nome do revisor
    reviewer_name = scrapy.Field()

    # Campo para armazenar a posição do revisor
    reviewer_position = scrapy.Field()

    # Campo para armazenar a empresa do revisor
    reviewer_company = scrapy.Field()

    # Campo para armazenar a data de publicação da avaliação
    published_date = scrapy.Field()

    # Campo para armazenar as notas de avaliação
    grades = scrapy.Field()

    # Campo para armazenar perguntas e respostas da avaliação
    answers = scrapy.Field()

