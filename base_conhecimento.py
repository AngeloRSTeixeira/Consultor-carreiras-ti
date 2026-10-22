"""Base de conhecimento e motor de inferência do Consultor de Carreiras em TI.

Fase 2 do trabalho: fatos (``Fact``) e regras (``@Rule``) do Experta.
O raciocínio usa encadeamento para frente em três camadas:

1. R01–R05: inferem traços de perfil a partir das respostas;
2. R06–R30: cruzam respostas e traços e pontuam as trilhas;
3. R31: escolhe a trilha vencedora e monta a justificativa.

A matriz completa está em ``docs/matriz_decisao.md``.
"""
from dataclasses import dataclass, field

import compat  # noqa: F401  (precisa vir antes do experta)
from experta import AS, NOT, OR, Fact, KnowledgeEngine, P, Rule

# --------------------------------------------------------------------------
# Domínio
# --------------------------------------------------------------------------
TRILHAS = {
    "backend": "Desenvolvimento Back-end",
    "frontend": "Desenvolvimento Front-end & UI/UX",
    "ciencia_dados": "Ciência de Dados e Machine Learning",
    "engenharia_dados": "Engenharia de Dados",
    "seguranca": "Cibersegurança (Security / Pentesting)",
    "devops": "DevOps & SRE",
    "cloud": "Computação em Nuvem (Cloud Architecture)",
    "mobile": "Desenvolvimento Mobile",
    "qa": "Engenharia de Qualidade e Testes (QA)",
    "produto": "Gestão de Produtos (Product Management)",
}

DESCRICOES = {
    "backend": "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
    "frontend": "Interfaces web responsivas, experiência do usuário e frameworks reativos.",
    "ciencia_dados": "Estatística, modelagem preditiva, análise de grandes massas de dados e IA.",
    "engenharia_dados": "Arquitetura de dados, pipelines ETL/ELT e infraestrutura para Data Lakes.",
    "seguranca": "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
    "devops": "Automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
    "cloud": "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
    "mobile": "Ecossistema de dispositivos móveis, nativo ou multiplataforma (Flutter/React Native).",
    "qa": "Testes automatizados, confiabilidade de software e processos de qualidade.",
    "produto": "Ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização.",
}

# Valores aceitos em cada pergunta (usados para validar a entrada)
DOMINIO = {
    "matematica": ("baixa", "media", "alta"),
    "atividade": ("algoritmos", "layouts", "servidores", "dados", "seguranca", "testes", "pessoas"),
    "ferramenta": ("python", "javascript", "linux_redes", "java_csharp", "sql", "mobile", "nenhuma"),
    "entrega": ("produto", "infraestrutura", "seguranca", "dados", "qualidade", "negocio"),
    "plataforma": ("web", "mobile", "nuvem", "indiferente"),
    "automacao": ("sim", "nao"),
    "comunicacao": ("baixa", "media", "alta"),
    "detalhista": ("sim", "nao"),
}


def um_de(*valores):
    """Restrição de campo: o valor precisa estar entre os informados."""
    return P(lambda v: v in valores)


def nenhum_de(*valores):
    """Restrição de campo: o valor não pode estar entre os informados."""
    return P(lambda v: v not in valores)


# --------------------------------------------------------------------------
# Fatos
# --------------------------------------------------------------------------
class Perfil(Fact):
    """Respostas do usuário na entrevista."""


class Traco(Fact):
    """Fato intermediário inferido pela camada 1 (ex.: perfil analítico)."""


class Ponto(Fact):
    """Evidência a favor de uma trilha: trilha, peso, regra e motivo."""


class Recomendacao(Fact):
    """Conclusão final do sistema."""


