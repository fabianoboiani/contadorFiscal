
# 📊 Agente Fiscal Inteligente

Este projeto implementa um agente fiscal com IA, conectado a um banco de dados PostgreSQL com dados de notas fiscais, permitindo consultas inteligentes via linguagem natural, tanto via terminal quanto via interface web (Streamlit).



## Pré-requisitos

* Python 3.9+

* Docker + Docker Compose

* Conta na OpenAI (ou provedor de LLM)

* Navegador web (para rodar o Streamlit)
## Instalação

#### ✅Passo 1: Subindo o banco de dados com Docker Compose

```bash
  docker-compose up -d
```

Isso vai subir o PostgreSQL localmente acessível em:

* Host: localhost
* Porta: 5432
* Usuário: admin
* Senha: senha123
* Banco: fiscal_db

#### ✅Passo 2: Criando o ambiente virtual (venv)
```bash
  python -m venv venv
```
Ative o ambiente:
* Windows (PowerShell):
```bash
  .\venv\Scripts\activate
```
* Linux/Mac:
```bash
  source venv/bin/activate
```

#### ✅Passo 3: Instalando as dependências
```bash
  pip install -r requirements.txt
```

#### ✅Passo 4: Configurando o .env
Crie seu arquivo .env a partir do exemplo:
```bash
  cp .env.example .env
```
Depois, edite o .env e preencha sua API KEY da OpenAI, exemplo:
```ini
  OPENAI_API_KEY=sk-xxxxxx
```

#### ✅Passo 5: Carregando os dados de Notas Fiscais no banco
Coloque o arquivo .zip contendo os CSVs (exemplo: 202401_NFs.zip) na raiz do projeto.

Rode o ETL:
```bash
   python carregar_dados.py
```
Isso cria e popula as tabelas notas_fiscais e itens_nota.

#### ✅ Passo 6: Rodando o Agente Fiscal no modo Terminal (console)
```bash
  python agente_fiscal.py
```
👉 O agente vai abrir um prompt no terminal:

Exemplos de perguntas:

* "Quantas notas fiscais existem?"

* "Qual o total de vendas em janeiro de 2024?"

Digite `sair` para encerrar.

#### ✅ Passo 7: Rodando o Agente Fiscal via Interface Web (Streamlit)
```bash
  streamlit run run_agent_streamlit.py
```
Depois, acesse pelo navegador:
```arduino
  http://localhost:8501
```
👉 Você verá um chat web onde pode fazer as mesmas perguntas ao agente.


### ✅ Opções de Interação

| Modo             | Comando                                |
| ---------------- | -------------------------------------- |
| Terminal (texto) | `python agente_fiscal.py`              |
| Web (Streamlit)  | `streamlit run run_agent_streamlit.py` |

### ✅ Possíveis Melhorias Futuras
* Exportar relatórios em PDF/Excel

* Dashboard com Streamlit Charts

* Integração com WhatsApp ou Telegram

* Deploy em servidor remoto





