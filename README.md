# 🧭 Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em Regras, feito em Python com **Experta** (motor de inferência com encadeamento para frente) e **Streamlit** (interface web). O sistema entrevista o usuário com 8 perguntas objetivas e recomenda uma entre **10 trilhas de carreira em TI**, mostrando as regras que levaram à conclusão.

> Trabalho da disciplina de Inteligência Artificial — Ciência da Computação, UNIPAC Barbacena.
>
> **Aluno:** Angelo Ricardo de Souza Teixeira · **Professor:** Felipe Roncalli de Paula Carneiro

## Trilhas cobertas

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança (Security / Pentesting)
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Como funciona

O motor tem **31 regras** organizadas em três camadas:

| Camada | Regras | O que faz |
|---|---|---|
| 1. Traços de perfil | R01–R05 | Infere fatos intermediários (analítico, infraestrutura, visual, negócio, construtor) a partir das respostas. |
| 2. Pontuação | R06–R30 | Cruza respostas e traços e soma pontos a cada trilha, guardando o motivo. |
| 3. Decisão | R31 | Roda por último (`salience=-100`), escolhe a trilha com mais pontos e monta a justificativa. |

As regras cruzadas evitam ambiguidades entre perfis parecidos — por exemplo, a afinidade com matemática separa **Ciência de Dados** de **Engenharia de Dados**, e o ambiente preferido separa **DevOps** de **Cloud**. A matriz de decisão completa está em [`docs/matriz_decisao.md`](docs/matriz_decisao.md).

## Estrutura do repositório

```
consultor-carreiras-ti/
├── app.py                  # Interface web (Streamlit)
├── base_conhecimento.py    # Fatos, regras e motor de inferência (Experta)
├── compat.py               # Ajuste para o Experta rodar no Python 3.10+
├── personas.py             # Personas de teste e relatório de validação
├── tests/
│   └── test_personas.py    # Testes automatizados (pytest)
├── docs/
│   └── matriz_decisao.md   # Fase 1: engenharia de conhecimento
└── requirements.txt
```

## Instalação

Requer **Python 3.10 ou superior**.

```bash
git clone https://github.com/AngeloRSTeixeira/consultor-carreiras-ti.git
cd consultor-carreiras-ti

# (opcional) ambiente virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
pip install experta==1.9.4 --no-deps
```

> **Por que o `--no-deps`?** O Experta 1.9.4 exige `frozendict==1.2`, que não instala no Python 3.10+. Instalamos uma versão nova do `frozendict` pelo `requirements.txt` e o Experta sem dependências; o arquivo `compat.py` cuida do restante.

## Execução

Interface web:

```bash
streamlit run app.py
```

O navegador abre em `http://localhost:8501`.

Validação pelas personas (terminal):

```bash
python personas.py
```

Testes automatizados:

```bash
python -m pytest -q
```

## Validação com personas

| Persona | Perfil | Trilha recomendada | Regras disparadas |
|---|---|---|---|
| Ana | Analítico | Ciência de Dados e ML | R01, R11, R12 |
| Bruno | Infra/segurança | Cibersegurança | R02, R16, R17, R18 |
| Carla | Visual/front-end | Front-end & UI/UX | R03, R09, R10 |
| Diego | Negócios/produto | Product Management | R04, R28, R29, R30 |
| Eduardo | Construtor de APIs | Back-end | R05, R06, R07, R08 |
| Fernanda | Pipelines de dados | Engenharia de Dados | R13, R15 |
| Gustavo | Automação de deploys | DevOps & SRE | R02, R19, R20 |
| Helena | Arquitetura em nuvem | Cloud Architecture | R02, R21, R22 |
| Igor | Apps | Mobile | R05, R23, R24 |
| Júlia | Caça a bugs | QA | R25, R26, R27 |

Resultado: **10/10 acertos**. Os testes também conferem os pares mais confundíveis (Ciência × Engenharia de Dados, DevOps × Cloud, Front-end × Mobile).

## Tecnologias

- Python 3.10+
- [Experta](https://github.com/nilp0inter/experta) — regras SE-ENTÃO com encadeamento para frente
- [Streamlit](https://streamlit.io/) — interface web
- pytest — testes
