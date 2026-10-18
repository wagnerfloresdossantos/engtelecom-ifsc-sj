# Experimento exploratório com o DeepEval Synthesizer

## Objetivo e escopo

Verificar a viabilidade de utilizar o Synthesizer como apoio à elaboração de cenários conversacionais sintéticos para o TCC. O primeiro teste foi realizado em 17/10/2026 e aborda falta de Internet com luzes verdes na ONT e persistência após reinicialização.

Este experimento é de preparação e não integra o conjunto definitivo de 48 cenários proposto na metodologia. Não utiliza conversas de clientes reais. Não foi utilizado usuário simulado adaptativo: a execução empregou mensagens fixas, iguais nas duas arquiteturas.

## Papéis das ferramentas e do pesquisador

| Etapa | Responsabilidade |
|---|---|
| Especificação | Definição da situação, regras e desfecho de referência |
| Synthesizer | Geração de uma descrição candidata e de um desfecho esperado |
| Revisão com apoio de IA | Identificação e correção da inconsistência temporal |
| Preparação e conferência pelo pesquisador | Revisão do roteiro de três mensagens e dos critérios de avaliação |
| Protótipo | Produção das respostas pelas arquiteturas de agente único e multiagente |
| Avaliador determinístico | Comparação dos campos estruturados e das rotas |
| DeepEval conversacional | Avaliação das mensagens e respostas finais |
| Revisão manual | Inspeção complementar das respostas e das saídas internas |

O roteiro e seus critérios foram elaborados posteriormente com apoio de IA e conferidos pelo pesquisador. Portanto, o cenário executável não foi produzido integralmente pelo Synthesizer.

## Organização

Caminhos relativos à pasta `prototipos`:

- `experimentos/synthesizer/gerar_candidato.py`: script de geração.
- `experimentos/synthesizer/contextos/suporte-sem-conexao.md`: contexto fornecido.
- `experimentos/synthesizer/gerados/`: saídas originais, preservadas sem edição.
- `experimentos/synthesizer/revisados/revisao-suporte-001.md`: registro da revisão.
- `experimentos/synthesizer/revisados/cenario-suporte-001.json`: roteiro executável revisado.
- `resultados/`: execuções das arquiteturas.
- `resultados/avaliacoes/`: relatórios determinísticos.
- `resultados/avaliacoes-deepeval/`: relatórios conversacionais.

## Configuração registrada

| Componente | Valor |
|---|---|
| DeepEval | 4.2.8 |
| Modelo gerador | gpt-4.1-mini |
| Modelo de atendimento | gpt-4.1-mini |
| Modelo avaliador | gpt-4.1-mini |
| Protótipo | 0.3.1 |
| Cliente LLM | 0.2.1 |
| Conjunto de prompts de atendimento | 0.3.5 |
| Conjunto de bases | 0.3.3 |
| Cenário executável | synthesizer-suporte-001, versão 0.1.0 |
| Limiar das métricas conversacionais | 0,5, exploratório |

A geração utilizou `generate_conversational_goldens_from_contexts`, com um contexto, `include_expected_outcome=True` e `max_goldens_per_context=1`. O construtor foi configurado com `async_mode=False`, `max_concurrent=1` e `ConversationalStylingConfig`. O máximo solicitado não representa garantia de quantidade em futuras gerações.

O contexto delimitava a situação e fornecia as regras e o desfecho de referência. Este teste avalia uma geração dirigida; não demonstra descoberta autônoma de situações ou diversidade do conjunto.

## Geração e revisão

- Identificador da geração: `762ffb137f6341629c9e85218fb72cc7`.
- Arquivo original: `candidato-suporte-762ffb137f6341629c9e85218fb72cc7.json`.
- Quantidade retornada: um candidato.
- O campo `turns` retornou `null`: a saída contém descrição e desfecho, sem diálogo completo.

O candidato descrevia o cliente como já tendo reiniciado a ONT, mas previa que o assistente orientasse novamente o mesmo procedimento. A apresentação gradual das informações também não estava suficientemente definida.

A revisão reorganizou a sequência: relato inicial, informação das luzes, orientação e confirmação posterior de realização sem restabelecimento. A pontuação interna `synthetic_scenario_quality=1.0` não impediu a presença dessa inconsistência e não foi tratada como aprovação pelo pesquisador.

## Roteiro fixo revisado

