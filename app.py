"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.

Fase 3 do trabalho. Execute com:  streamlit run app.py
"""
import pandas as pd
import streamlit as st

from base_conhecimento import DESCRICOES, TRILHAS, consultar

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

# Pergunta -> (texto exibido, {valor interno: rótulo exibido})
PERGUNTAS = {
    "matematica": ("1. Qual sua afinidade com matemática e estatística?", {
        "baixa": "Baixa", "media": "Média", "alta": "Alta",
    }),
    "atividade": ("2. O que você mais gostaria de fazer no dia a dia?", {
        "algoritmos": "Escrever algoritmos e lógica de sistemas",
        "layouts": "Criar layouts e interfaces visuais",
        "servidores": "Lidar com servidores e infraestrutura",
        "dados": "Analisar e organizar dados brutos",
        "seguranca": "Garantir a segurança de sistemas",
        "testes": "Testar e validar software",
        "pessoas": "Coordenar pessoas e priorizar demandas",
    }),
    "ferramenta": ("3. Com qual linguagem/ferramenta você tem mais afinidade hoje?", {
        "python": "Python",
        "javascript": "JavaScript / TypeScript",
        "linux_redes": "Linux / Redes",
        "java_csharp": "Java / C#",
        "sql": "SQL / Bancos de dados",
        "mobile": "Kotlin / Swift / Dart",
        "nenhuma": "Nenhuma (sou iniciante)",
    }),
    "entrega": ("4. Que tipo de entrega de valor te motiva mais?", {
        "produto": "O produto final que o usuário usa",
        "infraestrutura": "A infraestrutura que sustenta o sistema",
        "seguranca": "A segurança contra invasões",
        "dados": "Insights e informações extraídos de dados",
        "qualidade": "Software confiável e sem falhas",
        "negocio": "Resultados estratégicos para o negócio",
    }),
    "plataforma": ("5. Em qual ambiente você prefere atuar?", {
        "web": "Web", "mobile": "Celulares e tablets",
        "nuvem": "Nuvem (AWS / Azure / GCP)", "indiferente": "Indiferente",
    }),
    "automacao": ("6. Você gosta de automatizar tarefas repetitivas com scripts?", {
        "sim": "Sim", "nao": "Não",
    }),
    "comunicacao": ("7. Quanto você gosta de interagir com pessoas, negociar e apresentar ideias?", {
        "baixa": "Pouco", "media": "Moderadamente", "alta": "Muito",
    }),
    "detalhista": ("8. Você gosta de caçar falhas e erros nos mínimos detalhes?", {
        "sim": "Sim", "nao": "Não",
    }),
}

st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.caption("Sistema especialista baseado em regras (Experta). Responda as 8 perguntas e "
           "descubra qual das 10 trilhas combina mais com você.")

with st.form("entrevista"):
    respostas = {}
    for chave, (texto, opcoes) in PERGUNTAS.items():
        respostas[chave] = st.radio(
            texto, options=list(opcoes), format_func=opcoes.get, index=None, key=chave,
        )
    enviar = st.form_submit_button("Descobrir minha trilha", type="primary", width="stretch")

if enviar:
    faltando = [PERGUNTAS[c][0].split(".")[0] for c, v in respostas.items() if v is None]
    if faltando:
        st.warning(f"Responda todas as perguntas. Faltam as de número: {', '.join(faltando)}.")
        st.stop()

    resultado = consultar(respostas)

    if resultado.trilha is None:
        st.info("Suas respostas não acionaram nenhuma regra com força suficiente. "
                "Tente revisar as respostas sobre atividade e tipo de entrega.")
        st.stop()

    st.divider()
    st.subheader("Trilha recomendada")
    st.success(f"### {resultado.nome}\n{DESCRICOES[resultado.trilha]}")

    col1, col2 = st.columns(2)
    col1.metric("Pontuação", resultado.placar[resultado.trilha])
    col2.metric("Peso entre as evidências", f"{resultado.confianca}%")

    st.markdown("#### Por que esta trilha?")
    for m in resultado.motivos:
        st.markdown(f"- **{m['regra']}** (+{m['peso']}) — {m['motivo']}")

    if resultado.tracos:
        st.markdown("#### Traços de perfil identificados")
        for t in sorted(resultado.tracos, key=lambda t: t["regra"]):
            st.markdown(f"- **{t['regra']}** — {t['motivo']}")

    if resultado.segunda:
        st.caption(f"Segunda opção: **{TRILHAS[resultado.segunda]}** "
                   f"({resultado.placar[resultado.segunda]} pontos).")

    with st.expander("Placar completo das 10 trilhas"):
        tabela = pd.DataFrame(
            {"Trilha": [TRILHAS[t] for t in resultado.placar],
             "Pontos": list(resultado.placar.values())}
        ).sort_values("Pontos", ascending=False)
        st.dataframe(tabela, hide_index=True, width="stretch",
                     column_config={"Pontos": st.column_config.ProgressColumn(
                         "Pontos", min_value=0, max_value=int(tabela["Pontos"].max()), format="%d")})
