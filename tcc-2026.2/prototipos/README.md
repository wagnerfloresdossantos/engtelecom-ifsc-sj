# Protótipo experimental

Este diretório contém os protótipos utilizados para comparar duas arquiteturas de atendimento textual baseadas em modelos de linguagem:

- agente único, responsável pelo atendimento das quatro áreas;
- sistema multiagente, formado por triagem e especialistas de primeiro atendimento, comercial, ouvidoria e suporte técnico.

O objetivo desta etapa é verificar a viabilidade da orquestração, do registro das conversas e da avaliação. Os resultados apresentados são exploratórios e não pertencem ao experimento principal do TCC2.

## Estado atual — 14/10/2026

- Orquestração implementada para agente único e multiagente
  com triagem e quatro especialistas.
- Piloto-001 executado para comercial, suporte e mudança de assunto.
- Piloto-002 executado com oito turnos envolvendo as quatro áreas
  e recuperação do CEP após mudanças de assunto.
- Últimas execuções do piloto-002 aprovadas nas verificações
  determinísticas nas duas arquiteturas.
- Relevância, retenção e completude avaliadas com DeepEval `4.2.8`
  e avaliador `gpt-4.1-mini`, com pontuação 1,00 nas duas conversas.
- Controle negativo do piloto-001 avaliado e reprovado
  nas três métricas.
- Revisão manual identificou pendências nos fatos internos,
  nos resumos e em uma afirmação produzida pela triagem.
- Aprovação integral do piloto e procedimento definitivo
  de avaliação ainda pendentes.

## Estrutura principal

```text
prototipos/
├── base-conhecimento/
│   ├── base-comum.md
│   ├── base-triagem.md
│   ├── base-primeiro-atendimento.md
│   ├── base-comercial.md
│   ├── base-ouvidoria.md
│   └── base-suporte.md
├── cenarios/
│   ├── README.md
│   ├── cenario-piloto-001.json
│   └── cenario-piloto-002.json
├── controles/
│   └── controle-negativo-piloto-001.json
├── diagramas/
│   └── fontes/
├── prompts/
│   ├── agente-unico.md
│   ├── triagem.md
│   ├── primeiro-atendimento.md
│   ├── comercial.md
│   ├── ouvidoria.md
│   └── suporte.md
├── resultados/
│   ├── avaliacoes/
│   └── avaliacoes-deepeval/
├── src/
│   ├── modelos.py
│   ├── carregador.py
│   ├── cliente_llm.py
│   ├── agente_unico.py
│   ├── multiagente.py
│   ├── executar_piloto.py
│   ├── avaliar_resultados.py
│   └── avaliar_deepeval.py
├── .env.example
├── requirements.txt
└── requirements-lock.txt
```

A árvore apresenta os arquivos principais da versão atual. Arquivos auxiliares e resultados anteriores podem permanecer no diretório.

## Componentes em Python

| Arquivo | Responsabilidade |
|---|---|
| `modelos.py` | Define saídas estruturadas, áreas, destinos humanos, estado da conversa e medições de chamadas. |
| `carregador.py` | Lê documentos e preenche os marcadores dos prompts em uma única passagem. |
| `cliente_llm.py` | Implementa chamadas reais e respostas simuladas. Registra tokens e latência por chamada. |
| `agente_unico.py` | Fornece histórico, fatos e base completa ao mesmo agente em cada mensagem. |
| `multiagente.py` | Mantém o estado e o especialista ativo; aciona triagem e especialistas conforme as decisões estruturadas. |
| `executar_piloto.py` | Seleciona cenário e arquitetura, reúne as bases e grava cada conversa com identificador exclusivo. |
| `avaliar_resultados.py` | Compara intenção, área, ação, destino humano e rota; consolida consumo e trocas de especialistas. |
| `avaliar_deepeval.py` | Avalia a conversa apresentada ao usuário e grava pontuações, justificativas e configuração do avaliador. |

## Orquestração e contexto