| Turno | Mensagem do usuário | Comportamento esperado |
|---|---|---|
| 1 | Já sou cliente e estou sem Internet desde ontem. | Perguntar sobre as luzes da ONT |
| 2 | As luzes da ONT estão verdes, mas continuo sem conexão. | Orientar desligar da energia, aguardar 30 segundos e ligar novamente; solicitar o resultado |
| 3 | Desliguei da energia, esperei 30 segundos e liguei novamente. Continuo sem Internet. | Indicar atendimento técnico humano e resumir os fatos |

As respostas não foram fixadas: foram produzidas por cada arquitetura. Os critérios e rotas esperados ficaram disponíveis aos avaliadores, sem serem enviados aos agentes como gabarito.

Rotas esperadas no agente único: `agente_unico` nos três turnos. No multiagente: `triagem → support`, `support`, `support`.

## Comandos utilizados

Executar a partir de `prototipos`, com a `.venv` ativa. A geração, o atendimento em modo `openai` e a avaliação conversacional consomem créditos de API. A validação JSON e a avaliação determinística não chamam o modelo.

### Geração

```bash
python experimentos/synthesizer/gerar_candidato.py
```

O comando gera um novo candidato; não é necessário repeti-lo para avaliar os arquivos já produzidos. A geração pode envolver várias chamadas internas e não garante saída idêntica.

### Validação do cenário

```bash
python -m json.tool \
  experimentos/synthesizer/revisados/cenario-suporte-001.json \
  > /dev/null
```

### Execução das arquiteturas

```bash
python src/executar_piloto.py \
  --mode openai \
  --architecture both \
  --scenario experimentos/synthesizer/revisados/cenario-suporte-001.json
```

### Avaliação determinística dos resultados deste checkpoint

```bash
python src/avaliar_resultados.py \
  resultados/execucao-v0.3.1-single-openai-62df5309e9dc465b9b784a7225682468.json \
  resultados/execucao-v0.3.1-multi-openai-f40be14e27f74feba6a3ab1abc77d59b.json \
  --scenario experimentos/synthesizer/revisados/cenario-suporte-001.json
```

### Avaliação conversacional dos mesmos resultados

```bash
python src/avaliar_deepeval.py \
  resultados/execucao-v0.3.1-single-openai-62df5309e9dc465b9b784a7225682468.json \
  resultados/execucao-v0.3.1-multi-openai-f40be14e27f74feba6a3ab1abc77d59b.json \
  --scenario experimentos/synthesizer/revisados/cenario-suporte-001.json
```

Novas execuções recebem outros identificadores. Nesse caso, substituir os nomes dos resultados nos comandos de avaliação e preservar os arquivos anteriores.

## Resultados de 17/10/2026

Lote comum às duas execuções: `be2fc3067c704848ac397c48aefe343b`.

| Medida | Agente único | Multiagente |
|---|---:|---:|
| Turnos processados | 3 | 3 |
| Intenções corretas | 3/3 | 3/3 |
| Áreas corretas | 3/3 | 3/3 |
| Ações e destinos humanos corretos | 3/3 | 3/3 |
| Rotas corretas | 3/3 | 3/3 |
| Chamadas ao modelo | 3 | 4 |
| Tokens de entrada | 20.914 | 16.508 |
| Tokens de saída | 342 | 426 |
| Tokens totais | 21.256 | 16.934 |
| Soma das latências das chamadas | 8,56 s | 6,85 s |
| Trocas entre especialistas | Não se aplica | 0 |
| Relevância dos turnos | 1,00 | 1,00 |
| Retenção de conhecimento | 1,00 | 1,00 |
| Completude da conversa | 1,00 | 1,00 |

O multiagente realizou uma triagem inicial e três chamadas ao suporte. A seleção inicial não é contada como troca de especialista. A latência é a soma das chamadas registradas, não uma medida geral de desempenho. Os tokens da tabela correspondem ao atendimento; não incluem geração do candidato ou avaliação. Não foi consolidado custo financeiro.

### Identificação dos relatórios

| Registro | Identificador |
|---|---|
| Execução do agente único | 62df5309e9dc465b9b784a7225682468 |
| Execução multiagente | f40be14e27f74feba6a3ab1abc77d59b |
| Avaliação DeepEval do agente único | bf8a6213fa7247eca981e79db2668025 |
| Avaliação DeepEval multiagente | de7b4127d89443ff8493ddf3882b66a3 |

Os relatórios determinísticos possuem o prefixo `avaliacao-` seguido do nome da execução. Os conversacionais possuem o prefixo `deepeval-`, o nome da execução e o identificador da avaliação.

