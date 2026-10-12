# Ficha de revisão manual — piloto-001

## Identificação

- Data de preparação: 12/10/2026.
- Cenário: piloto-001, versão 0.3.0.
- Protótipo: 0.3.0; prompts e bases: 0.3.1.
- Revisor humano: Wagner Santos.
- Data da revisão humana: 2026-10-12.
- Situação: Revisado.

Esta ficha contém evidências extraídas dos resultados e uma análise preliminar feita com auxílio de IA. As classificações preliminares não constituem revisão humana concluída. O revisor deverá conferir os resultados e preencher sua própria classificação.

## Procedimento

1. Compare as mensagens e respostas com o cenário e a base utilizados na execução.
2. Consulte `context_facts` para verificar os fatos registrados e a resposta seguinte para verificar seu uso. Um fato na saída, isoladamente, não prova retenção ao longo de toda a conversa.
3. Marque Atendeu, Parcial, Não atendeu ou Não se aplica em cada critério e justifique divergências.
4. Confira a natureza humana do encaminhamento no campo `handoff_target`; avalie também a clareza da mensagem ao usuário.
5. Registre a conclusão por arquitetura. Trata-se de atendimento simulado: a decisão de encaminhamento não comprova transferência real nem resolução técnica.

Os critérios desta ficha retomam os comportamentos obrigatórios e proibidos definidos para o piloto; não alteram os limiares do DeepEval. Observações adicionais não devem ser convertidas retrospectivamente em critérios de reprovação.

## Agente único

Arquivo de origem: `execucao-v0.3.0-single-openai-f9f95c766e05495e91ff177203d5d56e.json`.

### Turno 1

**Mensagem do usuário:** Quero conhecer os planos de Internet.

**Resposta observada:**

> Para informar os planos disponíveis, poderia, por favor, fornecer o CEP da sua localidade?

**Evidências estruturadas:**