Nas duas arquiteturas, o componente externo mantém o histórico completo e a lista atualizada de fatos relevantes. Os fatos complementam o histórico; não o substituem.

O agente único recebe a parte comum e as bases das quatro áreas. Ele identifica a área em `active_area`, responde e decide sobre atendimento humano, sem trocar de agente.

No multiagente, o orquestrador aciona a triagem quando ainda não existe especialista ativo. A triagem devolve `destination`, intenção, justificativa e contexto ao orquestrador, que aciona o especialista escolhido.

O especialista permanece ativo enquanto atende à mesma área. Quando solicita `request_reroute`, devolve `response=null` e `handoff_target=null`. O orquestrador realiza nova triagem e aciona o especialista indicado para processar a mesma mensagem. Os agentes não se acionam diretamente.

Cada especialista recebe o histórico completo, os fatos e a base comum acrescida de sua base específica. O fluxo permite uma nova triagem por mensagem; uma segunda solicitação é tratada como erro para impedir ciclos indefinidos.

O encaminhamento humano é uma decisão registrada. Não existe integração para transferir atendimentos, abrir chamados ou realizar contato externo.

## Cenários piloto

### Piloto-001 — comercial e suporte

O [piloto-001](cenarios/cenario-piloto-001.json) contém quatro mensagens:

1. Solicitação de planos de Internet.
2. Informação do CEP `88110-000`.
3. Mudança para falta de conexão desde ontem, com informação de que já é cliente.
4. Informação de luz LOS vermelha.

O desfecho esperado é indicar atendimento técnico humano e preservar o início da falha e o estado da luz LOS.

| Turno | Área esperada | Chamadas no agente único | Chamadas no multiagente |
|---|---|---|---|
| 1 | `commercial` | `agente_unico` | `triagem → commercial` |
| 2 | `commercial` | `agente_unico` | `commercial` |
| 3 | `support` | `agente_unico` | `commercial → triagem → support` |
| 4 | `support` | `agente_unico` | `support` |

As expectativas não são fornecidas aos agentes. Consulte [cenarios/README.md](cenarios/README.md) para a explicação dos campos.

### Piloto-002 — quatro áreas e recuperação de contexto

O [piloto-002](cenarios/cenario-piloto-002.json), versão `0.3.0`,
contém oito turnos. A conversa começa com um pedido genérico de ajuda,
passa por comercial, suporte e ouvidoria e retorna ao comercial.

O cenário verifica mudanças de assunto, preservação de informações,
distinção entre orientação e procedimento realizado pelo usuário
e decisões de encaminhamento humano.

| Turno | Solicitação resumida | Área esperada | Ação final esperada |
|---|---|---|---|
| 1 | Pedido genérico de ajuda | `first_contact` | Solicitar esclarecimento |
| 2 | Consulta de planos | `commercial` | Solicitar o CEP |
| 3 | Informação do CEP | `commercial` | Apresentar cobertura e planos fictícios |
| 4 | Cliente sem Internet desde ontem | `support` | Perguntar sobre as luzes da ONT |
| 5 | Luzes verdes e conexão indisponível | `support` | Orientar reinicialização pela energia e perguntar sobre o resultado |
| 6 | Reinicialização sem restabelecimento | `support` | Indicar atendimento técnico humano |
| 7 | Três ocorrências na semana e pedido de reclamação | `ombudsman` | Indicar atendimento humano de ouvidoria |
| 8 | Retorno à consulta comercial | `commercial` | Recuperar o CEP anterior e apresentar os planos |

No agente único, o mesmo agente processa todos os turnos.
No multiagente, são esperadas as seguintes rotas:

| Turno | Rota esperada |
|---|---|
| 1 | `triagem → first_contact` |
| 2 | `first_contact → triagem → commercial` |
| 3 | `commercial` |
| 4 | `commercial → triagem → support` |
| 5 | `support` |
| 6 | `support` |
| 7 | `support → triagem → ombudsman` |
| 8 | `ombudsman → triagem → commercial` |

