import zipfile
import pandas as pd
from sqlalchemy import create_engine
import os

# Configurações
zip_path = "202401_NFs.zip"
extract_dir = "temp_extracao"
db_url = "postgresql://admin:senha123@localhost:5432/fiscal_db"

# Conectar ao banco
engine = create_engine(db_url)

# Extrair o .zip
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Identificar os dois arquivos CSV
csv_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]

# Identificar o arquivo de cabeçalho e itens (por nome ou número de colunas)
df1 = pd.read_csv(os.path.join(extract_dir, csv_files[0]), sep=None, engine='python')
df2 = pd.read_csv(os.path.join(extract_dir, csv_files[1]), sep=None, engine='python')

# O de cabeçalho tem menos linhas por chave; o de itens repete a chave de acesso
if df1["CHAVE DE ACESSO"].nunique() == len(df1):
    df_cabecalho = df1
    df_itens = df2
else:
    df_cabecalho = df2
    df_itens = df1

# Processar cabeçalho
df_cabecalho_clean = df_cabecalho[[
    "CHAVE DE ACESSO", "MODELO", "SÉRIE", "NÚMERO",
    "DATA EMISSÃO", "CPF/CNPJ Emitente", "RAZÃO SOCIAL EMITENTE",
    "VALOR NOTA FISCAL"
]].rename(columns={
    "CHAVE DE ACESSO": "chave_acesso",
    "MODELO": "modelo",
    "SÉRIE": "serie",
    "NÚMERO": "numero",
    "DATA EMISSÃO": "data_emissao",
    "CPF/CNPJ Emitente": "cnpj_emitente",
    "RAZÃO SOCIAL EMITENTE": "razao_social_emitente",
    "VALOR NOTA FISCAL": "valor_nota_fiscal"
})
df_cabecalho_clean["data_emissao"] = pd.to_datetime(df_cabecalho_clean["data_emissao"])
df_cabecalho_clean.to_sql("notas_fiscais", engine, if_exists="append", index=False)

# Processar itens
df_itens_clean = df_itens[[
    "CHAVE DE ACESSO", "NÚMERO PRODUTO", "DESCRIÇÃO DO PRODUTO/SERVIÇO",
    "CÓDIGO NCM/SH", "CFOP", "QUANTIDADE", "UNIDADE",
    "VALOR UNITÁRIO", "VALOR TOTAL"
]].rename(columns={
    "CHAVE DE ACESSO": "chave_acesso",
    "NÚMERO PRODUTO": "numero_produto",
    "DESCRIÇÃO DO PRODUTO/SERVIÇO": "descricao_produto",
    "CÓDIGO NCM/SH": "ncm",
    "CFOP": "cfop",
    "QUANTIDADE": "quantidade",
    "UNIDADE": "unidade",
    "VALOR UNITÁRIO": "valor_unitario",
    "VALOR TOTAL": "valor_total"
})
df_itens_clean.to_sql("itens_nota", engine, if_exists="append", index=False)

print("✅ Dados carregados com sucesso do .zip para o PostgreSQL!")
