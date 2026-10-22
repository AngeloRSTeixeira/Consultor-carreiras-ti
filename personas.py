"""Fase 4 — Personas de teste usadas para validar o sistema.

As quatro primeiras são as exigidas no enunciado (analítico, infra/segurança,
visual/front-end, negócios/produto). As demais cobrem as outras trilhas.
Execute ``python personas.py`` para ver o relatório de validação.
"""
from base_conhecimento import TRILHAS, consultar

PERSONAS = [
    {
        "nome": "Ana — perfil analítico",
        "esperado": "ciencia_dados",
        "respostas": dict(matematica="alta", atividade="dados", ferramenta="python",
                          entrega="dados", plataforma="indiferente", automacao="nao",
                          comunicacao="media", detalhista="sim"),
    },
    {
        "nome": "Bruno — perfil infra/segurança",
        "esperado": "seguranca",
        "respostas": dict(matematica="media", atividade="seguranca", ferramenta="linux_redes",
                          entrega="seguranca", plataforma="indiferente", automacao="sim",
                          comunicacao="baixa", detalhista="sim"),
    },
    {
        "nome": "Carla — perfil visual/front-end",
        "esperado": "frontend",
        "respostas": dict(matematica="baixa", atividade="layouts", ferramenta="javascript",
                          entrega="produto", plataforma="web", automacao="nao",
                          comunicacao="media", detalhista="nao"),
    },
    {
        "nome": "Diego — perfil negócios/produto",
        "esperado": "produto",
        "respostas": dict(matematica="media", atividade="pessoas", ferramenta="nenhuma",
                          entrega="negocio", plataforma="indiferente", automacao="nao",
                          comunicacao="alta", detalhista="nao"),
    },
    {
        "nome": "Eduardo — construtor de APIs",
        "esperado": "backend",
        "respostas": dict(matematica="media", atividade="algoritmos", ferramenta="java_csharp",
                          entrega="produto", plataforma="web", automacao="nao",
                          comunicacao="baixa", detalhista="nao"),
    },
    {
        "nome": "Fernanda — arquiteta de pipelines",
        "esperado": "engenharia_dados",
        "respostas": dict(matematica="media", atividade="dados", ferramenta="sql",
                          entrega="dados", plataforma="indiferente", automacao="sim",
                          comunicacao="baixa", detalhista="nao"),
    },
    {
        "nome": "Gustavo — automatizador de deploys",
        "esperado": "devops",
        "respostas": dict(matematica="media", atividade="servidores", ferramenta="linux_redes",
                          entrega="infraestrutura", plataforma="indiferente", automacao="sim",
                          comunicacao="baixa", detalhista="nao"),
    },
    {
        "nome": "Helena — arquiteta de nuvem",
        "esperado": "cloud",
        "respostas": dict(matematica="media", atividade="servidores", ferramenta="linux_redes",
                          entrega="infraestrutura", plataforma="nuvem", automacao="nao",
                          comunicacao="alta", detalhista="nao"),
    },
    {
        "nome": "Igor — dev de apps",
        "esperado": "mobile",
        "respostas": dict(matematica="media", atividade="algoritmos", ferramenta="mobile",
                          entrega="produto", plataforma="mobile", automacao="nao",
                          comunicacao="media", detalhista="nao"),
    },
    {
        "nome": "Júlia — caçadora de bugs",
        "esperado": "qa",
        "respostas": dict(matematica="media", atividade="testes", ferramenta="python",
                          entrega="qualidade", plataforma="web", automacao="sim",
                          comunicacao="media", detalhista="sim"),
    },
]


def validar_personas():
    acertos = 0
    for persona in PERSONAS:
        r = consultar(persona["respostas"])
        ok = r.trilha == persona["esperado"]
        acertos += ok
        status = "OK  " if ok else "ERRO"
        print(f"[{status}] {persona['nome']:<36} -> {r.nome} "
              f"({r.placar.get(r.trilha, 0)} pts, regras {', '.join(r.regras_disparadas)})")
        if not ok:
            print(f"        esperado: {TRILHAS[persona['esperado']]}")
    print(f"\nAcurácia: {acertos}/{len(PERSONAS)}")
    return acertos == len(PERSONAS)


if __name__ == "__main__":
    validar_personas()
