# scrapy_project/settings.py

"""
Módulo de configuração do Scrapy para o projeto 'scrapy_project'.
"""

# Define os módulos de Spider para o Scrapy procurar
SPIDER_MODULES = ['spiders']

# Define o módulo para novos Spiders
NEWSPIDER_MODULE = 'spiders'

# Configura o pipeline para processar os itens coletados
ITEM_PIPELINES = {
    'scrapy_project.pipelines.ScrapyProjectPipeline': 300,
    # O valor 300 é a prioridade do pipeline. Menor valor significa maior prioridade.
}

# Define o User-Agent que será utilizado nas requisições HTTP
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/58.0.3029.110 '
              'Safari/537.3'
              )

# Define um atraso entre os downloads para evitar sobrecarga no servidor
DOWNLOAD_DELAY = 2
