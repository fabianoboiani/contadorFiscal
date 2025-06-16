import streamlit as st
from agente_fiscal import agent_executor
from langchain_core.messages import HumanMessage

st.title("🧑‍💼 Agente Fiscal - Chat com Banco de Dados Fiscal 📊")

# Histórico de conversa
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Controle de última resposta
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Controle de processamento
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ---------------- Botões de Controle ---------------- #
col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Limpar Chat"):
        st.session_state.chat_history = []
        st.session_state.last_response = ""
        st.rerun()

with col2:
    if st.button("🚪 Encerrar"):
        st.markdown("✅ Sessão encerrada. Pode fechar a aba.")
        st.stop()

# ---------------- Formulário de Pergunta ---------------- #
with st.form(key="form_pergunta"):
    pergunta = st.text_input(
        "Digite sua pergunta:",
        disabled=st.session_state.is_processing  # Desativa o campo enquanto processa
    )
    enviar = st.form_submit_button("Enviar Pergunta")

# ---------------- Processamento da Pergunta ---------------- #
if enviar and pergunta.strip() != "":
    if pergunta.lower() in ["sair", "exit", "quit"]:
        st.markdown("✅ Sessão encerrada via comando 'sair'.")
        st.stop()

    st.session_state.is_processing = True

    with st.spinner("🕐 Processando... Por favor, aguarde..."):
        mensagens = [HumanMessage(content=pergunta)]
        resposta = agent_executor.invoke({"messages": mensagens})
        resposta_texto = resposta["messages"][-1].content

        # Salvar resultado
        st.session_state.chat_history.append((pergunta, resposta_texto))
        st.session_state.last_response = resposta_texto

    st.session_state.is_processing = False
    st.rerun()

# ---------------- Exibir Última Resposta ---------------- #
if st.session_state.last_response:
    st.markdown("### 📥 Resposta:")
    st.markdown(st.session_state.last_response)

# ---------------- Exibir Histórico Completo ---------------- #
st.markdown("### 💬 Histórico Completo:")
for idx, (q, r) in enumerate(st.session_state.chat_history, start=1):
    st.markdown(f"**{idx}. Pergunta:** {q}")
    st.markdown(f"**Resposta:** {r}")
    st.markdown("---")