Os encaminhamentos humanos são decisões simuladas e não interrompem
o envio dos turnos seguintes. O retorno ao comercial não significa
que a falha técnica ou a reclamação tenham sido resolvidas.

A conclusão exige os comportamentos definidos no cenário, incluindo
a recuperação do CEP `88110-000` no turno 8 sem nova coleta.
A aprovação dos campos estruturados ou das métricas conversacionais,
isoladamente, não comprova o cumprimento de todos os critérios.

## Preparação do ambiente

Execute os comandos a partir da pasta `prototipos`. Para um ambiente novo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Se o ambiente já existir, basta ativá-lo. No VS Code, selecione `.venv/bin/python` como interpretador.

O `requirements.txt` lista as dependências sem fixar versões. O `requirements-lock.txt` anterior precisa ser conferido e atualizado para representar o ambiente atual. Após essa conferência, registre as versões com:

```bash
python -m pip freeze > requirements-lock.txt
```

Para recriar um ambiente com as versões registradas, utilize `python -m pip install -r requirements-lock.txt`.

## Configuração

Se ainda não existir um `.env`, copie o exemplo:

```bash
cp .env.example .env
```

Configure:

```dotenv
OPENAI_API_KEY=sua-chave
TCC_OPENAI_MODEL=gpt-4.1-mini
TCC_DEEPEVAL_MODEL=gpt-4.1-mini
```

Não versionar o `.env` ou credenciais. A execução do atendimento e a avaliação com DeepEval utilizam chamadas separadas e consomem créditos separadamente.

## Verificações locais

```bash
python -m compileall -q src
python -m json.tool cenarios/cenario-piloto-001.json > /dev/null
python -m json.tool controles/controle-negativo-piloto-001.json > /dev/null
python -c "from deepeval.metrics import TurnRelevancyMetric, KnowledgeRetentionMetric, ConversationCompletenessMetric; print('Importações OK')"
```

Esses comandos não chamam o modelo avaliador. Verificam sintaxe e importações, sem comprovar a qualidade do atendimento.

## Execução simulada

```bash
python src/executar_piloto.py --mode mock --architecture both
```

O modo simulado não consome créditos e possui respostas programadas
para os pilotos, incluindo as quatro áreas de atendimento no
piloto-002. Ele permite verificar a integração, as rotas e o registro
das saídas, mas não demonstra interpretação dos prompts, qualidade
das respostas ou retenção real de contexto por um modelo de linguagem.

Para executar o piloto-002 em modo simulado:

```bash
python src/executar_piloto.py \
  --mode mock \
  --architecture both \
  --scenario cenarios/cenario-piloto-002.json
```

## Execução real

```bash
python src/executar_piloto.py --mode openai --architecture both
```

O comando executa uma conversa em cada arquitetura. Também aceita `--architecture single`, `--architecture multi` e seleção de cenário por `--scenario cenarios/cenario-piloto-001.json`.

Os arquivos recebem nomes no formato `execucao-v0.3.1-ARQUITETURA-MODO-UUID.json`, preservando execuções anteriores. Registram lote, execução, versões declaradas, modelo configurado, datas, mensagens, respostas e chamadas.

## Avaliação determinística

Exemplo com os arquivos da última execução revisada:

```bash
python src/avaliar_resultados.py \
  resultados/execucao-v0.3.0-single-openai-f9f95c766e05495e91ff177203d5d56e.json \
  resultados/execucao-v0.3.0-multi-openai-b16e0f804103424f80fea76f652ecdd6.json
```

O script verifica correspondência de cenário, versão, mensagens e ordem dos turnos. Compara a área declarada pelo agente único com a área do especialista que respondeu no multiagente, além de intenção, ação, destino e rota.

As trocas internas contam mudanças entre especialistas, sem incluir a seleção inicial ou chamadas de triagem. No agente único, essa medida é `null` por não se aplicar.

Os relatórios são gravados em `resultados/avaliacoes/`. As buscas por expressões proibidas são parciais e podem exigir revisão. A aprovação não comprova todos os comportamentos, a correção factual ou a conclusão da tarefa.

