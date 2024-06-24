import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string
import sqlite3

# Carregar o modelo de língua portuguesa do spaCy
nlp = spacy.load('pt_core_news_sm')

# Certifique-se de que as stopwords do NLTK estão baixadas
nltk.download('stopwords')
nltk.download('punkt')

# Lista de stopwords em português
stop_words = set(stopwords.words('portuguese'))

# Configurações do banco de dados
db_path = './scrapy_project.db'  # Substitua pelo caminho do seu banco de dados
table_name = 'items'  # Nome da tabela que contém os comentários
columns_to_tokenize = ['preferencias', 'melhorias', 'problemas_resolvidos_beneficios']  # Colunas a serem tokenizadas

# Conectar ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Adicionar novas colunas para armazenar os tokens se ainda não existirem
for column in columns_to_tokenize:
    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column}_tokens TEXT")
    except sqlite3.OperationalError:
        # A coluna já existe
        pass

# Função de pré-processamento de texto
def preprocess_text(text):
    # Conversão para minúsculas
    text = text.lower()

    # Remoção de caracteres especiais e pontuação
    text = ''.join([char for char in text if char not in string.punctuation])

    # Segmentação em frases usando NLTK
    sentences = sent_tokenize(text, language='portuguese')

    processed_sentences = []
    for sentence in sentences:
        # Tokenização e remoção de stopwords com NLTK
        words = word_tokenize(sentence, language='portuguese')
        tokens = [word for word in words if word not in stop_words]

        # Lematização com spaCy
        doc = nlp(' '.join(tokens))
        lemmas = [token.lemma_ for token in doc]

        processed_sentences.append(' '.join(lemmas))

    # Juntar as frases processadas em um único texto
    return ' '.join(processed_sentences)

# Extrair os textos das colunas especificadas
columns_str = ', '.join(columns_to_tokenize)
cursor.execute(f"SELECT id, {columns_str} FROM {table_name}")
rows = cursor.fetchall()

# Processar e tokenizar os textos
for row in rows:
    id = row[0]
    tokenized_data = {}
    for idx, column in enumerate(columns_to_tokenize):
        original_text = row[idx + 1]
        tokenized_text = preprocess_text(original_text) if original_text else ''
        tokenized_data[f"{column}_tokens"] = tokenized_text

    # Atualizar a tabela com os tokens processados
    set_clause = ', '.join([f"{col} = ?" for col in tokenized_data.keys()])
    values = list(tokenized_data.values())
    values.append(id)

    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", values)

# Confirmar as mudanças e fechar a conexão com o banco de dados
conn.commit()
conn.close()

print("Tokenização e atualização do banco de dados concluídas.")