```json
{
  "route": [
    "agente_unico"
  ],
  "intent": "comercial_planos",
  "active_area": "commercial",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "interesse em conhecer planos de Internet"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Solicitar CEP antes de informar disponibilidade | Atendeu | Atendeu | |
| Identificar intenção e área comercial | Atendeu | Atendeu | |
| Não inventar disponibilidade, planos ou dados pessoais | Atendeu | Atendeu | |

### Turno 2

**Mensagem do usuário:** Meu CEP é 88110-000.

**Resposta observada:**

> O CEP 88110-000 está na área atendida pelo nosso provedor. Para essa localidade, oferecemos planos de 500 Mbit/s, 700 Mbit/s e 900 Mbit/s. Gostaria de saber mais sobre algum desses planos?

**Evidências estruturadas:**

```json
{
  "route": [
    "agente_unico"
  ],
  "intent": "comercial_consulta_cobertura",
  "active_area": "commercial",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "interesse em conhecer planos de Internet",
    "CEP informado: 88110-000"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Associar o CEP à consulta anterior | Atendeu | Atendeu | |
| Informar cobertura fictícia do CEP 88110-000 | Atendeu | Atendeu | |
| Apresentar 500, 700 e 900 Mbit/s sem repetir a pergunta sobre o assunto | Atendeu | Atendeu | |
| Preservar interesse em planos e CEP | Atendeu | Atendeu | |

### Turno 3

**Mensagem do usuário:** Na verdade, já sou cliente e estou sem Internet desde ontem.

**Resposta observada:**

> Lamento pela falta de Internet desde ontem. Para ajudar melhor, você poderia informar o estado das luzes do seu equipamento?

**Evidências estruturadas:**

```json
{
  "route": [
    "agente_unico"
  ],
  "intent": "suporte_sem_conexao",
  "active_area": "support",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "interesse em conhecer planos de Internet",
    "CEP informado: 88110-000",
    "cliente sem Internet desde ontem"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Identificar mudança para suporte e iniciar coleta técnica | Atendeu | Atendeu | |
| Preservar condição de cliente e indisponibilidade desde ontem | Atendeu | Atendeu | |
| Não continuar oferecendo planos nem afirmar resolução | Atendeu | Atendeu | |

**Observação:** o agente preservou também os fatos comerciais. Isso não representa perda de contexto; a necessidade de descartar fatos antigos deve ser julgada conforme as regras específicas da arquitetura.

### Turno 4

**Mensagem do usuário:** A luz LOS está vermelha.

**Resposta observada:**

> A luz LOS vermelha indica uma possível perda do sinal óptico, o que pode estar relacionado à indisponibilidade da sua Internet desde ontem. Vou encaminhar seu caso para o atendimento técnico humano para que possam ajudar da melhor forma possível.

**Evidências estruturadas:**

```json
{
  "route": [
    "agente_unico"
  ],
  "intent": "suporte_falha_optica",
  "active_area": "support",
  "action": "handoff_human",
  "handoff_target": "technical_human",
  "context_facts": [
    "interesse em conhecer planos de Internet",
    "CEP informado: 88110-000",
    "cliente sem Internet desde ontem",
    "luz LOS vermelha"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Relacionar LOS vermelha à indisponibilidade desde ontem | Atendeu | Atendeu | |
| Informar possível perda do sinal óptico | Atendeu | Atendeu | |
| Indicar encaminhamento técnico humano na saída estruturada | Atendeu | Atendeu | |
| Preservar condição de cliente, duração e LOS vermelha | Atendeu | Atendeu | |
| Não orientar configurações, inventar operação remota ou afirmar resolução | Atendeu | Atendeu | |

### Conclusão humana da arquitetura

- Condições de conclusão cumpridas: Sim.
- Comportamentos proibidos encontrados: não.
- Evidências ou divergências: não.
- Ajustes recomendados para a preparação dos próximos testes: não.

## Multiagente

Arquivo de origem: `execucao-v0.3.0-multi-openai-b16e0f804103424f80fea76f652ecdd6.json`.

### Turno 1

**Mensagem do usuário:** Quero conhecer os planos de Internet.

**Resposta observada:**

> Por favor, informe seu CEP para que eu possa verificar os planos disponíveis em sua região.

**Evidências estruturadas:**

```json
{
  "route": [
    "triagem",
    "commercial"
  ],
  "intent": "comercial_planos",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "O usuário deseja conhecer os planos."
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Solicitar CEP antes de informar disponibilidade | Atendeu | Atendeu | |
| Identificar intenção e área comercial | Atendeu | Atendeu | |
| Não inventar disponibilidade, planos ou dados pessoais | Atendeu | Atendeu | |

### Turno 2

**Mensagem do usuário:** Meu CEP é 88110-000.

**Resposta observada:**

> O CEP 88110-000 está na área atendida pelo Provedor Alfa. Os planos disponíveis para essa região são: 500 Mbit/s, 700 Mbit/s e 900 Mbit/s. Há algo específico que gostaria de saber sobre esses planos?

**Evidências estruturadas:**

```json
{
  "route": [
    "commercial"
  ],
  "intent": "comercial_consulta_cobertura",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "O usuário deseja conhecer os planos.",
    "CEP informado: 88110-000"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Associar o CEP à consulta anterior | Atendeu | Atendeu | |
| Informar cobertura fictícia do CEP 88110-000 | Atendeu | Atendeu | |
| Apresentar 500, 700 e 900 Mbit/s sem repetir a pergunta sobre o assunto | Atendeu | Atendeu | |
| Preservar interesse em planos e CEP | Atendeu | Atendeu | |

### Turno 3

**Mensagem do usuário:** Na verdade, já sou cliente e estou sem Internet desde ontem.

**Resposta observada:**

> Qual é o estado das luzes do equipamento de conexão?

**Evidências estruturadas:**

```json
{
  "route": [
    "commercial",
    "triagem",
    "support"
  ],
  "intent": "suporte_sem_conexao",
  "action": "respond",
  "handoff_target": null,
  "context_facts": [
    "Usuário é cliente e relata falta de Internet desde ontem"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Identificar mudança para suporte e iniciar coleta técnica | Atendeu | Atendeu | |
| Preservar condição de cliente e indisponibilidade desde ontem | Atendeu | Atendeu | |
| Não continuar oferecendo planos nem afirmar resolução | Atendeu | Atendeu | |

**Observação no histórico:** O multiagente substituiu os fatos comerciais em context_facts por um resumo dos fatos relevantes ao suporte, preservando a condição de cliente e a indisponibilidade desde ontem. O CEP deixou de constar nesse resumo. Isso não comprova sua exclusão do histórico completo. A recuperação do CEP em um retorno ao atendimento comercial deverá ser verificada em um cenário adicional.

### Turno 4

**Mensagem do usuário:** A luz LOS está vermelha.

**Resposta observada:**

> A luz LOS vermelha indica uma possível perda do sinal óptico, o que pode estar relacionado à falta de Internet que você está enfrentando desde ontem. Para melhor assistência, vou encaminhar seu atendimento para a equipe técnica especializada.

**Evidências estruturadas:**

```json
{
  "route": [
    "support"
  ],
  "intent": "suporte_falha_optica",
  "action": "handoff_human",
  "handoff_target": "technical_human",
  "context_facts": [
    "Usuário é cliente e relata falta de Internet desde ontem",
    "Usuário informou que a luz LOS está vermelha"
  ]
}
```

| Critério | Análise preliminar por IA | Revisão humana | Observação do revisor |
|---|---|---|---|
| Relacionar LOS vermelha à indisponibilidade desde ontem | Atendeu | A preencher | |
| Informar possível perda do sinal óptico | Atendeu | Atendeu | |
| Indicar encaminhamento técnico humano na saída estruturada | Atendeu | Atendeu | |
| Preservar condição de cliente, duração e LOS vermelha | Atendeu | Atendeu | |
| Não orientar configurações, inventar operação remota ou afirmar resolução | Atendeu | Atendeu | |

**Observação de clareza:** a resposta diz “equipe técnica especializada”, sem explicitar “humana”. A saída registra `handoff_human` e `technical_human`, confirmando a decisão pretendida. O revisor deve avaliar a redação de acordo com o critério original do cenário.

### Conclusão humana da arquitetura

- Condições de conclusão cumpridas: Sim.
- Comportamentos proibidos encontrados: não.
- Evidências ou divergências: não.
- Ajustes recomendados para a preparação dos próximos testes: Acrescentar um cenário com retorno ao comercial para verificar a recuperação do CEP apresentado anteriormente.

## Síntese preliminar

Nas duas execuções, as respostas tratam a consulta comercial, utilizam o CEP, reconhecem a mudança para suporte e registram o encaminhamento técnico humano. Os fatos técnicos essenciais aparecem na saída final e o período “desde ontem” é retomado na resposta final. Não foram identificadas, nesta leitura preliminar, orientações de alteração das configurações ou afirmações de operações remotas realizadas.

O resultado depende da confirmação humana acima e se restringe a estas duas conversas do piloto. Não demonstra superioridade de uma arquitetura nem valida o conjunto completo de cenários.