## Avaliação conversacional com DeepEval

```bash
python src/avaliar_deepeval.py \
  resultados/execucao-v0.3.0-single-openai-f9f95c766e05495e91ff177203d5d56e.json \
  resultados/execucao-v0.3.0-multi-openai-b16e0f804103424f80fea76f652ecdd6.json
```

O script utiliza `TurnRelevancyMetric`, `KnowledgeRetentionMetric` e `ConversationCompletenessMetric`. O avaliador recebe as mensagens do usuário e as respostas finais, sem as saídas internas de triagem.

O limiar padrão `0.5` é exploratório. Pode ser informado com `--threshold`, mas o limiar definitivo ainda será definido e documentado no teste-piloto, antes do experimento principal.

As avaliações ficam em `resultados/avaliacoes-deepeval/`, com identificador próprio, pontuações, justificativas, modelo avaliador e versão do DeepEval. Os critérios do cenário são registrados, mas não avaliados individualmente por este script. A completude não deve ser interpretada como comprovação automática de todos esses critérios.

## Controle negativo

O [controle negativo](controles/controle-negativo-piloto-001.json) foi construído manualmente com as mesmas mensagens do piloto e respostas inadequadas: assunto irrelevante, repetição da pergunta de CEP, tratamento do cliente como novo e contradição sobre a falta de conexão.

```bash
python src/avaliar_deepeval.py \
  controles/controle-negativo-piloto-001.json
```

Ele não representa uma terceira arquitetura nem deve entrar na comparação de consumo dos agentes. Não utilize `avaliar_resultados.py` nesse arquivo, pois não contém chamadas estruturadas dos agentes.

## Resultados exploratórios

### Correção durante a preparação

Na primeira execução real da versão `0.3.0`, o multiagente classificou o turno 3 como contratação e indicou atendimento comercial humano. A nova triagem ocorreu somente no turno 4. O avaliador determinístico detectou a falha.

Foi reforçada a prioridade de mudança de assunto no prompt comercial e adicionada à base comum a proibição de prometer contato externo. Na execução seguinte, com prompts e bases `0.3.1`, a rota passou a corresponder ao cenário. Os resultados anteriores devem ser preservados como histórico de preparação, separados da comparação definitiva.

### Piloto-001 — execução histórica revisada

| Verificação | Agente único | Multiagente | Controle negativo |
|---|---:|---:|---:|
| Áreas corretas | 4/4 | 4/4 | Não se aplica |
| Rotas corretas | 4/4 | 4/4 | Não se aplica |
| Verificações determinísticas | Passou | Passou | Não se aplica |
| Relevância dos turnos | 1,00 | 1,00 | 0,00 |
| Retenção de conhecimento | 1,00 | 1,00 | 0,00 |
| Completude da conversa | 1,00 | 1,00 | 0,00 |

As métricas distinguiram as conversas adequadas deste controle claramente inadequado. Esse resultado não comprova sensibilidade a falhas sutis, não define o melhor limiar e não demonstra superioridade de uma arquitetura.

| Recursos do atendimento | Agente único | Multiagente |
|---|---:|---:|
| Chamadas ao modelo | 4 | 7 |
| Tokens de entrada | 22.454 | 22.095 |
| Tokens de saída | 362 | 494 |
| Tokens totais | 22.816 | 22.589 |
| Trocas entre especialistas | Não se aplica | 1 |

Esses valores correspondem somente ao atendimento. O consumo do avaliador DeepEval não está incluído. Não se deve inferir uma vantagem geral de consumo a partir de uma única conversa.

## Relação com o experimento principal

O pré-projeto prevê 48 cenários sintéticos, com 12 por área: três situações e quatro variações de redação em cada situação. Cada cenário será executado uma vez em cada arquitetura, totalizando 96 conversas.

As novas execuções realizadas durante a preparação servem para corrigir e verificar o procedimento. Elas não alteram o plano de execução única no experimento principal e não serão incluídas na comparação final.

