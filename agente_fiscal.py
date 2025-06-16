from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa LLM e banco
llm = ChatOpenAI(model="gpt-4", temperature=0)
db = SQLDatabase.from_uri("postgresql://admin:senha123@localhost:5432/fiscal_db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# Prompt com orientação em português
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um agente fiscal. Sempre responda em português de forma objetiva."),
    MessagesPlaceholder(variable_name="messages")
])

# Cria executor com LangGraph 0.4.x
agent_executor = create_react_agent(
    tools=tools,
    model=llm,
    prompt=prompt,
    debug=True
)

if __name__ == "__main__":
    print("🤖 Agente Fiscal pronto! Pergunte algo ou digite 'sair'.")
    while True:
        pergunta = input("\nPergunta: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            break
        mensagens = [HumanMessage(content=pergunta)]
        resultado = agent_executor.invoke({"messages": mensagens})
        print("\nResposta:", resultado["messages"][-1].content)