# --------------------------------------------------------------------------
# Motor de inferência
# --------------------------------------------------------------------------
class ConsultorCarreiras(KnowledgeEngine):
    """Sistema especialista que recomenda uma entre 10 trilhas de carreira."""

    def __init__(self):
        super().__init__()
        self.resultado = None

    def pontuar(self, trilha, peso, regra, motivo):
        self.declare(Ponto(trilha=trilha, peso=peso, regra=regra, motivo=motivo))

    def inferir_traco(self, nome, regra, motivo):
        self.declare(Traco(nome=nome, regra=regra, motivo=motivo))

    # ---------------- Camada 1: traços de perfil (salience alta) ----------
    @Rule(Perfil(matematica="alta"),
          OR(Perfil(atividade="dados"), Perfil(ferramenta="python")),
          salience=10)
    def r01_traco_analitico(self):
        self.inferir_traco("analitico", "R01",
                           "Alta afinidade com matemática somada a interesse por dados/Python indica perfil analítico.")

    @Rule(OR(Perfil(atividade="servidores"), Perfil(ferramenta="linux_redes")), salience=10)
    def r02_traco_infra(self):
        self.inferir_traco("infra", "R02",
                           "Gosto por servidores ou domínio de Linux/Redes indica perfil de infraestrutura.")

    @Rule(OR(Perfil(atividade="layouts"), Perfil(ferramenta="javascript")), salience=10)
    def r03_traco_visual(self):
        self.inferir_traco("visual", "R03",
                           "Interesse por layouts ou afinidade com JavaScript indica perfil visual/interface.")

    @Rule(Perfil(comunicacao="alta"),
          OR(Perfil(entrega="negocio"), Perfil(atividade="pessoas")),
          salience=10)
    def r04_traco_negocio(self):
        self.inferir_traco("negocio", "R04",
                           "Comunicação forte voltada a pessoas/negócio indica perfil de produto.")

    @Rule(OR(Perfil(atividade="algoritmos"), Perfil(ferramenta="java_csharp")), salience=10)
    def r05_traco_construtor(self):
        self.inferir_traco("construtor", "R05",
                           "Gosto por algoritmos ou linguagens de back-end indica perfil construtor de sistemas.")

    # ---------------- Camada 2: pontuação das trilhas ---------------------
    # Back-end
    @Rule(Traco(nome="construtor"),
          Perfil(entrega="produto", plataforma=um_de("web", "indiferente")))
    def r06_backend_construtor(self):
        self.pontuar("backend", 3, "R06", "Perfil construtor que quer entregar o produto em aplicações web/servidor.")

    @Rule(Perfil(atividade="algoritmos", ferramenta=um_de("java_csharp", "sql")))
    def r07_backend_stack(self):
        self.pontuar("backend", 2, "R07", "Algoritmos + Java/C#/SQL é o núcleo de APIs e bancos de dados.")

    @Rule(Perfil(atividade="algoritmos", matematica=um_de("media", "alta")))
    def r08_backend_logica(self):
        self.pontuar("backend", 1, "R08", "Boa base lógico-matemática ajuda nas regras de negócio do servidor.")

    # Front-end & UI/UX
    @Rule(Traco(nome="visual"), Perfil(entrega="produto", plataforma="web"))
    def r09_frontend_visual(self):
        self.pontuar("frontend", 4, "R09", "Perfil visual focado no produto final na web.")

    @Rule(Perfil(atividade="layouts", comunicacao=um_de("media", "alta")))
    def r10_frontend_ux(self):
        self.pontuar("frontend", 2, "R10", "Gosto por layouts + empatia/comunicação favorece UI/UX.")

    # Ciência de Dados
    @Rule(Traco(nome="analitico"), Perfil(entrega="dados"))
    def r11_ciencia_analitico(self):
        self.pontuar("ciencia_dados", 4, "R11", "Perfil analítico que quer gerar valor com insights de dados.")

    @Rule(Perfil(matematica="alta", atividade="dados", ferramenta="python"))
    def r12_ciencia_stack(self):
        self.pontuar("ciencia_dados", 2, "R12", "Estatística forte + análise de dados + Python é a base de ML.")

    # Engenharia de Dados
    @Rule(Perfil(atividade="dados", matematica=um_de("baixa", "media")))
    def r13_engdados_dados(self):
        self.pontuar("engenharia_dados", 3, "R13",
                     "Gosta de dados, mas sem foco em estatística avançada: perfil de quem constrói a estrutura.")

    @Rule(Traco(nome="infra"), Perfil(entrega="dados"))
    def r14_engdados_infra(self):
        self.pontuar("engenharia_dados", 3, "R14", "Perfil de infraestrutura aplicado a dados: pipelines e Data Lakes.")

    @Rule(Perfil(entrega="dados", automacao="sim", matematica=nenhum_de("alta")))
    def r15_engdados_automacao(self):
        self.pontuar("engenharia_dados", 2, "R15", "Automatizar o fluxo de dados (ETL/ELT) é o dia a dia do engenheiro de dados.")

    # Cibersegurança
    @Rule(Perfil(atividade="seguranca"))
    def r16_seguranca_atividade(self):
        self.pontuar("seguranca", 3, "R16", "Prefere atuar garantindo a segurança dos sistemas.")

    @Rule(Perfil(entrega="seguranca"))
    def r17_seguranca_entrega(self):
        self.pontuar("seguranca", 3, "R17", "Quer entregar valor protegendo contra invasões.")

    @Rule(Traco(nome="infra"), Perfil(detalhista="sim", entrega="seguranca"))
    def r18_seguranca_pentest(self):
        self.pontuar("seguranca", 2, "R18", "Infraestrutura + olhar detalhista para falhas é o perfil de pentester.")

    # DevOps & SRE
    @Rule(Traco(nome="infra"), Perfil(automacao="sim", entrega="infraestrutura"))
    def r19_devops_automacao(self):
        self.pontuar("devops", 4, "R19", "Infraestrutura + automação: CI/CD, contêineres e confiabilidade.")

    @Rule(Perfil(atividade="servidores", automacao="sim", plataforma=nenhum_de("nuvem")))
    def r20_devops_servidores(self):
        self.pontuar("devops", 2, "R20", "Automatizar servidores fora de um foco exclusivo em nuvem é típico de DevOps/SRE.")

    # Cloud
    @Rule(Perfil(plataforma="nuvem", entrega="infraestrutura"))
    def r21_cloud_infra(self):
        self.pontuar("cloud", 4, "R21", "Quer sustentar sistemas em AWS/Azure/GCP.")

    @Rule(Traco(nome="infra"), Perfil(plataforma="nuvem", comunicacao=um_de("media", "alta")))
    def r22_cloud_arquiteto(self):
        self.pontuar("cloud", 2, "R22", "Infraestrutura em nuvem + comunicação para desenhar e negociar arquiteturas.")

    # Mobile
    @Rule(Perfil(plataforma="mobile", entrega="produto"))
    def r23_mobile_produto(self):
        self.pontuar("mobile", 4, "R23", "Quer entregar o produto final em dispositivos móveis.")

    @Rule(Perfil(ferramenta="mobile"))
    def r24_mobile_stack(self):
        self.pontuar("mobile", 3, "R24", "Já tem afinidade com Kotlin/Swift/Dart.")

    # QA
    @Rule(Perfil(atividade="testes"))
    def r25_qa_atividade(self):
        self.pontuar("qa", 3, "R25", "Prefere atuar testando e validando software.")

    @Rule(Perfil(entrega="qualidade"))
    def r26_qa_entrega(self):
        self.pontuar("qa", 3, "R26", "Quer entregar valor garantindo a confiabilidade do software.")

    @Rule(Perfil(detalhista="sim", automacao="sim", entrega="qualidade"))
    def r27_qa_automacao(self):
        self.pontuar("qa", 2, "R27", "Detalhista + automação = testes automatizados.")

    # Product Management
    @Rule(Traco(nome="negocio"))
    def r28_produto_perfil(self):
        self.pontuar("produto", 4, "R28", "Perfil de negócio e comunicação, ponte entre áreas.")

    @Rule(Perfil(atividade="pessoas"))
    def r29_produto_pessoas(self):
        self.pontuar("produto", 3, "R29", "Prefere coordenar pessoas e priorizar demandas.")

    @Rule(Perfil(entrega="negocio"))
    def r30_produto_negocio(self):
        self.pontuar("produto", 2, "R30", "Quer gerar valor estratégico para o negócio.")

    # ---------------- Camada 3: decisão (salience mínima) ------------------
    @Rule(AS.perfil << Perfil(), NOT(Recomendacao()), salience=-100)
    def r31_decisao(self, perfil):
        pontos = [f for f in self.facts.values() if isinstance(f, Ponto)]
        tracos = [f for f in self.facts.values() if isinstance(f, Traco)]

        placar = {t: 0 for t in TRILHAS}
        regras = {t: [] for t in TRILHAS}
        for p in pontos:
            placar[p["trilha"]] += p["peso"]
            regras[p["trilha"]].append(p)

        ordem = list(TRILHAS)
        ranking = sorted(TRILHAS, key=lambda t: (-placar[t], -len(regras[t]), ordem.index(t)))
        vencedora = ranking[0]

        if placar[vencedora] == 0:
            self.resultado = Resultado(trilha=None, placar=placar, tracos=tracos)
            self.declare(Recomendacao(trilha=None))
            return

        total = sum(placar.values())
        self.resultado = Resultado(
            trilha=vencedora,
            placar=placar,
            confianca=round(100 * placar[vencedora] / total),
            motivos=sorted(regras[vencedora], key=lambda p: p["regra"]),
            tracos=tracos,
            segunda=ranking[1] if placar[ranking[1]] > 0 else None,
        )
        self.declare(Recomendacao(trilha=vencedora))


