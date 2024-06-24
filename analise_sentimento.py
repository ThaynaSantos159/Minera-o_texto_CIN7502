import pandas as pd
import sqlite3

# Configurações do banco de dados
db_path = './scrapy_project.db'  # Substitua pelo caminho do seu banco de dados
table_name = 'items'  # Nome da tabela que contém as colunas de avaliações
columns_to_read = ['custo_beneficio', 'facilidade_uso', 'funcionalidades', 'suporte_cliente']
# Nome das colunas de avaliações

# Conectar ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Extrair os dados das colunas de avaliações
query = f"SELECT id, {', '.join(columns_to_read)} FROM {table_name}"
df = pd.read_sql_query(query, conn)

# Converter colunas para numérico, substituindo valores não numéricos por NaN
for col in columns_to_read:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Calcular a média das avaliações para cada linha, ignorando NaNs
df['media'] = df[columns_to_read].mean(axis=1, skipna=True)


# Definir função para converter a média em sentimentos
def categorize_sentiment(mean_rating):
    if mean_rating >= 4.5:
        return 'Positivo'
    elif 3.0 <= mean_rating < 4.5:
        return 'Neutro'
    else:
        return 'Negativo'


# Aplicar a função de categorização
df['sentimento'] = df['media'].apply(categorize_sentiment)

# Adicionar as novas colunas ao banco de dados
try:
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN media REAL")
except sqlite3.OperationalError:
    # A coluna já existe
    pass

try:
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN sentimento_estrelas TEXT")
except sqlite3.OperationalError:
    # A coluna já existe
    pass


# Atualizar o banco de dados com os sentimentos e médias calculados
for index, row in df.iterrows():
    id = row['id']
    media_value = row['media']
    sentiment = row['sentimento']
    cursor.execute(f"UPDATE {table_name} SET media = ?, sentimento_estrelas = ? WHERE id = ?", (media_value, sentiment, id))

# Confirmar as mudanças e fechar a conexão com o banco de dados
conn.commit()
conn.close()


# Consulta para verificar a nova coluna ao lado de 'suporte_cliente'
# Esta consulta organiza a coluna na exibição para que ela fique ao lado de 'suporte_cliente'.
query_result = pd.read_sql_query(f"""
    SELECT id, custo_beneficio, facilidade_uso, funcionalidades, suporte_cliente, media, sentimento_estrelas
    FROM {table_name}
""", sqlite3.connect(db_path))

print(query_result.head())

print(
    "Análise de sentimentos concluída e atualizada no banco de dados, com a coluna 'media' "
    "e 'sentimento_estrelas' ao lado de 'suporte_cliente'."
)