## Limitações e próximos passos

1. Documentar a ficha de revisão por critério do piloto-002, consolidando as pendências identificadas após a aprovação determinística e conversacional.
2. Documentar a revisão manual dos comportamentos obrigatórios, informações preservadas e condições de conclusão.
3. Testar erros mais sutis no procedimento de avaliação, mantendo critérios definidos antes de avaliar.
4. Definir e registrar os parâmetros de geração de forma igual nas duas arquiteturas. Atualmente, o cliente não os fixa explicitamente.
5. Registrar o identificador de modelo retornado pela API e melhorar a rastreabilidade com hashes dos documentos ou identificador de commit; as versões atuais são declaradas manualmente.
6. Conferir e atualizar o `requirements-lock.txt` e o `.env.example`.
7. Implementar registro de falhas e consumo de tentativas incompletas; atualmente, uma exceção pode interromper a conversa sem salvar o resultado parcial.
8. Estimar o custo com preços, fonte e data documentados, separando atendimento e avaliação. O script do DeepEval ainda não consolida seu consumo financeiro.
9. Consolidar resultados, matrizes de confusão e comparações por área.
10. Revisar os diagramas para refletir a orquestração e o histórico completo atuais, sem comunicação direta entre agentes.

O estado atual constitui um protótipo exploratório executado
nas quatro áreas de atendimento. A implementação definitiva,
o conjunto completo de cenários e o procedimento de avaliação
ainda serão refinados antes do experimento principal.

## Checkpoint — 18/10/2026 — geração exploratória do PA-01

Preparados contexto e script para geração de cenário de primeiro
atendimento com apoio do Synthesizer.

A primeira geração introduziu uma comparação fora do escopo.
Após configurar `num_evolutions=0`, a segunda produziu uma descrição
compatível com a situação prevista. Os dois candidatos foram
preservados e a revisão foi documentada.

As quatro variações de redação estão em preparação.
O PA-01 ainda não foi executado nas arquiteturas.

Detalhes: [Experimento com Synthesizer](experimentos/synthesizer/README.md).

## Checkpoint — 17/10/2026 — experimento com Synthesizer

Realizado um teste exploratório do DeepEval Synthesizer como apoio
à elaboração de cenários conversacionais sintéticos.

- Gerado um candidato de suporte a partir de contexto preparado.
- Identificada uma inconsistência temporal na saída original.
- Revisada a descrição e elaborado, com apoio de IA e conferência
  do pesquisador, um roteiro fixo de três turnos.
- Executado o cenário `synthesizer-suporte-001`, versão `0.1.0`,
  nas arquiteturas de agente único e multiagente.
- Ambas passaram nas verificações determinísticas dos três turnos
  e receberam nota 1,00 nas métricas de relevância, retenção
  e completude do DeepEval.
- Preservadas as observações manuais sobre uma suposição nos fatos
  internos do multiagente e uma indicação de continuidade humana
  no agente único.

O teste demonstra viabilidade inicial do procedimento, mas não
comprova geração automática de cenários prontos, diversidade
suficiente ou conformidade integral das respostas.

O cenário permanece exploratório e não integra o conjunto definitivo.

Detalhes, configuração, comandos e resultados:
[Experimento com Synthesizer](experimentos/synthesizer/README.md).

## Checkpoint — 14/10/2026 — avaliação do piloto-002

### Configuração

- Protótipo: 0.3.1.
- Cliente LLM: 0.2.1.
- Conjunto de prompts: 0.3.5.
- Conjunto de bases: 0.3.3.
- Cenário piloto-002: 0.3.0.
- Modelo de atendimento e avaliador: gpt-4.1-mini.
- DeepEval: 4.2.8; limiar exploratório: 0,5.

### Execuções de referência

- Agente único: 540720802d8b4a64bad025e6d0daeb44.
- Multiagente: bebc904fd36a4ce1987f986fdc679167.

As execuções pertencem a lotes distintos e constituem evidências
de preparação, sem integrar o experimento principal.

