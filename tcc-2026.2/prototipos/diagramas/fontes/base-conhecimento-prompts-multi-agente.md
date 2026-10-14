```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant O as Orquestrador
    participant C as Carregador
    participant T as Triagem
    participant E as Especialista ativo

    U->>O: mensagem_usuario
    Note over O: Mantém historico,<br/>fatos_relevantes e agente_ativo

    alt Ainda não existe especialista ativo
        O->>C: Prepara triagem.md
        Note over C: base_conhecimento = comum + triagem<br/>historico = mensagens + fatos<br/>mensagem_usuario = mensagem atual<br/>solicitacao_reencaminhamento = null
        C-->>O: Prompt de triagem preenchido
        O->>T: gerar(prompt, SaidaTriagem, mensagem)
        T-->>O: destination, intent, reason,<br/>context_to_forward
        Note over O: agente_ativo recebe destination
    end

    O->>C: Prepara prompt do especialista ativo
    Note over C: base_conhecimento = comum + base da área<br/>historico = mensagens + fatos + contexto encaminhado<br/>mensagem_usuario = mensagem atual
    C-->>O: Prompt especializado preenchido

    O->>E: gerar(prompt, esquema da área, mensagem)
    E-->>O: response, intent, action,<br/>handoff_target, context_facts

    alt action = request_reroute
        Note over E,O: response = null<br/>handoff_target = null
        O->>C: Prepara nova triagem.md
        Note over C: solicitacao_reencaminhamento<br/>recebe a saída do especialista anterior
        C-->>O: Prompt de nova triagem preenchido

        O->>T: Reclassifica a mesma mensagem
        T-->>O: destination, intent, reason,<br/>context_to_forward
        Note over O: Atualiza agente_ativo

        O->>C: Prepara prompt do especialista selecionado
        C-->>O: Prompt com histórico, fatos e contexto encaminhado
        O->>E: Processa a mesma mensagem na nova área
        E-->>O: Resposta final e fatos atualizados
    end

    Note over O: Acrescenta mensagem e resposta ao histórico<br/>Atualiza fatos_relevantes com context_facts
    O-->>U: response
```
***Nota***: Neste diagrama, “Especialista ativo” representa primeiro atendimento, comercial, ouvidoria ou suporte. Após a nova triagem, esse participante representa o especialista selecionado. Uma segunda solicitação de nova triagem na mesma mensagem é tratada como erro pelo código.

As variáveis usadas no preenchimento são:

| Variável do prompt | Conteúdo fornecido |
|---|---|
| `{{base_conhecimento}}` | Base reunida conforme o agente chamado |
| `{{historico}}` | Lista JSON de mensagens e fatos; fatos usam `role="context"` |
| `{{mensagem_usuario}}` | Mensagem atual |
| `{{solicitacao_reencaminhamento}}` | Saída do especialista que pediu nova triagem; `null` na triagem inicial |


`context_to_forward` retorna da triagem para o orquestrador e entra no contexto do próximo especialista. `context_facts` retorna do agente responsável e atualiza os fatos da conversa. O histórico completo permanece armazenado separadamente.