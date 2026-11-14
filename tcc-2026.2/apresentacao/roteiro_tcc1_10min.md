# Roteiro de fala — Seminário TCC1

**Autor:** Wagner Flores dos Santos  
**Título:** Análise Comparativa entre Arquiteturas de Agente Único e Multiagente Baseadas em LLM para Chatbots de Atendimento  
**Versão de referência:** PDF final `seminario-tcc1(1).pdf`, com 16 páginas e apêndice de cinco telas.  
**Duração planejada:** 9 minutos de fala, com 1 minuto de margem até o limite de 10 minutos. Perguntas e feedback: 5 minutos adicionais.  
**Como usar:** o texto abaixo serve de referência para o ensaio. Na apresentação, use os tópicos e o slide como apoio. Os tempos incluem pausas e transições e precisam ser confirmados em voz alta.

## Mapa de tempo

| Tela / número no rodapé | Duração | Tempo acumulado |
|---|---:|---:|
| Capa, sem número | 20 s | 0:20 |
| 1 — Problema | 55 s | 1:15 |
| 2 — Justificativa | 40 s | 1:55 |
| 3 — Literatura e lacuna | 60 s | 2:55 |
| 4 — Objetivos | 45 s | 3:40 |
| 5 — Agente único | 30 s | 4:10 |
| 6 — Multiagente | 40 s | 4:50 |
| 7 — Cenários | 55 s | 5:45 |
| 8 — Avaliação | 75 s | 7:00 |
| 9 — Controles e limitações | 65 s | 8:05 |
| 10 — Cronograma e fechamento | 55 s | 9:00 |

Após o slide principal 10, o PDF final traz o apêndice nesta ordem: referências (1/5), escopo (2/5), custo (3/5), seis estudos (4/5) e DeepEval/Synthesizer (5/5). Essas telas não entram nos 9 minutos de fala. Encerre no slide 10 e abra uma reserva somente quando a pergunta justificar.

## Capa — 0:00 a 0:20

Bom dia, pessoal. Eu sou o Wagner e vou apresentar a proposta do meu TCC, orientado pelo professor Arliones Hoeller. O trabalho compara duas formas de organizar um chatbot de atendimento: uma com agente único e outra com agentes especializados.

**Transição:** “O ponto de partida é uma dúvida prática sobre essa escolha.”

## Slide 1 — Problema — 0:20 a 1:15

Os modelos de linguagem em grande escala, ou LLMs, permitem interpretar mensagens e produzir respostas a partir de instruções e informações de contexto. Quando esse modelo é organizado com uma função e regras de atuação, temos um agente de atendimento.

Em um provedor de Internet, a conversa pode começar com uma pergunta sobre planos e terminar em suporte técnico ou reclamação. Além disso, o cliente costuma fornecer as informações aos poucos.

Uma possibilidade é deixar todas essas responsabilidades com um agente. Outra é dividir o atendimento entre especialistas. Essa divisão pode ajudar, mas também cria novas decisões de encaminhamento e exige preservar o contexto.

A pergunta do trabalho é: como essas arquiteturas diferem em qualidade, encaminhamentos e recursos consumidos durante uma conversa completa?

**Pausa breve depois da pergunta.**

## Slide 2 — Justificativa — 1:15 a 1:55

No agente único, as regras das quatro áreas ficam reunidas. Há menos coordenação entre componentes, mas o agente precisa lidar com um contexto mais amplo.

No multiagente, cada especialista recebe as regras da sua responsabilidade. Isso pode facilitar a especialização. Em contrapartida, o sistema pode selecionar o agente errado, perder informações na troca ou fazer chamadas adicionais ao modelo.

Por isso, a justificativa é avaliar os dois lados da escolha: se houver melhoria no atendimento, qual será o consumo de recursos necessário para obtê-la? A proposta não parte da ideia de que mais agentes necessariamente produzem um sistema melhor.

## Slide 3 — Literatura e lacuna — 1:55 a 2:55