### Resultados

As duas arquiteturas acertaram intenção, área, ação, destino humano
e rota nos oito turnos da avaliação determinística.

O multiagente realizou corretamente as mudanças entre primeiro
atendimento, comercial, suporte, ouvidoria e retorno ao comercial.
Ambas recuperaram o CEP informado anteriormente.

As três métricas do DeepEval — relevância, retenção e completude —
atribuíram pontuação 1,00 às duas conversas.

| Medida | Agente único | Multiagente |
|---|---:|---:|
| Chamadas ao modelo | 8 | 17 |
| Tokens de entrada | 57.531 | 67.128 |
| Tokens de saída | 911 | 1.567 |
| Tokens totais | 58.442 | 68.695 |
| Soma das latências das chamadas | 15,22 s | 30,31 s |
| Trocas entre especialistas | Não se aplica | 4 |

O consumo dos avaliadores e das tentativas anteriores não está
incluído nessa tabela.

### Pendências da revisão manual

- Ambas omitiram o registro da orientação de reinicialização
  em context_facts no turno 5.
- O agente único apresentou resumos incompletos nos turnos 6 e 7.
- O multiagente preservou a recorrência nos fatos, mas a resumiu
  de forma genérica na resposta do turno 7.
- A triagem do multiagente utilizou “reclamação registrada” no
  turno 8, sem que tivesse ocorrido registro em sistema externo.
- A triagem inicial utilizou necessidade_nao_identificada,
  enquanto o especialista retornou primeiro_atendimento_inicio.

### Interpretação e continuidade

O piloto passou nas verificações determinísticas e nas métricas
conversacionais utilizadas, mas ainda apresenta pendências de
conformidade com as regras.

O DeepEval recebeu somente as mensagens e respostas finais,
sem os fatos estruturados ou as saídas internas de triagem.
Os critérios específicos do cenário não foram avaliados
individualmente pelas métricas.

O próximo passo é documentar uma ficha de revisão por critério,
distinguindo resposta ao usuário, fatos internos e orquestração,
antes de realizar novos ajustes nos prompts.

Este checkpoint não demonstra superioridade de uma arquitetura
nem aprovação integral do piloto.


## Changelog — 12/10/2026

### Versões deste checkpoint

| Componente | Versão |
|---|---|
| Protótipo | 0.3.1 |
| Cliente LLM (`cliente_llm.py`) | 0.2.1 |
| Conjunto de prompts | 0.3.2 |
| Conjunto de bases de conhecimento | 0.3.2 |
| Cenário `piloto-002` | 0.3.0 |

As versões dos conjuntos são declaradas no executor e não significam que todos os documentos tenham a mesma versão individual. Os prompts de agente único, suporte e ouvidoria foram revisados para 0.3.2; os demais documentos conservam suas identificações individuais.



### Alterações realizadas

- Criado o `piloto-002`, com oito turnos: primeiro atendimento, consulta comercial, suporte com luzes verdes, reinicialização da ONT, reclamação e retorno ao comercial para recuperar o CEP anterior.
- Ampliado o mock para triagem, quatro especialistas e agente único, incluindo mudanças de assunto e decisões de encaminhamento humano.
- Corrigida, na versão 0.2.1 do cliente, a extração dos fatos enviados como entradas `role="context"` pelo carregador. A versão 0.2.0 não preservava corretamente esses fatos na integração.
- Incluído o fluxo da base de suporte 0.3.2: desligar a ONT da energia por 30 segundos e indicar atendimento técnico humano quando a conexão continuar indisponível após reinicialização relatada pelo usuário.
- Atualizado o executor para registrar `prototype_version="0.3.1"` e `client_version="0.2.1"`. Os resultados passam a usar o prefixo `execucao-v0.3.1-`.
- Reforçados os prompts de agente único, suporte e ouvidoria quanto ao registro de orientações, resumo de encaminhamento, coerência entre resposta e ação e distinção entre reclamação e pedido explícito de humano.
- Adicionada orientação de diagnóstico para que a exceção de nova triagem mostre agente, mensagem e saída estruturada. A validação de `response=null` e `handoff_target=null` permanece exigida para `request_reroute`.

