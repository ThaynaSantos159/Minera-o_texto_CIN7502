# scrapy_project/spiders/example_spider.py

"""
Módulo example_spider.py
Este módulo contém a definição de um Spider do Scrapy responsável por coletar avaliações de um produto específico no
site B2B Stack. O Spider, denominado `ExampleSpider`, automatiza a navegação e extração de dados das páginas web,
facilitando a coleta de informações estruturadas para posterior análise.
## Objetivo
O objetivo principal deste módulo é definir um Spider que navega por páginas de avaliações de produtos e extrai
 informações relevantes, como o título da avaliação, nome do revisor, posição, empresa, data de publicação, notas e
 perguntas/respostas. Essas informações são coletadas de forma sistemática e armazenadas em itens que podem ser
 processados e armazenados em um banco de dados ou outro formato estruturado.
## Componentes Importantes
- **scrapy**: Biblioteca principal utilizada para criar o Spider e definir os métodos de extração de dados.
- **ScrapyProjectItem**: Classe definida no módulo `items.py` que especifica a estrutura dos dados a serem extraídos
    pelo Spider.

## Funcionalidade do Spider
- **Nome**: `avaliacoes_b2bstack_astrea`
  - Define o identificador único do Spider.
- **Domínios Permitidos**: `['www.b2bstack.com.br']`
  - Restringe a ação do Spider a este domínio específico, prevenindo a coleta de dados fora do escopo desejado.
- **URLs Iniciais**: `['https://www.b2bstack.com.br/product/astrea/avaliacoes']`
  - Define as URLs de onde o Spider começará a coleta de dados.
## Métodos Principais
### `start_requests(self)`
Este método inicializa as requisições HTTP para as URLs definidas em `start_urls`. Ele configura cabeçalhos
personalizados para evitar bloqueios automáticos por parte do servidor e envia as requisições.
- **Cabeçalhos Personalizados**: Inclui informações de user-agent para emular um navegador e evitar detecção como um bot.
### `parse(self, response)`
Método de callback principal que processa a resposta das requisições. Ele extrai os elementos de interesse das páginas
de avaliação e cria instâncias de `ScrapyProjectItem` com os dados extraídos.

- **Extração de Dados**:
  - **Título da Avaliação**: Extraído do elemento `<h3>`.
  - **Nome do Revisor**: Extraído do elemento `<p class="reviewer">`.
  - **Posição e Empresa do Revisor**: Extraídos de `<span>` elementos dentro de um div específico.
  - **Data de Publicação**: Extraída de `<p class="published">`.
  - **Notas de Avaliação**: Coletadas e armazenadas como um dicionário.
  - **Perguntas e Respostas**: Coletadas e armazenadas como um dicionário.

- **Navegação de Páginas**: Verifica a existência de um link para a próxima página e, se presente, envia uma nova
requisição para continuar a coleta de dados.

### Exemplo de Uso

Este módulo pode ser executado como parte de um projeto Scrapy para coletar avaliações de produtos, permitindo a
análise detalhada de feedbacks de usuários. As informações estruturadas coletadas podem ser utilizadas para identificar
tendências, comparar produtos e obter insights valiosos para melhorias ou decisões de negócio.

## Notas
Este arquivo é uma peça fundamental para a automação da coleta de dados. Ele implementa um Spider que automatiza a
navegação por páginas web e a extração de dados, seguindo as melhores práticas para scraping e garantindo a integridade
e a precisão dos dados coletados.

"""

# Nota: O módulo Scrapy é utilizado para fornecer funcionalidades de web scraping e crawling, permitindo
# a extração eficiente de dados de websites. É uma das bibliotecas mais poderosas e flexíveis para scraping
# na linguagem Python, suportando tanto a coleta de abundância de dados quanto o processamento
# complexo de páginas web.

