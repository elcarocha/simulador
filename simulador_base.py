import streamlit as st
import json
import random

st.set_page_config(page_title="Simulador de Exame de Português", layout="centered")
st.title("📘 Simulador de Exame de Português")

# Botão para recomeçar o exame
if st.button("🔁 Recomeçar Exame"):
    st.session_state.pop("perguntas_selecionadas", None)
    st.session_state.pop("n_perguntas", None)
    st.experimental_rerun()  # Reinicia o app para voltar ao início

json_file = st.file_uploader("📂 Carrega o ficheiro JSON com perguntas", type="json")

# Só inicializar perguntas uma vez
if json_file and "perguntas_selecionadas" not in st.session_state:
    perguntas_completas = json.load(json_file)

    # Quantas perguntas no exame?
    n_perguntas = st.slider(
        "Quantas perguntas queres no exame?",
        min_value=1,
        max_value=min(50, len(perguntas_completas)),
        value=min(10, len(perguntas_completas)),
    )

    # Guardar perguntas aleatórias no estado da sessão
    st.session_state.perguntas_selecionadas = random.sample(perguntas_completas, n_perguntas)
    st.session_state.n_perguntas = n_perguntas

# Usar as perguntas guardadas
if "perguntas_selecionadas" in st.session_state:
    perguntas = st.session_state.perguntas_selecionadas
    n_perguntas = st.session_state.n_perguntas
    respostas_dadas = []

    st.write(f"### 📝 Exame com {n_perguntas} perguntas")
    with st.form("formulario_simulador"):
        for i, pergunta in enumerate(perguntas):
            st.markdown(f"**{i + 1}. {pergunta['pergunta']}**")
            resposta = st.radio(
                label="",
                options=pergunta["opcoes"],
                index=None,  # <--- Isto evita pré-selecionar qualquer opção
                key=f"pergunta_{pergunta['id']}"
            )
            respostas_dadas.append((pergunta, resposta))

            with st.expander("💡 Ver Ajuda"):
                st.markdown(pergunta.get("ajuda", "Sem ajuda disponível."))

        submeter = st.form_submit_button("✅ Submeter Respostas")

    if submeter:
        st.markdown("---")
        st.subheader("📊 Resultado Final")
        pontuacao = 0

        for i, (pergunta, resposta_utilizador) in enumerate(respostas_dadas):
            resposta_correta = pergunta["resposta"]
            correta = resposta_utilizador == resposta_correta

            if correta:
                pontuacao += 1
                st.success(f"{i + 1}. ✔️ Resposta correta: {resposta_utilizador}")
            else:
                st.error(f"{i + 1}. ❌ Resposta errada: {resposta_utilizador} (Correta: {resposta_correta})")

            with st.expander("💡 Explicação"):
                st.markdown(pergunta.get("explicacao", "Sem explicação."))

        st.markdown("---")
        st.info(f"**Pontuação Final: {pontuacao} / {n_perguntas}**")

elif json_file is None:
    st.warning("Por favor, carrega um ficheiro JSON para começar.")