@dataclass
class Resultado:
    trilha: str | None
    placar: dict
    confianca: int = 0
    motivos: list = field(default_factory=list)
    tracos: list = field(default_factory=list)
    segunda: str | None = None

    @property
    def nome(self):
        return TRILHAS.get(self.trilha, "Indefinida")

    @property
    def regras_disparadas(self):
        """Todas as regras que dispararam (traços + pontuação da vencedora)."""
        return sorted({t["regra"] for t in self.tracos} | {m["regra"] for m in self.motivos})


def validar(respostas: dict) -> None:
    for chave, valores in DOMINIO.items():
        if chave not in respostas:
            raise ValueError(f"Resposta ausente: {chave}")
        if respostas[chave] not in valores:
            raise ValueError(f"Valor inválido para {chave}: {respostas[chave]!r}")


def consultar(respostas: dict) -> Resultado:
    """Roda o motor de inferência com as respostas e devolve o resultado."""
    validar(respostas)
    motor = ConsultorCarreiras()
    motor.reset()
    motor.declare(Perfil(**respostas))
    motor.run()
    return motor.resultado


if __name__ == "__main__":
    exemplo = {
        "matematica": "alta", "atividade": "dados", "ferramenta": "python",
        "entrega": "dados", "plataforma": "indiferente", "automacao": "nao",
        "comunicacao": "media", "detalhista": "sim",
    }
    r = consultar(exemplo)
    print(f"Recomendação: {r.nome} ({r.confianca}% dos pontos)")
    for m in r.motivos:
        print(f"  [{m['regra']}] +{m['peso']} {m['motivo']}")