### Validação em modo mock

As duas execuções corrigidas processaram os oito turnos e corresponderam às intenções, áreas, ações, destinos e rotas esperadas. Os fatos técnicos foram preservados nos turnos 5 a 7 e o CEP foi recuperado no turno 8.

| Medida | Agente único | Multiagente |
|---|---:|---:|
| Turnos processados | 8 | 8 |
| Chamadas ao cliente simulado | 8 | 17 |
| Trocas entre especialistas | Não se aplica | 4 |
| Tokens | 0 | 0 |

Arquivos de referência:

- `execucao-v0.3.1-single-mock-c6b8d1277cb5462b9d032b571f572f11.json`
- `execucao-v0.3.1-multi-mock-7fbbe2ca20ca440f8dccdc248b3cb646.json`

O mock verifica o funcionamento da integração com regras determinísticas. Seus resultados não demonstram interpretação dos prompts por um LLM nem permitem comparar custo ou latência da API.

### Execuções com a API

Foram realizadas execuções exploratórias com `gpt-4.1-mini`. Uma tentativa do multiagente foi interrompida por uma saída incompatível com `request_reroute`. O executor não salvou o resultado parcial dessa tentativa; o traceback disponível deve ser preservado como evidência da preparação, sem pressupor consumo zero ou conversa concluída.

As últimas execuções completas com o conjunto de prompts 0.3.2 são:

- Agente único: `execucao-v0.3.1-single-openai-011b95a3cca3452794be1b2e63373f1c.json`.
- Multiagente: `execucao-v0.3.1-multi-openai-2fd9e19695014afd86de26915f26e484.json`.

| Medida | Agente único | Multiagente |
|---|---:|---:|
| Turnos processados | 8 | 8 |
| Turnos com intenção, área, ação e destino esperados | 7/8 | 7/8 |
| Chamadas à API | 8 | 15 |
| Tokens de entrada | 51.356 | 53.019 |
| Tokens de saída | 803 | 1.461 |
| Tokens totais | 52.159 | 54.480 |
| Soma das latências das chamadas | 16,35 s | 28,66 s |

As execuções pertencem a lotes diferentes, pois o multiagente foi executado separadamente após a interrupção. A soma de latências corresponde às chamadas de atendimento registradas, não a uma avaliação de desempenho geral. O consumo da tentativa interrompida e de avaliadores não está incluído nesta tabela.

### Pendências no ponto de continuidade

O `piloto-002` ainda não está integralmente aprovado com a API:

1. No turno 5, ambas as arquiteturas apresentam a orientação de reinicialização, mas não a registram em `context_facts`.
2. No turno 7, o agente único pede confirmação adicional e retorna `respond`, em vez do encaminhamento humano de ouvidoria esperado.
3. No turno 8, o multiagente permanece na ouvidoria apesar da mudança explícita para consulta comercial; não realiza nova triagem nem recupera o CEP nesse turno.
4. No multiagente, a resposta técnica do turno 6 não explicita a natureza humana da continuidade; o resumo da ouvidoria no turno 7 omite a reinicialização sem restabelecimento.

As regras adicionais propostas após essa análise ainda não foram implementadas ou testadas. A avaliação com DeepEval do piloto-002 também permanece pendente.

Este commit registra um checkpoint de preparação. Os resultados do piloto-001, as tentativas anteriores e seus documentos devem permanecer identificados pelas versões e execuções de origem. Não há evidência de superioridade de uma arquitetura nem validação do experimento principal.

### Retomada do trabalho

Corrigir as pendências acima, versionar o novo conjunto de prompts e repetir o piloto-002. Conferir os comportamentos obrigatórios e proibidos e executar a avaliação determinística e conversacional antes de declarar sua aprovação. Os próximos cenários devem permanecer separados dos resultados deste piloto.