A revisão encontrou trabalhos com contribuições diferentes. Moncada e colaboradores usam agentes para classificar chamados e produzir respostas, mas não comparam essa solução com agente único em conversas de vários turnos.

Lee e colaboradores apresentam uma organização com coordenação e especialistas em telecomunicações, sem uma comparação quantitativa própria entre as duas arquiteturas.

Amri e colaboradores chegam mais perto desta proposta, porque comparam agente único e multiagente em diálogos. Entretanto, o foco é a decisão de transferir para atendimento humano. O estudo não reúne a avaliação das respostas, da conclusão das tarefas e do consumo de recursos.

Assim, a lacuna que identifiquei, dentro dos trabalhos revisados, é essa avaliação conjunta durante a conversa. É nesse recorte que o TCC pretende contribuir.

**Aponte as limitações do quadro; não leia todas as células.**

## Slide 4 — Objetivos — 2:55 a 3:40

O objetivo geral é comparar experimentalmente as duas arquiteturas no atendimento textual de um provedor de Internet.

Para isso, vou definir uma base de conhecimento e regras comuns, implementar os dois protótipos e preparar os cenários de teste.

Depois, vou avaliar a correção e a relevância das respostas, a preservação das informações, a conclusão das tarefas e os encaminhamentos. Também vou registrar chamadas ao modelo, tokens e custo estimado.

A entrega esperada é uma análise das vantagens e limitações observadas, nas condições do experimento, sem precisar confirmar previamente a superioridade de uma arquitetura.

## Slide 5 — Agente único — 3:40 a 4:10

Neste desenho da monografia, o agente único recebe a base completa das quatro áreas. Um orquestrador em Python fornece o contexto, mantém o histórico e registra as saídas. As decisões de atendimento ficam com o agente.

## Slide 6 — Multiagente — 4:10 a 4:50

No multiagente, o orquestrador mantém histórico, fatos e especialista ativo. A triagem seleciona um dos quatro especialistas. Enquanto o assunto permanece na mesma área, as mensagens seguem para esse especialista. Se houver mudança, ele pede nova triagem, sem escolher diretamente outro agente.

Os blocos inferiores mostram a base comum e as informações por área. As respostas e decisões retornam ao orquestrador. Ele controla a execução em Python, sem produzir respostas de atendimento. O barramento representa possibilidades de comunicação; não significa que todos os agentes sejam acionados ao mesmo tempo.

**Aponte os agentes ligados ao orquestrador e diferencie as linhas contínuas das tracejadas. As conexões não representam comunicação direta entre especialistas nem execução simultânea obrigatória.**

## Slide 7 — Cenários — 4:50 a 5:45

O conjunto previsto terá 48 cenários: quatro áreas, três situações por área e quatro variações de redação por situação. Portanto, são 12 situações-base, com variações que preservam os fatos e os critérios esperados.

Cada cenário será aplicado uma vez em cada arquitetura, totalizando 96 conversas completas.

O exemplo começa no comercial, passa para suporte quando o usuário informa que já é cliente e está sem Internet, e chega à ouvidoria quando ele apresenta uma reclamação recorrente.

Vou observar se o sistema reconhece essas mudanças e mantém as informações já fornecidas. As mensagens terão a mesma ordem nas duas arquiteturas, e todos os dados serão fictícios. Os critérios esperados ficarão na avaliação, sem serem entregues aos agentes como respostas de referência.

## Slide 8 — Avaliação — 5:45 a 7:00

A avaliação terá quatro dimensões. Na qualidade da conversa, o DeepEval apoiará a medição da relevância, da retenção de informações e da completude. Uma amostra das avaliações será revisada manualmente.

A correção e a conclusão serão verificadas conforme as regras da base e os critérios de cada cenário. Uma resposta bem escrita não basta se inventar uma informação ou descumprir o procedimento.

Nos encaminhamentos, vou comparar a área esperada com a área identificada em cada turno. No agente único, essa área será registrada na saída estruturada; no multiagente, será a área do especialista acionado. Isso permite calcular acurácia e uma matriz de confusão, mostrando quais áreas foram confundidas.

