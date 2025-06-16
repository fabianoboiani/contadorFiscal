from sqlalchemy import create_engine, Column, String, Integer, Numeric, Text, TIMESTAMP, MetaData, Table

# Configuração do banco PostgreSQL
db_url = "postgresql://admin:senha123@localhost:5432/fiscal_db"
engine = create_engine(db_url)
metadata = MetaData()

# Tabela: notas_fiscais
notas_fiscais = Table(
    "notas_fiscais",
    metadata,
    Column("chave_acesso", String, primary_key=True),
    Column("modelo", Text),
    Column("serie", String),
    Column("numero", String),
    Column("data_emissao", TIMESTAMP),
    Column("cnpj_emitente", String),
    Column("razao_social_emitente", Text),
    Column("valor_nota_fiscal", Numeric),
)

# Tabela: itens_nota
itens_nota = Table(
    "itens_nota",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("chave_acesso", String),
    Column("numero_produto", Integer),
    Column("descricao_produto", Text),
    Column("ncm", String),
    Column("cfop", String),
    Column("quantidade", Numeric),
    Column("unidade", String),
    Column("valor_unitario", Numeric),
    Column("valor_total", Numeric),
)

# Criar as tabelas no banco
metadata.create_all(engine)

print("✅ Tabelas criadas com sucesso no banco fiscal_db!")
