# Protótipo experimental

Este diretório contém os protótipos utilizados para comparar duas arquiteturas de atendimento textual baseadas em modelos de linguagem:

- agente único, responsável pelo atendimento das quatro áreas;
- sistema multiagente, formado por triagem e especialistas de primeiro atendimento, comercial, ouvidoria e suporte técnico.

A versão `0.3.0` adapta a implementação à metodologia atual do pré-projeto. As bases e os prompts utilizados na última execução estão identificados como `0.3.1`. O cenário piloto está na versão `0.3.0`.

O objetivo desta etapa é verificar a viabilidade da orquestração, do registro das conversas e da avaliação. Os resultados apresentados são exploratórios e não pertencem ao experimento principal do TCC2.

## Estado atual — 11/10/2026

- Estruturas de saída e orquestração preparadas para quatro áreas.
- Bases e prompts das quatro áreas elaborados.
- Piloto comercial → suporte executado em modo simulado e com a API.
- Falha de mudança de assunto identificada na primeira execução real e corrigida nas instruções comerciais.
- Última execução aprovada nas verificações determinísticas nas duas arquiteturas.
- Avaliação conversacional realizada com DeepEval `4.2.8` e avaliador `gpt-4.1-mini`.
- Controle negativo manual avaliado e reprovado nas três métricas.
- Primeiro atendimento e ouvidoria ainda não testados.

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
│   └── cenario-piloto-001.json
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

## Cenário piloto

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

O modo simulado não consome créditos e cobre apenas o piloto comercial e técnico. As respostas fixas não demonstram interpretação dos prompts ou retenção real do contexto e ainda não atendem integralmente ao resumo e aos fatos esperados no cenário.

## Execução real

```bash
python src/executar_piloto.py --mode openai --architecture both
```

O comando executa uma conversa em cada arquitetura. Também aceita `--architecture single`, `--architecture multi` e seleção de cenário por `--scenario cenarios/cenario-piloto-001.json`.

Os arquivos recebem nomes no formato `execucao-v0.3.0-ARQUITETURA-MODO-UUID.json`, preservando execuções anteriores. Registram lote, execução, versões declaradas, modelo configurado, datas, mensagens, respostas e chamadas.

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

### Última execução revisada

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

1. Criar o `piloto-002`, incluindo primeiro atendimento e ouvidoria, e ampliar o cliente simulado para essas áreas.
2. Documentar a revisão manual dos comportamentos obrigatórios, informações preservadas e condições de conclusão.
3. Testar erros mais sutis no procedimento de avaliação, mantendo critérios definidos antes de avaliar.
4. Definir e registrar os parâmetros de geração de forma igual nas duas arquiteturas. Atualmente, o cliente não os fixa explicitamente.
5. Registrar o identificador de modelo retornado pela API e melhorar a rastreabilidade com hashes dos documentos ou identificador de commit; as versões atuais são declaradas manualmente.
6. Conferir e atualizar o `requirements-lock.txt` e o `.env.example`.
7. Implementar registro de falhas e consumo de tentativas incompletas; atualmente, uma exceção pode interromper a conversa sem salvar o resultado parcial.
8. Estimar o custo com preços, fonte e data documentados, separando atendimento e avaliação. O script do DeepEval ainda não consolida seu consumo financeiro.
9. Consolidar resultados, matrizes de confusão e comparações por área.
10. Revisar os diagramas para refletir a orquestração e o histórico completo atuais, sem comunicação direta entre agentes.

O estado atual constitui um protótipo exploratório funcional para o piloto comercial e técnico. A implementação definitiva, o conjunto completo de cenários e o procedimento de avaliação ainda serão refinados antes do experimento principal.