A indicação de atendimento humano será verificada nas duas arquiteturas. Já as trocas internas serão contadas apenas no multiagente.

Por fim, os registros em Python vão contabilizar chamadas e tokens de entrada e saída. O custo será estimado com os preços da data do experimento. Assim, a comparação considera o resultado e os recursos necessários para chegar até ele.

## Slide 9 — Controles e limitações — 7:00 a 8:05

As duas soluções usarão o mesmo GPT-4.1-mini, os mesmos parâmetros de geração, o mesmo conteúdo total e as mesmas mensagens. A organização das instruções muda conforme as responsabilidades de cada arquitetura.

Antes da execução principal, haverá um piloto para verificar os registros, os cenários e os critérios de avaliação. Depois serão congeladas as versões dos prompts, do modelo e das configurações. O piloto não entrará nos resultados finais.

O avaliador e os limiares também serão os mesmos nas duas arquiteturas.

Há limites importantes. Uma execução por cenário não permite medir a variação das respostas à mesma entrada. As variações de redação ampliam as formas de expressão, mas não substituem repetições. Além disso, os resultados ficam restritos ao modelo, à base e aos cenários escolhidos. Não serão generalizados diretamente para todos os sistemas comerciais.

## Slide 10 — Cronograma e fechamento — 8:05 a 9:00

O desenvolvimento definitivo está previsto para o TCC2, no primeiro semestre de 2027.

Em fevereiro e março, ficam a revisão da base, os prompts, os protótipos e os cenários. A integração das métricas e o piloto vão até abril. Depois do congelamento, o experimento será executado em abril, com análise em abril e maio.

A redação acompanha o semestre. A preparação da defesa está prevista para junho, e as correções e a entrega final, entre junho e julho, conforme o calendário oficial.

Para fechar, a mensagem central é esta: especializar agentes pode melhorar o atendimento, mas acrescenta coordenação. O trabalho vai medir qualidade e recursos para identificar essas diferenças, sem pressupor um vencedor. Obrigado.

**Pare o cronômetro. Não avance automaticamente para as reservas.**

## Plano de corte

Se o cronômetro indicar atraso superior a 30 segundos:

- No slide 3, destaque apenas Amri e a lacuna conjunta: economiza aproximadamente 20 segundos.
- No slide 7, explique a mudança comercial → suporte → ouvidoria sem ler as mensagens: economiza cerca de 15 segundos.
- No slide 10, agrupe as atividades em preparação, experimento e conclusão: economiza cerca de 15 segundos.

Preserve a pergunta de pesquisa, a comparação controlada, os critérios de avaliação e a limitação de execução única. A margem de 1 minuto é para pausas e imprevistos; não é conteúdo adicional a preencher.

## Perguntas prováveis — respostas de apoio

**Por que comparar se já existem estudos?**  
O recorte reúne qualidade, retenção, conclusão, encaminhamentos e recursos sob condições comuns. Na revisão apresentada, esses aspectos não aparecem avaliados conjuntamente.

**Por que 48 cenários?**  
É o conjunto planejado para quatro áreas e três situações-base por área, com quatro variações de redação. É um recorte de viabilidade e cobertura, não uma demonstração de suficiência estatística.

**Por que não repetir cada cenário?**  
O desenho atual prevê uma execução por combinação. Isso limita a análise da variabilidade e será declarado nos resultados. Repetições podem ser discutidas com o orientador conforme recursos e viabilidade.

**Como garantir uma comparação justa com prompts diferentes?**  
O conteúdo total e as regras são comuns. Os prompts mudam no necessário para representar as responsabilidades de cada organização e são congelados antes do experimento. Essa equivalência requer revisão cuidadosa; não elimina todas as ameaças à validade.

**Qual modelo avaliador e temperatura serão usados?**  
A versão fornecida da monografia prevê configurações iguais e registro dos parâmetros, mas não fixa todos os valores nem o avaliador. Esses pontos precisam ser definidos no piloto e documentados antes da execução principal. Não apresentar temperatura 0,2 como decisão desta versão.