# ScrapyProjectItem é uma classe definida no módulo items do projeto, que estende scrapy.Item. Esta classe
# é usada para definir os campos dos dados que serão coletados pelo spider. Cada campo é uma instância de
# scrapy.Field, permitindo a personalização e validação dos dados coletados durante o processo de scraping.

# Exemplo de uso no projeto:
# Utilizamos o ScrapyProjectItem para estruturar e padronizar a informação raspada, assegurando que todos
# os dados necessários sejam coletados e organizados de maneira consistente. Por exemplo, dados como título,
# nome do revisor, posição, empresa do revisor, data de publicação e outros detalhes são definidos como
# campos dentro do ScrapyProjectItem. Isso facilita a manipulação, armazenamento e análise dos dados
# posteriormente.

# Este approach modular e estruturado ajuda a manter o código organizado, facilita a manutenção e a
# extensão do projeto, permitindo a adaptação ou a adição de novos campos com mínima alteração no código
# existente do spider.

# Importação do módulo scrapy e de itens definidos no projeto
import scrapy
from scrapy_project.items import ScrapyProjectItem


class ExampleSpider(scrapy.Spider):
    """Spider para coletar avaliações do produto Astrea no site B2B Stack."""

    # Nome do Spider
    name = 'avaliacoes_b2bstack_astrea'
    # Domínios permitidos para o Spider
    allowed_domains = ['www.b2bstack.com.br']
    # URLs iniciais para começar a coleta
    start_urls = ['https://www.b2bstack.com.br/product/astrea/avaliacoes']

    def start_requests(self):
        """Define cookies e cabeçalhos personalizados para as requisições iniciais."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 '
                          'Safari/537.3'
        }
        # Faz requisições para cada URL inicial com cabeçalhos personalizados
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        """Extrai informações das avaliações da página de resposta."""
        # Seleciona todos os elementos de avaliação na página
        reviews = response.xpath('//div[@class="review"]')

        for review in reviews:
            # Extrai o título da avaliação
            title = review.xpath('.//h3/text()').get()
            # Extrai o nome do revisor
            reviewer_name = review.xpath('.//p[@class="reviewer"]/text()').get()
            # Extrai a posição do revisor
            reviewer_position = review.xpath('.//div[@class="flex gg-1"]//span[1]/text()').get()
            # Extrai a empresa do revisor
            reviewer_company = review.xpath('.//div[@class="flex gg-1"]//span[2]/text()').get()
            # Extrai a data de publicação da avaliação
            published_date = review.xpath('.//p[@class="published"]/text()').get()

            # Verificações para evitar erros de 'NoneType'
            title = title.strip() if title else 'No title'
            reviewer_name = reviewer_name.strip() if reviewer_name else 'No name'
            reviewer_position = reviewer_position.strip() if reviewer_position else 'No position'
            reviewer_company = reviewer_company.strip() if reviewer_company else 'No company'
            published_date = published_date.strip() if published_date else 'No date'

            # Extrai as notas de avaliação
            grades = {
                grade.xpath('.//p/text()').get().strip(): grade.xpath(
                    './/div[@class="star starsize-16"]/div/@style').get().strip()
                for grade in review.xpath('.//div[@class="grades"]/div')
            }

            # Extrai perguntas e respostas das avaliações
            answers = {}
            answer_blocks = review.xpath('.//div[@class="answers"]/h4')
            for block in answer_blocks:
                question = block.xpath('./text()').get().strip()
                answer = block.xpath('./following-sibling::p[@class="answer"][1]/text()').get().strip()
                answers[question] = answer

            # Cria um item ScrapyProjectItem com os dados extraídos
            scrapy_item = ScrapyProjectItem(
                title=title,
                reviewer_name=reviewer_name,
                reviewer_position=reviewer_position,
                reviewer_company=reviewer_company,
                published_date=published_date,
                grades=grades,
                answers=answers
            )

            # Envia o item para o pipeline
            yield scrapy_item

        # Procura pelo link da próxima página e faz uma nova requisição se encontrado
        next_page = response.xpath('//a[@class="next_page"]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
