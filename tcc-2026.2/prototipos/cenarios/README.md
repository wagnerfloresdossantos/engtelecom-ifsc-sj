# Cenários conversacionais

Esta pasta contém os cenários utilizados para comparar as arquiteturas de agente único e multiagente. Cada arquivo JSON define as mensagens do usuário e os critérios esperados para avaliar a conversa.

Os comentários ficam neste README porque JSON não aceita comentários. Não adicione `//` ou `/* ... */` aos arquivos de cenário.

## Cenário piloto

O arquivo `cenario-piloto-001.json`, versão `0.3.0`, contém quatro turnos:

| Turno | Mensagem resumida | Área esperada | Ação final esperada |
|---|---|---|---|
| 1 | Quero conhecer os planos | `commercial` | Solicitar o CEP |
| 2 | Meu CEP é 88110-000 | `commercial` | Informar disponibilidade e planos |
| 3 | Já sou cliente e estou sem Internet desde ontem | `support` | Solicitar o estado das luzes |
| 4 | A luz LOS está vermelha | `support` | Indicar atendimento técnico humano e resumir o problema |

Este cenário verifica comercial, suporte e mudança de assunto. Ele não cobre primeiro atendimento nem ouvidoria e não representa o conjunto definitivo do experimento.

## Campos gerais do arquivo

| Campo | Finalidade |
|---|---|
| `scenario_id` | Identificador do cenário, utilizado para relacionar execuções e avaliações. |
| `title` | Nome descritivo da conversa. |
| `version` | Versão do cenário. Deve ser atualizada quando mensagens ou critérios forem alterados. |
| `status` | Indica a finalidade do caso. Neste arquivo, `pilot` identifica um cenário exploratório. |
| `description` | Descreve a situação e o desfecho esperado; também fornece contexto à avaliação conversacional. |
| `data_policy` | Documenta a origem sintética dos dados e a ausência de dados pessoais reais. |
| `turns` | Lista ordenada das mensagens e dos critérios de cada turno. |
| `expected_route` | Sequência de chamadas internas esperada em cada arquitetura. |
| `task_completion` | Critérios necessários para considerar a tarefa concluída. |
| `metrics_to_collect` | Medidas previstas para análise. A lista não executa nem calcula as métricas automaticamente. |

Dentro de `data_policy`, `data_type` informa o tipo dos dados, `contains_real_personal_data` indica se existem dados pessoais reais e `notes` apresenta esclarecimentos sobre sua utilização.

## Campos de cada turno

| Campo | Significado |
|---|---|
| `turn_id` | Identificador do turno. A execução segue a ordem da lista `turns`. |
| `user_message` | Mensagem enviada ao sistema. |
| `expected_intent` | Intenção que esperamos identificar na saída final do turno. |
| `expected_area` | Área responsável pela resposta final, usando os mesmos identificadores nas duas arquiteturas. |
| `expected_action` | Ação esperada na saída final: `respond` ou `handoff_human` neste piloto. |
| `expected_handoff_target` | Destino humano esperado. `null` indica ausência de encaminhamento humano. |
| `required_behavior` | Comportamentos que a resposta deve apresentar. |
| `required_context_after_turn` | Informações que devem permanecer disponíveis após o turno. |
| `forbidden_behavior` | Respostas ou ações que representam falhas. |

Os identificadores de área são `first_contact`, `commercial`, `ombudsman` e `support`.

## Exemplo: turno 3

```json
{
  "turn_id": 3,
  "user_message": "Na verdade, já sou cliente e estou sem Internet desde ontem.",
  "expected_intent": "suporte_sem_conexao",
  "expected_area": "support",
  "expected_action": "respond",
  "expected_handoff_target": null
}
```

Este trecho ilustra os campos estruturados; não substitui o objeto completo do turno no cenário.

O sistema deve reconhecer uma solicitação de suporte, perguntar sobre as luzes e preservar que o usuário já é cliente e está sem conexão desde ontem. Ainda não se espera encaminhamento humano nesse turno.

`expected_action` descreve a decisão final do turno. Na arquitetura multiagente, podem ocorrer solicitações internas de nova triagem antes dessa resposta.

## Rotas esperadas

Na arquitetura de agente único, todos os turnos possuem a rota `agente_unico`.

Na arquitetura multiagente, o turno 3 possui a rota:

```text
commercial->triagem->support
```

Isso representa a ordem das chamadas ao modelo:

1. O orquestrador aciona o comercial, que solicita nova triagem.
2. O orquestrador aciona a triagem, que indica suporte.
3. O orquestrador aciona o suporte, que produz a resposta final.

Os agentes devolvem suas saídas ao orquestrador. A rota não representa comunicação direta entre eles e não inclui o orquestrador na contagem de chamadas ao modelo.

`expected_area` permite comparar a área identificada nas duas arquiteturas. `expected_route` verifica o procedimento interno específico de cada uma.

## Conclusão da tarefa

Em `task_completion`, `required` indica que a conclusão deve ser avaliada e `criteria` lista as condições esperadas para a conversa completa.

Neste piloto, o desfecho correto é indicar atendimento técnico humano, preservando o início da falha e o estado da luz LOS. Isso não significa reparar a conexão nem realizar uma transferência operacional em um sistema externo.

## Execução e avaliação

O executor envia aos agentes as mensagens de `user_message`, junto com os prompts, as bases de conhecimento e o contexto acumulado. Os resultados esperados não são fornecidos aos agentes.

Os campos de expectativa ficam disponíveis para a avaliação:

- Área, intenção, ação, destino humano e sequência de chamadas podem ser comparados diretamente com os registros estruturados.
- Comportamentos e retenção de informações descritos em linguagem natural exigem avaliação semântica ou revisão manual, salvo quando existir uma verificação objetiva específica.
- Buscas por palavras ou expressões proibidas são verificações parciais; não comprovam, sozinhas, a ausência de todos os comportamentos inadequados.

A presença de um campo no cenário não garante que ele já esteja sendo avaliado pelo código. Os scripts precisam implementar explicitamente cada verificação.

O modo `mock` verifica o funcionamento da orquestração com respostas fixas. Ele não demonstra qualidade dos prompts ou retenção real do contexto por um modelo de linguagem.

## Cuidados ao alterar cenários

- Manter dados sintéticos e critérios definidos antes da execução.
- Atualizar a versão após mudanças nas mensagens ou expectativas.
- Aplicar o mesmo cenário às duas arquiteturas.
- Separar resultados exploratórios dos resultados do experimento principal.
- Revisar a coerência entre mensagens, base de conhecimento e desfecho esperado.

Para verificar a sintaxe do arquivo, execute a partir da pasta `prototipos`:

```bash
python -m json.tool cenarios/cenario-piloto-001.json
```

Esse comando verifica a sintaxe JSON; não verifica a coerência metodológica do cenário.