**O DeepEval decide sozinho se a resposta está correta?**  
Não. Haverá critérios por cenário, verificações objetivas e revisão manual de uma amostra das avaliações. Os limiares serão definidos no piloto.

**Vai medir velocidade ou usar clientes reais?**  
Não. Latência está fora do escopo. Os cenários e dados serão fictícios, e o encaminhamento humano será registrado, sem transferência operacional.

**Já há resultados comparativos?**  
A apresentação é de um pré-projeto. O experimento definitivo e a análise estão previstos para o TCC2. Não apresentar a viabilidade exploratória como resultado do experimento principal.

## Preparação pessoal

Faça pelo menos três ensaios completos em voz alta, cronometrados; um deles para o orientador ou um colega. Grave um ensaio e observe ritmo, pausas e repetições como “né” e “então”. Memorize apenas a abertura e o fechamento; no restante, domine as ideias. Durante as perguntas, ouça até o fim e responda de forma breve. Peça a um colega para anotar o feedback.


# Roteiro do apêndice — perguntas e feedback

**Uso:** o professor prevê 5 minutos para perguntas e feedback, no total. Não apresente todas as reservas em sequência. Ouça a pergunta, responda diretamente e abra apenas o slide que ajuda a explicar. As falas abaixo são sugestões; use somente o trecho pertinente. Os tempos são aproximados e não precisam ser somados à fala principal.

## Apêndice 1/5 — Referências utilizadas na apresentação

**Página 12 do PDF. Quando abrir:** se pedirem a fonte de uma afirmação, o trabalho mais próximo ou quais documentos embasam o método.

**Fala de apoio — 15 a 20 segundos:**

“As referências estão reunidas aqui. A revisão analisa seis estudos científicos. A documentação do DeepEval e a página do modelo apoiam as escolhas de ferramentas. O trabalho mais próximo da comparação proposta é o de Amri e colaboradores, mas o recorte dele é a transferência para atendimento humano.”

**Se perguntarem sobre os três estudos do slide principal:**

“Eu selecionei três para apresentar a lacuna dentro do tempo disponível. A revisão da monografia considera seis, que estão no quadro de reserva.”

**Cuidado:** não ler as referências nem os identificadores DOI em voz alta. Localize a fonte relacionada à pergunta.

## Apêndice 2/5 — Reserva: escopo e decisões pendentes

**Página 13 do PDF. Quando abrir:** perguntas sobre viabilidade, delimitação, implantação, configurações ou o que será entregue em TCC2.

**Fala de apoio — 30 a 40 segundos:**

“O estudo está restrito ao atendimento textual de um provedor, em quatro áreas, com dados fictícios. Não haverá clientes reais nem implantação comercial. Os documentos da base serão colocados diretamente no contexto dos agentes, sem recuperação dinâmica. Também não vou comparar modelos, treinar um modelo ou medir latência. O foco é comparar as duas organizações usando o mesmo modelo e regras comuns. A versão exata, os parâmetros e a configuração da avaliação serão definidos e documentados antes da execução principal.”

**Pergunta: por que não medir latência?**

“O acesso depende de uma API externa e das condições da rede. No recorte atual, vou concentrar a comparação nos recursos registrados diretamente: chamadas e tokens, além do custo estimado. Isso significa que o trabalho não permitirá concluir qual arquitetura responde mais rápido.”

**Pergunta: qual é a diferença entre agente e orquestrador?**

“O agente usa o modelo de linguagem para interpretar e decidir conforme suas instruções. O orquestrador é o controle em Python: mantém o estado, chama os componentes e registra o que aconteceu. Ele não produz a resposta de atendimento.”

**Pergunta: por que GPT-4.1-mini?**

“É o modelo previsto no projeto por compatibilidade de capacidade e custo com o volume planejado. As duas arquiteturas usarão o mesmo modelo. A comparação entre diferentes modelos ficaria para outro estudo.”

