# Fase 1 — Engenharia de Conhecimento e Matriz de Decisão

## 1. Entrevista (variáveis de entrada)

| Código | Pergunta | Valores possíveis |
|---|---|---|
| `matematica` | Afinidade com matemática e estatística | `baixa`, `media`, `alta` |
| `atividade` | Preferência de atuação diária | `algoritmos`, `layouts`, `servidores`, `dados`, `seguranca`, `testes`, `pessoas` |
| `ferramenta` | Linguagem/ferramenta de maior afinidade | `python`, `javascript`, `linux_redes`, `java_csharp`, `sql`, `mobile` (Kotlin/Swift/Dart), `nenhuma` |
| `entrega` | Tipo de entrega de valor preferida | `produto`, `infraestrutura`, `seguranca`, `dados`, `qualidade`, `negocio` |
| `plataforma` | Ambiente onde prefere atuar | `web`, `mobile`, `nuvem`, `indiferente` |
| `automacao` | Gosta de automatizar tarefas repetitivas com scripts? | `sim`, `nao` |
| `comunicacao` | Gosto por interagir com pessoas, negociar e apresentar | `baixa`, `media`, `alta` |
| `detalhista` | Gosta de caçar falhas e erros nos detalhes? | `sim`, `nao` |

## 2. Arquitetura do raciocínio (encadeamento para frente)

O motor trabalha em três camadas. Cada camada usa fatos produzidos pela anterior:

1. **Camada 1 — Traços de perfil (R01–R05):** a partir das respostas, o sistema infere *fatos intermediários* (`Traco`) como "perfil analítico" ou "perfil de infraestrutura".
2. **Camada 2 — Pontuação das trilhas (R06–R30):** regras cruzam respostas e traços e declaram fatos `Ponto(trilha, peso, motivo)`.
3. **Camada 3 — Decisão (R31):** regra de menor prioridade (`salience=-100`) soma os pontos, escolhe a trilha vencedora e monta a justificativa.

Critério de desempate: maior pontuação → maior número de regras disparadas → ordem da lista de trilhas.

## 3. Camada 1 — Traços inferidos

| Regra | SE | ENTÃO (traço) |
|---|---|---|
| R01 | `matematica=alta` E (`atividade=dados` OU `ferramenta=python`) | analítico |
| R02 | `atividade=servidores` OU `ferramenta=linux_redes` | infraestrutura |
| R03 | `atividade=layouts` OU `ferramenta=javascript` | visual |
| R04 | `comunicacao=alta` E (`entrega=negocio` OU `atividade=pessoas`) | negócio |
| R05 | `atividade=algoritmos` OU `ferramenta=java_csharp` | construtor |

## 4. Camada 2 — Matriz de decisão (respostas × trilhas)

| Regra | SE | ENTÃO trilha | Peso |
|---|---|---|---|
| R06 | traço construtor E `entrega=produto` E `plataforma` ∈ {web, indiferente} | Back-end | +3 |
| R07 | `atividade=algoritmos` E `ferramenta` ∈ {java_csharp, sql} | Back-end | +2 |
| R08 | `atividade=algoritmos` E `matematica` ∈ {media, alta} | Back-end | +1 |
| R09 | traço visual E `entrega=produto` E `plataforma=web` | Front-end & UI/UX | +4 |
| R10 | `atividade=layouts` E `comunicacao` ∈ {media, alta} | Front-end & UI/UX | +2 |
| R11 | traço analítico E `entrega=dados` | Ciência de Dados & ML | +4 |
| R12 | `matematica=alta` E `atividade=dados` E `ferramenta=python` | Ciência de Dados & ML | +2 |
| R13 | `atividade=dados` E `matematica` ∈ {baixa, media} | Engenharia de Dados | +3 |
| R14 | traço infraestrutura E `entrega=dados` | Engenharia de Dados | +3 |
| R15 | `entrega=dados` E `automacao=sim` E `matematica` ≠ alta | Engenharia de Dados | +2 |
| R16 | `atividade=seguranca` | Cibersegurança | +3 |
| R17 | `entrega=seguranca` | Cibersegurança | +3 |
| R18 | traço infraestrutura E `detalhista=sim` E `entrega=seguranca` | Cibersegurança | +2 |
| R19 | traço infraestrutura E `automacao=sim` E `entrega=infraestrutura` | DevOps & SRE | +4 |
| R20 | `atividade=servidores` E `automacao=sim` E `plataforma` ≠ nuvem | DevOps & SRE | +2 |
| R21 | `plataforma=nuvem` E `entrega=infraestrutura` | Cloud Architecture | +4 |
| R22 | traço infraestrutura E `plataforma=nuvem` E `comunicacao` ∈ {media, alta} | Cloud Architecture | +2 |
| R23 | `plataforma=mobile` E `entrega=produto` | Mobile | +4 |
| R24 | `ferramenta=mobile` | Mobile | +3 |
| R25 | `atividade=testes` | QA | +3 |
| R26 | `entrega=qualidade` | QA | +3 |
| R27 | `detalhista=sim` E `automacao=sim` E `entrega=qualidade` | QA | +2 |
| R28 | traço negócio | Product Management | +4 |
| R29 | `atividade=pessoas` | Product Management | +3 |
| R30 | `entrega=negocio` | Product Management | +2 |

## 5. Regras que evitam ambiguidades

| Par confundível | Variável que separa | Como |
|---|---|---|
| Ciência de Dados × Engenharia de Dados | `matematica` | Alta → R01/R11/R12 (Ciência). Baixa/média → R13/R15 (Engenharia). Gosto por servidores reforça Engenharia (R14). |
| DevOps × Cloud | `plataforma` e `automacao` | Nuvem → R21/R22 (Cloud). Automação fora da nuvem → R19/R20 (DevOps). |
| Front-end × Mobile | `plataforma` | Web → R09. Mobile → R23, mesmo com JavaScript (React Native). |
| Back-end × Front-end | `atividade` e traço | Algoritmos/construtor → R06–R08. Layouts/visual → R09/R10. |
| Segurança × DevOps | `entrega` | Ambos têm traço infra; `entrega=seguranca` aciona R16–R18, `entrega=infraestrutura` aciona R19. |

## 6. Camada 3 — Decisão

| Regra | SE | ENTÃO |
|---|---|---|
| R31 | Existe `Perfil` E ainda não existe `Recomendacao` (prioridade mínima) | Soma os pontos por trilha, escolhe a vencedora, declara `Recomendacao` com justificativa e 2ª opção. Sem pontos: informa que as respostas não foram suficientes. |