## Revisão manual e limites da aprovação

1. No turno 2, o multiagente registrou que o usuário ainda não havia realizado a reinicialização, embora não houvesse informação suficiente para afirmar isso. O registro adequado seria realização ainda não confirmada.
2. No turno 3, o agente único afirmou que um atendente especializado daria continuidade, o que pode sugerir continuidade operacional garantida. O protótipo apenas produz uma decisão de encaminhamento.

Ambas as arquiteturas passaram nas verificações determinísticas e nas três métricas conversacionais. Isso não equivale a conformidade integral: o relatório determinístico registra `task_completion_assessed=false`, e o conversacional registra `scenario_criteria_individually_assessed=false`.

O avaliador conversacional recebe mensagens e respostas finais, sem `context_facts` ou saídas internas de triagem. Portanto, a suposição nos fatos internos não é diretamente observável por essas métricas. A frase sobre continuidade humana está na resposta final, mas não foi apontada nesta avaliação.

## Conclusão e próximos passos

Foi possível gerar um candidato com o Synthesizer, revisá-lo, elaborar um roteiro executável e aplicar as duas camadas de avaliação ao protótipo existente. A revisão humana foi necessária antes do uso.

Este único caso não demonstra qualidade ou diversidade suficientes para gerar o conjunto definitivo, nem superioridade de uma arquitetura. Também não constitui teste do ConversationSimulator.

Próximas atividades:

1. Manter a rastreabilidade entre contexto, candidato original, alterações e roteiro revisado.
2. Registrar o esforço e os motivos de aceitação, correção ou rejeição de novos candidatos.
3. Ampliar gradualmente o teste para outras situações e áreas.
4. Definir a composição e a justificativa do conjunto definitivo com o orientador.
5. Documentar na metodologia a participação do gerador, das ferramentas de apoio e do pesquisador.

## Referências técnicas consultadas

- [Golden Synthesizer](https://deepeval.com/docs/golden-synthesizer)
- [Geração a partir de contextos](https://deepeval.com/docs/synthesizer-generate-from-contexts)

As assinaturas utilizadas foram conferidas no ambiente local com DeepEval 4.2.8. A documentação online pode descrever versões posteriores.


## Checkpoint — 18/10/2026 — preparação do PA-01

### Objetivo

Avaliar a geração de uma descrição de cenário de primeiro atendimento,
com dois turnos: pedido genérico de ajuda seguido de pergunta sobre
o serviço oferecido pelo Provedor Alfa.

### Arquivos preparados

- Contexto: `contextos/pa-01-informacoes-gerais.md`.
- Script: `gerar_pa01.py`.
- Registro de revisão: `revisados/revisao-pa01-001.md`.

### Primeira geração

- Identificador: `91b26f70442e45f8bb0921cc9862d283`.
- Script: 0.1.0.
- Evoluções: configuração padrão; a saída registrou `Comparative`.
- Resultado: candidato fora do escopo delimitado, pois acrescentou
  comparação entre tecnologias e explicação de vantagens da fibra.

O candidato original foi preservado. A inconsistência foi documentada
na revisão.

### Segunda geração

- Identificador: `c0ccd56a27be4271a97a1c82734aa2d8`.
- Script: 0.1.1.
- Configuração explícita: `num_evolutions=0`.
- A saída registrou `evolutions=[]`.
- Resultado da análise: descrição e desfecho compatíveis com o contexto,
  sem comparação entre tecnologias.

As duas gerações utilizaram DeepEval 4.2.8 e gpt-4.1-mini.
O resultado de uma tentativa não comprova que a configuração
elimine desvios em gerações futuras.

### Preparação das variações

Foram propostas, na conversa de apoio com IA, quatro variações
de redação com dois turnos cada. Essas mensagens foram elaboradas
posteriormente à geração do Synthesizer.

A conferência final pelo pesquisador, a criação dos JSONs executáveis
e a execução das variações permanecem pendentes.

### Ponto de continuidade

1. Conferir a equivalência das quatro variações de redação.
2. Registrar as mensagens aprovadas e sua origem.
3. Preparar os quatro JSONs com critérios comuns e identificadores próprios.
4. Verificar sua sintaxe e coerência antes da execução.
5. Decidir quais casos permanecem exploratórios e quais poderão integrar
   o conjunto definitivo, antes de utilizar resultados para ajustes.

Nenhuma execução do PA-01 nas arquiteturas ou avaliação de suas
respostas foi realizada neste checkpoint.