**Cuidado:** não dizer que temperatura, avaliador ou limiares já estão fechados se ainda dependem do piloto. A apresentação não demonstra resultados definitivos do TCC2.

## Apêndice 3/5 — Reserva: custo e critérios de sucesso

**Página 14 do PDF. Quando abrir:** perguntas sobre custo, métricas de consumo, conclusão da tarefa ou sucesso da pesquisa.

**Fala de apoio — 30 a 40 segundos:**

“O custo estimado de uma execução será calculado multiplicando os tokens de entrada pelo preço de entrada e os tokens de saída pelo preço de saída. Os preços e a data da consulta serão registrados no experimento. Uma execução corresponde a uma conversa completa. Vou separar esse consumo do custo da avaliação. E o sucesso da pesquisa não depende de o multiagente vencer: depende de realizar uma comparação controlada e explicar as diferenças observadas.”

**Ao apontar a equação:**

- `Te`: quantidade de tokens de entrada.
- `Ts`: quantidade de tokens de saída.
- `Pe` e `Ps`: preço por token de entrada e saída, respectivamente.
- Usar preços e quantidades na mesma unidade; se a tarifa estiver por milhão de tokens, aplicar a conversão.

**Pergunta: o que são tokens?**

“São unidades de texto processadas pelo modelo. As instruções, o histórico e as respostas consomem tokens. Por isso, uma arquitetura pode usar mais tokens mesmo quando a resposta ao cliente é curta.”

**Pergunta: transferir para humano é fracassar?**

“Não necessariamente. Se o cenário e as regras exigirem atendimento humano, indicar corretamente esse encaminhamento e preservar os dados necessários pode ser a conclusão esperada. O problema é encaminhar quando não deveria, ou deixar de encaminhar quando deveria.”

**Pergunta: esse é o custo total da operação comercial?**

“Não. É uma estimativa do custo de uso do modelo durante o experimento. Ela não representa todo o custo de desenvolver, hospedar e manter um sistema comercial.”

## Apêndice 4/5 — Reserva: os seis estudos fundamentam o recorte da pesquisa

**Página 15 do PDF. Quando abrir:** perguntas sobre a abrangência da revisão, originalidade ou diferença em relação aos trabalhos existentes.

**Fala de apoio — 40 a 50 segundos:**

“A revisão contempla seis estudos. Moncada trata da classificação e resposta a chamados. Lee apresenta coordenação e especialistas em telecomunicações. Yang investiga a seleção de agentes. Amri compara agente único e multiagente na transferência humana. Yan organiza a literatura pela comunicação entre agentes. E Owotogbe propõe investigar robustez e propagação de falhas. Eles contribuem de formas diferentes. Dentro desse conjunto, a lacuna que identifiquei é a avaliação conjunta de qualidade, retenção, conclusão, encaminhamentos e consumo em conversas com vários turnos.”

**Para perguntas sobre um estudo específico:**

| Estudo | O que destacar | Limite que motiva o TCC |
|---|---|---|
| Moncada et al. (2025) | Agentes para classificar chamados e gerar respostas | Amostra de 20 chamados; sem comparação com agente único nem continuidade conversacional |
| Lee et al. (2025) | Coordenação e especialização em telecomunicações | Sem comparação quantitativa própria entre arquiteturas |
| Yang et al. (2025) | Seleção de agentes com TF-IDF e LLM | 30 consultas sintéticas; não avalia a conversa depois da seleção |
| Amri et al. (2026) | Comparação das arquiteturas em diálogos | Foco na decisão de transferência; sem análise do consumo de recursos |
| Yan et al. (2026) | Revisão centrada na comunicação entre agentes | Não realiza experimento próprio comparando as arquiteturas |
| Owotogbe (2025) | Proposta de investigação de robustez | Validação ainda em andamento na publicação, sem resultados quantitativos do framework |

**Pergunta: o que há de novo se Amri já compara as arquiteturas?**

“A contribuição pretendida está no recorte da avaliação. Além da indicação de humano, vou observar respostas, retenção, conclusão, identificação da área por turno e recursos consumidos. Não estou propondo que a comparação entre essas arquiteturas seja inédita em si.”

