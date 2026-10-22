import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from base_conhecimento import TRILHAS, consultar  # noqa: E402
from personas import PERSONAS  # noqa: E402


@pytest.mark.parametrize("persona", PERSONAS, ids=[p["nome"] for p in PERSONAS])
def test_persona_recebe_trilha_esperada(persona):
    resultado = consultar(persona["respostas"])
    assert resultado.trilha == persona["esperado"]
    assert resultado.motivos, "a recomendação precisa vir com justificativa"


def test_todas_as_trilhas_sao_alcancaveis():
    assert {p["esperado"] for p in PERSONAS} == set(TRILHAS)


def test_cientista_vs_engenheiro_de_dados():
    """A afinidade com matemática separa os dois perfis de dados."""
    base = dict(atividade="dados", ferramenta="python", entrega="dados",
                plataforma="indiferente", automacao="sim", comunicacao="media", detalhista="nao")
    assert consultar({**base, "matematica": "alta"}).trilha == "ciencia_dados"
    assert consultar({**base, "matematica": "media"}).trilha == "engenharia_dados"


def test_devops_vs_cloud():
    """O ambiente (nuvem ou não) separa DevOps de Cloud."""
    base = dict(matematica="media", atividade="servidores", ferramenta="linux_redes",
                entrega="infraestrutura", automacao="sim", comunicacao="media", detalhista="nao")
    assert consultar({**base, "plataforma": "indiferente"}).trilha == "devops"
    assert consultar({**base, "plataforma": "nuvem"}).trilha == "cloud"


def test_frontend_vs_mobile_com_javascript():
    """JavaScript na web leva a Front-end; no celular (React Native), a Mobile."""
    base = dict(matematica="baixa", atividade="layouts", ferramenta="javascript",
                entrega="produto", automacao="nao", comunicacao="media", detalhista="nao")
    assert consultar({**base, "plataforma": "web"}).trilha == "frontend"
    assert consultar({**base, "plataforma": "mobile"}).trilha == "mobile"


def test_resposta_invalida_gera_erro():
    respostas = dict(PERSONAS[0]["respostas"], matematica="altissima")
    with pytest.raises(ValueError):
        consultar(respostas)