**Cuidado:** afirmar “nos estudos revisados, não identifiquei” em vez de “nenhum trabalho existe”. TF-IDF representa textos por pesos de palavras; framework é uma estrutura de métodos e componentes.

**Correção de legenda no PDF:** o quadro diz “Referências completas no slide anterior”, mas as referências estão no início do apêndice. Ao editar o LaTeX, trocar por “Referências completas no início do apêndice”.

## Apêndice 5/5 — Reserva: DeepEval avalia; Synthesizer apoia os cenários

**Página 16 do PDF. Quando abrir:** perguntas sobre geração dos testes, avaliação automática, revisão humana e possível viés do avaliador.

**Fala de apoio — 40 a 50 segundos:**

“O DeepEval terá dois papéis em momentos diferentes. Na preparação, o módulo Synthesizer apoiará a geração de descrições de cenários e desfechos esperados a partir dos contextos preparados. Eu vou revisar essas sugestões e montar as mensagens e variações de redação. As mensagens finais serão fixadas e aplicadas nas duas arquiteturas. Depois da execução, as métricas vão apoiar a avaliação da relevância, da retenção de informações e da completude da conversa. Isso será complementado por verificações em Python e revisão manual de uma amostra. Gerar um cenário automaticamente não significa que ele já esteja validado.”

**Como explicar as três métricas, sem jargão:**

| Dimensão | Pergunta simples | Exemplo no atendimento |
|---|---|---|
| Relevância | A resposta trata da solicitação do turno? | Ao relatar falha de conexão, o cliente recebe orientação pertinente ao suporte |
| Retenção | O sistema preserva as informações anteriores? | Utiliza a condição de cliente e os dados já informados durante a conversa |
| Completude | As necessidades apresentadas foram atendidas? | Cumpre as condições do cenário, incluindo encaminhamento adequado quando necessário |

**Pergunta: o Synthesizer vai conversar livremente com cada protótipo?**

“Não no desenho proposto. Ele apoia a preparação dos cenários. Os turnos finais serão revisados e fixados antes do experimento, para que as duas arquiteturas recebam as mesmas mensagens, na mesma ordem.”

**Pergunta: o modelo pode gerar testes incorretos?**

“Pode. Por isso, as sugestões serão conferidas contra a base e as regras. Casos inadequados serão corrigidos ou elaborados manualmente, com registro da origem e das alterações. O gerador não substitui o pesquisador na definição do teste.”

**Pergunta: como confiar em um modelo que avalia outro?**

“A pontuação automática não será tratada como verdade absoluta. Vou usar as mesmas configurações nas duas arquiteturas, revisar manualmente uma amostra e verificar por regras os itens objetivos. O piloto servirá para identificar inconsistências antes da execução principal.”

**Pergunta: completude significa correção factual?**

“Não são a mesma coisa. A conversa pode parecer completa e ainda violar uma regra. A correção também será verificada pela conformidade com a base e pelos comportamentos definidos no cenário.”

**Pergunta: quais partes não dependem da avaliação por LLM?**

“A comparação entre a área prevista e a registrada, o número de chamadas, os tokens e a contabilização das trocas serão tratados diretamente pelos scripts. A revisão humana complementará as avaliações das respostas abertas.”

**Pergunta: quais serão os limiares, o tamanho da amostra manual e o modelo avaliador?**

“Os limiares e a configuração do avaliador serão definidos e registrados no piloto. O procedimento de seleção e o tamanho da amostra de revisão manual também precisam ficar documentados antes da comparação final. Não vou apresentar como fechadas decisões que ainda estão em preparação.”

# Cartão de encerramento das perguntas

Se não souber algo: “Esse ponto ainda não está definido. Vou verificar com o orientador e incorporar a decisão ao procedimento antes da execução.”

Se receber uma sugestão: “Obrigado. Vou registrar essa observação e avaliar como incorporá-la ao pré-projeto.”

Ao terminar: “Obrigado pelas perguntas e contribuições.”
